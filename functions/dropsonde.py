import os
import re
import time
import h5py
import importlib
import subprocess
import metpy.calc
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import colormaps as cmaps
from datetime import datetime, timedelta
from netCDF4 import Dataset
from scipy.interpolate import griddata
from tqdm.notebook import tqdm
from metpy.units import units
from scipy.interpolate import griddata
from IPython.display import display
from IPython.display import Image as IPImage
from wrf import getvar, latlon_coords, interplevel
from matplotlib.backends.backend_pdf import PdfPages
from combine_and_show_images import combine_images_grid

def create_Dropsonde_bufr_temp(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time=datetime(*itime)
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_HALO = os.path.join(dir_data, 'HALO')
    dir_HALO_bufr_temp = os.path.join(dir_HALO, 'bufr_temp')
    os.makedirs(dir_HALO, exist_ok=True)
    os.makedirs(dir_HALO_bufr_temp, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        time_s = anl_end_time - timedelta(hours=cycling_interval/2.0)
        time_e = anl_end_time + timedelta(hours=cycling_interval/2.0)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')

        dir_bufr_temp = os.path.join(dir_HALO_bufr_temp, anl_end_time_YYYYMMDD)
        os.makedirs(dir_bufr_temp, exist_ok=True)
        dir_bufr_temp = os.path.join(dir_bufr_temp, anl_end_time_HH)
        os.system(f"rm -rf {dir_bufr_temp}")
        os.makedirs(dir_bufr_temp, exist_ok=True)
        filenames = os.popen(f"ls {dir_HALO}/*HALO*.h5").readlines()
        n_total_data = 0
        YEAR = []
        MNTH = []
        DAYS = []
        HOUR = []
        MINU = []
        SECO = []
        QHDOP = []
        QHDOM = []
        CLAT = []
        CLON = []
        PRLC = []
        GP10 = []
        QMAT = []
        TMDB = []
        QMDD = []
        SPFH = []
        REHU = []

        for file_HALO in filenames:
            date = re.search(r"\d{8}", file_HALO).group()
            initial_time = datetime.strptime(date, "%Y%m%d")
            time_s_hours = (time_s - initial_time).total_seconds()/3600.0
            time_e_hours = (time_e - initial_time).total_seconds()/3600.0

            if 'CV' in dir_case:
                HALO = h5py.File(file_HALO.rstrip('\n'), 'r')
                n_loc = np.array(HALO['Nav_Data']['gps_lat']).size
                n_hgt = np.array(HALO['z']).size

                HALO_latitude = np.tile(np.array(HALO['Nav_Data']['gps_lat']), (1, n_hgt)).flatten()
                HALO_longitude = np.tile(np.array(HALO['Nav_Data']['gps_lon']), (1, n_hgt)).flatten()
                HALO_datetime = np.tile(np.array(HALO['Nav_Data']['gps_time']), (1, n_hgt)).flatten()
                HALO_year = np.array([(initial_time + timedelta(hours = d)).year for d in HALO_datetime], dtype='int64')
                HALO_mnth = np.array([(initial_time + timedelta(hours = d)).month for d in HALO_datetime], dtype='int64')
                HALO_days = np.array([(initial_time + timedelta(hours = d)).day for d in HALO_datetime], dtype='int64')
                HALO_hour = np.array([(initial_time + timedelta(hours = d)).hour for d in HALO_datetime], dtype='int64')
                HALO_minu = np.array([(initial_time + timedelta(hours = d)).minute for d in HALO_datetime], dtype='int64')
                HALO_seco = np.array([(initial_time + timedelta(hours = d)).second for d in HALO_datetime])
                HALO_mcse = np.array([(initial_time + timedelta(hours = d)).microsecond for d in HALO_datetime])
                HALO_seco = HALO_seco + HALO_mcse/1000000.0
                HALO_altitude = np.tile(HALO['z'], (n_loc, 1)).flatten()
                HALO_geopotential = np.array(metpy.calc.height_to_geopotential(HALO_altitude*units.m))
                HALO_pressure = np.array(HALO['State']['Pressure']).flatten()
                HALO_pressure = HALO_pressure*101325.0
                HALO_temperature = np.array(HALO['State']['Temperature']).flatten()
                HALO_mixing_ratio = np.array(HALO['h2o_mmr_v']).flatten()
                HALO_mixing_ratio = HALO_mixing_ratio/1000.0
                HALO_specific_humidity = HALO_mixing_ratio/(1+HALO_mixing_ratio)
                HALO_relative_humidity = np.array(HALO['State']['Relative_Humidity']).flatten()
                HALO_relative_humidity = HALO_relative_humidity*100.0
                HALO.close()

            if 'AW' in dir_case:
                HALO = h5py.File(file_HALO.rstrip('\n'), 'r')
                n_loc = np.array(HALO['Nav_Data']['gps_lat']).size
                n_hgt = np.array(HALO['DataProducts']['Altitude']).size

                HALO_latitude = np.tile(np.array(HALO['Nav_Data']['gps_lat']), (1, n_hgt)).flatten()
                HALO_longitude = np.tile(np.array(HALO['Nav_Data']['gps_lon']), (1, n_hgt)).flatten()
                HALO_datetime = np.tile(np.array(HALO['Nav_Data']['gps_time']), (1, n_hgt)).flatten()
                HALO_year = np.array([(initial_time + timedelta(hours = d)).year for d in HALO_datetime], dtype='int64')
                HALO_mnth = np.array([(initial_time + timedelta(hours = d)).month for d in HALO_datetime], dtype='int64')
                HALO_days = np.array([(initial_time + timedelta(hours = d)).day for d in HALO_datetime], dtype='int64')
                HALO_hour = np.array([(initial_time + timedelta(hours = d)).hour for d in HALO_datetime], dtype='int64')
                HALO_minu = np.array([(initial_time + timedelta(hours = d)).minute for d in HALO_datetime], dtype='int64')
                HALO_seco = np.array([(initial_time + timedelta(hours = d)).second for d in HALO_datetime])
                HALO_mcse = np.array([(initial_time + timedelta(hours = d)).microsecond for d in HALO_datetime])
                HALO_seco = HALO_seco + HALO_mcse/1000000.0
                HALO_altitude = np.tile(HALO['DataProducts']['Altitude'], (n_loc, 1)).flatten()
                HALO_geopotential = np.array(metpy.calc.height_to_geopotential(HALO_altitude*units.m))
                HALO_pressure = np.array(HALO['State']['Pressure']).flatten()
                HALO_pressure = HALO_pressure*101325.0
                HALO_temperature = np.array(HALO['State']['Temperature']).flatten()
                HALO_mixing_ratio = np.array(HALO['DataProducts']['h2o_mmr_v']).flatten()
                HALO_mixing_ratio = HALO_mixing_ratio/1000.0
                HALO_specific_humidity = HALO_mixing_ratio/(1+HALO_mixing_ratio)
                HALO_relative_humidity = np.array(HALO['State']['Relative_Humidity']).flatten()
                HALO.close()

            index = (HALO_datetime >= time_s_hours) & (HALO_datetime <= time_e_hours) & \
                    (~np.isnan(HALO_mixing_ratio)) & (HALO_mixing_ratio > 0) & \
                    (HALO_altitude > 0)

            n_data = sum(index==True)
            if n_data > 0:

                n_total_data += n_data
                YEAR += HALO_year[index].tolist()
                MNTH += HALO_mnth[index].tolist()
                DAYS += HALO_days[index].tolist()
                HOUR += HALO_hour[index].tolist()
                MINU += HALO_minu[index].tolist()
                SECO += HALO_seco[index].tolist()
                QHDOP += np.full((n_data), 0, dtype='int').tolist()
                QHDOM += np.full((n_data), 0, dtype='int').tolist()
                CLAT += HALO_latitude[index].tolist()
                CLON += HALO_longitude[index].tolist()
                PRLC += HALO_pressure[index].tolist()
                GP10 += HALO_geopotential[index].tolist()
                QMAT += np.full((n_data), 2, dtype='int').tolist()
                TMDB += HALO_temperature[index].tolist()
                QMDD += np.full((n_data), 2, dtype='int').tolist()
                SPFH += HALO_specific_humidity[index].tolist()
                REHU += HALO_relative_humidity[index].tolist()

        with open(os.path.join(dir_bufr_temp,  '1.txt'), 'ab') as f:
            np.savetxt(f, YEAR)
        with open(os.path.join(dir_bufr_temp,  '2.txt'), 'ab') as f:
            np.savetxt(f, MNTH)
        with open(os.path.join(dir_bufr_temp,  '3.txt'), 'ab') as f:
            np.savetxt(f, DAYS)
        with open(os.path.join(dir_bufr_temp,  '4.txt'), 'ab') as f:
            np.savetxt(f, HOUR)
        with open(os.path.join(dir_bufr_temp,  '5.txt'), 'ab') as f:
            np.savetxt(f, MINU)
        with open(os.path.join(dir_bufr_temp,  '6.txt'), 'ab') as f:
            np.savetxt(f, SECO)
        with open(os.path.join(dir_bufr_temp,  '7.txt'), 'ab') as f:
            np.savetxt(f, QHDOP)
        with open(os.path.join(dir_bufr_temp,  '8.txt'), 'ab') as f:
            np.savetxt(f, QHDOM)
        with open(os.path.join(dir_bufr_temp,  '9.txt'), 'ab') as f:
            np.savetxt(f, CLAT)
        with open(os.path.join(dir_bufr_temp, '10.txt'), 'ab') as f:
            np.savetxt(f, CLON)
        with open(os.path.join(dir_bufr_temp, '11.txt'), 'ab') as f:
            np.savetxt(f, PRLC)
        with open(os.path.join(dir_bufr_temp, '12.txt'), 'ab') as f:
            np.savetxt(f, GP10)
        with open(os.path.join(dir_bufr_temp, '13.txt'), 'ab') as f:
            np.savetxt(f, QMAT)
        with open(os.path.join(dir_bufr_temp, '14.txt'), 'ab') as f:
            np.savetxt(f, TMDB)
        with open(os.path.join(dir_bufr_temp, '15.txt'), 'ab') as f:
            np.savetxt(f, QMDD)
        with open(os.path.join(dir_bufr_temp, '16.txt'), 'ab') as f:
            np.savetxt(f, SPFH)
        with open(os.path.join(dir_bufr_temp, '17.txt'), 'ab') as f:
            np.savetxt(f, REHU)
        np.savetxt(dir_bufr_temp + '/0.txt', [n_total_data])

def create_HALO_bufr(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time=datetime(*itime)
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_HALO = os.path.join(dir_data, 'HALO')
    dir_HALO_bufr = os.path.join(dir_HALO, 'bufr')
    dir_HALO_bufr_temp = os.path.join(dir_HALO, 'bufr_temp')
    os.makedirs(dir_HALO, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')

        dir_bufr = os.path.join(dir_HALO_bufr, anl_end_time_YYYYMMDD)
        file_bufr = os.path.join(dir_bufr, f"gdas.t{anl_end_time_HH}z.halo.tm00.bufr_d")
        dir_fortran = os.path.join(dir_HALO, 'fortran_files')
        file_fortran_bufr = os.path.join(dir_fortran, 'gdas.halo.bufr')
        os.makedirs(dir_bufr, exist_ok=True)
        os.system(f"rm -rf {file_fortran_bufr}")

        print('Check bufr_temp: ')
        flag = True
        info = os.popen(f"cd {dir_HALO_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH} && ls ./*.txt").readlines()
        if len(info) != 18:
            flag = False
        print(len(info))
        print(flag)

        if flag:

            fdata = ''
            with open(f"{dir_fortran}/bufr_encode_halo.f90", 'r') as f:
                for line in f.readlines():
                    if(line.find('idate = ') == 4): line = f"    idate = {anl_end_time_YYYYMMDD}{anl_end_time_HH}\n"
                    if(line.find('dir_files = ') == 4): line = f"    dir_files = '{dir_HALO_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH}/'\n"
                    fdata += line
            f.close()

            with open(f"{dir_fortran}/bufr_encode_halo.f90", 'w') as f:
                f.writelines(fdata)
            f.close()

            os.popen(f"cd {dir_fortran} && ./run_encode_halo.sh > log_out")
            flag = True
            file_size = 0
            while flag:
                time.sleep(5)
                file_size_temp = os.popen(f"stat -c '%s' {file_fortran_bufr}").read()
                if file_size_temp:
                    file_size_next = int(file_size_temp)
                    if file_size_next == file_size:
                        flag = False
                    else:
                        file_size = file_size_next
                print(file_size)

            os.system(f"mv {file_fortran_bufr} {file_bufr}")

def wrf_extract_HALO(data_library_names, dir_cases, case_names, exp_names):

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
        dir_HALO = os.path.join(dir_data, 'HALO')
        dir_HALO_bufr_temp = os.path.join(dir_HALO, 'bufr_temp')
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
                    time_now_YYYYMMDD = time_now.strftime('%Y%m%d')
                    time_now_HH = time_now.strftime('%H')
                    time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')
                    dir_bufr_temp = os.path.join(dir_HALO_bufr_temp, time_now_YYYYMMDD)
                    dir_bufr_temp = os.path.join(dir_bufr_temp, time_now_HH)

                    with open(os.path.join(dir_bufr_temp, '0.txt'), 'r') as f:
                        n_time = int(float(f.read().strip()))
                    
                    if n_time > 0:

                        filename = os.path.join(dir_cross_section_case, f"{time_now_YYYYMMDDHH}_HALO_{dom}.nc")
                        os.system(f"rm -rf {filename}")

                        ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                        ncfile_output.createDimension('n_time', n_time)
                        ncfile_output.createVariable('year',   'f8', ('n_time'))
                        ncfile_output.createVariable('month',  'f8', ('n_time'))
                        ncfile_output.createVariable('days',   'f8', ('n_time'))
                        ncfile_output.createVariable('hour',   'f8', ('n_time'))
                        ncfile_output.createVariable('minute', 'f8', ('n_time'))
                        ncfile_output.createVariable('second', 'f8', ('n_time'))
                        ncfile_output.createVariable('lat',    'f8', ('n_time'))
                        ncfile_output.createVariable('lon',    'f8', ('n_time'))
                        ncfile_output.createVariable('p',      'f8', ('n_time'))
                        ncfile_output.createVariable('geopt',  'f8', ('n_time'))
                        ncfile_output.createVariable('q_obs',  'f8', ('n_time'))
                        ncfile_output.createVariable('q_bkg',  'f8', ('n_time'))
                        ncfile_output.createVariable('q_anl',  'f8', ('n_time'))
                        ncfile_output.createVariable('q_OmB',  'f8', ('n_time'))
                        ncfile_output.createVariable('q_OmA',  'f8', ('n_time'))

                        df = pd.read_csv(os.path.join(dir_bufr_temp,  '1.txt'), header=None)
                        year = np.array(df[0])
                        df = pd.read_csv(os.path.join(dir_bufr_temp,  '2.txt'), header=None)
                        month = np.array(df[0])
                        df = pd.read_csv(os.path.join(dir_bufr_temp,  '3.txt'), header=None)
                        days = np.array(df[0])
                        df = pd.read_csv(os.path.join(dir_bufr_temp,  '4.txt'), header=None)
                        hour = np.array(df[0])
                        df = pd.read_csv(os.path.join(dir_bufr_temp,  '5.txt'), header=None)
                        minute = np.array(df[0])
                        df = pd.read_csv(os.path.join(dir_bufr_temp,  '6.txt'), header=None)
                        second = np.array(df[0])
                        df = pd.read_csv(os.path.join(dir_bufr_temp,  '9.txt'), header=None)
                        lat = np.array(df[0])
                        df = pd.read_csv(os.path.join(dir_bufr_temp, '10.txt'), header=None)
                        lon = np.array(df[0])
                        df = pd.read_csv(os.path.join(dir_bufr_temp, '11.txt'), header=None)
                        p = np.array(df[0])/100.0

                        df = pd.read_csv(os.path.join(dir_bufr_temp, '12.txt'), header=None)
                        geopt = units.Quantity(np.array(df[0]), 'm^2/s^2')
                        height = np.array(metpy.calc.geopotential_to_height(geopt))
                        levels = np.unique(height)
                        n_levels = len(levels)

                        df = pd.read_csv(os.path.join(dir_bufr_temp, '16.txt'), header=None)
                        sh = np.array(df[0])
                        q = sh/(1-sh)

                        ncfile_output.variables['year'][:] = year
                        ncfile_output.variables['month'][:] = month
                        ncfile_output.variables['days'][:] = days
                        ncfile_output.variables['hour'][:] = hour
                        ncfile_output.variables['minute'][:] = minute
                        ncfile_output.variables['second'][:] = second
                        ncfile_output.variables['lat'][:] = lat
                        ncfile_output.variables['lon'][:] = lon
                        ncfile_output.variables['p'][:] = p
                        ncfile_output.variables['geopt'][:] = height
                        ncfile_output.variables['q_obs'][:] = q

                        dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'bkg')
                        wrfout = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:%M:00')}")
                        ncfile = Dataset(wrfout)
                        bkg_z = getvar(ncfile, 'height', units='m')
                        bkg_p = getvar(ncfile, 'pressure')
                        bkg_q = getvar(ncfile, 'QVAPOR')
                        ncfile.close()

                        dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'da')
                        wrfout = os.path.join(dir_wrfout, f"wrf_inout.{time_now.strftime('%Y%m%d%H')}.{dom}")
                        ncfile = Dataset(wrfout)
                        anl_z = getvar(ncfile, 'height', units='m')
                        anl_p = getvar(ncfile, 'pressure')
                        anl_q = getvar(ncfile, 'QVAPOR')
                        ncfile.close()

                        bkg_q_levels = interplevel(bkg_q, bkg_z, levels)
                        anl_q_levels = interplevel(anl_q, anl_z, levels)

                        bkg_lat, bkg_lon = latlon_coords(bkg_p)
                        bkg_lat = np.array(bkg_lat)
                        bkg_lon = np.array(bkg_lon)
                        bkg_index = (bkg_lat < np.max(lat) + 15.0) & (bkg_lat > np.min(lat) - 15.0) & \
                                    (bkg_lon < np.max(lon) + 15.0) & (bkg_lon > np.min(lon) - 15.0)
                        bkg_lat_1d = bkg_lat[bkg_index]
                        bkg_lon_1d = bkg_lon[bkg_index]

                        anl_lat, anl_lon = latlon_coords(anl_p)
                        anl_lat = np.array(anl_lat)
                        anl_lon = np.array(anl_lon)
                        anl_index = (anl_lat < np.max(lat) + 15.0) & (anl_lat > np.min(lat) - 15.0) & \
                                    (anl_lon < np.max(lon) + 15.0) & (anl_lon > np.min(lon) - 15.0)
                        anl_lat_1d = anl_lat[anl_index]
                        anl_lon_1d = anl_lon[anl_index]
                        
                        for idl in tqdm(range(n_levels), desc='Levels', position=0, leave=True):

                            bkg_q_level = np.array(bkg_q_levels[idl,:,:])
                            anl_q_level = np.array(anl_q_levels[idl,:,:])

                            index_level = (height == levels[idl])
                            idx_level = np.where(index_level)[0]
                            lat_level = lat[index_level]
                            lon_level = lon[index_level]

                            ncfile_output.variables['q_bkg'][idx_level] = griddata((bkg_lon_1d, bkg_lat_1d), bkg_q_level[bkg_index], \
                                                                                   (lon_level, lat_level), method='linear')
                            ncfile_output.variables['q_anl'][idx_level] = griddata((anl_lon_1d, anl_lat_1d), anl_q_level[anl_index], \
                                                                                   (lon_level, lat_level), method='linear')

                        ncfile_output.variables['q_OmB'][:] = ncfile_output.variables['q_obs'][:] - ncfile_output.variables['q_bkg'][:]
                        ncfile_output.variables['q_OmA'][:] = ncfile_output.variables['q_obs'][:] - ncfile_output.variables['q_anl'][:]
                        ncfile_output.close()

def draw_HALO_comparison(data_library_names, dir_cases, case_names, exp_names, scatter_var, scatter_levels, \
                         domains=['d01'], da_cycle=1, var_time=20000101010000):

    # Import the necessary library
    (data_library_name, dir_case, case_name, exp_name) = (data_library_names[0], dir_cases[0], case_names[0], exp_names[0])
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_colormaps = attributes[(dir_case, case_name)]['dir_colormaps']
    time_window_max = attributes[(dir_case, case_name)]['time_window_max']
    dir_cross_section = os.path.join(dir_exp, 'cross_section')
    dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
    dir_best_track = os.path.join(dir_track_intensity, 'best_track')

    dir_ScientificColourMaps7 = os.path.join(dir_colormaps, 'ScientificColourMaps7')
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    var_time_datetime = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')
    start_time = float(var_time_datetime.strftime('%H')) - time_window_max
    end_time = float(var_time_datetime.strftime('%H')) + time_window_max

    for dom in tqdm(domains, desc='Domains', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        
        image_files = []
        dir_save = os.path.join(dir_cross_section, 'figures')
        output_filename = (
            f"{str(var_time)}_HALO_{scatter_var}_"
            f"{dom}_C{str(da_cycle).zfill(2)}"
        )
        output_file = os.path.join(dir_save, output_filename+'.png')

        for idc in tqdm(range(len(dir_cases)), desc='Cases', position=0, leave=True):

            # Import the necessary library
            (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])
            specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
            dir_cross_section_case = os.path.join(dir_cross_section, specific_case)
            
            filename = os.path.join(dir_cross_section_case, f"{str(var_time)[0:10]}_HALO_{dom}.nc")
            ncfile = Dataset(filename, 'r')
            hour = ncfile.variables['hour'][:]
            minute = ncfile.variables['minute'][:]
            second = ncfile.variables['second'][:]
            geopt = ncfile.variables['geopt'][:]/1000.0
            temp = ncfile.variables[scatter_var][:]*10000.0
            ncfile.close()

            time = hour + minute/60.0 + second/3600.0

            fig_width = 2.75*1.6
            fig_height = 2.75+0.75
            clb_aspect = 25*1.6

            filename = (
                f"{str(var_time)}_HALO_{scatter_var}_"
                f"{dom}_C{str(da_cycle).zfill(2)}"
            )
            pdfname = os.path.join(dir_cross_section_case, filename+'.pdf')
            pngname = os.path.join(dir_cross_section_case, filename+'.png')
            image_files.append(pngname)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                ax = axs

                pcm = ax.scatter(time, geopt, marker='s', s=1.0, linewidths=0.0, c=temp, \
                                 vmin=np.min(scatter_levels), vmax=np.max(scatter_levels), cmap=cmaps.imola, zorder=0)

                extent = [start_time, end_time, 0, 15]
                ax.set_ylabel('Height (km)', fontsize=10.0)
                ax.set_xticks(np.arange(start_time, end_time + 0.1, 1.0))
                ax.set_yticks(np.arange(0, 16, 3))
                ax.text(start_time+0.1, 14.5, exp_name, ha='left', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                clb.set_label(f"{scatter_var}" + " ($\mathregular{gkg^{-1}}$)", fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                clb.ax.minorticks_off()
                clb.set_ticks(scatter_levels)
                clb.set_ticklabels(scatter_levels)

                plt.tight_layout()
                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()
                
            command = f"convert {pngname} -trim {pngname}"
            subprocess.run(command, shell=True)
            
        combine_images_grid(image_files, output_file)
        command = f"convert {output_file} -trim {output_file}"
        subprocess.run(command, shell=True)
        image = IPImage(filename=output_file)
        display(image)
