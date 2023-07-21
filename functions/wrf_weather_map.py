import os
import importlib
import subprocess
import numpy as np
import pandas as pd
import cal_polar_to_latlon as clatlon
import matplotlib.pyplot as plt
import colormaps as cmaps
from set_parameters import set_variables
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
                        contour_var='null', contour_var_level=9999, contour_var_ref_exp_name='GFS',
                        quiver_vars=['null', 'null'], quiver_var_level=9999, quiver_var_ref_exp_name='GFS', quiver_var_space=10,
                        domains=['d01'], da_cycle=1, var_time=20000101010000, region='null'):

    radii = [150.0, 300.0, 450.0]
    angles = np.arange(0.0, 360.0, 2.0)
    quiver_var_1 = quiver_vars[0]
    quiver_var_2 = quiver_vars[1]

    # Import the necessary library
    (data_library_name, dir_case, case_name, exp_name) = (data_library_names[0], dir_cases[0], case_names[0], exp_names[0])
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
    dir_weather_map = os.path.join(dir_exp, 'weather_map')
    dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
    dir_best_track = os.path.join(dir_track_intensity, 'best_track')
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))

    for dom in tqdm(domains, desc='Domains', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        
        image_files = []
        dir_save = os.path.join(dir_weather_map, 'figures')
        output_filename = (
            f"{str(var_time)}_{contourf_var}_{str(contour_var_level)}_"
            f"{contour_var}_{str(contour_var_level)}_"
            f"{quiver_var_1}_{quiver_var_2}_{str(quiver_var_level)}_"
            f"{region}_{dom}_C{str(da_cycle).zfill(2)}"
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
                f"{region}_{dom}_C{str(da_cycle).zfill(2)}"
            )
            pdfname = os.path.join(dir_weather_map_case, filename+'.pdf')
            pngname = os.path.join(dir_weather_map_case, filename+'.png')
            image_files.append(pngname)

            contourf_var_filename = os.path.join(dir_weather_map_case, f"{contourf_var}_{dom}.nc")
            contourf_var_ncfile = Dataset(contourf_var_filename)
            contourf_var_times = contourf_var_ncfile.variables['time'][:]
            contourf_var_levels = contourf_var_ncfile.variables['level'][:]
            idt = np.where(contourf_var_times == var_time)[0][0]
            idl = np.where(contourf_var_levels == contourf_var_level)[0][0]
            lat = contourf_var_ncfile.variables['lat'][:,:]
            lon = contourf_var_ncfile.variables['lon'][:,:]
            contourf_var_value = contourf_var_ncfile.variables[contourf_var][idt,idl,:,:]
            contourf_var_ncfile.close()

            if 'null' not in contour_var:
                dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                if 'IMERG' in exp_name or 'CMORPH' in exp_name or 'GSMaP' in exp_name:
                    ref_case = '_'.join([case_name, contour_var_ref_exp_name, 'C'+str(da_cycle).zfill(2)])
                    dir_weather_map_case = os.path.join(dir_weather_map, ref_case)
            
                contour_var_filename = os.path.join(dir_weather_map_case, f"{contour_var}_{dom}.nc")
                contour_var_ncfile = Dataset(contour_var_filename)
                contour_var_times = contour_var_ncfile.variables['time'][:]
                contour_var_levels = contour_var_ncfile.variables['level'][:]
                idt = np.where(contour_var_times == var_time)[0][0]
                idl = np.where(contour_var_levels == contour_var_level)[0][0]
                contour_var_value = contourf_var_ncfile.variables[contourf_var][idt,idl,:,:]
                contour_var_ncfile.close()
            
            if 'null' not in quiver_vars:
                dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                if 'IMERG' in exp_name or 'CMORPH' in exp_name or 'GSMaP' in exp_name:
                    ref_case = '_'.join([case_name, quiver_var_ref_exp_name, 'C'+str(da_cycle).zfill(2)])
                    dir_weather_map_case = os.path.join(dir_weather_map, ref_case)
            
                quiver_var_1_filename = os.path.join(dir_weather_map_case, f"{quiver_var_1}_{dom}.nc")
                quiver_var_1_ncfile = Dataset(quiver_var_1_filename)
                quiver_var_1_times = quiver_var_1_ncfile.variables['time'][:]
                quiver_var_1_levels = quiver_var_1_ncfile.variables['level'][:]
                idt = np.where(quiver_var_1_times == var_time)[0][0]
                idl = np.where(quiver_var_1_levels == quiver_var_level)[0][0]
                quiver_var_1_value = quiver_var_1_ncfile.variables[quiver_var_1][idt,idl,:,:]
                quiver_var_1_ncfile.close()
                quiver_var_2_filename = os.path.join(dir_weather_map_case, f"{quiver_var_2}_{dom}.nc")
                quiver_var_2_ncfile = Dataset(quiver_var_2_filename)
                quiver_var_2_times = quiver_var_2_ncfile.variables['time'][:]
                quiver_var_2_levels = quiver_var_2_ncfile.variables['level'][:]
                idt = np.where(quiver_var_2_times == var_time)[0][0]
                idl = np.where(quiver_var_2_levels == quiver_var_level)[0][0]
                quiver_var_2_value = quiver_var_2_ncfile.variables[quiver_var_2][idt,idl,:,:]
                quiver_var_2_ncfile.close()

            if 'null' in region:
                extent = [lon[0,0], lon[-1,-1], lat[0,0], lat[-1,-1]]
            else:
                if 'tc' in region: best_track = os.path.join(dir_best_track, attributes[(dir_case, case_name)]['NHC_best_track'])
                if 'aew' in region: best_track = os.path.join(dir_best_track, attributes[(dir_case, case_name)]['AEW_best_track'])

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

            fig_width = 2.75*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])
            fig_height = 2.75+0.75
            clb_aspect = 25*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                ax = axs

                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                mlon, mlat = m(lon, lat)
                (contourf_information, contourf_levels) = set_variables(contourf_var)
                (contourf_labels, contourf_cmap) = contourf_levels[contourf_var_level]
                pcm = ax.contourf(mlon, mlat, contourf_information['factor']*contourf_var_value, \
                                  levels=list(map(float, contourf_labels)), cmap=contourf_cmap, extend=contourf_information['extend'], zorder=1)
                
                if 'null' not in contour_var:
                    (contour_information, contour_levels) = set_variables(contour_var)

                if 'null' not in quiver_vars:

                    (quiver_1_information, quiver_1_levels) = set_variables(quiver_var_1)
                    (quiver_2_information, quiver_2_levels) = set_variables(quiver_var_2)
                    ax.quiver(mlon[::quiver_var_space, ::quiver_var_space], mlat[::quiver_var_space, ::quiver_var_space], \
                              quiver_var_1_value[::quiver_var_space, ::quiver_var_space], quiver_var_2_value[::quiver_var_space, ::quiver_var_space], \
                              width=0.001, headwidth=5.0, headlength=7.5, scale=75.0, scale_units='inches', zorder=1)
                
                if 'null' in region:
                    ax.set_xticks(np.arange(-180, 181, 10))
                    ax.set_yticks(np.arange(-90, 91, 10))
                    ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                    ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                else:
                    ax.plot([-180.0, 180.0], [bt_lat, bt_lat], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                    ax.plot([bt_lon, bt_lon], [-90.0, 90.0],   '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                    
                    lat_polar = np.zeros((len(radii), len(angles)))
                    lon_polar = np.zeros((len(radii), len(angles)))
                    for idr in range(0, len(radii)):
                        for ida in range(0, len(angles)):
                            lat_polar[idr,ida], lon_polar[idr,ida] = clatlon.Cal_LatLon(bt_lat, bt_lon, radii[idr], angles[ida])
                        ax.plot(lon_polar[idr,:], lat_polar[idr,:], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)

                    ax.set_xticks(np.arange(-180, 181, 5))
                    ax.set_yticks(np.arange(-90, 91, 5))
                    ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 5)])
                    ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  5)])

                ax.text(extent[0]+0.4, extent[3]-0.4, exp_name, ha='left', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)
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