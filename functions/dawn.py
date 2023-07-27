import os
import re
import time
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
from IPython.display import display
from IPython.display import Image as IPImage
from wrf import getvar, latlon_coords, interplevel
from matplotlib.backends.backend_pdf import PdfPages
from combine_and_show_images import combine_images_grid

def create_DAWN_bufr_temp(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_DAWN = os.path.join(dir_data, 'DAWN')
    dir_DAWN_bufr_temp = os.path.join(dir_DAWN, 'bufr_temp')
    os.makedirs(dir_DAWN, exist_ok=True)
    os.makedirs(dir_DAWN_bufr_temp, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        time_s = anl_end_time - timedelta(hours=cycling_interval/2.0)
        time_e = anl_end_time + timedelta(hours=cycling_interval/2.0)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')

        dir_bufr_temp = os.path.join(dir_DAWN_bufr_temp, anl_end_time_YYYYMMDD)
        os.makedirs(dir_bufr_temp, exist_ok=True)
        dir_bufr_temp = os.path.join(dir_bufr_temp, anl_end_time_HH)
        os.system(f"rm -rf {dir_bufr_temp}")
        os.makedirs(dir_bufr_temp, exist_ok=True)
        filenames = os.popen(f"ls {dir_DAWN}/*DAWN*.nc")
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
        QMWN = []
        WDIR = []
        WSPD = []
        PKWDSP = []

        for file_DAWN in filenames:
            date = re.search(r"\d{8}", file_DAWN).group()
            initial_time = datetime.strptime(date, "%Y%m%d")
            time_s_hours = (time_s - initial_time).total_seconds()/3600.0
            time_e_hours = (time_e - initial_time).total_seconds()/3600.0

            if 'CV' in dir_case:
                ncfile = Dataset(file_DAWN.rstrip('\n'))
                altitude = np.arange(-0.015, 12.980, 0.030)*1000.0
                (n_loc, n_hgt) = ncfile.variables['smoothed_Wind_Speed'][:, :].shape

                DAWN_latitude = np.transpose(np.tile(ncfile.variables['lat'][:], (n_hgt, 1))).flatten('F')
                DAWN_longitude = np.transpose(np.tile(ncfile.variables['lon'][:], (n_hgt, 1))).flatten('F')
                DAWN_time = np.transpose(np.tile(ncfile.groups['Date_Time'].variables['Profile_Time'][:], (n_hgt, 1))).flatten('F')
                DAWN_year = np.zeros(n_loc*n_hgt, dtype=int)
                DAWN_mnth = np.zeros(n_loc*n_hgt, dtype=int)
                DAWN_days = np.zeros(n_loc*n_hgt, dtype=int)
                DAWN_hour = np.zeros(n_loc*n_hgt, dtype=int)
                DAWN_minu = np.zeros(n_loc*n_hgt, dtype=int)
                DAWN_seco = np.zeros(n_loc*n_hgt, dtype=int)
                DAWN_mcse = np.zeros(n_loc*n_hgt, dtype=int)
                for idd, dtime in enumerate(DAWN_time):
                    DAWN_year[idd] = (initial_time + timedelta(hours = dtime)).year
                    DAWN_mnth[idd] = (initial_time + timedelta(hours = dtime)).month
                    DAWN_days[idd] = (initial_time + timedelta(hours = dtime)).day
                    DAWN_hour[idd] = (initial_time + timedelta(hours = dtime)).hour
                    DAWN_minu[idd] = (initial_time + timedelta(hours = dtime)).minute
                    DAWN_seco[idd] = (initial_time + timedelta(hours = dtime)).second
                    DAWN_mcse[idd] = (initial_time + timedelta(hours = dtime)).microsecond
                    DAWN_seco[idd] = DAWN_seco[idd] + DAWN_mcse[idd]/1000000.0
                DAWN_altitude = np.tile(altitude, (n_loc, 1)).flatten('F')
                DAWN_geopotential = np.array(metpy.calc.height_to_geopotential(DAWN_altitude*units.m))
                DAWN_pressure = np.array(metpy.calc.height_to_pressure_std(DAWN_altitude*units.m))*100.0
                DAWN_wind_direction = np.array(ncfile.variables['smoothed_Wind_Direction'][:, :].flatten('F'))
                DAWN_wind_speed = np.array(ncfile.variables['smoothed_Wind_Speed'][:, :].flatten('F'))
                DAWN_qc_flag = np.array(ncfile.groups['Data_Quality'].variables['QC_flag'][:,:].flatten('F'))
                DAWN_ac_roll = np.abs(np.transpose(np.tile(ncfile.groups['Nav_Data'].variables['AC_Roll'][:], (n_hgt, 1))).flatten('F'))
                ncfile.close()

                index = ~np.isnan(DAWN_wind_speed) & (DAWN_time >= time_s_hours) & (DAWN_time < time_e_hours) & \
                        (DAWN_qc_flag != 1) & (DAWN_ac_roll <= 3) & (DAWN_altitude > 15)

            if 'AW' in dir_case:
                ncfile = Dataset(file_DAWN.rstrip('\n'))
                altitude = np.arange(np.min(ncfile.variables['Profile_Altitude'][:]), np.max(ncfile.variables['Profile_Altitude'][:])+0.001, 0.033)*1000.0
                n_loc = len(ncfile.variables['Profile_Latitude'][:])
                n_hgt = len(ncfile.variables['Profile_Altitude'][:])

                DAWN_latitude = np.tile(ncfile.variables['Profile_Latitude'][:], (n_hgt, 1)).flatten('F')
                DAWN_longitude = np.tile(ncfile.variables['Profile_Longitude'][:], (n_hgt, 1)).flatten('F')
                DAWN_time = np.tile(ncfile.variables['Profile_Time'][:], (n_hgt, 1)).flatten('F')
                DAWN_year = np.array([(initial_time + timedelta(hours = d)).year for d in DAWN_time], dtype='int64')
                DAWN_mnth = np.array([(initial_time + timedelta(hours = d)).month for d in DAWN_time], dtype='int64')
                DAWN_days = np.array([(initial_time + timedelta(hours = d)).day for d in DAWN_time], dtype='int64')
                DAWN_hour = np.array([(initial_time + timedelta(hours = d)).hour for d in DAWN_time], dtype='int64')
                DAWN_minu = np.array([(initial_time + timedelta(hours = d)).minute for d in DAWN_time], dtype='int64')
                DAWN_seco = np.array([(initial_time + timedelta(hours = d)).second for d in DAWN_time])
                DAWN_mcse = np.array([(initial_time + timedelta(hours = d)).microsecond for d in DAWN_time])
                DAWN_seco = DAWN_seco + DAWN_mcse/1000000.0
                DAWN_altitude = np.transpose(np.tile(altitude, (n_loc, 1))).flatten('F')
                DAWN_geopotential = np.array(metpy.calc.height_to_geopotential(DAWN_altitude*units.m))
                DAWN_pressure = np.array(metpy.calc.height_to_pressure_std(DAWN_altitude*units.m))*100.0
                DAWN_wind_direction = ncfile.variables['Wind_Direction'][:,:].flatten('F')
                DAWN_wind_speed = ncfile.variables['Wind_Speed'][:,:].flatten('F')
                DAWN_ac_roll = np.abs(np.tile(ncfile.variables['AC_Roll'][:], (n_hgt, 1))).flatten('F')
                ncfile.close()

                index = (~DAWN_wind_speed.mask) & (DAWN_time >= time_s_hours) & (DAWN_time < time_e_hours) & \
                        (DAWN_ac_roll <= 3) & (DAWN_altitude > 15)

            n_data = sum(index==True)
            if n_data > 0:

                n_total_data += n_data
                YEAR += DAWN_year[index].tolist()
                MNTH += DAWN_mnth[index].tolist()
                DAYS += DAWN_days[index].tolist()
                HOUR += DAWN_hour[index].tolist()
                MINU += DAWN_minu[index].tolist()
                SECO += DAWN_seco[index].tolist()
                QHDOP += np.full((n_data), 0, dtype='int').tolist()
                QHDOM += np.full((n_data), 0, dtype='int').tolist()
                CLAT += DAWN_latitude[index].tolist()
                CLON += DAWN_longitude[index].tolist()
                PRLC += DAWN_pressure[index].tolist()
                GP10 += DAWN_geopotential[index].tolist()
                QMWN += np.full((n_data), 2, dtype='int').tolist()
                WDIR += DAWN_wind_direction[index].tolist()
                WSPD += DAWN_wind_speed[index].tolist()
                PKWDSP += np.full((n_data), 0.0, dtype='float64').tolist()

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
            np.savetxt(f, QMWN)
        with open(os.path.join(dir_bufr_temp, '14.txt'), 'ab') as f:
            np.savetxt(f, WDIR)
        with open(os.path.join(dir_bufr_temp, '15.txt'), 'ab') as f:
            np.savetxt(f, WSPD)
        with open(os.path.join(dir_bufr_temp, '16.txt'), 'ab') as f:
            np.savetxt(f, PKWDSP)
        np.savetxt(os.path.join(dir_bufr_temp, '0.txt'), [n_total_data])

def create_DAWN_bufr(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_DAWN = os.path.join(dir_data, 'DAWN')
    dir_DAWN_bufr_temp = os.path.join(dir_DAWN, 'bufr_temp')
    os.makedirs(dir_DAWN, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')

        dir_DAWN_bufr = os.path.join(dir_DAWN, anl_end_time_YYYYMMDD)
        file_DAWN_bufr = os.path.join(dir_DAWN_bufr, f"gdas.t{anl_end_time_HH}z.dawn.tm00.bufr_d")
        dir_fortran = os.path.join(dir_DAWN, 'fortran_files')
        file_fortran_bufr = os.path.join(dir_fortran, 'gdas.dawn.bufr')
        os.makedirs(dir_DAWN_bufr, exist_ok=True)
        os.system(f"rm -rf {file_fortran_bufr}")

        print('Check bufr_temp: ')
        flag = True
        info = os.popen(f"cd {dir_DAWN_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH} && ls ./*.txt").readlines()
        if len(info) != 17:
            flag = False
        print(len(info))
        print(flag)

        if flag:

            fdata = ''
            with open(f"{dir_fortran}/bufr_encode_dawn.f90", 'r') as f:
                for line in f.readlines():
                    if(line.find('idate = ') == 4): line = f"    idate = {anl_end_time_YYYYMMDD}{anl_end_time_HH}\n"
                    if(line.find('dir_files = ') == 4): line = f"    dir_files = '{dir_DAWN_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH}/'\n"
                    fdata += line
            f.close()

            with open(f"{dir_fortran}/bufr_encode_dawn.f90", 'w') as f:
                f.writelines(fdata)
            f.close()

            os.popen(f"cd {dir_fortran} && ./run_encode_dawn.sh > log_out")
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

            os.system(f"mv {file_fortran_bufr} {file_DAWN_bufr}")

def wrf_extract_DAWN(data_library_names, dir_cases, case_names, exp_names):

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
        dir_DAWN = os.path.join(dir_data, 'DAWN')
        dir_DAWN_bufr_temp = os.path.join(dir_DAWN, 'bufr_temp')
        os.makedirs(dir_cross_section, exist_ok=True)

        for dom in tqdm(da_domains, desc='Domains', leave=False): 
            # for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', leave=False):
            for da_cycle in tqdm(range(4, 5, 1), desc='Cycles', leave=False):

                anl_start_time = initial_time + timedelta(hours=cycling_interval)
                n_time = int(da_cycle)
                specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
                dir_cross_section_case = os.path.join(dir_cross_section, specific_case)
                os.makedirs(dir_cross_section_case, exist_ok=True)

                for idt in tqdm(range(n_time), desc='Times', leave=False):

                    time_now = anl_start_time + timedelta(hours = idt*cycling_interval)
                    time_now_YYYYMMDD = time_now.strftime('%Y%m%d')
                    time_now_HH = time_now.strftime('%H')
                    time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')
                    dir_bufr_temp = os.path.join(dir_DAWN_bufr_temp, time_now_YYYYMMDD)
                    dir_bufr_temp = os.path.join(dir_bufr_temp, time_now_HH)

                    with open(os.path.join(dir_bufr_temp, '0.txt'), 'r') as f:
                        n_time = int(float(f.read().strip()))
                    
                    if n_time > 0:

                        filename = os.path.join(dir_cross_section_case, f"{time_now_YYYYMMDDHH}_DAWN_{dom}.nc")
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
                        ncfile_output.createVariable('u_obs',  'f8', ('n_time'))
                        ncfile_output.createVariable('v_obs',  'f8', ('n_time'))
                        ncfile_output.createVariable('u_bkg',  'f8', ('n_time'))
                        ncfile_output.createVariable('v_bkg',  'f8', ('n_time'))
                        ncfile_output.createVariable('u_anl',  'f8', ('n_time'))
                        ncfile_output.createVariable('v_anl',  'f8', ('n_time'))
                        ncfile_output.createVariable('u_OmB',  'f8', ('n_time'))
                        ncfile_output.createVariable('v_OmB',  'f8', ('n_time'))
                        ncfile_output.createVariable('u_OmA',  'f8', ('n_time'))
                        ncfile_output.createVariable('v_OmA',  'f8', ('n_time'))
                        
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

                        df = pd.read_csv(os.path.join(dir_bufr_temp, '14.txt'), header=None)
                        wdir = units.Quantity(np.array(df[0]), units.deg)
                        df = pd.read_csv(os.path.join(dir_bufr_temp, '15.txt'), header=None)
                        wspd = units.Quantity(np.array(df[0]), 'm/s')
                        (u, v) = metpy.calc.wind_components(wspd, wdir)
                        u = np.array(u)
                        v = np.array(v)

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
                        ncfile_output.variables['u_obs'][:] = u
                        ncfile_output.variables['v_obs'][:] = v

                        dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'bkg')
                        wrfout = os.path.join(dir_wrfout, f"wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:%M:00')}")
                        ncfile = Dataset(wrfout)
                        bkg_z = getvar(ncfile, 'height', units='m')
                        bkg_p = getvar(ncfile, 'pressure')
                        (bkg_u, bkg_v) = getvar(ncfile, 'uvmet', units='ms-1')
                        ncfile.close()

                        dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'da')
                        wrfout = os.path.join(dir_wrfout, f"wrf_inout.{time_now.strftime('%Y%m%d%H')}.{dom}")
                        ncfile = Dataset(wrfout)
                        anl_z = getvar(ncfile, 'height', units='m')
                        anl_p = getvar(ncfile, 'pressure')
                        (anl_u, anl_v) = getvar(ncfile, 'uvmet', units='ms-1')
                        ncfile.close()

                        bkg_u_levels = interplevel(bkg_u, bkg_z, levels)
                        bkg_v_levels = interplevel(bkg_v, bkg_z, levels)
                        anl_u_levels = interplevel(anl_u, anl_z, levels)
                        anl_v_levels = interplevel(anl_v, anl_z, levels)

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
                        
                        for idl in tqdm(range(n_levels), desc='Levels', leave=False):
                        # for idl in tqdm(range(1), desc='Levels', leave=False):

                            bkg_u_level = np.array(bkg_u_levels[idl,:,:])
                            bkg_v_level = np.array(bkg_v_levels[idl,:,:])
                            anl_u_level = np.array(anl_u_levels[idl,:,:])
                            anl_v_level = np.array(anl_v_levels[idl,:,:])

                            index_level = (height == levels[idl])
                            idx_level = np.where(index_level)[0]
                            lat_level = lat[index_level]
                            lon_level = lon[index_level]

                            ncfile_output.variables['u_bkg'][idx_level] = griddata((bkg_lon_1d, bkg_lat_1d), bkg_u_level[bkg_index], \
                                                                                   (lon_level, lat_level), method='linear')
                            ncfile_output.variables['v_bkg'][idx_level] = griddata((bkg_lon_1d, bkg_lat_1d), bkg_v_level[bkg_index], \
                                                                                   (lon_level, lat_level), method='linear')
                            ncfile_output.variables['u_anl'][idx_level] = griddata((anl_lon_1d, anl_lat_1d), anl_u_level[anl_index], \
                                                                                   (lon_level, lat_level), method='linear')
                            ncfile_output.variables['v_anl'][idx_level] = griddata((anl_lon_1d, anl_lat_1d), anl_v_level[anl_index], \
                                                                                   (lon_level, lat_level), method='linear')

                        ncfile_output.variables['u_OmB'][:] = ncfile_output.variables['u_obs'][:] - ncfile_output.variables['u_bkg'][:]
                        ncfile_output.variables['v_OmB'][:] = ncfile_output.variables['v_obs'][:] - ncfile_output.variables['v_bkg'][:]
                        ncfile_output.variables['u_OmA'][:] = ncfile_output.variables['u_obs'][:] - ncfile_output.variables['u_anl'][:]
                        ncfile_output.variables['v_OmA'][:] = ncfile_output.variables['v_obs'][:] - ncfile_output.variables['v_anl'][:]           
                        ncfile_output.close()

def draw_DAWN_comparison(data_library_names, dir_cases, case_names, exp_names, scatter_var, scatter_levels, \
                         domains=['d01'], da_cycle=1, var_time=20000101010000):
    
    obs_error_DAWN = 2.0

    # Import the necessary library
    (data_library_name, dir_case, case_name, exp_name) = (data_library_names[0], dir_cases[0], case_names[0], exp_names[0])
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
    time_window_max = attributes[(dir_case, case_name)]['time_window_max']
    dir_cross_section = os.path.join(dir_exp, 'cross_section')
    dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
    dir_best_track = os.path.join(dir_track_intensity, 'best_track')
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    var_time_datetime = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')
    start_time = float(var_time_datetime.strftime('%H')) - time_window_max
    end_time = float(var_time_datetime.strftime('%H')) + time_window_max

    for dom in tqdm(domains, desc='Domains', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        
        image_files = []
        dir_save = os.path.join(dir_cross_section, 'figures')
        output_filename = (
            f"{str(var_time)}_DAWN_{scatter_var}_"
            f"{dom}_C{str(da_cycle).zfill(2)}"
        )
        output_file = os.path.join(dir_save, output_filename+'.png')

        for idc in tqdm(range(len(dir_cases)), desc='Cases', leave=False):

            # Import the necessary library
            (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])
            specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
            dir_cross_section_case = os.path.join(dir_cross_section, specific_case)
            
            filename = os.path.join(dir_cross_section_case, f"{str(var_time)[0:10]}_DAWN_{dom}.nc")
            ncfile = Dataset(filename, 'r')
            hour = ncfile.variables['hour'][:]
            minute = ncfile.variables['minute'][:]
            second = ncfile.variables['second'][:]
            geopt = ncfile.variables['geopt'][:]/1000.0
            temp = ncfile.variables[scatter_var][:]
            ncfile.close()

            time = hour + minute/60.0 + second/3600.0

            fig_width = 2.75*1.6
            fig_height = 2.75+0.75
            clb_aspect = 25*1.6

            filename = (
                f"{str(var_time)}_DAWN_{scatter_var}_"
                f"{dom}_C{str(da_cycle).zfill(2)}"
            )
            pdfname = os.path.join(dir_cross_section_case, filename+'.pdf')
            pngname = os.path.join(dir_cross_section_case, filename+'.png')
            image_files.append(pngname)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                ax = axs

                pcm = ax.scatter(time, geopt, marker='s', s=1.0, linewidths=0.0, c=temp, \
                                 vmin=np.min(scatter_levels), vmax=np.max(scatter_levels), cmap=cmaps.vik, zorder=0)

                extent = [start_time, end_time, 0, 15]
                ax.set_ylabel('Geopotential height (km)', fontsize=10.0)
                ax.set_xticks(np.arange(start_time, end_time + 0.1, 1.0))
                ax.set_yticks(np.arange(0, 16, 3))
                ax.text(start_time+0.1, 14.5, exp_name, ha='left', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                clb.set_label('OmA of u ($\mathregular{ms^{-1}}$)', fontsize=10.0, labelpad=4.0)
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