import os
import h5py
import importlib
import requests
import pygrib
import metpy.calc
import numpy as np
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from wrf import getvar, latlon_coords, interplevel, g_geoht
from netCDF4 import Dataset, num2date
from scipy.interpolate import griddata
from metpy.units import units

def wrf_extract_variables_6h(data_library_names, dir_cases, case_names, exp_names,
                             specific_level, da_cycle, ref_exp_name='CTRL', variables=['u']):

    time_interval = 6
    accumulated_hours = 6.0

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        module = importlib.import_module(f"set_parameters_{data_library_name}")
        set_variables = getattr(module, 'set_variables')

        itime = attributes[(dir_case, case_name)]['itime']
        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        da_domains = attributes[(dir_case, case_name)]['da_domains']
        forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        history_interval = attributes[(dir_case, case_name)]['history_interval']
        initial_time = datetime(*itime)

        dir_cycling_da = os.path.join(dir_exp, 'cycling_da')
        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        dir_data = os.path.join(dir_exp, 'data')
        dir_ERA5 = os.path.join(dir_data, 'ERA5')
        dir_GFS = os.path.join(dir_data, 'GFS')
        dir_CMORPH = os.path.join(dir_data, 'CMORPH')
        dir_IMERG = os.path.join(dir_data, 'IMERG')
        dir_GSMaP = os.path.join(dir_data, 'GSMaP')
        os.makedirs(dir_weather_map, exist_ok=True)

        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
        n_time = da_cycle*cycling_interval/time_interval + int(forecast_hours/history_interval) + 1
        n_time = int(n_time)

        specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
        dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
        os.makedirs(dir_weather_map_case, exist_ok=True)

        if len(forecast_domains) > len(da_domains):
            domains = forecast_domains
        else:
            domains = da_domains
        # domains = ['d02']
        for dom in tqdm(domains, desc='Domains', position=0, leave=True):
            if 'IMERG'  in exp_name or \
               'CMORPH' in exp_name or \
               'GSMaP'  in exp_name or \
               'GFS'    in exp_name or \
               'ERA5'   in exp_name:
                dir_wrfout = os.path.join(dir_cycling_da, f"{case_name}_{ref_exp_name}_C{str(da_cycle).zfill(2)}", 'bkg')
            else:
                dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'bkg')
            wrfout = os.path.join(dir_wrfout, f"wrfout_{dom}_{anl_end_time.strftime('%Y-%m-%d_%H:%M:00')}")
            ncfile = Dataset(wrfout)
            p = getvar(ncfile, 'pressure')
            ncfile.close()
            lat, lon = latlon_coords(p)
            (n_lat, n_lon) = lat.shape
            for var in tqdm(variables, desc='Variables', position=0, leave=True):
                (information, levels) = set_variables(var)
                n_level = len(levels.keys())
                filename = os.path.join(dir_weather_map_case, f"{var}_{specific_level}_{dom}.nc")
                os.system(f"rm -rf {filename}")
                ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                ncfile_output.createDimension('n_time',  n_time)
                ncfile_output.createDimension('n_level', n_level)
                ncfile_output.createDimension('n_lat',   n_lat)
                ncfile_output.createDimension('n_lon',   n_lon)
                ncfile_output.createVariable('time',  'f8', ('n_time'))
                ncfile_output.createVariable('lat',   'f8', ('n_lat', 'n_lon'))
                ncfile_output.createVariable('lon',   'f8', ('n_lat', 'n_lon'))
                ncfile_output.createVariable(var,     'f8', ('n_time', 'n_lat', 'n_lon'))
                ncfile_output.variables['lat'][:,:] = lat
                ncfile_output.variables['lon'][:,:] = lon
                ncfile_output.variables[var][:,:,:] = 0.0
                for idt in tqdm(range(n_time), desc='Times', position=0, leave=True):
                    time_now = initial_time + timedelta(hours = idt*time_interval)
                    ncfile_output.variables['time'][idt] = int(time_now.strftime('%Y%m%d%H%M00'))
                    # To Calculate 6-hr accumulated precipitation
                    if var == 'rain_6h':
                        if 'IMERG' in exp_name:
                            IMERG_time_resolution = 0.5
                            IMERG_version = attributes[(dir_case, case_name)]['IMERG_version']
                            IMERG_version_run = IMERG_version['run']
                            IMERG_version_version = IMERG_version['version']
                            IMERG_prep = np.zeros((3600, 1800), dtype=float)
                            for dh in np.arange(0, accumulated_hours, IMERG_time_resolution):
                                time_IMERG = time_now + timedelta(hours=dh)
                                YYMMDD = time_IMERG.strftime('%Y%m%d')
                                HHMMSS = time_IMERG.strftime('%H%M%S')
                                info = os.popen(f'ls {dir_IMERG}/{YYMMDD}/*{IMERG_version_run}*{YYMMDD}-S{HHMMSS}*{IMERG_version_version}.HDF5').readlines()
                                file_IMERG = info[0].strip()
                                f = h5py.File(file_IMERG)
                                IMERG_prep = IMERG_prep + IMERG_time_resolution*f['Grid']['precipitationCal'][0,:,:]
                                IMERG_lat = np.tile(f['Grid']['lat'][:], (3600, 1))
                                IMERG_lon = np.transpose(np.tile(f['Grid']['lon'][:], (1800, 1)))
                                IMERG_lon[IMERG_lon > 180.0] = IMERG_lon[IMERG_lon > 180.0] - 360.0
                                IMERG_index = (IMERG_lat < np.array(lat[-1, -1]) + 15.0) & (IMERG_lat > np.array(lat[0, 0]) - 15.0) & \
                                              (IMERG_lon < np.array(lon[-1, -1]) + 15.0) & (IMERG_lon > np.array(lon[0, 0]) - 15.0)
                                f.close()
                            IMERG_prep_1d = IMERG_prep[IMERG_index]
                            IMERG_lat_1d  = IMERG_lat[IMERG_index]
                            IMERG_lon_1d  = IMERG_lon[IMERG_index]
                            ncfile_output.variables[var][idt,:,:] = griddata((IMERG_lon_1d, IMERG_lat_1d), IMERG_prep_1d, (lon, lat), method='linear')
                        elif 'CMORPH' in exp_name:
                            CMORPH_time_resolution = 0.5
                            CMORPH_version = attributes[(dir_case, case_name)]['CMORPH_version']
                            CMORPH_prep = np.zeros((1649, 4948), dtype=float)
                            for dh in np.arange(0, accumulated_hours, CMORPH_time_resolution):
                                time_CMORPH = time_now + timedelta(hours=dh)
                                YYMMDD = time_CMORPH.strftime('%Y%m%d')
                                YYMMDDHH = time_CMORPH.strftime('%Y%m%d%H')
                                mm_index = int(int(time_CMORPH.strftime('%M'))/30)
                                info = os.popen(f'ls {dir_CMORPH}/{YYMMDD}/*{CMORPH_version}_{YYMMDDHH}.nc').readlines()
                                file_CMORPH = info[0].strip()
                                f = Dataset(file_CMORPH)
                                CMORPH_prep = CMORPH_prep + CMORPH_time_resolution*f['cmorph'][mm_index,:,:]
                                
                                CMORPH_lat_1 = f['lat_bounds'][:,0]
                                CMORPH_lat_2 = f['lat_bounds'][:,1]
                                CMORPH_lat   = np.transpose(np.tile((CMORPH_lat_1 + CMORPH_lat_2)/2.0, (4948, 1)))
                                CMORPH_lon_1 = f['lon_bounds'][:,0]
                                CMORPH_lon_2 = f['lon_bounds'][:,1]
                                CMORPH_lon   = np.tile((CMORPH_lon_1 + CMORPH_lon_2)/2.0, (1649, 1))
                                CMORPH_lon[CMORPH_lon > 180.0] = CMORPH_lon[CMORPH_lon > 180.0] - 360.0
                                CMORPH_index = (CMORPH_lat < np.array(lat[-1, -1]) + 15.0) & (CMORPH_lat > np.array(lat[0, 0]) - 15.0) & \
                                               (CMORPH_lon < np.array(lon[-1, -1]) + 15.0) & (CMORPH_lon > np.array(lon[0, 0]) - 15.0)
                                f.close()
                            CMORPH_prep_1d = CMORPH_prep[CMORPH_index]
                            CMORPH_lat_1d  = CMORPH_lat[CMORPH_index]
                            CMORPH_lon_1d  = CMORPH_lon[CMORPH_index]
                            ncfile_output.variables[var][idt,:,:] = griddata((CMORPH_lon_1d, CMORPH_lat_1d), CMORPH_prep_1d, (lon, lat), method='linear')
                        elif 'GSMaP' in exp_name:
                            GSMaP_time_resolution = 1.0
                            GSMaP_version = attributes[(dir_case, case_name)]['GSMaP_version']
                            GSMaP_prep = np.zeros((3600, 1800), dtype=float)
                            for dh in np.arange(0, accumulated_hours, GSMaP_time_resolution):
                                time_GSMaP = time_now + timedelta(hours=dh)
                                YYMMDD = time_GSMaP.strftime('%Y%m%d')
                                YYMMDDHHMM = time_GSMaP.strftime('%Y%m%d%H%M')
                                
                                info = os.popen(f'ls {dir_GSMaP}/{YYMMDD}/*{YYMMDDHHMM[2:]}*{GSMaP_version}.h5').readlines()
                                file_GSMaP = info[0].strip()
                                f = h5py.File(file_GSMaP)
                                GSMaP_prep = GSMaP_prep + GSMaP_time_resolution*f['Grid']['hourlyPrecipRateGC'][:,:]
                                GSMaP_lat = f['Grid']['Latitude'][:,:]
                                GSMaP_lon = f['Grid']['Longitude'][:,:]
                                GSMaP_lon[GSMaP_lon > 180.0] = GSMaP_lon[GSMaP_lon > 180.0] - 360.0
                                GSMaP_index = (GSMaP_lat < np.array(lat[-1, -1]) + 15.0) & (GSMaP_lat > np.array(lat[0, 0]) - 15.0) & \
                                              (GSMaP_lon < np.array(lon[-1, -1]) + 15.0) & (GSMaP_lon > np.array(lon[0, 0]) - 15.0)
                                f.close()
                            GSMaP_prep_1d = GSMaP_prep[GSMaP_index]
                            GSMaP_lat_1d  = GSMaP_lat[GSMaP_index]
                            GSMaP_lon_1d  = GSMaP_lon[GSMaP_index]
                            ncfile_output.variables[var][idt,:,:] = griddata((GSMaP_lon_1d, GSMaP_lat_1d), GSMaP_prep_1d, (lon, lat), method='linear')         
                        else:
                            if time_now < anl_end_time:
                                time_resolution = cycling_interval
                            else:
                                time_resolution = history_interval
                            for idx in range(0, int(accumulated_hours), time_resolution):
                                time_0 = time_now + timedelta(hours = idx)
                                time_1 = time_now + timedelta(hours = idx+history_interval)
                                wrfout_0 = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_0.strftime('%Y-%m-%d_%H:%M:00')}")
                                wrfout_1 = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_1.strftime('%Y-%m-%d_%H:%M:00')}")
                                if os.path.exists(wrfout_0) and os.path.exists(wrfout_1):
                                    ncfile   = Dataset(wrfout_0)
                                    RAINNC_0 = getvar(ncfile, 'RAINNC')
                                    RAINC_0  = getvar(ncfile, 'RAINC')
                                    ncfile.close()
                                    ncfile   = Dataset(wrfout_1)
                                    RAINNC_1 = getvar(ncfile, 'RAINNC')
                                    RAINC_1  = getvar(ncfile, 'RAINC')
                                    ncfile.close()
                                    if time_0 <= anl_end_time:
                                        RAINNC_0 = 0.0
                                        RAINC_0 = 0.0
                                    rainfall = RAINNC_1 + RAINC_1 - RAINNC_0 - RAINC_0
                                    ncfile_output.variables[var][idt,:,:] = ncfile_output.variables[var][idt,:,:] + rainfall
                    elif 'inc' in var:
                        var_bkg = var.replace('_inc', '')
                        var_anl = var.replace('_inc', '_anl')
                        filename_bkg = filename.replace('_inc', '')
                        filename_anl = filename.replace('_inc', '_anl')
                        ncfile_bkg = Dataset(filename_bkg)
                        ncfile_anl = Dataset(filename_anl)
                        ncfile_output.variables[var][idt,:,:] = ncfile_anl.variables[var_anl][idt,:,:] - ncfile_bkg.variables[var_bkg][idt,:,:]
                        ncfile_bkg.close()
                        ncfile_anl.close()
                    
                    elif var == 'vo' and var == 'vo_anl':
                        var_avo = var.replace('vo', 'avo')
                        filename_avo = filename.replace('vo', 'avo')
                        ncfile_avo = Dataset(filename_avo)
                        lat_avo = ncfile_output.variables['lat'][:,:]
                        ncfile_output.variables[var][idt,:,:] = ncfile_avo.variables[var_avo][idt,:,:] - metpy.calc.coriolis_parameter(lat_avo)
                        print(metpy.calc.coriolis_parameter(lat_avo))
                        print(miao)
                        ncfile_avo.close()
                    
                    else:
                        if 'GFS' in exp_name:
                            if 'anl' in var:
                                var_bkg = var.replace('_anl', '')
                                filename_bkg = filename.replace('_anl', '')
                                ncfile_bkg = Dataset(filename_bkg)
                                ncfile_output.variables[var][idt,:,:] = ncfile_bkg.variables[var_bkg][idt,:,:]
                                ncfile_bkg.close()
                            
                            else:
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
                                if specific_level == 9999:
                                    if var == 'u10' or var == 'v10':
                                        GFS_temp = GFS_pygrib.select(name=information['GFS'], typeOfLevel='heightAboveGround', level=10)[0]
                                        GFS_lat, GFS_lon = GFS_temp.latlons()
                                    elif var == 'wspd10':
                                        GFS_temp_u10 = GFS_pygrib.select(name=information['GFS'][0], typeOfLevel='heightAboveGround', level=10)[0]
                                        GFS_temp_v10 = GFS_pygrib.select(name=information['GFS'][1], typeOfLevel='heightAboveGround', level=10)[0]
                                        GFS_lat, GFS_lon = GFS_temp_u10.latlons()
                                    elif var == 'sp':
                                        GFS_temp = GFS_pygrib.select(name=information['GFS'], typeOfLevel='surface', level=0)[0]
                                        GFS_lat, GFS_lon = GFS_temp.latlons()
                                    elif var == 'slp':
                                        GFS_temp = GFS_pygrib.select(name=information['GFS'], typeOfLevel='meanSea', level=0)[0]
                                        GFS_lat, GFS_lon = GFS_temp.latlons()

                                    GFS_lon[GFS_lon>180.0] = GFS_lon[GFS_lon>180.0] - 360.0
                                    GFS_index = (GFS_lat < np.array(lat[-1, -1]) + 15.0) & (GFS_lat > np.array(lat[0, 0]) - 15.0) & \
                                                (GFS_lon < np.array(lon[-1, -1]) + 15.0) & (GFS_lon > np.array(lon[0, 0]) - 15.0)
                                    
                                    GFS_lat_1d = GFS_lat[GFS_index]
                                    GFS_lon_1d = GFS_lon[GFS_index]

                                    if var == 'wspd10':
                                        GFS_temp_1d = np.sqrt(np.square(GFS_temp_u10.values[GFS_index]) + np.square(GFS_temp_v10.values[GFS_index]))
                                    else:
                                        GFS_temp_1d = GFS_temp.values[GFS_index]
                                    if var == 'slp': GFS_temp_1d = GFS_temp_1d/100.0
                                else:
                                    GFS_temp = GFS_pygrib.select(name=information['GFS'], typeOfLevel='isobaricInhPa', level=specific_level)[0]
                                    GFS_lat, GFS_lon = GFS_temp.latlons()
                                    GFS_lon[GFS_lon>180.0] = GFS_lon[GFS_lon>180.0] - 360.0
                                    GFS_index = (GFS_lat < np.array(lat[-1, -1]) + 15.0) & (GFS_lat > np.array(lat[0, 0]) - 15.0) & \
                                                (GFS_lon < np.array(lon[-1, -1]) + 15.0) & (GFS_lon > np.array(lon[0, 0]) - 15.0)

                                    GFS_lat_1d = GFS_lat[GFS_index]
                                    GFS_lon_1d = GFS_lon[GFS_index]
                                    GFS_temp_1d = GFS_temp.values[GFS_index]
                                    if var == 'avo': GFS_temp_1d = GFS_temp_1d*100000.0
                                    if var == 'q':
                                        GFS_temperature = GFS_pygrib.select(name='Temperature', typeOfLevel='isobaricInhPa', level=specific_level)[0]
                                        GFS_temperature_1d = GFS_temperature.values[GFS_index]
                                        GFS_temp_1d = np.array(GFS_temp_1d)
                                        GFS_temperature_1d = np.array(GFS_temperature_1d)
                                        GFS_dewpoint_1d = np.array(metpy.calc.dewpoint_from_relative_humidity(GFS_temperature_1d*units.K, GFS_temp_1d*units.percent))
                                        GFS_temp_1d = np.array(metpy.calc.specific_humidity_from_dewpoint(specific_level*units.hPa, GFS_dewpoint_1d*units.degC).to('kg/kg'))

                                ncfile_output.variables[var][idt,:,:] = griddata((GFS_lon_1d, GFS_lat_1d), GFS_temp_1d, (lon, lat), method='linear')
                                GFS_pygrib.close()
                        elif 'ERA5' in exp_name:
                            if 'anl' in var:
                                
                                var_bkg = var.replace('_anl', '')
                                filename_bkg = filename.replace('_anl', '')
                                ncfile_bkg = Dataset(filename_bkg)
                                ncfile_output.variables[var][idt,:,:] = ncfile_bkg.variables[var_bkg][idt,:,:]
                                ncfile_bkg.close()
                            
                            else:
                                if specific_level == 9999:
                                    ERA5_filename = os.path.join(dir_ERA5, 'ERA5_single_level.nc')
                                    ERA5_ncfile = Dataset(ERA5_filename)
                                    ERA5_hour = ERA5_ncfile.variables['time']
                                    ERA5_time = num2date(ERA5_hour, ERA5_hour.units, ERA5_hour.calendar)
                                    ERA5_idt = np.where(ERA5_time == time_now)[0][0]
                                    if var == 'wspd10':
                                        ERA5_temp_u10 = ERA5_ncfile.variables[information['ERA5'][0]][ERA5_idt,:,:]
                                        ERA5_temp_v10 = ERA5_ncfile.variables[information['ERA5'][1]][ERA5_idt,:,:]
                                        ERA5_temp = np.sqrt(np.square(ERA5_temp_u10) + np.square(ERA5_temp_v10))     
                                    else:
                                        ERA5_temp = ERA5_ncfile.variables[information['ERA5']][ERA5_idt,:,:]
                                    ERA5_lat = np.transpose(np.tile(ERA5_ncfile.variables['latitude'][:], (1440, 1)))
                                    ERA5_lon = np.tile(ERA5_ncfile.variables['longitude'][:], (721, 1))
                                    ERA5_lon[ERA5_lon>180.0] = ERA5_lon[ERA5_lon>180.0] - 360.0
                                    ERA5_index = (ERA5_lat < np.array(lat[-1, -1]) + 15.0) & (ERA5_lat > np.array(lat[0, 0]) - 15.0) & \
                                                 (ERA5_lon < np.array(lon[-1, -1]) + 15.0) & (ERA5_lon > np.array(lon[0, 0]) - 15.0)
                                else:
                                    ERA5_filename = os.path.join(dir_ERA5, 'ERA5_pressure_levels.nc')
                                    ERA5_ncfile = Dataset(ERA5_filename)
                                    ERA5_hour = ERA5_ncfile.variables['time']
                                    ERA5_level = ERA5_ncfile.variables['level'][:]
                                    ERA5_time = num2date(ERA5_hour, ERA5_hour.units, ERA5_hour.calendar)
                                    ERA5_idt = np.where(ERA5_time == time_now)[0][0]
                                    ERA5_idl = np.where(ERA5_level == specific_level)[0][0]
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
                                if var == 'geopt': ERA5_temp_1d = ERA5_temp_1d/9.80665
                                if var == 'slp': ERA5_temp_1d = ERA5_temp_1d/100.0
                                ncfile_output.variables[var][idt,:,:] = griddata((ERA5_lon_1d, ERA5_lat_1d), ERA5_temp_1d, (lon, lat), method='linear')
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
                                        if var == 'geopt' or var == 'geopt_anl':
                                            var_value = g_geoht.get_height(ncfile, msl=True)
                                    else:
                                        var_value = getvar(ncfile, information['name'], units=information['unit'])
                                ncfile.close()
                                if 9999 in levels:
                                    ncfile_output.variables[var][idt,:,:] = var_value
                                else:
                                    temp_var_value = interplevel(var_value, p, specific_level)
                                    ncfile_output.variables[var][idt,:,:] = temp_var_value
                ncfile_output.close()
