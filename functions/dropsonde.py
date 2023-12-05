import os
import re
import time
import h5py
import glob
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

def dropsonde_to_csv(data_library_name, dir_case, case_name):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_data = os.path.join(dir_exp, 'data')
    dir_Dropsonde = os.path.join(dir_data, 'Dropsonde')

    filenames = glob.glob(os.path.join(dir_Dropsonde, 'CPEX*DC8*ict'))
    for filename in tqdm(filenames, desc='Files', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        if filename != '':
            df = pd.DataFrame(columns=['TIME', 'LAT', 'LON', 'PRLC', 'GP10', 'TMDB', 'SPFH', 'REHU', 'WDIR', 'WSPD'])
            with open(filename, encoding='windows-1252') as f:
                lines = f.readlines()

                #Get the first line of the record
                line = lines[0:1][0].rstrip('\n')
                items = line.split(',')
                first_line = int(items[0])

                #Get the date
                line = lines[29:30][0].rstrip('\n')
                pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})'
                pattern_match = re.search(pattern, line)
                launch_time_str = pattern_match.group(1)
                launch_time = datetime.strptime(launch_time_str, '%Y-%m-%d %H:%M:%S')
                launch_time_str = launch_time.strftime('%Y%m%d%H%M%S')

                time_list = []
                lat_list  = []
                lon_list  = []
                prlc_list = []
                gp10_list = []
                tmdb_list = []
                spfh_list = []
                rehu_list = []
                wdir_list = []
                wspd_list = []
                
                for line in lines[first_line:]:
                    line = line.rstrip('\n')
                    items = line.split(',')
                    flag = ('-9999' in items) or ('' in items)

                    if not flag:
                        time_now = launch_time + timedelta(seconds = float(items[1]))
                        time_now_str = int(time_now.strftime('%Y%m%d%H%M%S'))
                        e = 6.112*np.exp((17.67*float(items[11]))/(float(items[11])+243.5))
                        q = 0.622*e/(float(items[2])-0.378*e)

                        time_list += [time_now_str]
                        lat_list  += [float(items[7])]
                        lon_list  += [float(items[8])]
                        prlc_list += [float(items[2])*100.0]
                        gp10_list += [float(items[9])*9.80665]
                        tmdb_list += [float(items[3])+273.15]
                        spfh_list += [q]
                        rehu_list += [float(items[4])]
                        wdir_list += [float(items[6])]
                        wspd_list += [float(items[5])]

            row = pd.DataFrame({'TIME': time_list, \
                                'LAT': lat_list, \
                                'LON': lon_list, \
                                'PRLC': prlc_list, \
                                'GP10': gp10_list, \
                                'TMDB': tmdb_list, \
                                'SPFH': spfh_list, \
                                'REHU': rehu_list, \
                                'WDIR': wdir_list, \
                                'WSPD': wspd_list})
            
            # df = pd.concat([df, row], ignore_index=True)
            df = pd.concat([row.iloc[0:2], row.iloc[2:]], ignore_index=True)

            filename_dropsonde = '_'.join(['Dropsonde', 'DC8', launch_time_str+'.csv'])
            save_file = os.path.join(dir_Dropsonde, filename_dropsonde)
            df.to_csv(save_file, index=False)
            print(filename_dropsonde)

