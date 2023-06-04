import os
import glob
import netCDF4
import datetime
import importlib
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pathlib import Path
from netCDF4 import Dataset
from tqdm.notebook import tqdm
from mpl_toolkits.basemap import Basemap
from IPython.display import Image as IPImage
from matplotlib.colors import LinearSegmentedColormap
from combine_and_show_images import combine_images_grid
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import Image as IPImage

def draw_CYGNSS_wind_speed(data_library_names, dir_cases, case_names):

    sns_bright_cmap = sns.color_palette('bright')

    n_cases = len(dir_cases)
    for idc in tqdm(range(n_cases), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        (data_library_names, dir_case, case_name) = (data_library_names[idc], dir_cases[idc], case_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        itime = attributes[(dir_case, case_name)]['itime']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        time_window_max = attributes[(dir_case, case_name)]['time_window_max']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        dir_cygnss = '/'.join([attributes[(dir_case, case_name)]['dir_cygnss'], case_name])
        dir_wrfout = '/'.join([dir_exp, 'cycling_da', 'Data', case_name, 'CON_ENS_C03', 'bkg'])
        dir_save = '/'.join([dir_exp, 'draw_Tropics', 'cygnss'])
        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
        grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

        initial_time = datetime.datetime(*itime)
        anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)
        anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(total_da_cycles-1))
        anl_start_time_str = anl_start_time.strftime('%Y%m%d%H%M%S')
        anl_end_time_str = anl_end_time.strftime('%Y%m%d%H%M%S')

        wrfout_format='wrfout_d01_{ctime:%Y-%m-%d_%H:%M:00}'
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

            time_now = anl_start_time + datetime.timedelta(hours=cycling_interval*da_cycle)

            da_window_ST = time_now - datetime.timedelta(hours=time_window_max)
            da_window_ET = time_now + datetime.timedelta(hours=time_window_max)
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
                time_ST = datetime.datetime.strptime(date_st_str, '%Y%m%d-%H%M%S')
                time_ET = datetime.datetime.strptime(date_et_str, '%Y%m%d-%H%M%S')
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

def draw_TROPICS_tpw(data_library_names, dir_cases, case_names):

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
        dir_wrfout = '/'.join([dir_exp, 'cycling_da', 'Data', case_name, 'CON_ENS_C03', 'bkg'])
        dir_save = '/'.join([dir_exp, 'draw_Tropics', 'total_precipitable_water'])
        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
        grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

        initial_time = datetime.datetime(*itime)
        anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)
        anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(total_da_cycles-1))
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
            time_ST = datetime.datetime.strptime(time_ST_str, '%Y%m%d%H%M%S')
            time_ET = datetime.datetime.strptime(time_ET_str, '%Y%m%d%H%M%S')

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

    pdfname = dir_save + '/total_precipitable_water_cdf.pdf'
    pngname = dir_save + '/total_precipitable_water_cdf.png'

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
        ax.legend(loc='upper left', fontsize=5.0, handlelength=2.5).set_zorder(102)

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
