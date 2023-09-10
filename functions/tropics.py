import os
import re
import time
import glob
import netCDF4
import importlib
import subprocess
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pathlib import Path
from netCDF4 import Dataset
from tqdm.notebook import tqdm
from mpl_toolkits.basemap import Basemap
from IPython.display import Image as IPImage
from matplotlib.colors import LinearSegmentedColormap
from combine_and_show_images import combine_images_grid
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import Image as IPImage
from metpy.calc import height_to_geopotential, dewpoint_from_specific_humidity, precipitable_water
from metpy.units import units

def create_TROPICS_bufr_temp(data_library_name, dir_case, case_name, version='V2_SEA_AS'):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_TROPICS = os.path.join(dir_data, f"TROPICS_{version}")
    dir_TROPICS_bufr_temp = os.path.join(dir_TROPICS, 'bufr_temp')
    os.makedirs(dir_TROPICS, exist_ok=True)
    os.makedirs(dir_TROPICS_bufr_temp, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        time_s = anl_end_time - timedelta(hours=cycling_interval/2.0)
        time_e = anl_end_time + timedelta(hours=cycling_interval/2.0)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')
        print(anl_end_time)

        dir_bufr_temp = os.path.join(dir_TROPICS_bufr_temp, anl_end_time_YYYYMMDD)
        os.makedirs(dir_bufr_temp, exist_ok=True)
        dir_bufr_temp = os.path.join(dir_bufr_temp, anl_end_time_HH)
        os.system(f"rm -rf {dir_bufr_temp}")
        os.makedirs(dir_bufr_temp, exist_ok=True)
        filenames = os.popen(f"ls {dir_TROPICS}/TROPICS01*.nc").readlines()

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

        for file_TROPICS in filenames:
                            
            pattern = r'ST(\d{8}-\d{6}).ET(\d{8}-\d{6})'
            pattern_match = re.search(pattern, file_TROPICS)
            date_st_str = pattern_match.group(1)
            date_et_str = pattern_match.group(2)
            date_st = datetime.strptime(date_st_str, '%Y%m%d-%H%M%S')
            date_et = datetime.strptime(date_et_str, '%Y%m%d-%H%M%S')

            if date_st <= time_e and date_et >= time_s:

                if 'V1' in version:

                    ncfile = netCDF4.Dataset(file_TROPICS.rstrip('\n'), mode='r', format='NETCDF4')
                    (n_scans, n_spots, n_vertical_levels) = ncfile.variables['PTemp'][:,:,:].shape
                    n_data = n_vertical_levels*n_scans*n_spots
                    print(file_TROPICS.rstrip('\n'))

                    TROPICS_YEAR = np.transpose(np.tile(ncfile.variables['ScanTime_year'][:],   (n_vertical_levels, n_spots, 1))).flatten()
                    TROPICS_MNTH = np.transpose(np.tile(ncfile.variables['ScanTime_month'][:],  (n_vertical_levels, n_spots, 1))).flatten()
                    TROPICS_DAYS = np.transpose(np.tile(ncfile.variables['ScanTime_dom'][:],    (n_vertical_levels, n_spots, 1))).flatten()
                    TROPICS_HOUR = np.transpose(np.tile(ncfile.variables['ScanTime_hour'][:],   (n_vertical_levels, n_spots, 1))).flatten()
                    TROPICS_MINU = np.transpose(np.tile(ncfile.variables['ScanTime_minute'][:], (n_vertical_levels, n_spots, 1))).flatten()
                    TROPICS_SECO = np.transpose(np.tile(ncfile.variables['ScanTime_second'][:], (n_vertical_levels, n_spots, 1))).flatten()
                    TROPICS_QHDOP = np.full((n_data), 0, dtype='int')
                    TROPICS_QHDOM = np.full((n_data), 0, dtype='int')
                    TROPICS_CLAT = np.transpose(np.tile(np.transpose(ncfile.variables['Latitude'][:,:]), (n_vertical_levels, 1, 1))).flatten()
                    TROPICS_Longitude = ncfile.variables['Longitude'][:,:]
                    TROPICS_Longitude[TROPICS_Longitude<0] = TROPICS_Longitude[TROPICS_Longitude<0] + 360.0
                    TROPICS_CLON = np.transpose(np.tile(np.transpose(TROPICS_Longitude), (n_vertical_levels, 1, 1))).flatten()
                    TROPICS_PRLC = np.tile(ncfile.variables['Player'][:]*100.0, (n_scans, n_spots, 1)).flatten()
                    TROPICS_GP10 = np.full((n_data), 0.0, dtype='float64')
                    TROPICS_QMAT = np.full((n_data), 2, dtype='int')
                    TROPICS_TMDB = ncfile.variables['PTemp'][:,:,:].flatten()
                    TROPICS_QMDD = np.full((n_data), 2, dtype='int')
                    TROPICS_SPFH = (ncfile.variables['PVapor'][:,:,:].flatten()/1000.0)/(ncfile.variables['PVapor'][:,:,:].flatten()/1000.0+1.0)
                    TROPICS_es = 6.112*np.exp((17.67*(TROPICS_TMDB-273.16))/(TROPICS_TMDB-29.65))
                    TROPICS_ws = 0.622*TROPICS_es/(TROPICS_PRLC/100.0)
                    TROPICS_REHU = 100.0*ncfile.variables['PVapor'][:,:,:].flatten()/1000.0/TROPICS_ws
                    TROPICS_QMWN = np.full((n_data), 2, dtype='int')
                    TROPICS_WDIR = np.full((n_data), 0.0, dtype='float64')
                    TROPICS_WSPD = np.full((n_data), 0.0, dtype='float64')
                    TROPICS_PKWDSP = np.full((n_data), 0.0, dtype='float64')

                    Bad_Qual_Flag = np.transpose(np.tile(np.transpose(ncfile.variables['Qc'][:,:,0]), (n_vertical_levels, 1, 1))).flatten()
                    # Clear_Sky_Flag = np.transpose(np.tile(np.transpose(ncfile.variables['Qc'][:,:,1]), (n_vertical_levels, 1, 1))).flatten()

                    file_tpw = os.path.join(dir_TROPICS, f"ST{date_st_str}.ET{date_et_str}_TPW.nc")
                    ncfile_tpw = Dataset(file_tpw, 'r')
                    Clear_Sky_Flag = np.transpose(np.tile(np.transpose(ncfile_tpw.variables['clear_sky'][:,:]), (n_vertical_levels, 1, 1))).flatten()
                    print(file_tpw)

                    if 'SEA' in version and 'AS' in version:
                        index = (Bad_Qual_Flag < 2) & \
                                (np.array(TROPICS_TMDB.tolist()) != None) & (np.array(TROPICS_SPFH.tolist()) != None)
                    elif 'SEA' in version and 'CS' in version:
                        index = (Bad_Qual_Flag < 2) & (Clear_Sky_Flag < 1) & \
                                (np.array(TROPICS_TMDB.tolist()) != None) & (np.array(TROPICS_SPFH.tolist()) != None)

                    ncfile.close()
                    ncfile_tpw.close()

                elif 'V2' in version:
                
                    ncfile = netCDF4.Dataset(file_TROPICS.rstrip('\n'), mode='r', format='NETCDF4')
                    (n_vertical_levels, n_scans, n_spots) = ncfile.variables['t'][:,:,:].shape
                    n_data = n_vertical_levels*n_scans*n_spots
                    print(file_TROPICS.rstrip('\n'))

                    TROPICS_YEAR = np.tile(np.transpose(np.tile(ncfile.variables['Year'][:],   (n_spots, 1))), (n_vertical_levels, 1, 1)).flatten()
                    TROPICS_MNTH = np.tile(np.transpose(np.tile(ncfile.variables['Month'][:],  (n_spots, 1))), (n_vertical_levels, 1, 1)).flatten()
                    TROPICS_DAYS = np.tile(np.transpose(np.tile(ncfile.variables['Day'][:],    (n_spots, 1))), (n_vertical_levels, 1, 1)).flatten()
                    TROPICS_HOUR = np.tile(np.transpose(np.tile(ncfile.variables['Hour'][:],   (n_spots, 1))), (n_vertical_levels, 1, 1)).flatten()
                    TROPICS_MINU = np.tile(np.transpose(np.tile(ncfile.variables['Minute'][:], (n_spots, 1))), (n_vertical_levels, 1, 1)).flatten()
                    TROPICS_SECO = np.tile(np.transpose(np.tile(ncfile.variables['Second'][:], (n_spots, 1))), (n_vertical_levels, 1, 1)).flatten()
                    TROPICS_QHDOP = np.full((n_data), 0, dtype='int')
                    TROPICS_QHDOM = np.full((n_data), 0, dtype='int')
                    TROPICS_CLAT = np.tile(ncfile.variables['losLat_deg'][:,:], (n_vertical_levels, 1, 1)).flatten()
                    TROPICS_Longitude = ncfile.variables['losLon_deg'][:,:]
                    TROPICS_Longitude[TROPICS_Longitude<0] = TROPICS_Longitude[TROPICS_Longitude<0] + 360.0
                    TROPICS_CLON = np.tile(TROPICS_Longitude, (n_vertical_levels, 1, 1)).flatten()
                    TROPICS_PRLC = (ncfile.variables['press'][:,:,:]*100.0).flatten()
                    TROPICS_GP10 = np.full((n_data), 0.0, dtype='float64')
                    TROPICS_QMAT = np.full((n_data), 1, dtype='int')
                    TROPICS_TMDB = ncfile.variables['t'][:,:,:].flatten()
                    TROPICS_QMDD = np.full((n_data), 1, dtype='int')
                    TROPICS_SPFH = ncfile.variables['q'][:,:,:].flatten()/(ncfile.variables['q'][:,:,:].flatten()+1.0)
                    TROPICS_es = 6.112*np.exp((17.67*(TROPICS_TMDB-273.16))/(TROPICS_TMDB-29.65))
                    TROPICS_ws = 0.622*TROPICS_es/(TROPICS_PRLC/100.0)
                    TROPICS_REHU = 100.0*ncfile.variables['q'][:,:,:].flatten()/TROPICS_ws
                    TROPICS_QMWN = np.full((n_data), 2, dtype='int')
                    TROPICS_WDIR = np.full((n_data), 0.0, dtype='float64')
                    TROPICS_WSPD = np.full((n_data), 0.0, dtype='float64')
                    TROPICS_PKWDSP = np.full((n_data), 0.0, dtype='float64')
                    TROPICS_LEVEL = np.transpose(np.tile(range(n_vertical_levels), (n_spots, n_scans, 1))).flatten()

                    #Quality Control
                    Bad_Scan_Flag = np.tile(ncfile.variables['bad_scan_flag'][:,:], (n_vertical_levels, 1, 1)).flatten()
                    Bad_Latlon = np.tile(ncfile.variables['bad_latlon'][:,:], (n_vertical_levels, 1, 1)).flatten()
                    Bad_CalQual_Flag = np.tile(ncfile.variables['bad_calQual_flag'][:,:], (n_vertical_levels, 1, 1)).flatten()
                    Lat_Region = np.tile(ncfile.variables['lat_region'][:,:], (n_vertical_levels, 1, 1)).flatten()
                    Land_Flag = np.tile(ncfile.variables['land_flag'][:,:], (n_vertical_levels, 1, 1)).flatten()
                    Process = np.tile(ncfile.variables['process'][:,:], (n_vertical_levels, 1, 1)).flatten()

                    file_tpw = os.path.join(dir_TROPICS, f"ST{date_st_str}.ET{date_et_str}_TPW.nc")
                    ncfile_tpw = Dataset(file_tpw, 'r')
                    Clear_Sky_Flag = np.tile(ncfile_tpw.variables['clear_sky'][:,:], (n_vertical_levels, 1, 1)).flatten()
                    print(file_tpw)

                    if 'SEA' in version and 'AS' in version:
                        index = (Lat_Region == 1) & (Bad_Scan_Flag == 0) & (Bad_Latlon == 0) & (Land_Flag == 0) & \
                                (TROPICS_LEVEL > 2) & (np.array(TROPICS_TMDB.tolist()) != None) & (np.array(TROPICS_SPFH.tolist()) != None)
                    elif 'SEA' in version and 'CS' in version:
                        index = (Lat_Region == 1) & (Bad_Scan_Flag == 0) & (Bad_Latlon == 0) & (Land_Flag == 0) & (Clear_Sky_Flag < 1) & \
                                (TROPICS_LEVEL > 2) & (np.array(TROPICS_TMDB.tolist()) != None) & (np.array(TROPICS_SPFH.tolist()) != None)

                    ncfile.close()
                    ncfile_tpw.close()

                n_data = sum(index==True)
                print(n_data)
                if n_data > 0:
                    n_total_data += n_data
                    YEAR   += TROPICS_YEAR[index].tolist()
                    MNTH   += TROPICS_MNTH[index].tolist()
                    DAYS   += TROPICS_DAYS[index].tolist()
                    HOUR   += TROPICS_HOUR[index].tolist()
                    MINU   += TROPICS_MINU[index].tolist()
                    SECO   += TROPICS_SECO[index].tolist()
                    QHDOP  += TROPICS_QHDOP[index].tolist()
                    QHDOM  += TROPICS_QHDOM[index].tolist()
                    CLAT   += TROPICS_CLAT[index].tolist()
                    CLON   += TROPICS_CLON[index].tolist()
                    PRLC   += TROPICS_PRLC[index].tolist()
                    GP10   += TROPICS_GP10[index].tolist()
                    QMAT   += TROPICS_QMAT[index].tolist()
                    TMDB   += TROPICS_TMDB[index].tolist()
                    QMDD   += TROPICS_QMDD[index].tolist()
                    SPFH   += TROPICS_SPFH[index].tolist()
                    REHU   += TROPICS_REHU[index].tolist()
                    QMWN   += TROPICS_QMWN[index].tolist()
                    WDIR   += TROPICS_WDIR[index].tolist()
                    WSPD   += TROPICS_WSPD[index].tolist()
                    PKWDSP += TROPICS_PKWDSP[index].tolist()
                    
                    # print('TMDB')
                    # print(len(TMDB))
                    # non_numeric_values = []
                    # non_numeric_values_index = []
                    # for idt, item in enumerate(TMDB):
                    #     if not isinstance(item, (int, float)):
                    #         non_numeric_values.append(item)
                    #         non_numeric_values_index.append(idt)
                    # print('Non-Numeric Values: ', non_numeric_values)
                    # print('Non-Numeric Values Index: ', non_numeric_values_index)
        
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
        np.savetxt(os.path.join(dir_bufr_temp, '0.txt'), [n_total_data])
        print('\n')

def create_TROPICS_bufr(data_library_name, dir_case, case_name, version='V2_SEA_AS'):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_TROPICS = os.path.join(dir_data, f"TROPICS_{version}")
    dir_TROPICS_bufr = os.path.join(dir_TROPICS, 'bufr')
    dir_TROPICS_bufr_temp = os.path.join(dir_TROPICS, 'bufr_temp')
    os.makedirs(dir_TROPICS, exist_ok=True)
    os.makedirs(dir_TROPICS_bufr, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')

        dir_bufr = os.path.join(dir_TROPICS_bufr, anl_end_time_YYYYMMDD)
        file_bufr = os.path.join(dir_bufr, f"gdas.t{anl_end_time_HH}z.tropics.tm00.bufr_d")
        dir_fortran = os.path.join(dir_TROPICS, 'fortran_files')
        file_fortran_bufr = os.path.join(dir_fortran, 'gdas.tropics.bufr')
        os.makedirs(dir_bufr, exist_ok=True)
        os.system(f"rm -rf {file_fortran_bufr}")

        print('Check bufr_temp: ')
        flag = True
        info = os.popen(f"cd {dir_TROPICS_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH} && ls ./*.txt").readlines()
        if len(info) != 22:
            flag = False
        print(len(info))
        print(flag)

        if flag:

            fdata = ''
            with open(f"{dir_fortran}/bufr_encode_tropics.f90", 'r') as f:
                for line in f.readlines():
                    if(line.find('idate = ') == 4): line = f"    idate = {anl_end_time_YYYYMMDD}{anl_end_time_HH}\n"
                    if(line.find('dir_files = ') == 4): line = f"    dir_files = '{dir_TROPICS_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH}/'\n"
                    fdata += line
            f.close()

            with open(f"{dir_fortran}/bufr_encode_tropics.f90", 'w') as f:
                f.writelines(fdata)
            f.close()

            os.popen(f"cd {dir_fortran} && ./run_encode_tropics.sh > log_out")
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

def calculate_TROPICS_tpw(data_library_name, dir_case, case_name, version):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    dir_data = os.path.join(dir_exp, 'data')
    dir_TROPICS_data = os.path.join(dir_data, f"TROPICS_{version}")
    dir_tropics = os.path.join(dir_exp, 'observations', 'tropics')
    os.makedirs(dir_tropics, exist_ok=True)

    time_s = initial_time + timedelta(hours=cycling_interval) - timedelta(hours=cycling_interval/2.0)
    time_e = initial_time + timedelta(hours=cycling_interval*total_da_cycles) + timedelta(hours=cycling_interval/2.0)
    filenames = os.popen(f"ls {dir_TROPICS_data}/TROPICS01*.nc").readlines()

    for file_TROPICS in tqdm(filenames, desc='Files', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        print(file_TROPICS.rstrip('\n'))
        pattern = r'ST(\d{8}-\d{6}).ET(\d{8}-\d{6})'
        pattern_match = re.search(pattern, file_TROPICS)
        date_st_str = pattern_match.group(1)
        date_et_str = pattern_match.group(2)
        date_st = datetime.strptime(date_st_str, '%Y%m%d-%H%M%S')
        date_et = datetime.strptime(date_et_str, '%Y%m%d-%H%M%S')

        if date_st <= time_e and date_et >= time_s:

            file_tpw = os.path.join(dir_TROPICS_data, f"ST{date_st_str}.ET{date_et_str}_TPW.nc")
            ncfile_tpw = Dataset(file_tpw, 'w', format='NETCDF4')

            if 'V1' in version:

                ncfile = netCDF4.Dataset(file_TROPICS.rstrip('\n'), mode='r', format='NETCDF4')
                (n_scans, n_spots, n_vertical_levels) = ncfile.variables['PTemp'][:,:,:].shape

                lat = ncfile.variables['Latitude'][:,:]
                lon = ncfile.variables['Longitude'][:,:]

                mixing_ratio = np.array(ncfile.variables['PVapor'][:,:,:])
                pressure = np.array(np.tile(ncfile.variables['Player'][:], (n_scans, n_spots, 1)))
                temperature = np.array(ncfile.variables['PTemp'][:,:,:])
                specific_humidity = mixing_ratio/(mixing_ratio/1000.0+1.0)
                dewpoint = np.array(dewpoint_from_specific_humidity(pressure*units.hPa, temperature*units.degK, specific_humidity*units('g/kg')))
                tpw = np.zeros((n_scans, n_spots))
                tpw_tropics = ncfile.variables['TPW'][:,:]
                clear_sky = np.zeros((n_scans, n_spots))
                clear_sky_tropics = ncfile.variables['Qc'][:,:,1]

                for idscan in tqdm(range(n_scans), desc='Scans', position=0, leave=True):
                    for idspot in tqdm(range(n_spots), desc='Spots', position=0, leave=True, disable=True):
                        pressure_pw = np.array(pressure[idscan,idspot,:])
                        dewpoint_pw = np.array(dewpoint[idscan,idspot,:])
                        index = (~np.isnan(pressure_pw)) & (~np.isnan(dewpoint_pw))
                        pressure_pw = pressure_pw[index]
                        dewpoint_pw = dewpoint_pw[index]
                        if (len(dewpoint_pw) > 0):
                            tpw[idscan, idspot] = np.array(precipitable_water(pressure_pw*units.hPa, dewpoint_pw*units.degC, bottom=pressure_pw[-1]*units.hPa, top=pressure_pw[0]*units.hPa))

            elif 'V2' in version:

                ncfile = netCDF4.Dataset(file_TROPICS.rstrip('\n'), mode='r', format='NETCDF4')
                (n_vertical_levels, n_scans, n_spots) = ncfile.variables['t'][:,:,:].shape

                lat = ncfile.variables['losLat_deg'][:,:]
                lon = ncfile.variables['losLon_deg'][:,:]

                mixing_ratio = np.array(ncfile.variables['q'][3:,:,:])
                pressure = np.array(ncfile.variables['press'][3:,:,:])
                temperature = np.array(ncfile.variables['t'][3:,:,:])
                specific_humidity = mixing_ratio*1000.0/(mixing_ratio+1.0)
                dewpoint = np.array(dewpoint_from_specific_humidity(pressure*units.hPa, temperature*units.degK, specific_humidity*units('g/kg')))
                tpw = np.zeros((n_scans, n_spots))
                tpw_tropics = np.zeros((n_scans, n_spots))
                clear_sky = np.zeros((n_scans, n_spots))
                clear_sky_tropics = np.zeros((n_scans, n_spots))

                for idscan in tqdm(range(n_scans), desc='Scans', position=0, leave=True):
                    for idspot in tqdm(range(n_spots), desc='Spots', position=0, leave=True, disable=True):
                        pressure_pw = np.array(pressure[:,idscan,idspot])
                        dewpoint_pw = np.array(dewpoint[:,idscan,idspot])
                        index = (~np.isnan(pressure_pw)) & (~np.isnan(dewpoint_pw))
                        pressure_pw = pressure_pw[index]
                        dewpoint_pw = dewpoint_pw[index]
                        if (len(dewpoint_pw) > 0):
                            tpw[idscan, idspot] = np.array(precipitable_water(pressure_pw*units.hPa, dewpoint_pw*units.degC, bottom=pressure_pw[-1]*units.hPa, top=pressure_pw[0]*units.hPa))

            index = tpw >= 55.5
            clear_sky[index] = 1

            ncfile_tpw.createDimension('n_scans',  n_scans)
            ncfile_tpw.createDimension('n_spots',  n_spots)
            ncfile_tpw.createVariable('lat',               'f8', ('n_scans', 'n_spots'))
            ncfile_tpw.createVariable('lon',               'f8', ('n_scans', 'n_spots'))
            ncfile_tpw.createVariable('tpw',               'f8', ('n_scans', 'n_spots'))
            ncfile_tpw.createVariable('tpw_tropics',       'f8', ('n_scans', 'n_spots'))
            ncfile_tpw.createVariable('clear_sky',         'f8', ('n_scans', 'n_spots'))
            ncfile_tpw.createVariable('clear_sky_tropics', 'f8', ('n_scans', 'n_spots'))
            ncfile_tpw.variables['lat'][:,:] = lat
            ncfile_tpw.variables['lon'][:,:] = lon
            ncfile_tpw.variables['tpw'][:,:] = tpw
            ncfile_tpw.variables['tpw_tropics'][:,:] = tpw_tropics
            ncfile_tpw.variables['clear_sky'][:,:] = clear_sky
            ncfile_tpw.variables['clear_sky_tropics'][:,:] = clear_sky_tropics

            ncfile_tpw.close()

def draw_TROPICS_tpw(data_library_names, dir_cases, case_names, versions, ref_exp_names, domains, projections):

    n_cases = len(dir_cases)
    for idc in tqdm(range(n_cases), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        data_library_name = data_library_names[idc]
        dir_case = dir_cases[idc]
        case_name = case_names[idc]
        version = versions[idc]
        ref_exp_name = ref_exp_names[idc]
        domain = domains[idc]
        projection = projections[idc]

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        itime = attributes[(dir_case, case_name)]['itime']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_colormaps = attributes[(dir_case, case_name)]['dir_colormaps']
        dir_ScientificColourMaps7 = os.path.join(dir_colormaps, 'ScientificColourMaps7')
        dir_cycling_da = os.path.join(dir_exp, 'cycling_da')
        dir_tropics = os.path.join(dir_exp, 'observations', 'tropics')
        dir_TROPICS_data = os.path.join(dir_exp, 'data', f"TROPICS_{version}")

        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
        grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

        initial_time = datetime(*itime)
        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(total_da_cycles-1))
        anl_start_time_str = anl_start_time.strftime('%Y%m%d%H%M%S')
        anl_end_time_str = anl_end_time.strftime('%Y%m%d%H%M%S')

        dir_wrfout = os.path.join(dir_cycling_da, f"{case_name}_{ref_exp_name}_C{str(total_da_cycles).zfill(2)}", 'bkg')
        wrfout_format='wrfout_{domain}_{ctime:%Y-%m-%d_%H:%M:00}'
        file_wrfout = '/'.join([dir_wrfout, wrfout_format.format(domain=domain, ctime=initial_time)])
        wrfout = Dataset(file_wrfout)
        wrflat = wrfout.variables['XLAT'][0,:,:]
        wrflon = wrfout.variables['XLONG'][0,:,:]
        extent = [wrflon[0,0], wrflon[-1,-1], wrflat[0,0], wrflat[-1,-1]]
        wrfout.close()

        output_filename = f"tpw_{version}_{domain}"
        output_file = os.path.join(dir_tropics, output_filename+'.png')
        image_files = []

        filenames = os.popen(f"ls {dir_TROPICS_data}/*TPW.nc").readlines()
        for filename in tqdm(filenames, desc="Processing files", position=0, leave=True):

            print(filename.rstrip('\n'))
            pattern = r'ST(\d{8}-\d{6}).ET(\d{8}-\d{6})'
            pattern_match = re.search(pattern, filename)
            date_st_str = pattern_match.group(1)
            date_et_str = pattern_match.group(2)
            date_st = datetime.strptime(date_st_str, '%Y%m%d-%H%M%S')
            date_et = datetime.strptime(date_et_str, '%Y%m%d-%H%M%S')

            ncfile = Dataset(filename.rstrip('\n'), mode='r', format='NETCDF4')
            lat = ncfile.variables['lat'][:,:]
            lon = ncfile.variables['lon'][:,:]
            tpw = ncfile.variables['tpw'][:,:]
            tpw_tropics = ncfile.variables['tpw_tropics'][:,:]
            clear_sky = ncfile.variables['clear_sky'][:,:]
            clear_sky_tropics = ncfile.variables['clear_sky_tropics'][:,:]
            ncfile.close()

            filename = f"ST{date_st_str}_ET{date_et_str}_tpw_{version}_{domain}"
            pdfname = os.path.join(dir_tropics, filename+'.pdf')
            pngname = os.path.join(dir_tropics, filename+'.png')
            image_files.append(pngname)

            fig_width = 2.75*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])
            fig_height = 2.75+0.75
            clb_aspect = 25*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])
            if projection == 'lcc' and domain == 'd01':
                fig_width = 2.75*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])-0.5

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                ax = axs

                if projection == 'cyl':
                    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                                projection=projection, resolution='i', ax=ax)
                elif projection == 'lcc':
                    m = Basemap(llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], \
                                projection=projection, lat_1=lat_1, lat_2=lat_2, lon_0=lon_0, resolution='i', ax=ax)
                    m.drawmeridians(np.arange(-180, 181, 10), labels=[0,0,0,1], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=grayC_cm_data[53])
                    m.drawparallels(np.arange( -90,  91, 10), labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=grayC_cm_data[53])

                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                mlon, mlat = m(lon, lat)
                
                if 'AS' in version:
                    index = (tpw > 0)
                elif 'CS' in version:
                    index = (tpw > 0) & (clear_sky == 0)
                pcm = ax.scatter(mlon[index], mlat[index], c=tpw[index], marker='s', s=2.50, linewidths=0.0, vmin=0, vmax=70, cmap='jet', zorder=0)
                # ax.text(m(extent[1], extent[3])[0], m(extent[1], extent[3])[1], f"{date_st_str}", \
                #             ha='right', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

                if projection == 'cyl':
                    ax.set_xticks(np.arange(-180, 181, 10))
                    ax.set_yticks(np.arange(-90, 91, 10))
                    ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                    ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                    ax.axis(extent)

                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                clb.set_label(r'TPW (kg m$^{-2}$)', fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                clb.ax.minorticks_off()
                clb.set_ticks(range(0, 71, 10))

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


def draw_TROPICS_tpw_cdf(data_library_names, dir_cases, case_names, versions):

    sns_bright_cmap = sns.color_palette('bright')
    
    module = importlib.import_module(f"data_library_{data_library_names[0]}")
    attributes = getattr(module, 'attributes')
    dir_exp = attributes[(dir_cases[0], case_names[0])]['dir_exp']
    dir_tropics = os.path.join(dir_exp, 'observations', 'tropics')
    output_file = os.path.join(dir_tropics, 'tpw_cdf.png')
    image_files = []

    n_cases = len(dir_cases)
    for idc in tqdm(range(n_cases), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        data_library_name = data_library_names[idc]
        dir_case = dir_cases[idc]
        case_name = case_names[idc]
        version = versions[idc]

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_colormaps = attributes[(dir_case, case_name)]['dir_colormaps']
        dir_ScientificColourMaps7 = os.path.join(dir_colormaps, 'ScientificColourMaps7')
        dir_TROPICS_data = os.path.join(dir_exp, 'data', f"TROPICS_{version}")
        dir_tropics = os.path.join(dir_exp, 'observations', 'tropics')

        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
        grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

        filename = f"tpw_cdf_{version}"
        pdfname = os.path.join(dir_tropics, filename+'.pdf')
        pngname = os.path.join(dir_tropics, filename+'.png')
        image_files.append(pngname)

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.0))
            ax = axs
            xmax = 99999999.9

            tpw_all = []
            filenames = os.popen(f"ls {dir_TROPICS_data}/*TPW.nc").readlines()

            for filename in filenames:
                with netCDF4.Dataset(filename.rstrip('\n'), mode='r', format='NETCDF4') as ncfile:
                    if 'AS' in version:
                        tpw = ncfile.variables['tpw'][:,:].flatten()
                        index = (tpw > 0.0) & (np.array(tpw.tolist()) != None)
                    elif 'CS' in version:
                        tpw = ncfile.variables['tpw'][:,:].flatten()
                        clear_sky = ncfile.variables['clear_sky'][:,:].flatten()
                        index = (tpw > 0.0) & (np.array(tpw.tolist()) != None) & (clear_sky == 0)

                tpw = tpw[index]
                tpw_all.extend(tpw.tolist())

            tpw_all = np.sort(tpw_all)
            percentile_90 = np.percentile(tpw_all, 90)
            cdf = np.arange(1, len(tpw_all) + 1)/len(tpw_all)
            print(f"90th percentile of {version} is: {percentile_90:.2f}")

            specific_value = 55.5
            percentage = np.sum(tpw_all > specific_value)/len(tpw_all)*100
            print(f"Percentage of values over {specific_value} in {version}: {percentage:.2f}%")
            print(len(tpw_all))

            xmax = np.min([xmax, np.max(tpw)])
            print(xmax)
            ax.plot(tpw_all, cdf, color=sns_bright_cmap[0], ls='-', ms=2.00, linewidth=1.25, label=version, zorder=3)

            ax.plot([55.5, 55.5], [0.0, 0.9], color='k', ls='-', ms=2.00, linewidth=1.25, zorder=3)
            ax.plot([ 0.0, 55.5], [0.9, 0.9], color='k', ls='-', ms=2.00, linewidth=1.25, zorder=3)
            ax.set_xlabel(r'TPW (kg m$^{-2}$)', fontsize=10.0)
            ax.set_ylabel('Cumulative Probability', fontsize=10.0)
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.axis([0, 70, 0, 1.2])
            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
            ax.legend(loc='best', fontsize=5.0, handlelength=2.5).set_zorder(102)

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
