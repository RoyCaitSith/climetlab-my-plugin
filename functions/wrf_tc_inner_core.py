import os
import h5py
import importlib
import requests
import pygrib
import metpy.calc
import numpy as np
import pandas as pd
import cal_polar_to_latlon as clatlon
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from wrf import getvar, latlon_coords, interplevel, g_geoht
from netCDF4 import Dataset, num2date
from scipy.interpolate import griddata
from metpy.units import units

def wrf_tc_inner_core_6h(data_library_names, dir_cases, case_names, exp_names, da_cycle,
                         variables=['u']):

    time_interval = 6
    levels=range(25, 1001, 25)
    angles = range(0, 361, 5)
    radii = range(0, 361, 5)
    n_level = len(levels)
    n_angle = len(angles)
    n_radius = len(radii)

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
        dir_inner_core = os.path.join(dir_exp, 'inner_core')
        dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
        dir_best_track = os.path.join(dir_track_intensity, 'best_track')
        os.makedirs(dir_inner_core, exist_ok=True)

        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        n_time = da_cycle*cycling_interval/time_interval + int(forecast_hours/history_interval)
        n_time = int(n_time)
        n_time = 1

        specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
        dir_inner_core_case = os.path.join(dir_inner_core, specific_case)
        os.makedirs(dir_inner_core_case, exist_ok=True)

        dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'bkg')

        if len(forecast_domains) > len(da_domains):
            domains = forecast_domains
        else:
            domains = da_domains
        # domains = ['d02']

        for dom in tqdm(domains, desc='Domains', position=0, leave=True):      
            for var in tqdm(variables, desc='Variables', position=0, leave=True):
                (information, specific_levels) = set_variables(var)
                filename = os.path.join(dir_inner_core_case, f"{var}_{dom}.nc")
                os.system(f"rm -rf {filename}")
                ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                ncfile_output.createDimension('n_time',   n_time)
                ncfile_output.createDimension('n_level',  n_level)
                ncfile_output.createDimension('n_angle',  n_angle)
                ncfile_output.createDimension('n_radius', n_radius)
                ncfile_output.createVariable('time',   'f8', ('n_time'))
                ncfile_output.createVariable('level',  'f8', ('n_level'))
                ncfile_output.createVariable('angle',  'f8', ('n_angle'))
                ncfile_output.createVariable('radius', 'f8', ('n_radius'))
                ncfile_output.createVariable('lat',   'f8', ('n_angle', 'n_radius'))
                ncfile_output.createVariable('lon',   'f8', ('n_angle', 'n_radius'))
                ncfile_output.createVariable(var,     'f8', ('n_time', 'n_level', 'n_angle', 'n_radius'))
                ncfile_output.variables['level'][:]  = levels
                ncfile_output.variables['angle'][:]  = angles
                ncfile_output.variables['radius'][:] = radii 
                ncfile_output.variables['lat'][:,:] = 0.0
                ncfile_output.variables['lon'][:,:] = 0.0
                ncfile_output.variables[var][:,:,:] = 0.0

                for idt in tqdm(range(n_time), desc='Times', position=0, leave=True):
                    time_now = anl_start_time + timedelta(hours = idt*time_interval)
                    time_now_int = int(time_now.strftime('%Y%m%d%H%M00'))
                    ncfile_output.variables['time'][idt] = time_now_int
                    # To Calculate 6-hr accumulated precipitation
                    if 'inc' in var:
                        var_bkg = var.replace('_inc', '')
                        var_anl = var.replace('_inc', '_anl')
                        filename_bkg = filename.replace('_inc', '')
                        filename_anl = filename.replace('_inc', '_anl')
                        ncfile_bkg = Dataset(filename_bkg)
                        ncfile_anl = Dataset(filename_anl)
                        ncfile_output.variables[var][idt,:,:] = ncfile_anl.variables[var_anl][idt,:,:] - ncfile_bkg.variables[var_bkg][idt,:,:]
                        ncfile_bkg.close()
                        ncfile_anl.close()
                    
                    elif 'anl' in var:
                        var_bkg = var.replace('_anl', '')
                        filename_bkg = filename.replace('_anl', '')
                        ncfile_bkg = Dataset(filename_bkg)
                        ncfile_output.variables[var][idt,:,:] = ncfile_bkg.variables[var_bkg][idt,:,:]
                        ncfile_bkg.close()

                    else:
                        wrfout = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:%M:00')}")
                        if 'anl' in var:
                            dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'da')
                            wrfout = os.path.join(dir_wrfout, f"wrf_inout.{time_now.strftime('%Y%m%d%H')}.{dom}")
                            
                        if os.path.exists(wrfout):
                            ncfile = Dataset(wrfout)
                            p = getvar(ncfile, 'pressure')
                            wrf_lat, wrf_lon = latlon_coords(p)
                            wrf_lat = np.array(wrf_lat)
                            wrf_lon = np.array(wrf_lon)

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

                            best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", f"{dom}.csv"]))
                            if not os.path.exists(best_track):
                                best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", 'd01.csv']))

                            df = pd.read_csv(best_track)
                            bt_lats = list(df['LAT'][:])
                            bt_lons = list(df['LON'][:])
                            bt_dates = list(df['Date_Time'][:])

                            time_now_datetime = datetime.strptime(str(time_now_int), '%Y%m%d%H%M%S')
                            for id_bt, bt_date in enumerate(bt_dates):
                                bt_datetime = datetime.strptime(bt_date, '%Y-%m-%d %H:%M:%S')
                                if bt_datetime == time_now_datetime:
                                    bt_lat = bt_lats[id_bt]
                                    bt_lon = bt_lons[id_bt]
                            
                            for idr in range(0, len(radii)):
                                for ida in range(0, len(angles)):
                                    lat_polar, lon_polar = clatlon.Cal_LatLon(bt_lat, bt_lon, radii[idr], angles[ida])
                                    ncfile_output.variables['lat'][ida,idr] = lat_polar
                                    ncfile_output.variables['lon'][ida,idr] = lon_polar
                            
                            tc_index = (wrf_lat < bt_lat + 15.0) & (wrf_lat > bt_lat - 15.0) & \
                                       (wrf_lon < bt_lon + 15.0) & (wrf_lon > bt_lon - 15.0)
                            wrf_lon_1d = wrf_lon[tc_index]
                            wrf_lat_1d = wrf_lat[tc_index]

                            temp_var_value = interplevel(var_value, p, levels)
                            temp_var_value = np.array(temp_var_value)

                            for idl, lev in enumerate(levels):
                                print(lev)
                                wrf_temp_1d = temp_var_value[idl, tc_index]
                                ncfile_output.variables[var][idt,idl,:,:] = griddata((wrf_lon_1d, wrf_lat_1d), wrf_temp_1d, \
                                         (ncfile_output.variables['lon'][:,:], ncfile_output.variables['lat'][:,:]), method='linear')

                ncfile_output.close()
