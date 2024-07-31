import re
import os
import glob
import time
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

def create_CYGNSS_bufr_temp(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_CYGNSS = os.path.join(dir_data, 'CYGNSS')
    dir_CYGNSS_bufr_temp = os.path.join(dir_CYGNSS, 'bufr_temp')
    os.makedirs(dir_CYGNSS, exist_ok=True)
    os.makedirs(dir_CYGNSS_bufr_temp, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        time_s = anl_end_time - timedelta(hours=cycling_interval/2.0)
        time_e = anl_end_time + timedelta(hours=cycling_interval/2.0)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')
        print(anl_end_time)

        dir_bufr_temp = os.path.join(dir_CYGNSS_bufr_temp, anl_end_time_YYYYMMDD)
        os.makedirs(dir_bufr_temp, exist_ok=True)
        dir_bufr_temp = os.path.join(dir_bufr_temp, anl_end_time_HH)
        os.system(f"rm -rf {dir_bufr_temp}")
        os.makedirs(dir_bufr_temp, exist_ok=True)
        filenames = os.popen(f"ls {dir_CYGNSS}/cyg*l2*.nc").readlines()
        n_total_data = 0

        SID  = []
        XOB  = []
        YOB  = []
        DHR  = []
        TYP  = []
        ELV  = []
        SAID = []
        T29  = []
        POB  = []
        QOB  = []
        TOB  = []
        ZOB  = []
        UOB  = []
        VOB  = []
        PWO  = []
        CAT  = []
        PRSS = []
        PQM  = []
        QQM  = []
        TQM  = []
        ZQM  = []
        WQM  = []
        NUL1 = []
        PWQ  = []
        POE  = []
        QOE  = []
        TOE  = []
        NUL2 = []
        WOE  = []
        NUL3 = []
        PWE  = []

        for file_CYGNSS in filenames:

            pattern = r's(\d{8}-\d{6})-e(\d{8}-\d{6})'
            pattern_match = re.search(pattern, file_CYGNSS)
            date_st_str = pattern_match.group(1)
            date_et_str = pattern_match.group(2)
            date_st = datetime.strptime(date_st_str, '%Y%m%d-%H%M%S')
            date_et = datetime.strptime(date_et_str, '%Y%m%d-%H%M%S')

            if date_st <= time_e and date_et >= time_s:

                ncfile = netCDF4.Dataset(file_CYGNSS.rstrip('\n'), mode='r', format='NETCDF4')
                n_data = len(list(ncfile.variables['sample_time'][:]))
                print(file_CYGNSS.rstrip('\n'))

                CYGNSS_SID  = np.full((n_data), 48112, dtype='float')
                CYGNSS_XOB  = ncfile.variables['lon'][:]
                CYGNSS_YOB  = ncfile.variables['lat'][:]
                CYGNSS_TYP  = np.full((n_data), 283, dtype='float')
                CYGNSS_ELV  = np.full((n_data), 0.0, dtype='float')
                CYGNSS_SAID = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_T29  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_POB  = np.full((n_data), 1013.0, dtype='float')
                CYGNSS_QOB  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_TOB  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_ZOB  = np.full((n_data), 0.0, dtype='float')
                CYGNSS_UOB  = ncfile.variables['wind_speed'][:]
                CYGNSS_VOB  = np.full((n_data), 0.0, dtype='float')
                CYGNSS_PWO  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_CAT  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_PRSS = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_PQM  = np.full((n_data), 2, dtype='float')
                CYGNSS_QQM  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_TQM  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_ZQM  = np.full((n_data), 2, dtype='float')
                CYGNSS_WQM  = np.full((n_data), 1, dtype='float')
                CYGNSS_NUL1 = np.full((n_data), 1, dtype='float')
                CYGNSS_PWQ  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_POE  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_QOE  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_TOE  = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_NUL2 = np.full((n_data), 10.0e10, dtype='float')
                CYGNSS_WOE  = np.full((n_data), 2.2, dtype='float')
                CYGNSS_NUL3 = np.full((n_data), 2.2, dtype='float')
                CYGNSS_PWE  = np.full((n_data), 10.0e10, dtype='float')

                CYGNSS_TIME = ncfile.variables['sample_time'][:]
                CYGNSS_DHR = np.full((n_data), 0.0, dtype='float64')
                for idt, cyg_time in enumerate(CYGNSS_TIME):
                    CYGNSS_DHR[idt] = (date_st + timedelta(seconds=cyg_time) - anl_end_time).total_seconds()/3600.0

                index = (CYGNSS_DHR >= -1.0*cycling_interval/2.0) & (CYGNSS_DHR <= cycling_interval/2.0) & \
                        (np.array(CYGNSS_XOB.tolist()) != None) & (np.array(CYGNSS_UOB.tolist()) != None)

                n_data = sum(index==True)
                print(n_data)
                if n_data > 0:
                    n_total_data += n_data
                    SID  += CYGNSS_SID[index].tolist()
                    XOB  += CYGNSS_XOB[index].tolist()
                    YOB  += CYGNSS_YOB[index].tolist()
                    DHR  += CYGNSS_DHR[index].tolist()
                    TYP  += CYGNSS_TYP[index].tolist()
                    ELV  += CYGNSS_ELV[index].tolist()
                    SAID += CYGNSS_SAID[index].tolist()
                    T29  += CYGNSS_T29[index].tolist()
                    POB  += CYGNSS_POB[index].tolist()
                    QOB  += CYGNSS_QOB[index].tolist()
                    TOB  += CYGNSS_TOB[index].tolist()
                    ZOB  += CYGNSS_ZOB[index].tolist()
                    UOB  += CYGNSS_UOB[index].tolist()
                    VOB  += CYGNSS_VOB[index].tolist()
                    PWO  += CYGNSS_PWO[index].tolist()
                    CAT  += CYGNSS_CAT[index].tolist()
                    PRSS += CYGNSS_PRSS[index].tolist()
                    PQM  += CYGNSS_PQM[index].tolist()
                    QQM  += CYGNSS_QQM[index].tolist()
                    TQM  += CYGNSS_TQM[index].tolist()
                    ZQM  += CYGNSS_ZQM[index].tolist()
                    WQM  += CYGNSS_WQM[index].tolist()
                    NUL1 += CYGNSS_NUL1[index].tolist()
                    PWQ  += CYGNSS_PWQ[index].tolist()
                    POE  += CYGNSS_POE[index].tolist()
                    QOE  += CYGNSS_QOE[index].tolist()
                    TOE  += CYGNSS_TOE[index].tolist()
                    NUL2 += CYGNSS_NUL2[index].tolist()
                    WOE  += CYGNSS_WOE[index].tolist()
                    NUL3 += CYGNSS_NUL3[index].tolist()
                    PWE  += CYGNSS_PWE[index].tolist()

        with open(os.path.join(dir_bufr_temp, '1.txt'), 'ab') as f:
            np.savetxt(f, SID)
        with open(os.path.join(dir_bufr_temp, '2.txt'), 'ab') as f:
            np.savetxt(f, XOB)
        with open(os.path.join(dir_bufr_temp, '3.txt'), 'ab') as f:
            np.savetxt(f, YOB)
        with open(os.path.join(dir_bufr_temp, '4.txt'), 'ab') as f:
            np.savetxt(f, DHR)
        with open(os.path.join(dir_bufr_temp, '5.txt'), 'ab') as f:
            np.savetxt(f, TYP)
        with open(os.path.join(dir_bufr_temp, '6.txt'), 'ab') as f:
            np.savetxt(f, ELV)
        with open(os.path.join(dir_bufr_temp, '7.txt'), 'ab') as f:
            np.savetxt(f, SAID)
        with open(os.path.join(dir_bufr_temp, '8.txt'), 'ab') as f:
            np.savetxt(f, T29)
        with open(os.path.join(dir_bufr_temp, '9.txt'), 'ab') as f:
            np.savetxt(f, POB)
        with open(os.path.join(dir_bufr_temp, '10.txt'), 'ab') as f:
            np.savetxt(f, QOB)
        with open(os.path.join(dir_bufr_temp, '11.txt'), 'ab') as f:
            np.savetxt(f, TOB)
        with open(os.path.join(dir_bufr_temp, '12.txt'), 'ab') as f:
            np.savetxt(f, ZOB)
        with open(os.path.join(dir_bufr_temp, '13.txt'), 'ab') as f:
            np.savetxt(f, UOB)
        with open(os.path.join(dir_bufr_temp, '14.txt'), 'ab') as f:
            np.savetxt(f, VOB)
        with open(os.path.join(dir_bufr_temp, '15.txt'), 'ab') as f:
            np.savetxt(f, PWO)
        with open(os.path.join(dir_bufr_temp, '16.txt'), 'ab') as f:
            np.savetxt(f, CAT)
        with open(os.path.join(dir_bufr_temp, '17.txt'), 'ab') as f:
            np.savetxt(f, PRSS)
        with open(os.path.join(dir_bufr_temp, '18.txt'), 'ab') as f:
            np.savetxt(f, PQM)
        with open(os.path.join(dir_bufr_temp, '19.txt'), 'ab') as f:
            np.savetxt(f, QQM)
        with open(os.path.join(dir_bufr_temp, '20.txt'), 'ab') as f:
            np.savetxt(f, TQM)
        with open(os.path.join(dir_bufr_temp, '21.txt'), 'ab') as f:
            np.savetxt(f, ZQM)
        with open(os.path.join(dir_bufr_temp, '22.txt'), 'ab') as f:
            np.savetxt(f, WQM)
        with open(os.path.join(dir_bufr_temp, '23.txt'), 'ab') as f:
            np.savetxt(f, NUL1)
        with open(os.path.join(dir_bufr_temp, '24.txt'), 'ab') as f:
            np.savetxt(f, PWQ)
        with open(os.path.join(dir_bufr_temp, '25.txt'), 'ab') as f:
            np.savetxt(f, POE)
        with open(os.path.join(dir_bufr_temp, '26.txt'), 'ab') as f:
            np.savetxt(f, QOE)
        with open(os.path.join(dir_bufr_temp, '27.txt'), 'ab') as f:
            np.savetxt(f, TOE)
        with open(os.path.join(dir_bufr_temp, '28.txt'), 'ab') as f:
            np.savetxt(f, NUL2)
        with open(os.path.join(dir_bufr_temp, '29.txt'), 'ab') as f:
            np.savetxt(f, WOE)
        with open(os.path.join(dir_bufr_temp, '30.txt'), 'ab') as f:
            np.savetxt(f, NUL3)
        with open(os.path.join(dir_bufr_temp, '31.txt'), 'ab') as f:
            np.savetxt(f, PWE)

        np.savetxt(os.path.join(dir_bufr_temp, '0.txt'), [n_total_data])
        print('\n')

def create_CYGNSS_bufr(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_CYGNSS = os.path.join(dir_data, 'CYGNSS')
    dir_CYGNSS_bufr = os.path.join(dir_CYGNSS, 'bufr')
    dir_CYGNSS_bufr_temp = os.path.join(dir_CYGNSS, 'bufr_temp')
    os.makedirs(dir_CYGNSS, exist_ok=True)
    os.makedirs(dir_CYGNSS_bufr, exist_ok=True)

    for idc in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        anl_end_time = initial_time + timedelta(hours=cycling_interval*idc)
        anl_end_time_YYYYMMDD = anl_end_time.strftime('%Y%m%d')
        anl_end_time_HH = anl_end_time.strftime('%H')

        dir_bufr = os.path.join(dir_CYGNSS_bufr, anl_end_time_YYYYMMDD)
        file_bufr = os.path.join(dir_bufr, f"gdas.t{anl_end_time_HH}z.cygnss.tm00.bufr_d")
        dir_fortran = os.path.join(dir_CYGNSS, 'fortran_files')
        file_fortran_bufr = os.path.join(dir_fortran, 'gdas.cygnss.bufr')
        os.makedirs(dir_bufr, exist_ok=True)
        os.system(f"rm -rf {file_fortran_bufr}")

        print('Check bufr_temp: ')
        flag = True
        info = os.popen(f"cd {dir_CYGNSS_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH} && ls ./*.txt").readlines()
        if len(info) != 32:
            flag = False
        print(len(info))
        print(flag)

        if flag:

            fdata = ''
            with open(f"{dir_fortran}/prepbufr_encode_CYGNSS.f90", 'r') as f:
                for line in f.readlines():
                    if(line.find('idate = ') == 4): line = f"    idate = {anl_end_time_YYYYMMDD}{anl_end_time_HH}\n"
                    if(line.find('dir_files = ') == 4): line = f"    dir_files = '{dir_CYGNSS_bufr_temp}/{anl_end_time_YYYYMMDD}/{anl_end_time_HH}/'\n"
                    fdata += line
            f.close()

            with open(f"{dir_fortran}/prepbufr_encode_CYGNSS.f90", 'w') as f:
                f.writelines(fdata)
            f.close()

            os.popen(f"cd {dir_fortran} && ./run_prepbufr_encode_CYGNSS.sh > log_out")
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

def draw_CYGNSS_wind_speed(data_library_names, dir_cases, case_names, cygnss_exp_name):

    sns_bright_cmap = sns.color_palette('bright')

    n_cases = len(dir_cases)
    for idc in tqdm(range(n_cases), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        (data_library_name, dir_case, case_name) = (data_library_names[idc], dir_cases[idc], case_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        itime = attributes[(dir_case, case_name)]['itime']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        time_window_max = attributes[(dir_case, case_name)]['time_window_max']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        dir_cygnss = '/'.join([attributes[(dir_case, case_name)]['dir_cygnss'], case_name])
        dir_wrfout = '/'.join([dir_exp, 'cycling_da', f"{case_name}_{cygnss_exp_name}_C{str(total_da_cycles).zfill(2)}", 'bkg'])
        dir_save = '/'.join([dir_exp, 'draw_Tropics', 'cygnss'])
        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
        grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

        initial_time = datetime(*itime)
        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(total_da_cycles-1))
        anl_start_time_str = anl_start_time.strftime('%Y%m%d%H%M%S')
        anl_end_time_str = anl_end_time.strftime('%Y%m%d%H%M%S')

        wrfout_format = 'wrfout_d01_{ctime:%Y-%m-%d_%H:%M:00}'
        file_wrfout_d01 = '/'.join([dir_wrfout, wrfout_format.format(ctime=initial_time)])

        wrfout_d01 = Dataset(file_wrfout_d01)
        lat_d01 = wrfout_d01.variables['XLAT'][0,:,:]
        lon_d01 = wrfout_d01.variables['XLONG'][0,:,:]
        extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
        wrfout_d01.close()

        filenames = os.popen('cd ' + dir_cygnss + ' && ls cyg.ddmi*l2*').readlines()

        image_files = []
        output_file = f'{dir_save}/{anl_start_time_str}_{anl_end_time_str}_cygnss_wind_speed_d01.png'
        for da_cycle in tqdm(range(0, total_da_cycles), desc='Cycles', leave=False, unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

            time_now = anl_start_time + timedelta(hours=cycling_interval*da_cycle)

            da_window_ST = time_now - timedelta(hours=time_window_max)
            da_window_ET = time_now + timedelta(hours=time_window_max)
            da_window_ST_str = da_window_ST.strftime('%Y%m%d%H%M%S')
            da_window_ET_str = da_window_ET.strftime('%Y%m%d%H%M%S')

            pdfname = f'{dir_save}/{da_window_ST_str}_{da_window_ET_str}_cygnss_wind_speed_d01.pdf'
            pngname = f'{dir_save}/{da_window_ST_str}_{da_window_ET_str}_cygnss_wind_speed_d01.png'
            image_files.append(pngname)

            cygnss_lon = []
            cygnss_lat = []
            cygnss_wind_speed = []

            for filename in filenames:

                filename = filename.strip('\n')
                date_st_str = filename[10:25]
                date_et_str = filename[27:42]
                time_ST = datetime.strptime(date_st_str, '%Y%m%d-%H%M%S')
                time_ET = datetime.strptime(date_et_str, '%Y%m%d-%H%M%S')
                da_window_ST_seconds = (da_window_ST-time_ST).total_seconds()
                da_window_ET_seconds = (da_window_ET-time_ST).total_seconds()

                if time_ST <= da_window_ET and time_ET >= da_window_ST:

                    filename = '/'.join([dir_cygnss, filename])
                    nc_fid = Dataset(filename, mode='r', format='NETCDF4')
                    cygnss_time = nc_fid.variables['sample_time'][:]
                    lat = nc_fid.variables['lat'][:]
                    lon = nc_fid.variables['lon'][:]
                    lon[lon>180.0] = lon[lon>180.0]-360.0
                    wind_speed = nc_fid.variables['wind_speed'][:]
                    wind_speed_uncertainty = nc_fid.variables['wind_speed_uncertainty'][:]
                    nc_fid.close()

                    nan_mask = np.isnan(cygnss_time) | np.isnan(lat) | np.isnan(lon) | np.isnan(wind_speed)
                    non_nan_mask = ~nan_mask
                    cygnss_time = cygnss_time[non_nan_mask]
                    lat = lat[non_nan_mask]
                    lon = lon[non_nan_mask]
                    wind_speed = wind_speed[non_nan_mask]

                    index = (cygnss_time >= da_window_ST_seconds) & (cygnss_time <= da_window_ET_seconds)
                    cygnss_lon.extend(lon[index])
                    cygnss_lat.extend(lat[index])
                    cygnss_wind_speed.extend(wind_speed[index])

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                mlons, mlats = m(cygnss_lon, cygnss_lat)
                pcm = ax.scatter(mlons, mlats, marker='s', s=2.50, linewidths=0.0, c=cygnss_wind_speed, vmin=0, vmax=18, cmap='jet', zorder=0)

                ax.set_xticks(np.arange(-180, 181, 10))
                ax.set_yticks(np.arange(-90, 91, 10))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                lb_title = 'Wind Speed (m/s) for C' + str(da_cycle+1).zfill(2)
                clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(0, 19, 3), orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
                clb.set_label(lb_title, fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                plt.tight_layout()
                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

        combine_images_grid(image_files, output_file)
        command = f"convert {output_file} -trim {output_file}"
        subprocess.run(command, shell=True)
        image = IPImage(filename=output_file)
        display(image)
