import os
import importlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import colormaps as cmaps
from datetime import datetime, timedelta
from netCDF4 import Dataset
from scipy.interpolate import griddata
from tqdm.notebook import tqdm
from metpy.units import units
from IPython.display import display
from IPython.display import Image as IPImage
from wrf import getvar, latlon_coords, interplevel
from matplotlib.backends.backend_pdf import PdfPages
from combine_and_show_images import combine_images_grid

def wrf_extract_APR(data_library_names, dir_cases, case_names, exp_names):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        da_domains = attributes[(dir_case, case_name)]['da_domains']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        initial_time = datetime(*itime)

        dir_cycling_da = os.path.join(dir_exp, 'cycling_da')
        dir_cross_section = os.path.join(dir_exp, 'cross_section')
        dir_data = os.path.join(dir_exp, 'data')
        dir_APR = os.path.join(dir_data, 'APR-3')
        os.makedirs(dir_cross_section, exist_ok=True)

        for dom in tqdm(da_domains, desc='Domains', position=0, leave=True):
            # for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', position=0, leave=True):
            for da_cycle in tqdm(range(4, 5, 1), desc='Cycles', position=0, leave=True):

                anl_start_time = initial_time + timedelta(hours=cycling_interval)
                n_time = int(da_cycle)
                specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
                dir_cross_section_case = os.path.join(dir_cross_section, specific_case)
                os.makedirs(dir_cross_section_case, exist_ok=True)

                for idt in tqdm(range(n_time), desc='Times', position=0, leave=True):

                    time_now = anl_start_time + timedelta(hours = idt*cycling_interval)
                    anl_start_time_YYYYMMDD = anl_start_time.strftime('%Y%m%d')
                    time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')

                    filename_APR3nad = os.path.join(dir_APR, f"cpexcv-APR3nad_DC8_{anl_start_time_YYYYMMDD}_R0.nc")
                    ncfile_APR3nad = Dataset(filename_APR3nad, 'r')
                    lores_zhh14 = ncfile_APR3nad.variables['lores_zhh14'][:,:]
                    lores_zhh35 = ncfile_APR3nad.variables['lores_zhh35'][:,:]
                    lores_zZN35 = ncfile_APR3nad.variables['lores_zZN35'][:,:]
                    lat = ncfile_APR3nad.variables['lat'][:,:]
                    lon = ncfile_APR3nad.variables['lon'][:,:]
                    alt_ac = ncfile_APR3nad.variables['alt_ac'][:]
                    alt_range = ncfile_APR3nad.variables['alt_range'][:]
                    time = ncfile_APR3nad.variables['time'][:]
                    ncfile_APR3nad.close()

                    (n_time, n_geopt) = lores_zhh14.shape

                    filename = os.path.join(dir_cross_section_case, f"{time_now_YYYYMMDDHH}_APR3_{dom}.nc")
                    os.system(f"rm -rf {filename}")

                    # Ns: numbers of scans (along track), at low resolution
                    # Nr: number of range bins
                    ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                    ncfile_output.createDimension('n_time',  n_time)
                    ncfile_output.createDimension('n_geopt', n_geopt)
                    ncfile_output.createVariable('alt_ac',  'f8', ('n_time'))
                    ncfile_output.createVariable('geopt',   'f8', ('n_time', 'n_geopt'))
                    ncfile_output.createVariable('time',    'f8', ('n_time', 'n_geopt'))
                    ncfile_output.createVariable('lat',     'f8', ('n_time', 'n_geopt'))
                    ncfile_output.createVariable('lon',     'f8', ('n_time', 'n_geopt'))
                    ncfile_output.createVariable('zhh14',   'f8', ('n_time', 'n_geopt'))
                    ncfile_output.createVariable('zhh35',   'f8', ('n_time', 'n_geopt'))
                    ncfile_output.createVariable('zZN35',   'f8', ('n_time', 'n_geopt'))
                    ncfile_output.createVariable('dbz_bkg', 'f8', ('n_time', 'n_geopt'))
                    ncfile_output.createVariable('dbz_anl', 'f8', ('n_time', 'n_geopt'))

                    ncfile_output.variables['alt_ac'][:] = alt_ac
                    ncfile_output.variables['geopt'][:,:] = np.tile(alt_range, (n_time, 1))
                    ncfile_output.variables['time'][:,:] = np.transpose(np.tile(time, (n_geopt, 1)))
                    ncfile_output.variables['lat'][:,:] = lat
                    ncfile_output.variables['lon'][:,:] = lon
                    ncfile_output.variables['zhh14'][:,:] = lores_zhh14
                    ncfile_output.variables['zhh35'][:,:] = lores_zhh35
                    ncfile_output.variables['zZN35'][:,:] = lores_zZN35

                    dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'bkg')
                    wrfout = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:%M:00')}")
                    ncfile = Dataset(wrfout)
                    bkg_z = getvar(ncfile, 'height', units='m')
                    bkg_dbz = getvar(ncfile, 'dbz')
                    ncfile.close()

                    dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'da')
                    wrfout = os.path.join(dir_wrfout, f"wrf_inout.{time_now.strftime('%Y%m%d%H')}.{dom}")
                    ncfile = Dataset(wrfout)
                    anl_z = getvar(ncfile, 'height', units='m')
                    anl_dbz = getvar(ncfile, 'dbz')
                    ncfile.close()

                    wrf_lat, wrf_lon = latlon_coords(anl_z)
                    wrf_lat_1d = np.reshape(wrf_lat.data, -1)
                    wrf_lon_1d = np.reshape(wrf_lon.data, -1)
                    bkg_dbz_geopt = interplevel(bkg_dbz, bkg_z, alt_range)
                    anl_dbz_geopt = interplevel(anl_dbz, anl_z, alt_range)

                    for idl in tqdm(range(n_geopt), desc='Levels', position=0, leave=True):
                        lats = ncfile_output.variables['lat'][:,idl]
                        lons = ncfile_output.variables['lon'][:,idl]
                        bkg_dbz_interpolate_1d = np.reshape(bkg_dbz_geopt[idl,:,:].data, -1)
                        anl_dbz_interpolate_1d = np.reshape(anl_dbz_geopt[idl,:,:].data, -1)
                        ncfile_output.variables['dbz_bkg'][:,idl] = griddata((wrf_lon_1d, wrf_lat_1d), bkg_dbz_interpolate_1d, (lons, lats), method='linear')
                        ncfile_output.variables['dbz_anl'][:,idl] = griddata((wrf_lon_1d, wrf_lat_1d), anl_dbz_interpolate_1d, (lons, lats), method='linear')

                    ncfile_output.close()

