import os
import importlib
import subprocess
import numpy as np
import pandas as pd
import cal_polar_to_latlon as clatlon
import matplotlib.pyplot as plt
import colormaps as cmaps
from datetime import datetime, timedelta
from combine_and_show_images import combine_images_grid
from mpl_toolkits.basemap import Basemap
from tqdm.notebook import tqdm
from wrf import getvar
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import Image as IPImage
from IPython.display import display

def draw_weather_map_6h(data_library_names, dir_cases, case_names, exp_names,
                        contourf_var, contourf_var_level,
                        contour_var='null', contour_var_level=9999, contour_var_ref_exp_name='ERA5',
                        contour_positive_clabel=False, contour_positive_levels=[0.75], contour_positive_color='w',
                        contour_negative_clabel=False, contour_negative_levels=[-0.75], contour_negative_color='w',
                        quiver_vars=['null', 'null'], quiver_var_level=9999, quiver_var_ref_exp_name='ERA5',
                        quiver_var_color='w', quiver_var_space=10, quiver_var_scale=25,
                        projection='lcc', lat_1=40.0, lat_2=20.0, lon_0=-80.0,
                        domains=['d01'], da_cycle=1, var_time=20000101010000, region_type='d02'):

    if region_type == 'tc':
        radii = [150.0, 300.0, 450.0]
        angles = np.arange(0.0, 360.0, 2.0)
    if region_type == 'aew':
        radii = [100.0, 200.0, 300.0]
        angles = np.arange(0.0, 360.0, 2.0)

    quiver_var_1 = quiver_vars[0]
    quiver_var_2 = quiver_vars[1]

    # Import the necessary library
    (data_library_name, dir_case, case_name, exp_name) = (data_library_names[0], dir_cases[0], case_names[0], exp_names[0])
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')
    module = importlib.import_module(f"set_parameters_{data_library_name}")
    set_variables = getattr(module, 'set_variables')

    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_colormaps = attributes[(dir_case, case_name)]['dir_colormaps']
    dir_weather_map = os.path.join(dir_exp, 'weather_map')
    dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
    dir_best_track = os.path.join(dir_track_intensity, 'best_track')
    dir_ScientificColourMaps7 = os.path.join(dir_colormaps, 'ScientificColourMaps7')
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))

    for dom in tqdm(domains, desc='Domains', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        
        image_files = []
        dir_save = os.path.join(dir_weather_map, 'figures')
        output_filename = (
            f"{str(var_time)}_{contourf_var}_{str(contour_var_level)}_"
            f"{contour_var}_{str(contour_var_level)}_"
            f"{quiver_var_1}_{quiver_var_2}_{str(quiver_var_level)}_"
            f"{region_type}_{dom}_C{str(da_cycle).zfill(2)}"
        )
        output_file = os.path.join(dir_save, output_filename+'.png')

        for idc in tqdm(range(len(dir_cases)), desc='Cases', leave=False):

            # Import the necessary library
            (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])
            specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
            dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
            
            filename = (
                f"{str(var_time)}_{contourf_var}_{str(contour_var_level)}_"
                f"{contour_var}_{str(contour_var_level)}_"
                f"{quiver_var_1}_{quiver_var_2}_{str(quiver_var_level)}_"
                f"{region_type}_{dom}_C{str(da_cycle).zfill(2)}"
            )
            pdfname = os.path.join(dir_weather_map_case, filename+'.pdf')
            pngname = os.path.join(dir_weather_map_case, filename+'.png')
            image_files.append(pngname)

            contourf_var_filename = os.path.join(dir_weather_map_case, f"{contourf_var}_{contourf_var_level}_{dom}.nc")
            contourf_var_ncfile = Dataset(contourf_var_filename)
            contourf_var_times = contourf_var_ncfile.variables['time'][:]
            idt = np.where(contourf_var_times == var_time)[0][0]
            lat = contourf_var_ncfile.variables['lat'][:,:]
            lon = contourf_var_ncfile.variables['lon'][:,:]
            contourf_var_value = contourf_var_ncfile.variables[contourf_var][idt,:,:]
            contourf_var_ncfile.close()

            contourf_var_filename = os.path.join(dir_weather_map_case, f"{contourf_var}_{contourf_var_level}_d01.nc")
            contourf_var_ncfile = Dataset(contourf_var_filename)
            lat_d01 = contourf_var_ncfile.variables['lat'][:,:]
            lon_d01 = contourf_var_ncfile.variables['lon'][:,:]
            contourf_var_ncfile.close()

            contourf_var_filename = os.path.join(dir_weather_map_case, f"{contourf_var}_{contourf_var_level}_d02.nc")
            contourf_var_ncfile = Dataset(contourf_var_filename)
            lat_d02 = contourf_var_ncfile.variables['lat'][:,:]
            lon_d02 = contourf_var_ncfile.variables['lon'][:,:]
            contourf_var_ncfile.close()

            if 'null' not in contour_var:
                dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                if 'IMERG' in exp_name or 'CMORPH' in exp_name or 'GSMaP' in exp_name:
                    ref_case = '_'.join([case_name, contour_var_ref_exp_name, 'C'+str(da_cycle).zfill(2)])
                    dir_weather_map_case = os.path.join(dir_weather_map, ref_case)
            
                contour_var_filename = os.path.join(dir_weather_map_case, f"{contour_var}_{contour_var_level}_{dom}.nc")
                contour_var_ncfile = Dataset(contour_var_filename)
                contour_var_times = contour_var_ncfile.variables['time'][:]
                idt = np.where(contour_var_times == var_time)[0][0]
                contour_var_value = contourf_var_ncfile.variables[contourf_var][idt,:,:]
                contour_var_ncfile.close()
            
            if 'null' not in quiver_vars:
                dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                if 'IMERG' in exp_name or 'CMORPH' in exp_name or 'GSMaP' in exp_name:
                    ref_case = '_'.join([case_name, quiver_var_ref_exp_name, 'C'+str(da_cycle).zfill(2)])
                    dir_weather_map_case = os.path.join(dir_weather_map, ref_case)
            
                quiver_var_1_filename = os.path.join(dir_weather_map_case, f"{quiver_var_1}_{quiver_var_level}_{dom}.nc")
                quiver_var_1_ncfile = Dataset(quiver_var_1_filename)
                quiver_var_1_times = quiver_var_1_ncfile.variables['time'][:]
                idt = np.where(quiver_var_1_times == var_time)[0][0]
                quiver_var_1_value = quiver_var_1_ncfile.variables[quiver_var_1][idt,:,:]
                quiver_var_1_ncfile.close()
                quiver_var_2_filename = os.path.join(dir_weather_map_case, f"{quiver_var_2}_{quiver_var_level}_{dom}.nc")
                quiver_var_2_ncfile = Dataset(quiver_var_2_filename)
                quiver_var_2_times = quiver_var_2_ncfile.variables['time'][:]
                idt = np.where(quiver_var_2_times == var_time)[0][0]
                quiver_var_2_value = quiver_var_2_ncfile.variables[quiver_var_2][idt,:,:]
                quiver_var_2_ncfile.close()

            if region_type == 'd01': extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
            if region_type == 'd02': extent = [lon_d02[0,0], lon_d02[-1,-1], lat_d02[0,0], lat_d02[-1,-1]]
            
            if region_type == 'tc':
                best_track = os.path.join(dir_best_track, attributes[(dir_case, case_name)]['NHC_best_track'])
                df = pd.read_csv(best_track)
                bt_lats = list(df['LAT'][:])
                bt_lons = list(df['LON'][:])
                bt_dates = list(df['Date_Time'][:])
                del df

                var_time_datetime = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')
                for id_bt, bt_date in enumerate(bt_dates):
                    bt_datetime = datetime.strptime(bt_date, '%Y-%m-%d %H:%M:%S')
                    if bt_datetime == var_time_datetime:
                        bt_lat = bt_lats[id_bt]
                        bt_lon = bt_lons[id_bt]
                        extent = [bt_lon-5.0, bt_lon+5.0, bt_lat-5.0, bt_lat+5.0]

            if region_type == 'aew':
                best_track = os.path.join(dir_best_track, attributes[(dir_case, case_name)]['AEW_best_track'])
                df = pd.read_csv(best_track)
                bt_lats = list(df['LAT'][:])
                bt_lons = list(df['LON'][:])
                bt_dates = list(df['Date_Time'][:])
                del df

                var_time_datetime = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')
                for id_bt, bt_date in enumerate(bt_dates):
                    bt_datetime = datetime.strptime(bt_date, '%Y-%m-%d %H:%M:%S')
                    if bt_datetime == var_time_datetime:
                        bt_lat = bt_lats[id_bt]
                        bt_lon = bt_lons[id_bt]
                        extent = [bt_lon-3.0, bt_lon+3.0, bt_lat-3.0, bt_lat+3.0]

            fig_width = 2.75*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])
            fig_height = 2.75+0.75
            clb_aspect = 25*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])
            if projection == 'lcc': fig_width = 2.75*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])-0.5

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
                    m.drawparallels(np.arange(-90, 91, 10),   labels=[1,0,0,0], fontsize=10.0, linewidth=0.5, dashes=[1,1], color=grayC_cm_data[53])

                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                mlon, mlat = m(lon, lat)
                (contourf_information, contourf_levels) = set_variables(contourf_var)
                (contourf_labels, contourf_cmap) = contourf_levels[contourf_var_level]
                pcm = ax.contourf(mlon, mlat, contourf_information['factor']*contourf_var_value, \
                                  levels=list(map(float, contourf_labels)), cmap=contourf_cmap, extend=contourf_information['extend'], zorder=1)
                # print(np.nanmax(contourf_var_value))
                # print(np.nanmin(contourf_var_value))
                
                if 'null' not in contour_var:
                    (contour_information, contour_levels) = set_variables(contour_var)
                    (contour_labels, contour_cmap) = contour_levels[contour_var_level]
                    if contour_positive_clabel == True:
                        CS1 = ax.contour(mlon, mlat, contour_information['factor']*contour_var_value, \
                                         levels=contour_positive_levels, linestyles='solid',  \
                                         colors=contour_positive_color, linewidths=1.0, zorder=1)
                        ax.clabel(CS1, inline=True, fontsize=5.0)
                    if contour_negative_clabel == True:
                        CS2 = ax.contour(mlon, mlat, contour_information['factor']*contour_var_value, \
                                         levels=contour_negative_levels, linestyles='dashed',  \
                                         colors=contour_negative_color, linewidths=1.0, zorder=1)
                        ax.clabel(CS2, inline=True, fontsize=5.0)
                # print(np.nanmax(contour_var_value))
                # print(np.nanmin(contour_var_value))

                if 'null' not in quiver_vars:

                    (quiver_1_information, quiver_1_levels) = set_variables(quiver_var_1)
                    (quiver_2_information, quiver_2_levels) = set_variables(quiver_var_2)
                    ax.quiver(mlon[::quiver_var_space, ::quiver_var_space], mlat[::quiver_var_space, ::quiver_var_space], \
                              quiver_1_information['factor']*quiver_var_1_value[::quiver_var_space, ::quiver_var_space], \
                              quiver_2_information['factor']*quiver_var_2_value[::quiver_var_space, ::quiver_var_space], \
                              width=0.0025, headwidth=5.0, headlength=7.5, \
                              color=quiver_var_color, scale=quiver_var_scale, scale_units='inches', zorder=1)
                
                if region_type == 'd01' or region_type == 'd02':
                    if projection == 'cyl':

                        ax.set_xticks(np.arange(-180, 181, 10))
                        ax.set_yticks(np.arange(-90, 91, 10))
                        ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                        ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                        ax.text(extent[0], extent[3], exp_name, ha='left', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)
                
                    elif projection == 'lcc':
                        ax.text(np.min(mlon), np.max(mlat), exp_name, ha='left', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

                else:

                    if projection == 'cyl':
                        ax.plot([-180.0, 180.0], [bt_lat, bt_lat], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                        ax.plot([bt_lon, bt_lon], [-90.0, 90.0],   '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                    
                        lat_polar = np.zeros((len(radii), len(angles)))
                        lon_polar = np.zeros((len(radii), len(angles)))
                        for idr in range(0, len(radii)):
                            for ida in range(0, len(angles)):
                                lat_polar[idr,ida], lon_polar[idr,ida] = clatlon.Cal_LatLon(bt_lat, bt_lon, radii[idr], angles[ida])
                            ax.plot(lon_polar[idr,:], lat_polar[idr,:], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                    
                        if region_type == 'tc':
                            ax.set_xticks(np.arange(-180, 181, 5))
                            ax.set_yticks(np.arange(-90, 91, 5))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 5)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  5)])
                            ax.text(extent[0], extent[3], exp_name, ha='left', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

                        if region_type == 'aew':
                            ax.set_xticks(np.arange(-180, 181, 3))
                            ax.set_yticks(np.arange(-90, 91, 3))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 3)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  3)])
                            ax.text(extent[0], extent[3], exp_name, ha='left', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

                if projection == 'cyl':
                    ax.tick_params('both', direction='in', labelsize=10.0)
                    ax.axis(extent)
                    ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                if contourf_var_level == 9999:
                    clb.set_label(f"{contourf_information['lb_title']}", fontsize=10.0, labelpad=4.0)
                else:
                    clb.set_label(f"{contourf_information['lb_title']} on {contourf_var_level} hPa", fontsize=10.0, labelpad=4.0)
                clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                clb.ax.minorticks_off()
                clb.set_ticks(list(map(float, contourf_labels[0::2])))
                clb.set_ticklabels(contourf_labels[0::2])

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
