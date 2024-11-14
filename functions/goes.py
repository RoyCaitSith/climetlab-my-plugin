import os
import re
import time
import glob
import netCDF4
import importlib
import subprocess
import numpy as np
import seaborn as sns
import pyorbital.orbital as po
import matplotlib.pyplot as plt
from pyorbital import astronomy
from datetime import datetime, timedelta, timezone
from pathlib import Path
from netCDF4 import Dataset, num2date
from tqdm.notebook import tqdm
from mpl_toolkits.basemap import Basemap
from IPython.display import Image as IPImage
from matplotlib.colors import LinearSegmentedColormap
from combine_and_show_images import combine_images_grid
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import Image as IPImage
from metpy.calc import height_to_geopotential, relative_humidity_from_specific_humidity, precipitable_water
from metpy.units import units

def parse_to_datetime(timestamp):
    # Extract components
    year = int(timestamp[:4])
    day_of_year = int(timestamp[4:7])
    hour = int(timestamp[7:9])
    minute = int(timestamp[9:11])
    second = int(timestamp[11:13])
    tenth_of_second = int(timestamp[13]) / 10  # Convert tenth of a second to fractional seconds

    # Create base date from year and Julian day
    base_date = datetime(year, 1, 1) + timedelta(days=day_of_year - 1)
    
    # Construct the final datetime object
    parsed_datetime = base_date.replace(hour=hour, minute=minute, second=second, microsecond=int(tenth_of_second * 1e6))

    return parsed_datetime