def create_dropsonde_bufr_temp(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time=datetime(*itime)
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_dropsonde = os.path.join(dir_data, 'Dropsonde')
    dir_dropsonde_bufr_temp = os.path.join(dir_dropsonde, 'bufr_temp')
    os.makedirs(dir_dropsonde, exist_ok=True)
    os.makedirs(dir_dropsonde_bufr_temp, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        time_s = anl_end_time - timedelta(hours=cycling_interval/2.0)
        time_e = anl_end_time + timedelta(hours=cycling_interval/2.0)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')
        print(time_s)
        print(time_e)

        dir_bufr_temp = os.path.join(dir_dropsonde_bufr_temp, anl_end_time_YYYYMMDD)
        os.makedirs(dir_bufr_temp, exist_ok=True)
        dir_bufr_temp = os.path.join(dir_bufr_temp, anl_end_time_HH)
        os.system(f"rm -rf {dir_bufr_temp}")
        os.makedirs(dir_bufr_temp, exist_ok=True)
        filenames = os.popen(f"ls {dir_dropsonde}/Dropsonde_DC8*csv").readlines()
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
        QMWN = []
        WDIR = []
        WSPD = []
        PKWDSP = []

        for file_dropsonde in filenames:
            print(file_dropsonde)
            df = pd.read_csv(file_dropsonde.strip('\n'))
            dropsonde_datetime = np.array([datetime.strptime(str(d), '%Y%m%d%H%M%S') for d in df['TIME']])
            dropsonde_year = np.array([(datetime.strptime(str(d), '%Y%m%d%H%M%S')).year for d in df['TIME']], dtype='int64')
            dropsonde_mnth = np.array([(datetime.strptime(str(d), '%Y%m%d%H%M%S')).month for d in df['TIME']], dtype='int64')
            dropsonde_days = np.array([(datetime.strptime(str(d), '%Y%m%d%H%M%S')).day for d in df['TIME']], dtype='int64')
            dropsonde_hour = np.array([(datetime.strptime(str(d), '%Y%m%d%H%M%S')).hour for d in df['TIME']], dtype='int64')
            dropsonde_minu = np.array([(datetime.strptime(str(d), '%Y%m%d%H%M%S')).minute for d in df['TIME']], dtype='int64')
            dropsonde_seco = np.array([(datetime.strptime(str(d), '%Y%m%d%H%M%S')).second for d in df['TIME']])
            dropsonde_mcse = np.array([(datetime.strptime(str(d), '%Y%m%d%H%M%S')).microsecond for d in df['TIME']])
            dropsonde_seco = dropsonde_seco + dropsonde_mcse/1000000.0
            dropsonde_latitude = np.array(df['LAT'])
            dropsonde_longitude = np.array(df['LON'])
            dropsonde_pressure = np.array(df['PRLC'])
            dropsonde_geopotential = np.array(df['GP10'])
            dropsonde_temperature = np.array(df['TMDB'])
            dropsonde_specific_humidity = np.array(df['SPFH'])
            dropsonde_relative_humidity = np.array(df['REHU'])
            dropsonde_wind_direction = np.array(df['WDIR'])
            dropsonde_wind_speed = np.array(df['WSPD'])

            index = (dropsonde_datetime >= time_s) & (dropsonde_datetime <= time_e)

            n_data = sum(index==True)
            if n_data > 0:
                n_total_data += n_data
                YEAR += dropsonde_year[index].tolist()
                MNTH += dropsonde_mnth[index].tolist()
                DAYS += dropsonde_days[index].tolist()
                HOUR += dropsonde_hour[index].tolist()
                MINU += dropsonde_minu[index].tolist()
                SECO += dropsonde_seco[index].tolist()
                QHDOP += np.full((n_data), 0, dtype='int').tolist()
                QHDOM += np.full((n_data), 0, dtype='int').tolist()
                CLAT += dropsonde_latitude[index].tolist()
                CLON += dropsonde_longitude[index].tolist()
                PRLC += dropsonde_pressure[index].tolist()
                GP10 += dropsonde_geopotential[index].tolist()
                QMAT += np.full((n_data), 2, dtype='int').tolist()
                TMDB += dropsonde_temperature[index].tolist()
                QMDD += np.full((n_data), 2, dtype='int').tolist()
                SPFH += dropsonde_specific_humidity[index].tolist()
                REHU += dropsonde_relative_humidity[index].tolist()
                QMWN += np.full((n_data), 2, dtype='int').tolist()
                WDIR += dropsonde_wind_direction[index].tolist()
                WSPD += dropsonde_wind_speed[index].tolist()
                PKWDSP += np.full((n_data), 0, dtype='int').tolist()

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
        with open(os.path.join(dir_bufr_temp, '18.txt'), 'ab') as f:
            np.savetxt(f, QMWN)
        with open(os.path.join(dir_bufr_temp, '19.txt'), 'ab') as f:
            np.savetxt(f, WDIR)
        with open(os.path.join(dir_bufr_temp, '20.txt'), 'ab') as f:
            np.savetxt(f, WSPD)
        with open(os.path.join(dir_bufr_temp, '21.txt'), 'ab') as f:
            np.savetxt(f, PKWDSP)
        np.savetxt(dir_bufr_temp + '/0.txt', [n_total_data])

def create_dropsonde_bufr(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time=datetime(*itime)
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_dropsonde = os.path.join(dir_data, 'Dropsonde')
    dir_dropsonde_bufr = os.path.join(dir_dropsonde, 'bufr')
    dir_dropsonde_bufr_temp = os.path.join(dir_dropsonde, 'bufr_temp')
    os.makedirs(dir_dropsonde_bufr, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')

        dir_bufr = os.path.join(dir_dropsonde_bufr, anl_end_time_YYYYMMDD)
        file_bufr = os.path.join(dir_bufr, f"gdas.t{anl_end_time_HH}z.dropsonde.tm00.bufr_d")
        dir_fortran = os.path.join(dir_dropsonde, 'fortran_files')
        file_fortran_bufr = os.path.join(dir_fortran, 'gdas.dropsonde.bufr')
        os.makedirs(dir_bufr, exist_ok=True)
        os.system(f"rm -rf {file_fortran_bufr}")

        print('Check bufr_temp: ')
        flag = True
        info = os.popen(f"cd {dir_dropsonde_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH} && ls ./*.txt").readlines()
        if len(info) != 22:
            flag = False
        print(len(info))
        print(flag)

        if flag:

            fdata = ''
            with open(f"{dir_fortran}/bufr_encode_dropsonde.f90", 'r') as f:
                for line in f.readlines():
                    if(line.find('idate = ') == 4): line = f"    idate = {anl_end_time_YYYYMMDD}{anl_end_time_HH}\n"
                    if(line.find('dir_files = ') == 4): line = f"    dir_files = '{dir_dropsonde_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH}/'\n"
                    fdata += line
            f.close()

            with open(f"{dir_fortran}/bufr_encode_dropsonde.f90", 'w') as f:
                f.writelines(fdata)
            f.close()

            os.popen(f"cd {dir_fortran} && ./run_encode_dropsonde.sh > log_out")
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
