import os
import re
import datetime
import importlib
import metpy.calc
import numpy as np
from netCDF4 import Dataset
from tqdm.notebook import tqdm
from metpy.units import units

def create_DAWN_bufr_temp_cv(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time=datetime.datetime(*itime)
    dir_data=attributes[(dir_case, case_name)]['dir_data']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    J2000 = datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo = datetime.timezone.utc)
    
    dir_DAWN = os.path.join(dir_data, 'DAWN')
    dir_DAWN_bufr_temp = os.path.join(dir_DAWN, 'bufr_temp')
    os.makedirs(dir_DAWN, exist_ok=True)
    os.makedirs(dir_DAWN_bufr_temp, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + datetime.timedelta(hours=cycling_interval*idc)
        time_s = anl_end_time - datetime.timedelta(hours=cycling_interval/2.0)
        time_e = anl_end_time + datetime.timedelta(hours=cycling_interval/2.0)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')

        filenames = os.popen(f"ls {dir_DAWN}/*DAWN*.nc")
        for file_DAWN in filenames:
            date = re.search(r"\d{8}", file_DAWN).group()
            initial_time = datetime.datetime.strptime(date, "%Y%m%d")
            time_s_hours = (time_s - initial_time).total_seconds()/3600.0
            time_e_hours = (time_e - initial_time).total_seconds()/3600.0

            ncfile = Dataset(file_DAWN.rstrip('\n'))
            lat = ncfile.variables['lat'][:]
            lon = ncfile.variables['lon'][:]
            altitude = np.arange(-0.015, 12.980, 0.030)*1000.0
            ws = ncfile.variables['smoothed_Wind_Speed'][:, :]
            wd = ncfile.variables['smoothed_Wind_Direction'][:, :]
            profile_time = ncfile.groups['Date_Time'].variables['Profile_Time'][:]
            qc_flag = ncfile.groups['Data_Quality'].variables['QC_flag'][:,:]
            ac_roll = ncfile.groups['Nav_Data'].variables['AC_Roll'][:]
            ncfile.close()

            (n_loc, n_hgt) = ws.shape
            DAWN_latitude = np.transpose(np.tile(lat, (n_hgt, 1))).flatten('F')
            DAWN_longitude = np.transpose(np.tile(lon, (n_hgt, 1))).flatten('F')
            DAWN_time = np.transpose(np.tile(profile_time, (n_hgt, 1))).flatten('F')
            DAWN_year = np.zeros(n_loc*n_hgt, dtype=int)
            DAWN_mnth = np.zeros(n_loc*n_hgt, dtype=int)
            DAWN_days = np.zeros(n_loc*n_hgt, dtype=int)
            DAWN_hour = np.zeros(n_loc*n_hgt, dtype=int)
            DAWN_minu = np.zeros(n_loc*n_hgt, dtype=int)
            DAWN_seco = np.zeros(n_loc*n_hgt, dtype=int)
            DAWN_mcse = np.zeros(n_loc*n_hgt, dtype=int)
            for idd, dtime in enumerate(DAWN_time):
                DAWN_year[idd] = (initial_time + datetime.timedelta(hours = dtime)).year
                DAWN_mnth[idd] = (initial_time + datetime.timedelta(hours = dtime)).month
                DAWN_days[idd] = (initial_time + datetime.timedelta(hours = dtime)).day
                DAWN_hour[idd] = (initial_time + datetime.timedelta(hours = dtime)).hour
                DAWN_minu[idd] = (initial_time + datetime.timedelta(hours = dtime)).minute
                DAWN_seco[idd] = (initial_time + datetime.timedelta(hours = dtime)).second
                DAWN_mcse[idd] = (initial_time + datetime.timedelta(hours = dtime)).microsecond
                DAWN_seco[idd] = DAWN_seco[idd] + DAWN_mcse[idd]/1000000.0
            DAWN_altitude = np.tile(altitude, (n_loc, 1)).flatten('F')
            DAWN_geopotential = np.array(metpy.calc.height_to_geopotential(DAWN_altitude*units.m))
            DAWN_pressure = np.array(metpy.calc.height_to_pressure_std(DAWN_altitude*units.m))*100.0
            DAWN_wind_direction = np.array(wd.flatten('F'))
            DAWN_wind_speed = np.array(ws.flatten('F'))
            DAWN_qc_flag = np.array(qc_flag.flatten('F'))
            DAWN_ac_roll = np.abs(np.transpose(np.tile(ac_roll, (n_hgt, 1))).flatten('F'))

            index = ~np.isnan(DAWN_wind_speed) & (DAWN_time >= time_s_hours) & (DAWN_time < time_e_hours) & \
                    (DAWN_qc_flag != 1) & (DAWN_ac_roll <= 3) & (DAWN_altitude > 15)
            n_data = sum(index==True)
            dir_bufr_temp = os.path.join(dir_DAWN_bufr_temp, anl_end_time_YYYYMMDD)
            os.makedirs(dir_bufr_temp, exist_ok=True)
            dir_bufr_temp = os.path.join(dir_bufr_temp, anl_end_time_HH)
            os.system(f"rm -rf {dir_bufr_temp}")
            os.makedirs(dir_bufr_temp, exist_ok=True)

            if n_data > -1:

                YEAR = DAWN_year[index]
                MNTH = DAWN_mnth[index]
                DAYS = DAWN_days[index]
                HOUR = DAWN_hour[index]
                MINU = DAWN_minu[index]
                SECO = DAWN_seco[index]
                QHDOP = np.full((n_data), 0, dtype='int')
                QHDOM = np.full((n_data), 0, dtype='int')
                CLAT = DAWN_latitude[index]
                CLON = DAWN_longitude[index]
                PRLC = DAWN_pressure[index]
                GP10 = DAWN_geopotential[index]
                QMWN = np.full((n_data), 2, dtype='int')
                WDIR = DAWN_wind_direction[index]
                WSPD = DAWN_wind_speed[index]
                PKWDSP = np.full((n_data), 0.0, dtype='float64')

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

            np.savetxt(dir_bufr_temp + '/0.txt', [n_data])
