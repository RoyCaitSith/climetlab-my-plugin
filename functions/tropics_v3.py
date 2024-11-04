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

def create_tropics_bufr_temp(dir_data, case, anl_start_time, anl_end_time, cycling_interval, version):

    total_hours = (anl_end_time-anl_start_time).total_seconds()/3600
    total_da_cycles = int(total_hours/cycling_interval+1)

    dir_tropics = os.path.join(dir_data, 'TROPICS', case, 'TROPICS_V3')
    dir_tropics_bufr_temp = os.path.join(dir_tropics, 'bufr_temp')
    dir_tropics_bufr_temp_version = os.path.join(dir_tropics_bufr_temp, version)
    os.makedirs(dir_tropics_bufr_temp, exist_ok=True)
    os.makedirs(dir_tropics_bufr_temp_version, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_now_time = anl_start_time + timedelta(hours=cycling_interval*(idc-1))
        time_s = anl_start_time - timedelta(hours=cycling_interval/2.0)
        time_e = anl_start_time + timedelta(hours=cycling_interval/2.0)
        anl_now_time_YYYYMMDD = anl_now_time.strftime('%Y%m%d')
        anl_now_time_HH = anl_now_time.strftime('%H')
        print(anl_now_time)

        dir_bufr_temp_YYYYMMDD = os.path.join(dir_tropics_bufr_temp_version, anl_now_time_YYYYMMDD)
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
        QHDOP  = []
        QHDOM  = []
        CLAT   = []
        CLON   = []
        PRLC   = []
        GP10   = []
        QMAT   = []
        TMDB   = []
        QMDD   = []
        SPFH   = []
        REHU   = []
        QMWN   = []
        WDIR   = []
        WSPD   = []
        PKWDSP = []

        filenames = os.popen(f"ls {dir_tropics}/TROPICS03*.nc").readlines()
        for file_tropics in filenames:
                            
            pattern = r'ST(\d{8}-\d{6}).ET(\d{8}-\d{6})'
            pattern_match = re.search(pattern, file_tropics)
            date_st_str = pattern_match.group(1)
            date_et_str = pattern_match.group(2)
            date_st = datetime.strptime(date_st_str, '%Y%m%d-%H%M%S')
            date_et = datetime.strptime(date_et_str, '%Y%m%d-%H%M%S')

            if date_st <= time_e and date_et >= time_s:
                
                print(file_tropics.rstrip('\n'))
                ncfile = netCDF4.Dataset(file_tropics.rstrip('\n'), mode='r', format='NETCDF4')
                uradl2a = ncfile.groups['URADL2A']
                geos_fc = ncfile.groups['GEOS_FC']
                nnavp = ncfile.groups['NNAVP']
                nnavp_profiles = nnavp.groups['profiles']
                nnavp_surface = nnavp.groups['surface']
                nnavp_masks = nnavp.groups['masks']

                # Extract dimensions
                (n_bands, n_scans, n_spots) = uradl2a.variables['latitude'][:,:,:].shape
                (n_channels, n_scans, n_spots) = uradl2a.variables['brightness_temperature'][:,:,:].shape
                (n_vertical_levels, n_scans, n_spots) = nnavp_profiles.variables['t'][:,:,:].shape
                n_data = n_vertical_levels*n_scans*n_spots

                TROPICS_TIME = uradl2a.variables['time'][:,:]
                # TROPICS_TIME = np.tile(TROPICS_TIME, (n_vertical_levels, 1, 1)).flatten()
                # TROPICS_DATE = num2date(TROPICS_TIME, units='seconds since 2000-01-01 00:00:00')
                # TROPICS_YEAR = np.array([date.year for date in TROPICS_DATE])
                # TROPICS_MNTH = np.array([date.month for date in TROPICS_DATE])
                # TROPICS_DAYS = np.array([date.day for date in TROPICS_DATE])
                # TROPICS_HOUR = np.array([date.hour for date in TROPICS_DATE])
                # TROPICS_MINU = np.array([date.minute for date in TROPICS_DATE])
                # TROPICS_SECO = np.array([date.second for date in TROPICS_DATE])
                # Quality for observed position
                TROPICS_QHDOP = np.full((n_data), 0, dtype='int')
                # Quality for observed meteorological parameters
                TROPICS_QHDOM = np.full((n_data), 0, dtype='int')
                # Latitude (coarse accuracy)
                TROPICS_CLAT = np.tile(uradl2a.variables['latitude'][0,:,:], (n_vertical_levels, 1, 1)).flatten()
                # Longitude (coarse accuracy)
                TROPICS_CLON = np.tile(uradl2a.variables['longitude'][0,:,:], (n_vertical_levels, 1, 1)).flatten()
                TROPICS_CLON[TROPICS_CLON<0] = TROPICS_CLON[TROPICS_CLON<0] + 360.0
                # Pressure (Pa)
                TROPICS_PRLC = nnavp_profiles.variables['press'][:,:,:].flatten()
                TROPICS_PRLC = 100.0*TROPICS_PRLC
                # Geopotential (m2s-2)
                TROPICS_GP10 = np.full((n_data), 0.0, dtype='float64')
                # SDMEDIT/QUIPS quality mark for air temperature
                TROPICS_QMAT = np.full((n_data), 1, dtype='int')
                # Temperature/air temperature (K)
                TROPICS_TMDB = nnavp_profiles.variables['t'][:,:,:].flatten()
                # SDMEDIT/QUIPS quality mark for moisture
                TROPICS_QMDD = np.full((n_data), 1, dtype='int')
                # Specific humidity (kgkg-1)
                TROPICS_SPFH = nnavp_profiles.variables['q'][:,:,:].flatten()
                # Calculate relative humidity
                TROPICS_REHU = []
                for (pressure, t, sh) in zip(TROPICS_PRLC, TROPICS_TMDB, TROPICS_SPFH):
                    if np.array(pressure.tolist()) == None and np.array(t.tolist()) == None and np.array(sh.tolist()) == None:
                        TROPICS_REHU += [666666]
                    else:
                        print(relative_humidity_from_specific_humidity(pressure*units.hPa, t*units.K, sh).to('percent'))
                        TROPICS_REHU += [relative_humidity_from_specific_humidity(pressure*units.hPa, t*units.K, sh).to('percent')]
                        print(TROPICS_REHU)
                        print(miao)

                TROPICS_ES = 6.112*np.exp((17.67*(TROPICS_TMDB-273.16))/(TROPICS_TMDB-29.65))
                TROPICS_E = (specific_humidity*pressure)/(0.622+(specific_humidity*(1-0.622)))
                TROPICS_ws = 0.622*TROPICS_ES/(TROPICS_PRLC/100.0)
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
                TPW = np.tile(ncfile_tpw.variables['tpw'][:,:], (n_vertical_levels, 1, 1)).flatten()
                Clear_Sky_Flag = np.tile(ncfile_tpw.variables['clear_sky'][:,:], (n_vertical_levels, 1, 1)).flatten()
                print(file_tpw)

                TROPICS_CLAT = np.array(TROPICS_CLAT.tolist())
                TROPICS_CLAT[np.array(TROPICS_CLAT.tolist()) == None] = 666666.0

                if 'AS' in version:
                    index = (Lat_Region == 1) & (Bad_Scan_Flag == 0) & (Bad_Latlon == 0) & (Land_Flag == 0) & \
                            (Bad_Qual_Flag < 2) & (TROPICS_CLAT <= 40.0) & (TROPICS_CLAT >= -40.0) & \
                            (TROPICS_CLAT <= 40.0) & (TROPICS_CLAT >= -40.0) & (TROPICS_LEVEL > 2) & \
                            (np.array(TROPICS_TMDB.tolist()) != None) & (np.array(TROPICS_SPFH.tolist()) != None)
                elif 'CS' in version:
                    index = (Lat_Region == 1) & (Bad_Scan_Flag == 0) & (Bad_Latlon == 0) & (Land_Flag == 0) & (Clear_Sky_Flag < 1) & \
                            (Lat_Region == 1) & (Bad_Scan_Flag == 0) & (Bad_Latlon == 0) & (TPW >= 0) & (TPW <= 56.5) & \
                            (TROPICS_CLAT <= 40.0) & (TROPICS_CLAT >= -40.0) & (TROPICS_LEVEL > 2) & \
                            (Bad_Qual_Flag < 2) & (Clear_Sky_Flag < 1) & (TROPICS_CLAT <= 40.0) & (TROPICS_CLAT >= -40.0) & \
                            (TPW >= 0.0) & (TPW <= 56.5) & \
                            (np.array(TROPICS_TMDB.tolist()) != None) & (np.array(TROPICS_SPFH.tolist()) != None)

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
            np.savetxt(f, QHDOP)
        with open(os.path.join(dir_bufr_temp_HH,  '8.txt'), 'ab') as f:
            np.savetxt(f, QHDOM)
        with open(os.path.join(dir_bufr_temp_HH,  '9.txt'), 'ab') as f:
            np.savetxt(f, CLAT)
        with open(os.path.join(dir_bufr_temp_HH, '10.txt'), 'ab') as f:
            np.savetxt(f, CLON)
        with open(os.path.join(dir_bufr_temp_HH, '11.txt'), 'ab') as f:
            np.savetxt(f, PRLC)
        with open(os.path.join(dir_bufr_temp_HH, '12.txt'), 'ab') as f:
            np.savetxt(f, GP10)
        with open(os.path.join(dir_bufr_temp_HH, '13.txt'), 'ab') as f:
            np.savetxt(f, QMAT)
        with open(os.path.join(dir_bufr_temp_HH, '14.txt'), 'ab') as f:
            np.savetxt(f, TMDB)
        with open(os.path.join(dir_bufr_temp_HH, '15.txt'), 'ab') as f:
            np.savetxt(f, QMDD)
        with open(os.path.join(dir_bufr_temp_HH, '16.txt'), 'ab') as f:
            np.savetxt(f, SPFH)
        with open(os.path.join(dir_bufr_temp_HH, '17.txt'), 'ab') as f:
            np.savetxt(f, REHU)
        with open(os.path.join(dir_bufr_temp_HH, '18.txt'), 'ab') as f:
            np.savetxt(f, QMWN)
        with open(os.path.join(dir_bufr_temp_HH, '19.txt'), 'ab') as f:
            np.savetxt(f, WDIR)
        with open(os.path.join(dir_bufr_temp_HH, '20.txt'), 'ab') as f:
            np.savetxt(f, WSPD)
        with open(os.path.join(dir_bufr_temp_HH, '21.txt'), 'ab') as f:
            np.savetxt(f, PKWDSP)
        np.savetxt(os.path.join(dir_bufr_temp_HH, '0.txt'), [n_total_data])
        print('\n')