def create_goes_bufr_temp(dir_data, case, anl_start_time, anl_end_time, cycling_interval, version):

    total_hours = (anl_end_time-anl_start_time).total_seconds()/3600
    total_da_cycles = int(total_hours/cycling_interval+1)

    dir_goes = os.path.join(dir_data, 'GOES', case)
    dir_goes_bufr_temp = os.path.join(dir_goes, 'bufr_temp')
    dir_goes_bufr_temp_version = os.path.join(dir_goes_bufr_temp, version)
    os.makedirs(dir_goes_bufr_temp, exist_ok=True)
    os.makedirs(dir_goes_bufr_temp_version, exist_ok=True)

    (n_channel, n_x, n_y) = (10, 5424, 5424)
    J2000 = datetime(2000, 1,  1, 12, 0, 0, tzinfo = timezone.utc)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_now_time = anl_start_time + timedelta(hours=cycling_interval*(idc-1))
        time_s = anl_now_time - timedelta(hours=cycling_interval/2.0)
        time_e = anl_now_time + timedelta(hours=cycling_interval/2.0)
        anl_now_time_YYYYMMDD = anl_now_time.strftime('%Y%m%d')
        anl_now_time_HH = anl_now_time.strftime('%H')
        print(time_s)
        print(time_e)

        dir_bufr_temp_YYYYMMDD = os.path.join(dir_goes_bufr_temp_version, anl_now_time_YYYYMMDD)
        dir_bufr_temp_HH = os.path.join(dir_bufr_temp_YYYYMMDD, anl_now_time_HH)
        os.system(f"rm -rf {dir_bufr_temp_HH}")
        os.makedirs(dir_bufr_temp_YYYYMMDD, exist_ok=True)
        os.makedirs(dir_bufr_temp_HH, exist_ok=True)

        n_total_data = 0
        YEAR   = []
        MNTH   = []
        DAYS   = []
        HOUR   = []
        MINU   = []
        SECO   = []
        CLATH  = []
        CLONH  = []
        SAZA   = []
        SOZA   = []
        BEARAZ = []
        SOLAZI = []
        HMSL   = []
        TMBR07 = []
        TMBR08 = []
        TMBR09 = []
        TMBR10 = []
        TMBR11 = []
        TMBR12 = []
        TMBR13 = []
        TMBR14 = []
        TMBR15 = []
        TMBR16 = []

        filenames = os.popen(f"ls {dir_goes}/*/OR_ABI-L2-CMIPF-M6C07_G16*.nc").readlines()
        for file_goes in filenames:
                            
            pattern = r's(\d{14})_e(\d{14})_c(\d{14})'
            pattern_match = re.search(pattern, file_goes)
            date_st_str = pattern_match.group(1)
            date_et_str = pattern_match.group(2)
            date_st = parse_to_datetime(date_st_str)
            date_et = parse_to_datetime(date_et_str)
            print(date_st)
            print(date_et)

            if date_st <= time_e and date_et >= time_s:
                for ich in range(7, 7+n_channel):

                    cfiles   = os.popen(f"ls {dir_goes}/*/OR_ABI-L2-CMIPF-M6C*{str(ich)}_G16_s{date_st_str[0:11]}*_e{date_et_str[0:11]}*.nc").readlines()
                    cfile    = cfiles[0].rstrip('\n')
                    ncfile   = netCDF4.Dataset(cfile, mode='r', format='NETCDF4')
                    CMI      = ncfile.variables['CMI'][:,:]
                    DQF      = ncfile.variables['DQF'][:,:]
                    t        = ncfile.variables['t'][:]
                    x        = ncfile.variables['x'][:]
                    y        = ncfile.variables['y'][:]
                    gip      = ncfile.variables['goes_imager_projection']
                    r_eq     = gip.semi_major_axis
                    r_pol    = gip.semi_minor_axis
                    H        = gip.perspective_point_height + gip.semi_major_axis
                    phi_0    = gip.latitude_of_projection_origin
                    lambda_0 = gip.longitude_of_projection_origin
                    print(cfile)

                    t     = J2000 + timedelta(seconds = float(t))
                    x, y  = np.meshgrid(x, y, indexing='xy')  
                    sin_x = np.sin(x)
                    cos_x = np.cos(x)
                    sin_y = np.sin(y)
                    cos_y = np.cos(y)
                    a     = np.power(sin_x, 2) + np.power(cos_x, 2)*(np.power(cos_y, 2)+np.power(r_eq*sin_y/r_pol, 2))
                    b     = -2.0*H*cos_x*cos_y
                    c     = np.power(H, 2) - np.power(r_eq, 2)
                    r_s   = (-1.0*b - np.sqrt(np.power(b, 2)-4*a*c))/(2*a)
                    s_x   = r_s*cos_x*cos_y
                    s_y   = -1.0*r_s*sin_x
                    s_z   = r_s*cos_x*sin_y
                    lat   = np.degrees(np.arctan(np.power(r_eq/r_pol, 2)*s_z/np.sqrt(np.power(H-s_x, 2)+np.power(s_y, 2))))
                    lon   = lambda_0 - np.degrees(np.arctan(s_y/(H-s_x)))

                    sensor_azimuth, sensor_zenith = po.get_observer_look(np.atleast_1d(lambda_0), \
                                                                         np.atleast_1d(phi_0), \
                                                                         np.atleast_1d((H-r_eq)/1000.0), \
                                                                         np.atleast_1d(t), \
                                                                         np.atleast_1d(lon), \
                                                                         np.atleast_1d(lat), \
                                                                         np.atleast_1d(0.0))
                    sensor_zenith  = 90.0 - sensor_zenith
                    sensor_zenith  = np.reshape(sensor_zenith, (-1))
                    sensor_azimuth = np.reshape(sensor_azimuth, (-1))

                    solar_zenith  = astronomy.sun_zenith_angle(t, lon, lat)
                    solar_altitude, solar_azimuth = astronomy.get_alt_az(t, lon, lat)
                    solar_azimuth = np.degrees(solar_azimuth)
                    solar_zenith  = np.reshape(solar_zenith, (-1))
                    solar_azimuth = np.reshape(solar_azimuth, (-1))
                    solar_azimuth[solar_azimuth < 0] = solar_azimuth[solar_azimuth < 0] + 360.0

                    # Year, Month, Day, Hour, Minute, Second
                    GOES_YEAR   = np.full(n_x*n_y, t.year)
                    GOES_MNTH   = np.full(n_x*n_y, t.month)
                    GOES_DAYS   = np.full(n_x*n_y, t.day)
                    GOES_HOUR   = np.full(n_x*n_y, t.hour)
                    GOES_MINU   = np.full(n_x*n_y, t.minute)
                    GOES_SECO   = np.full(n_x*n_y, t.second + t.microsecond/1000000.0)
                    GOES_CLATH  = np.reshape(lat, (-1))
                    GOES_CLONH  = np.reshape(lon, (-1))
                    GOES_SAZA   = sensor_zenith
                    GOES_SOZA   = solar_zenith
                    GOES_BEARAZ = sensor_azimuth
                    GOES_SOLAZI = solar_azimuth
                    GOES_HMSL   = np.full(n_x*n_y, H - r_eq)
                    GOES_DQF    = np.reshape(DQF, (-1))
                    GOES_TMBR07 = np.reshape(CMI, (-1))
                    GOES_TMBR08 = np.reshape(CMI, (-1))
                    GOES_TMBR09 = np.reshape(CMI, (-1))
                    GOES_TMBR10 = np.reshape(CMI, (-1))
                    GOES_TMBR11 = np.reshape(CMI, (-1))
                    GOES_TMBR12 = np.reshape(CMI, (-1))
                    GOES_TMBR13 = np.reshape(CMI, (-1))

                    #Quality Control
                    index = (GOES_DQF != 0) | (np.isnan(GOES_CLATH)) | (np.isnan(GOES_CLONH))
                    index = (index == False)
                    ncfile.close()

                    print(GOES_YEAR[index])
                    print(GOES_MNTH[index])
                    print(GOES_DAYS[index])
                    print(GOES_HOUR[index])
                    print(GOES_MINU[index])
                    print(GOES_SECO[index])
                    print(GOES_CLATH[index])
                    print(GOES_CLONH[index])
                    print(GOES_SAZA[index])
                    print(GOES_SOZA[index])
                    print(GOES_BEARAZ[index])
                    print(GOES_SOLAZI[index])
                    print(GOES_HMSL[index])
                    print(GOES_DQF[index])
                    print(GOES_TMBR07[index])

                    n_data = np.count_nonzero(index)
                    print(n_data)
                    if n_data > 0:
                        n_total_data += n_data
                        YEAR   += GOES_YEAR[index].tolist()
                        MNTH   += GOES_MNTH[index].tolist()
                        DAYS   += GOES_DAYS[index].tolist()
                        HOUR   += GOES_HOUR[index].tolist()
                        MINU   += GOES_MINU[index].tolist()
                        SECO   += GOES_SECO[index].tolist()
                        CLATH  += GOES_CLATH[index].tolist()
                        CLONH  += GOES_CLONH[index].tolist()
                        SAZA   += GOES_SAZA[index].tolist()
                        SOZA   += GOES_SOZA[index].tolist()
                        BEARAZ += GOES_BEARAZ[index].tolist()
                        SOLAZI += GOES_SOLAZI[index].tolist()
                        HMSL   += GOES_HMSL[index].tolist()
                        TMBR07 += GOES_TMBR07[index].tolist()
                        TMBR08 += GOES_TMBR08[index].tolist()
                        TMBR09 += GOES_TMBR09[index].tolist()
                        TMBR10 += GOES_TMBR10[index].tolist()
                        TMBR11 += GOES_TMBR11[index].tolist()
                        TMBR12 += GOES_TMBR12[index].tolist()
                        TMBR13 += GOES_TMBR13[index].tolist()

        with open(os.path.join(dir_bufr_temp_HH,  '1.txt'), 'ab') as f:
            np.savetxt(f, YEAR)
        with open(os.path.join(dir_bufr_temp_HH,  '2.txt'), 'ab') as f:
            np.savetxt(f, MNTH)
        with open(os.path.join(dir_bufr_temp_HH,  '3.txt'), 'ab') as f:
            np.savetxt(f, DAYS)
        with open(os.path.join(dir_bufr_temp_HH,  '4.txt'), 'ab') as f:
            np.savetxt(f, HOUR)
        with open(os.path.join(dir_bufr_temp_HH,  '5.txt'), 'ab') as f:
            np.savetxt(f, MINU)
        with open(os.path.join(dir_bufr_temp_HH,  '6.txt'), 'ab') as f:
            np.savetxt(f, SECO)
        with open(os.path.join(dir_bufr_temp_HH,  '7.txt'), 'ab') as f:
            np.savetxt(f, CLATH)
        with open(os.path.join(dir_bufr_temp_HH,  '8.txt'), 'ab') as f:
            np.savetxt(f, CLONH)
        with open(os.path.join(dir_bufr_temp_HH,  '9.txt'), 'ab') as f:
            np.savetxt(f, SAZA)
        with open(os.path.join(dir_bufr_temp_HH, '10.txt'), 'ab') as f:
            np.savetxt(f, SOZA)
        with open(os.path.join(dir_bufr_temp_HH, '11.txt'), 'ab') as f:
            np.savetxt(f, BEARAZ)
        with open(os.path.join(dir_bufr_temp_HH, '12.txt'), 'ab') as f:
            np.savetxt(f, SOLAZI)
        with open(os.path.join(dir_bufr_temp_HH, '13.txt'), 'ab') as f:
            np.savetxt(f, HMSL)
        with open(os.path.join(dir_bufr_temp_HH, '14.txt'), 'ab') as f:
            np.savetxt(f, TMBR07)
        with open(os.path.join(dir_bufr_temp_HH, '15.txt'), 'ab') as f:
            np.savetxt(f, TMBR08)
        with open(os.path.join(dir_bufr_temp_HH, '16.txt'), 'ab') as f:
            np.savetxt(f, TMBR09)
        with open(os.path.join(dir_bufr_temp_HH, '17.txt'), 'ab') as f:
            np.savetxt(f, TMBR10)
        with open(os.path.join(dir_bufr_temp_HH, '18.txt'), 'ab') as f:
            np.savetxt(f, TMBR11)
        with open(os.path.join(dir_bufr_temp_HH, '19.txt'), 'ab') as f:
            np.savetxt(f, TMBR12)
        with open(os.path.join(dir_bufr_temp_HH, '20.txt'), 'ab') as f:
            np.savetxt(f, TMBR13)
        np.savetxt(os.path.join(dir_bufr_temp_HH, '0.txt'), [n_total_data])
        print('\n')

