import os
import h5py
import importlib
import requests
import pygrib
import metpy.calc
import numpy as np
from set_parameters import set_variables
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from wrf import getvar, latlon_coords, interplevel, g_geoht, CoordPair, vertcross
from netCDF4 import Dataset, num2date
from scipy.interpolate import griddata
from metpy.units import units

def wrf_cross_section(data_library_names, dir_cases, case_names, exp_names,
                      da_cycle, var_time=20000101010000, 
                      lat_start=0, lat_end=0, lon_start=-70, lon_end=-50,
                      ref_exp_name='CTRL', variables=['u']):

    start_point = CoordPair(lat=lat_start, lon=lon_start)
    end_point = CoordPair(lat=lat_end, lon=lon_end)
    levels = np.arange(1000, 9, -1)
    lat = np.linspace(lat_start, lat_end, int(100*(lat_end-lat_start)+1))
    lon = np.linspace(lon_start, lon_end, int(100*(lon_end-lon_start)+1))
    latlon_idx = np.arange(0, int(100*(lon_end-lon_start)+1))
    n_level = len(levels)
    n_lon = len(lon)
    n_lat = len(lat)

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        da_domains = attributes[(dir_case, case_name)]['da_domains']
        forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
        initial_time = datetime(*itime)

        dir_cycling_da = os.path.join(dir_exp, 'cycling_da')
        dir_cross_section = os.path.join(dir_exp, 'cross_section')
        dir_data = os.path.join(dir_exp, 'data')
        dir_ERA5 = os.path.join(dir_data, 'ERA5')
        dir_GFS = os.path.join(dir_data, 'GFS')
        os.makedirs(dir_cross_section, exist_ok=True)

        time_now = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')

        specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
        dir_cross_section_case = os.path.join(dir_cross_section, specific_case)
        os.makedirs(dir_cross_section_case, exist_ok=True)

        if len(forecast_domains) > len(da_domains):
            domains = forecast_domains
        else:
            domains = da_domains
        # domains = ['d02']

        for dom in tqdm(domains, desc='Domains', leave=False):

            if 'GFS' in exp_name or 'ERA5' in exp_name:
                dir_wrfout = os.path.join(dir_cycling_da, f"{case_name}_{ref_exp_name}_C{str(da_cycle).zfill(2)}", 'bkg')
            else:
                dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'bkg')

            wrfout = os.path.join(dir_wrfout, f"wrfout_{dom}_{initial_time.strftime('%Y-%m-%d_%H:%M:00')}")
            ncfile = Dataset(wrfout)
            p = getvar(ncfile, 'pressure')
            ncfile.close()

            lat, lon = latlon_coords(p)
            (n_lat, n_lon) = lat.shape

            for var in tqdm(variables, desc='Variables', leave=False):

                (information, levels) = set_variables(var)
                n_level = len(levels.keys())

                filename = os.path.join(dir_cross_section_case, f"{var}_{dom}.nc")
                os.system(f"rm -rf {filename}")

                ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                ncfile_output.createDimension('n_level', n_level)
                ncfile_output.createDimension('n_lat',   n_lat)
                ncfile_output.createDimension('n_lon',   n_lon)
                ncfile_output.createVariable('level', 'f8', ('n_level'))
                ncfile_output.createVariable('lat',   'f8', ('n_lat'))
                ncfile_output.createVariable('lon',   'f8', ('n_lon'))
                ncfile_output.createVariable(var,     'f8', ('n_level', 'n_lat'))

                ncfile_output.variables['level'][:] = levels
                ncfile_output.variables['lat'][:,:] = lat
                ncfile_output.variables['lon'][:,:] = lon
                ncfile_output.variables[var][:,:,:,:] = 0.0

                if 'inc' in var:

                    var_bkg = var.replace('_inc', '')
                    var_anl = var.replace('_inc', '_anl')
                    filename_bkg = filename.replace('_inc', '')
                    filename_anl = filename.replace('_inc', '_anl')

                    ncfile_bkg = Dataset(filename_bkg)
                    ncfile_anl = Dataset(filename_anl)
                    ncfile_output.variables[var][idt,:,:,:] = ncfile_anl.variables[var_anl][idt,:,:,:] - ncfile_bkg.variables[var_bkg][idt,:,:,:]
                    ncfile_bkg.close()
                    ncfile_anl.close()
                        
                else:

                    if 'GFS' in exp_name:
                        YYYY = time_now.strftime('%Y')
                        YYMMDDHH = time_now.strftime('%Y%m%d%H')
                        YYYYMMDD = time_now.strftime('%Y%m%d')
                        
                        dir_rda = 'https://data.rda.ucar.edu/ds084.1'
                        GFS_filename = f"gfs.0p25.{YYMMDDHH}.f000.grib2"
                        GFS_file = os.path.join(dir_GFS, GFS_filename)

                        if not os.path.exists(GFS_file):
                            GFS_rda_filename = os.path.join(dir_rda, YYYY, YYYYMMDD, GFS_filename)
                            response = requests.get(GFS_rda_filename, stream=True)
                            with open(GFS_file, "wb") as f:
                                f.write(response.content)
                        GFS_pygrib = pygrib.open(GFS_file)
                        # for grb in GFS_pygrib:
                        #     print(grb)
                        for idl, lev in enumerate(levels):
                            GFS_temp = GFS_pygrib.select(name=information['GFS'], typeOfLevel='isobaricInhPa', level=lev)[0]
                            GFS_lat, GFS_lon = GFS_temp.latlons()
                            GFS_lon[GFS_lon>180.0] = GFS_lon[GFS_lon>180.0] - 360.0
                            GFS_index = (GFS_lat < np.array(lat[-1, -1]) + 15.0) & (GFS_lat > np.array(lat[0, 0]) - 15.0) & \
                                        (GFS_lon < np.array(lon[-1, -1]) + 15.0) & (GFS_lon > np.array(lon[0, 0]) - 15.0)
                            
                            GFS_lat_1d = GFS_lat[GFS_index]
                            GFS_lon_1d = GFS_lon[GFS_index]
                            GFS_temp_1d = GFS_temp.values[GFS_index]
                            if var == 'q': GFS_temp_1d = GFS_temp_1d/(1.0-GFS_temp_1d)
                            if var == 'avo': GFS_temp_1d = GFS_temp_1d*100000.0
                            ncfile_output.variables[var][idt,idl,:,:] = griddata((GFS_lon_1d, GFS_lat_1d), GFS_temp_1d, (lon, lat), method='linear')
                        GFS_pygrib.close()

                    if 'ERA5' in exp_name:
                        ERA5_filename = os.path.join(dir_ERA5, 'ERA5_pressure_levels.nc')
                        ERA5_ncfile = Dataset(ERA5_filename)
                        for idl, lev in enumerate(levels):
                                
                            ERA5_hour = ERA5_ncfile.variables['time']
                            ERA5_level = ERA5_ncfile.variables['level'][:]
                            ERA5_time = num2date(ERA5_hour, ERA5_hour.units, ERA5_hour.calendar)
                            ERA5_idt = np.where(ERA5_time == time_now)[0][0]
                            ERA5_idl = np.where(ERA5_level == lev)[0][0]
                            ERA5_temp = ERA5_ncfile.variables[information['ERA5']][ERA5_idt,ERA5_idl,:,:]
                            ERA5_lat = np.transpose(np.tile(ERA5_ncfile.variables['latitude'][:], (1440, 1)))
                            ERA5_lon = np.tile(ERA5_ncfile.variables['longitude'][:], (721, 1))
                            ERA5_lon[ERA5_lon>180.0] = ERA5_lon[ERA5_lon>180.0] - 360.0
                            ERA5_index = (ERA5_lat < np.array(lat[-1, -1]) + 15.0) & (ERA5_lat > np.array(lat[0, 0]) - 15.0) & \
                                         (ERA5_lon < np.array(lon[-1, -1]) + 15.0) & (ERA5_lon > np.array(lon[0, 0]) - 15.0)
                            
                            ERA5_lat_1d = ERA5_lat[ERA5_index]
                            ERA5_lon_1d = ERA5_lon[ERA5_index]
                            ERA5_temp_1d = ERA5_temp[ERA5_index]
                            if var == 'q': ERA5_temp_1d = ERA5_temp_1d/(1.0-ERA5_temp_1d)
                            if var == 'avo':
                                ERA5_coriolis_parameter = metpy.calc.coriolis_parameter(np.deg2rad(ERA5_lat_1d))
                                ERA5_temp_1d = ERA5_temp_1d+ERA5_coriolis_parameter
                                ERA5_temp_1d = ERA5_temp_1d*100000.0
                            if var == 'geopt':
                                ERA5_temp_1d = ERA5_temp_1d/9.80665
                            ncfile_output.variables[var][idt,idl,:,:] = griddata((ERA5_lon_1d, ERA5_lat_1d), ERA5_temp_1d, (lon, lat), method='linear')
                            ERA5_ncfile.close()

                        else:
                            wrfout = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:%M:00')}")
                            if 'anl' in var:
                                dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'da')
                                wrfout = os.path.join(dir_wrfout, f"wrf_inout.{time_now.strftime('%Y%m%d%H')}.{dom}")
                            
                            if os.path.exists(wrfout):

                                ncfile = Dataset(wrfout)
                                p = getvar(ncfile, 'pressure')
                                if 'index' in information.keys():
                                    if information['unit'] == 'null':
                                        var_value = getvar(ncfile, information['name'])[information['index']]
                                    else:
                                        var_value = getvar(ncfile, information['name'], units=information['unit'])[information['index']]
                                else:
                                    if information['unit'] == 'null':
                                        var_value = getvar(ncfile, information['name'])
                                        if var == 'geopt': var_value = g_geoht.get_height(ncfile, msl=True)
                                    else:
                                        var_value = getvar(ncfile, information['name'], units=information['unit'])
                                ncfile.close()

                                temp = vertcross(var_value, p, wrfin=ncfile, levels=levels, \
                                                 start_point=start_point, end_point=end_point, latlon=True, meta=True)
                                      
lat_1d = []      
lon_1d = []      
coord_pairs = to_np(temp.coords['xy_loc'])
latlon_idx_cross_section = range(0, len(coord_pairs))

for pair in coord_pairs:
 18                   latlon_str = pair.latlon_str()
 19                         lat_1d.append(float(latlon_str.split(',')[0]))
 20                         lon_1d.append(float(latlon_str.split(',')[1]))
 21                         
 22                     lon_1d_2d, level_1d_2d = np.meshgrid(lon_1d, level, sparse=False, indexing='xy')
 23                     lon_1d   = np.reshape(lon_1d_2d, -1)
 24                     level_1d = np.reshape(level_1d_2d, -1)
 25                     temp_1d  = np.reshape(temp.data, -1)
 26                     ncfile.variables[var][idt,idd,:,:] = griddata((lon_1d, level_1d), temp_1d, (lon_2d, level_2d), method='linear')

                                temp_var_value = interplevel(var_value, p, list(levels.keys()))
                                ncfile_output.variables[var][idt,:,:,:] = temp_var_value

                    ncfile_output.close()