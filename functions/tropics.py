import os
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

def create_DAWN_bufr_temp(data_library_name, dir_case, case_name, version):

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

def draw_TROPICS_tpw(data_library_names, dir_cases, case_names, cygnss_exp_name):

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
        product = attributes[(dir_case, case_name)]['product']
        dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        dir_wrfout = '/'.join([dir_exp, 'cycling_da', f"{case_name}_{cygnss_exp_name}_C{str(total_da_cycles).zfill(2)}", 'bkg'])
        dir_save = '/'.join([dir_exp, 'draw_Tropics', 'total_precipitable_water'])
        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
        grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

        initial_time = datetime(*itime)
        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(total_da_cycles-1))
        anl_start_time_str = anl_start_time.strftime('%Y%m%d%H%M%S')
        anl_end_time_str = anl_end_time.strftime('%Y%m%d%H%M%S')

        wrfout_format='wrfout_d01_{ctime:%Y-%m-%d_%H:%M:00}'
        file_wrfout_d01 = '/'.join([dir_wrfout, wrfout_format.format(ctime=initial_time)])

        wrfout_d01 = Dataset(file_wrfout_d01)
        lat_d01 = wrfout_d01.variables['XLAT'][0,:,:]
        lon_d01 = wrfout_d01.variables['XLONG'][0,:,:]
        extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
        wrfout_d01.close()

        if 'TROPICS V1' in product: output_file = f'{dir_save}/{anl_start_time_str}_{anl_end_time_str}_tropics_v1_tpw_d01.png'
        if 'TROPICS V3' in product: output_file = f'{dir_save}/{anl_start_time_str}_{anl_end_time_str}_tropics_v3_tpw_d01.png'

        image_files = []
        filenames = os.popen('cd ' + dir_save + ' && ls *total_precipitable_water.nc').readlines()
        for filename in tqdm(filenames, desc='Cycles', leave=False, unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

            filename = filename.strip('\n')
            time_ST_str = filename[ 0:14]
            time_ET_str = filename[15:29]
            time_ST = datetime.strptime(time_ST_str, '%Y%m%d%H%M%S')
            time_ET = datetime.strptime(time_ET_str, '%Y%m%d%H%M%S')

            filename = '/'.join([dir_save, filename])
            nc_fid = Dataset(filename, mode='r', format='NETCDF4')
            lat = nc_fid.variables['lat'][:]
            lon = nc_fid.variables['lon'][:]
            total_precipitable_water = nc_fid.variables['total_precipitable_water'][:]
            nc_fid.close()

            if 'TROPICS V1' in product:
                pdfname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v1_tpw_all_sky_d01.pdf'
                pngname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v1_tpw_all_sky_d01.png'
            if 'TROPICS V3' in product:
                pdfname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v3_tpw_all_sky_d01.pdf'
                pngname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v3_tpw_all_sky_d01.png'

            image_files.append(pngname)
            index = (total_precipitable_water >= 0.0)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                mlons, mlats = m(lon, lat)
                pcm = ax.scatter(mlons[index], mlats[index], marker='s', s=2.50, linewidths=0.0, c=total_precipitable_water[index], vmin=40, vmax=70, cmap='jet', zorder=0)

                ax.set_xticks(np.arange(-180, 181, 10))
                ax.set_yticks(np.arange(-90, 91, 10))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                lb_title = r'TPW (kg m$^{-2}$) in AS'
                clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(40, 71, 5), orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
                clb.set_label(lb_title, fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                plt.tight_layout()
                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

            if 'TROPICS V1' in product:
                pdfname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v1_tpw_clear_sky_d01.pdf'
                pngname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v1_tpw_clear_sky_d01.png'
            if 'TROPICS V3' in product:
                pdfname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v3_tpw_clear_sky_d01.pdf'
                pngname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v3_tpw_clear_sky_d01.png'

            image_files.append(pngname)
            index = (total_precipitable_water >= 0.0) & (total_precipitable_water <= 56.5)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                mlons, mlats = m(lon, lat)
                pcm = ax.scatter(mlons[index], mlats[index], marker='s', s=2.50, linewidths=0.0, c=total_precipitable_water[index], vmin=40, vmax=70, cmap='jet', zorder=0)

                ax.set_xticks(np.arange(-180, 181, 10))
                ax.set_yticks(np.arange(-90, 91, 10))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                lb_title = r'TPW (kg m$^{-2}$) in CS'
                clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(40, 71, 5), orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
                clb.set_label(lb_title, fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

                plt.tight_layout()
                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

            if 'TROPICS V1' in product:
                pdfname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v1_tpw_cloudy_sky_d01.pdf'
                pngname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v1_tpw_cloudy_sky_d01.png'
            if 'TROPICS V3' in product:
                pdfname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v3_tpw_cloudy_sky_d01.pdf'
                pngname = f'{dir_save}/{time_ST_str}_{time_ET_str}_tropics_v3_tpw_cloudy_sky_d01.png'

            image_files.append(pngname)
            index = (total_precipitable_water >= 56.5)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                mlons, mlats = m(lon, lat)
                pcm = ax.scatter(mlons[index], mlats[index], marker='s', s=2.50, linewidths=0.0, c=total_precipitable_water[index], vmin=40, vmax=70, cmap='jet', zorder=0)

                ax.set_xticks(np.arange(-180, 181, 10))
                ax.set_yticks(np.arange(-90, 91, 10))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                lb_title = r'TPW (kg m$^{-2}$) in CS'
                clb = fig.colorbar(pcm, ax=ax, ticks=np.arange(40, 71, 5), orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
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

def draw_TROPICS_tpw_cdf(data_library_names, dir_cases, case_names):

    sns_bright_cmap = sns.color_palette('bright')

    data_library_name = data_library_names[0]
    dir_case = dir_cases[0]
    case_name = case_names[0]

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
    dir_save = os.path.join(dir_exp, 'draw_Tropics', 'total_precipitable_water')
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

    pdfname = os.path.join(dir_save, 'total_precipitable_water_cdf.pdf')
    pngname = os.path.join(dir_save, 'total_precipitable_water_cdf.png')

    with PdfPages(pdfname) as pdf:

        fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.0))
        ax = axs
        xmax = 99999999.9

        for idc, (dir_case, case_name) in enumerate(zip(dir_cases, case_names)):

            dir_exp = attributes[(dir_case, case_name)]['dir_exp']
            product = attributes[(dir_case, case_name)]['product']
            dir_tpw = os.path.join(dir_exp, 'draw_Tropics', 'total_precipitable_water')
            tpw_files = glob.glob(os.path.join(dir_tpw, '*precipitable_water.nc'))
            tpw = []

            for filename in tpw_files:
                with netCDF4.Dataset(filename, mode='r', format='NETCDF4') as nc_fid:
                    total_precipitable_water = nc_fid.variables['total_precipitable_water'][:]

                index = (total_precipitable_water >= 0.0)
                total_precipitable_water = total_precipitable_water[index]
                tpw.extend(total_precipitable_water.tolist())

            tpw = np.sort(tpw)
            percentile_90 = np.percentile(tpw, 90)
            cdf = np.arange(1, len(tpw) + 1)/len(tpw)
            print(f"90th percentile of {product} is: {percentile_90:.2f}%")

            specific_value = 56.5
            percentage = np.sum(tpw > specific_value)/len(tpw)*100
            print(f"Percentage of values over {specific_value} in {product}: {percentage:.2f}%")

            xmax = np.min([xmax, np.max(tpw)])
            ax.plot(tpw, cdf, color=sns_bright_cmap[idc], ls='-', ms=2.00, linewidth=1.25, label=product, zorder=3)

        ax.plot([56.5, 56.5], [0.0, 0.9], color='k', ls='-', ms=2.00, linewidth=1.25, zorder=3)
        ax.plot([ 0.0, 56.5], [0.9, 0.9], color='k', ls='-', ms=2.00, linewidth=1.25, zorder=3)
        ax.set_xlabel(r'Total Precipitable Water (kg m$^{-2}$)', fontsize=10.0)
        ax.set_ylabel('Cumulative Probability', fontsize=10.0)
        ax.tick_params('both', direction='in', labelsize=10.0)
        ax.axis([0, xmax, 0, 1.2])
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
    image = IPImage(filename=pngname)
    display(image)
