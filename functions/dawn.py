import os
import re
import time
import importlib
import metpy.calc
import numpy as np
from datetime import datetime, timedelta
from netCDF4 import Dataset
from tqdm.notebook import tqdm
from metpy.units import units

def create_DAWN_bufr_temp(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time=datetime(*itime)
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']

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

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time=datetime(*itime)
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']

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
