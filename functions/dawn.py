import os
import datetime
import numpy as np
from netCDF4 import Dataset

def create_DAWN_stream(data_library_name, dir_case, case_name, exp_name):

dir_main = '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/03_CPEX_DAWN/08_CPEX_AW_2021/DAWN'
dir_bufr = dir_main + '/create_bufr/bufr_temp'
#file_DAWN = dir_main + '/data/20210820/CPEXAW_DAWN_DC8_20210820.nc'
#file_DAWN = dir_main + '/data/20210821/CPEXAW_DAWN_DC8_20210821.nc'
#file_DAWN = dir_main + '/data/20210828/CPEXAW_DAWN_DC8_20210828.nc'
file_DAWN = dir_main + '/data/20210904/CPEXAW_DAWN_DC8_20210904.nc'

#initial_time   = datetime.datetime(2021, 8, 20,  0, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 20, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 21,  0, 0, 0)
#initial_time   = datetime.datetime(2021, 8, 21,  0, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 21, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 22,  0, 0, 0)
#initial_time   = datetime.datetime(2021, 8, 28,  0, 0, 0)
#anl_start_time = datetime.datetime(2021, 8, 28, 18, 0, 0)
#anl_end_time   = datetime.datetime(2021, 8, 29,  0, 0, 0)
initial_time   = datetime.datetime(2021, 9,  4,  0, 0, 0)
anl_start_time = datetime.datetime(2021, 9,  4, 18, 0, 0)
anl_end_time   = datetime.datetime(2021, 9,  5,  0, 0, 0)

    dir_

time_interval  = 1
window_time    = 1
J2000 = datetime.datetime(2000, 1, 1, 0, 0, 0, tzinfo = datetime.timezone.utc)

time_now = anl_start_time
while time_now <= anl_end_time:

    time_now_str = time_now.strftime('%Y%m%d%H')
    time_now_s = (time_now - datetime.timedelta(hours = window_time/2.0) - initial_time).total_seconds()/3600.0
    time_now_e = (time_now + datetime.timedelta(hours = window_time/2.0) - initial_time).total_seconds()/3600.0
    print(time_now_str)
    print(time_now_s)
    print(time_now_e)

    ncfile_DAWN = Dataset(file_DAWN)
    n_loc = len(ncfile_DAWN.variables['Profile_Latitude'][:])
    n_hgt = len(ncfile_DAWN.variables['Profile_Altitude'][:])
    print(n_loc)
    print(n_hgt)
    print(np.tile(ncfile_DAWN.variables['Profile_Latitude'][:], (n_hgt, 1)).shape)

    DAWN_latitude = np.tile(ncfile_DAWN.variables['Profile_Latitude'][:], (n_hgt, 1)).flatten('F')
    DAWN_longitude = np.tile(ncfile_DAWN.variables['Profile_Longitude'][:], (n_hgt, 1)).flatten('F')
    DAWN_datetime = np.tile(ncfile_DAWN.variables['Profile_Time'][:], (n_hgt, 1)).flatten('F')
    DAWN_year = np.array([(initial_time + datetime.timedelta(hours = d)).year for d in DAWN_datetime], dtype='int64')
    DAWN_mnth = np.array([(initial_time + datetime.timedelta(hours = d)).month for d in DAWN_datetime], dtype='int64')
    DAWN_days = np.array([(initial_time + datetime.timedelta(hours = d)).day for d in DAWN_datetime], dtype='int64')
    DAWN_hour = np.array([(initial_time + datetime.timedelta(hours = d)).hour for d in DAWN_datetime], dtype='int64')
    DAWN_minu = np.array([(initial_time + datetime.timedelta(hours = d)).minute for d in DAWN_datetime], dtype='int64')
    DAWN_seco = np.array([(initial_time + datetime.timedelta(hours = d)).second for d in DAWN_datetime])
    DAWN_mcse = np.array([(initial_time + datetime.timedelta(hours = d)).microsecond for d in DAWN_datetime])
    DAWN_seco = DAWN_seco + DAWN_mcse/1000000.0
    DAWN_altitude = np.transpose(np.tile(ncfile_DAWN.variables['Profile_Altitude'][:], (n_loc, 1))).flatten('F')*1000.0
    DAWN_geopotential = DAWN_altitude*9.80665
    DAWN_pressure = np.array([101325.0*np.exp(-1.0*d*0.02896968/288.16/8.314462618) for d in DAWN_geopotential])
    DAWN_wind_direction = ncfile_DAWN.variables['Wind_Direction'][:,:].flatten('F')
    DAWN_wind_speed = ncfile_DAWN.variables['Wind_Speed'][:,:].flatten('F')

    index = (~DAWN_wind_speed.mask) & (DAWN_datetime >= time_now_s) & (DAWN_datetime <= time_now_e)
    n_data = sum(index==True)

    #BUHD = np.full((n_data), 'URNT15')
    #BORG = np.full((n_data), 'KWBC')
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

    dir_out = dir_bufr + '/' + time_now_str
    os.system('rm -rf ' + dir_out)
    os.system('mkdir ' + dir_out)

    #with open(dir_out + '/1.txt', 'ab') as f:
        #np.savetxt(f, BUHD, fmt='%s')
    #with open(dir_out + '/2.txt', 'ab') as f:
        #np.savetxt(f, BORG, fmt='%s')
    with open(dir_out + '/1.txt', 'ab') as f:
        np.savetxt(f, YEAR)
    with open(dir_out + '/2.txt', 'ab') as f:
        np.savetxt(f, MNTH)
    with open(dir_out + '/3.txt', 'ab') as f:
        np.savetxt(f, DAYS)
    with open(dir_out + '/4.txt', 'ab') as f:
        np.savetxt(f, HOUR)
    with open(dir_out + '/5.txt', 'ab') as f:
        np.savetxt(f, MINU)
    with open(dir_out + '/6.txt', 'ab') as f:
        np.savetxt(f, SECO)
    with open(dir_out + '/7.txt', 'ab') as f:
        np.savetxt(f, QHDOP)
    with open(dir_out + '/8.txt', 'ab') as f:
        np.savetxt(f, QHDOM)
    with open(dir_out + '/9.txt', 'ab') as f:
        np.savetxt(f, CLAT)
    with open(dir_out + '/10.txt', 'ab') as f:
        np.savetxt(f, CLON)
    with open(dir_out + '/11.txt', 'ab') as f:
        np.savetxt(f, PRLC)
    with open(dir_out + '/12.txt', 'ab') as f:
        np.savetxt(f, GP10)
    with open(dir_out + '/13.txt', 'ab') as f:
        np.savetxt(f, QMWN)
    with open(dir_out + '/14.txt', 'ab') as f:
        np.savetxt(f, WDIR)
    with open(dir_out + '/15.txt', 'ab') as f:
        np.savetxt(f, WSPD)
    with open(dir_out + '/16.txt', 'ab') as f:
        np.savetxt(f, PKWDSP)

    np.savetxt(dir_out + '/0.txt', [n_data])
    time_now = time_now + datetime.timedelta(hours = time_interval)
