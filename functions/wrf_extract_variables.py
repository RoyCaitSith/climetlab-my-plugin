import os
import h5py
import importlib
import numpy as np
from set_parameters import set_variables
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
from tqdm.notebook import tqdm
from wrf import getvar, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata

def wrf_extract_variables(data_library_names, dir_cases, case_names, exp_names, ref_exp_name='CONV', variables=['ua']):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        itime = attributes[(dir_case, case_name)]['itime']

        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        da_domains = attributes[(dir_case, case_name)]['da_domains']
        forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        history_interval = attributes[(dir_case, case_name)]['history_interval']
        initial_time = datetime(*itime)

        dir_data = os.path.join(dir_exp, 'data')
        dir_ERA5 = os.path.join(dir_data, 'ERA5')
        dir_GFS = os.path.join(dir_data, 'GFS')
        dir_IMERG = os.path.join(dir_data, 'IMERG')
        dir_cycling_da = os.path.join(dir_exp, 'cycling_da')
        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        os.makedirs(dir_weather_map, exist_ok=True)

        for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', leave=False):

            anl_start_time = initial_time + timedelta(hours=cycling_interval)
            anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
            n_time = total_da_cycles + int(forecast_hours/history_interval)

            specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
            dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
            os.makedirs(dir_weather_map_case, exist_ok=True)

            if len(forecast_domains) > len(da_domains):
                domains = forecast_domains
            else:
                domains = da_domains

            for dom in tqdm(domains, desc='Domains', leave=False):

                if 'IMERG' in exp_name or 'GFS' in exp_name or 'ERA5' in exp_name:
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

                    filename = os.path.join(dir_weather_map_case, f"{var}_{dom}.nc")
                    os.system(f"rm -rf {filename}")

                    ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                    ncfile_output.createDimension('n_time',  n_time)
                    ncfile_output.createDimension('n_level', n_level)
                    ncfile_output.createDimension('n_lat',   n_lat)
                    ncfile_output.createDimension('n_lon',   n_lon)
                    ncfile_output.createVariable('time',  'f8', ('n_time'))
                    ncfile_output.createVariable('level', 'f8', ('n_level'))
                    ncfile_output.createVariable('lat',   'f8', ('n_lat', 'n_lon'))
                    ncfile_output.createVariable('lon',   'f8', ('n_lat', 'n_lon'))
                    ncfile_output.createVariable(var,     'f8', ('n_time', 'n_level', 'n_lat', 'n_lon'))

                    ncfile_output.variables['level'][:] = list(levels.keys())
                    ncfile_output.variables['lat'][:,:] = lat
                    ncfile_output.variables['lon'][:,:] = lon
                    ncfile_output.variables[var][:,:,:,:] = 0.0

                    print(list(levels.keys()))

                    time_now = anl_start_time
                    idt = 0
                    while idt < n_time:

                        ncfile_output.variables['time'][idt] = int(time_now.strftime('%Y%m%d%H%M00'))
                        if time_now < anl_end_time:
                            time_interval = cycling_interval
                        else:
                            time_interval = history_interval

                        if 'rain_6h' in var:

                            accumulated_hours = 6.0

                            if 'IMERG' in exp_name:

                                IMERG_time_resolution = 0.5
                                IMERG_prep = np.zeros((3600, 1800), dtype=float)

                                for dh in np.arange(0.0, accumulated_hours, IMERG_time_resolution):

                                    time_IMERG = time_now + timedelta(hours=dh)
                                    YYMMDD = time_IMERG.strftime('%Y%m%d')
                                    HHMMSS = time_IMERG.strftime('%H%M%S')

                                    info = os.popen(f'ls {dir_IMERG}/{YYMMDD}/3B-HHR.MS.MRG.3IMERG.{YYMMDD}-S{HHMMSS}*').readlines()
                                    file_IMERG = info[0].strip()
                                    f = h5py.File(file_IMERG)
                                    IMERG_prep = IMERG_prep + IMERG_time_resolution*f['Grid']['precipitationCal'][0,:,:]

                                    IMERG_prep  = IMERG_prep
                                    IMERG_lat   = np.tile(f['Grid']['lat'][:], (3600, 1))
                                    IMERG_lon   = np.transpose(np.tile(f['Grid']['lon'][:], (1800, 1)))
                                    IMERG_index = (IMERG_lat < np.array(lat[-1, -1]) + 15.0) & (IMERG_lat > np.array(lat[0, 0]) - 15.0) & \
                                                  (IMERG_lon < np.array(lon[-1, -1]) + 15.0) & (IMERG_lon > np.array(lon[0, 0]) - 15.0)

                                IMERG_prep_1d = IMERG_prep[IMERG_index]
                                IMERG_lat_1d  = IMERG_lat[IMERG_index]
                                IMERG_lon_1d  = IMERG_lon[IMERG_index]
                                ncfile_output.variables['rainfall'][idt,0,:,:] = griddata((IMERG_lon_1d, IMERG_lat_1d), IMERG_prep_1d, (lon, lat), method='linear')

                            else:

                                for idx in range(0, int(accumulated_hours), time_interval):

                                    time_0 = time_now + timedelta(hours = idx)
                                    time_1 = time_now + timedelta(hours = idx+history_interval)

                                    wrfout_0 = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_0.strftime('%Y-%m-%d_%H:%M:00')}")
                                    wrfout_1 = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_1.strftime('%Y-%m-%d_%H:%M:00')}")

                                    ncfile   = Dataset(wrfout_0)
                                    RAINNC_0 = getvar(ncfile, 'RAINNC')
                                    RAINC_0  = getvar(ncfile, 'RAINC')
                                    ncfile.close()

                                    ncfile   = Dataset(wrfout_1)
                                    RAINNC_1 = getvar(ncfile, 'RAINNC')
                                    RAINC_1  = getvar(ncfile, 'RAINC')
                                    ncfile.close()

                                    if time_0 < anl_end_time:
                                        RAINNC_0 = 0.0
                                        RAINC_0 = 0.0

                                    rainfall = RAINNC_1 + RAINC_1 - RAINNC_0 - RAINC_0
                                    ncfile_output.variables[var][idt,0,:,:] = ncfile_output.variables[var][idt,0,:,:] + rainfall

                        else:

                            if 'GFS' in exp_name:

                                wrfout = '1'

                            else:

                                wrfout = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:%M:00')}")
                                if 'anl' in var:
                                    dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'da')
                                    wrfout = os.path.join(dir_wrfout, f"wrf_inout.{time_now.strftime('%Y%m%d%H')}.{dom}")

                                if not ('anl' in var and time_now > anl_end_time):

                                    ncfile = Dataset(wrfout)
                                    p = getvar(ncfile, 'pressure')
                                    if information['unit'] == 'null':
                                        var_value = getvar(ncfile, var)
                                    else:
                                        var_value = getvar(ncfile, var, units=information['unit'])
                                    ncfile.close()

                                if 9999 in levels:
                                    ncfile_output.variables[var][idt,0,0,:,:] = var_value
                                else:
                                    temp_var_value = interplevel(var_bkg, p_bkg, list(levels.keys()))
                                    ncfile_output.variables[var][idt,idl,:,:] = temp_var_value

                        time_now = time_now + timedelta(hours = time_interval)
                        idt += 1

                    ncfile_output.close()