def wrf_extract_APR3_composite(data_library_names, dir_cases, case_names, exp_names):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        initial_time = datetime(*itime)

        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        dir_data = os.path.join(dir_exp, 'data')
        dir_APR = os.path.join(dir_data, 'APR-3')
        os.makedirs(dir_weather_map, exist_ok=True)

        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        specific_case = '_'.join([case_name, exp_name, 'C'+str(total_da_cycles).zfill(2)])
        dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
        os.makedirs(dir_weather_map_case, exist_ok=True)

        anl_start_time_YYYYMMDD = anl_start_time.strftime('%Y%m%d')
        dir_cpexcv_APR3 = os.path.join(dir_APR, f"cpexcv-APR3_DC8_{anl_start_time_YYYYMMDD}_R0") 

        filenames = os.popen(f"ls {dir_cpexcv_APR3}/cpexcv-APR3*.nc").readlines()
        n_times = 0
        n_cross = 0
        n_geopt = 0
        for filename in filenames:
            filename_APR3nad = os.path.join(filename.rstrip('\n'))
            ncfile_APR3nad = Dataset(filename_APR3nad, 'r')
            lores_zhh14 = ncfile_APR3nad.variables['lores_zhh14'][:,:,:]
            (Ns, Nb, Nr) = lores_zhh14.shape
            n_times += Ns
            n_cross = np.max([n_cross, Nb])
            n_geopt = np.max([n_geopt, Nr])
            ncfile_APR3nad.close()
                
        print(n_times)
        print(n_cross)
        print(n_geopt)

        filename = os.path.join(dir_weather_map_case, f"{anl_start_time_YYYYMMDD}_APR3_3D.nc")
        os.system(f"rm -rf {filename}")

        ncfile_output = Dataset(filename, 'w', format='NETCDF4')
        ncfile_output.createDimension('n_times', n_times)
        ncfile_output.createDimension('n_cross', n_cross)
        ncfile_output.createDimension('n_geopt', n_geopt)
        ncfile_output.createVariable('zhh14', 'f8', ('n_times', 'n_cross', 'n_geopt'))
        ncfile_output.createVariable('zhh35', 'f8', ('n_times', 'n_cross', 'n_geopt'))
        ncfile_output.createVariable('zZN35', 'f8', ('n_times', 'n_cross', 'n_geopt'))
        ncfile_output.createVariable('lat',   'f8', ('n_times', 'n_cross', 'n_geopt'))
        ncfile_output.createVariable('lon',   'f8', ('n_times', 'n_cross', 'n_geopt'))
        ncfile_output.createVariable('geopt', 'f8', ('n_times', 'n_cross', 'n_geopt'))
        ncfile_output.createVariable('time',  'f8', ('n_times', 'n_cross', 'n_geopt'))

        n_times = 0
        for filename in filenames:

            filename_APR3nad = os.path.join(filename.rstrip('\n'))
            ncfile_APR3nad = Dataset(filename_APR3nad, 'r')
            lores_zhh14 = ncfile_APR3nad.variables['lores_zhh14'][:,:,:]
            lores_zhh35 = ncfile_APR3nad.variables['lores_zhh35'][:,:,:]
            lores_zZN35 = ncfile_APR3nad.variables['lores_zZN35'][:,:,:]
            lores_lat3D = ncfile_APR3nad.variables['lores_lat3D'][:,:,:]
            lores_lon3D = ncfile_APR3nad.variables['lores_lon3D'][:,:,:]
            lores_alt3D = ncfile_APR3nad.variables['lores_alt3D'][:,:,:]
            lores_times = ncfile_APR3nad.variables['time'][:]
            ncfile_APR3nad.close()

            (Ns, Nb, Nr) = lores_zhh14.shape
            print(filename.rstrip('\n'))
            print(lores_zhh14.shape)
            print(n_times)
            print(n_times+Ns)

            ncfile_output.variables['zhh14'][n_times:n_times+Ns,0:Nb,0:Nr] = lores_zhh14
            ncfile_output.variables['zhh35'][n_times:n_times+Ns,0:Nb,0:Nr] = lores_zhh35
            ncfile_output.variables['zZN35'][n_times:n_times+Ns,0:Nb,0:Nr] = lores_zZN35
            ncfile_output.variables['lat'][n_times:n_times+Ns,0:Nb,0:Nr] = lores_lat3D
            ncfile_output.variables['lon'][n_times:n_times+Ns,0:Nb,0:Nr] = lores_lon3D
            ncfile_output.variables['geopt'][n_times:n_times+Ns,0:Nb,0:Nr] = lores_alt3D
            ncfile_output.variables['time'][n_times:n_times+Ns,0:Nb,0:Nr] = np.transpose(np.tile(lores_times, (Nr, Nb, 1)))

            n_times += int(Ns)

        ncfile_output.close()