def create_tropics_bufr_file(dir_data, case, anl_start_time, anl_end_time, cycling_interval, version):

    total_hours = (anl_end_time-anl_start_time).total_seconds()/3600
    total_da_cycles = int(total_hours/cycling_interval+1)

    dir_tropics = os.path.join(dir_data, 'TROPICS', case, 'TROPICS_V3')
    dir_tropics_bufr_temp = os.path.join(dir_tropics, 'bufr_temp')
    dir_tropics_bufr_file = os.path.join(dir_tropics, 'bufr_file')
    dir_tropics_bufr_temp_version = os.path.join(dir_tropics_bufr_temp, version)
    dir_tropics_bufr_file_version = os.path.join(dir_tropics_bufr_file, version)
    os.makedirs(dir_tropics_bufr_file, exist_ok=True)
    os.makedirs(dir_tropics_bufr_file_version, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_now_time = anl_start_time + timedelta(hours=cycling_interval*(idc-1))
        anl_now_time_YYYYMMDD = anl_now_time.strftime('%Y%m%d')
        anl_now_time_HH = anl_now_time.strftime('%H')
        print(anl_now_time)

        dir_bufr_file_YYYYMMDD = os.path.join(dir_tropics_bufr_file_version, anl_now_time_YYYYMMDD)
        bufr_file = os.path.join(dir_bufr_file_YYYYMMDD, f"gdas.t{anl_now_time_HH}z.tropics.tm00.bufr_d")
        dir_fortran_files = os.path.join(dir_data, 'TROPICS', 'Fortran_Files')
        bufr_file_fortran = os.path.join(dir_fortran_files, 'gdas.tropics.bufr')
        os.makedirs(dir_bufr_file_YYYYMMDD, exist_ok=True)
        os.system(f"rm -rf {bufr_file_fortran}")

        print('Check bufr_temp: ')
        flag = True
        info = os.popen(f"cd {dir_tropics_bufr_temp_version}/{anl_now_time_YYYYMMDD}/{anl_now_time_HH} && ls ./*.txt").readlines()
        if len(info) != 22:
            flag = False
        print(len(info))
        print(flag)

        if flag:

            fdata = ''
            with open(f"{dir_fortran_files}/bufr_encode_tropics.f90", 'r') as f:
                for line in f.readlines():
                    if(line.find('idate = ') == 4): line = f"    idate = {anl_now_time_YYYYMMDD}{anl_now_time_HH}\n"
                    if(line.find('dir_files = ') == 4): line = f"    dir_files = '{dir_tropics_bufr_temp}/{version}/{anl_now_time_YYYYMMDD}/{anl_now_time_HH}/'\n"
                    fdata += line
            f.close()

            with open(f"{dir_fortran_files}/bufr_encode_tropics.f90", 'w') as f:
                f.writelines(fdata)
            f.close()

            os.popen(f"cd {dir_fortran_files} && ./run_encode_tropics.sh > log_out")
            flag = True
            file_size = 0
            while flag:
                time.sleep(5)
                file_size_temp = os.popen(f"stat -c '%s' {bufr_file_fortran}").read()
                if file_size_temp:
                    file_size_next = int(file_size_temp)
                    if file_size_next == file_size:
                        flag = False
                    else:
                        file_size = file_size_next
                print(file_size)

            os.system(f"mv {bufr_file_fortran} {bufr_file}")
