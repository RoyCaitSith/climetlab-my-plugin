import os
import importlib
import subprocess
import numpy as np
import matplotlib.pyplot as plt
import colormaps as cmaps
from datetime import datetime, timedelta
from mpl_toolkits.basemap import Basemap
from tqdm.notebook import tqdm
from wrf import getvar
from netCDF4 import Dataset
from matplotlib.backends.backend_pdf import PdfPages

def draw_sfc_wind_individual(data_library_names, dir_cases, case_names, exp_names):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        dir_exp=attributes[(dir_case, case_name)]['dir_exp']
        dir_ScientificColourMaps7=attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        itime=attributes[(dir_case, case_name)]['itime']
        initial_time = datetime(*itime)
        total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
        cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
        history_interval=attributes[(dir_case, case_name)]['history_interval']
        forecast_domains=attributes[(dir_case, case_name)]['forecast_domains']
        forecast_hours=attributes[(dir_case, case_name)]['forecast_hours']
        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))

        for da_cycle in tqdm(range(1, total_da_cycles+1), desc='DA Cycles', leave=False):
            for dom in tqdm(forecast_domains, desc='DA Domains', leave=False):

                dir_weather_map = os.path.join(dir_exp, 'weather_map')
                os.makedirs(dir_weather_map, exist_ok=True)
                dir_weather_map = os.path.join(dir_weather_map, 'sfc_wind')
                os.makedirs(dir_weather_map, exist_ok=True)
                specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
                dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                os.makedirs(dir_weather_map_case, exist_ok=True)
                dir_bkg = os.path.join(dir_exp, 'cycling_da', specific_case, 'bkg')

                for idt in range(0, int(forecast_hours/history_interval+1)):

                    anl_end_time = initial_time + timedelta(hours=cycling_interval*da_cycle)
                    forecast_start_time = anl_end_time
                    time_now = forecast_start_time + timedelta(hours = (idt+1)*history_interval)
                    time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')

                    wrfout = f"wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:00:00')}"
                    filename = os.path.join(dir_bkg, wrfout)
                    ncfile = Dataset(filename)
                    lat = ncfile.variables['XLAT'][0,:,:]
                    lon = ncfile.variables['XLONG'][0,:,:]
                    (u10, v10) = getvar(ncfile, 'uvmet10', units='ms-1')
                    (spd, dir) = getvar(ncfile, 'uvmet10_wspd_wdir', units='ms-1')
                    ncfile.close()

                    extent = [lon[0,0], lon[-1,-1], lat[0,0], lat[-1,-1]]
                    fig_width = 2.75*np.abs(lon[-1,-1]-lon[0,0])/np.abs(lat[-1,-1]-lat[0,0])
                    fig_height = 2.75+0.75
                    clb_aspect = 25*np.abs(lon[-1,-1]-lon[0,0])/np.abs(lat[-1,-1]-lat[0,0])

                    pdfname = os.path.join(dir_weather_map_case, '_'.join([time_now_YYYYMMDDHH, 'sfc_wind', dom+'.pdf']))
                    pngname = os.path.join(dir_weather_map_case, '_'.join([time_now_YYYYMMDDHH, 'sfc_wind', dom+'.png']))

                    with PdfPages(pdfname) as pdf:

                        fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                        ax = axs

                        m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                        m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                        mlon, mlat = m(lon, lat)

                        space = 20
                        pcm1 = ax.contourf(mlon, mlat, spd, levels=np.arange(0, 30.1, 1.0), cmap=cmaps.hawaii, extend='max', zorder=1)
                        ax.quiver(mlon[::space, ::space], mlat[::space, ::space], u10[::space, ::space], v10[::space, ::space],
                                  width=0.001, headwidth=5.0, headlength=7.5, scale=75.0, scale_units='inches', zorder=1)

                        ax.set_xticks(np.arange(-180, 181, 10))
                        ax.set_yticks(np.arange(-90, 91, 10))
                        ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                        ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                        ax.tick_params('both', direction='in', labelsize=10.0)
                        ax.axis(extent)
                        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                        clb = fig.colorbar(pcm1, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                        clb.set_label("10 m Wind ($\mathregular{ms^{-1}}$)", fontsize=10.0, labelpad=4.0)
                        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                        clb.ax.minorticks_off()
                        clb.set_ticks(np.arange(0, 30.1, 5.0))
                        clb.set_ticklabels(range(0, 31, 5))

                        plt.tight_layout()
                        plt.savefig(pngname, dpi=600)
                        pdf.savefig(fig)
                        plt.cla()
                        plt.clf()
                        plt.close()

                    command = f"convert {pngname} -trim {pngname}"
                    subprocess.run(command, shell=True)

def draw_slp_rain_individual(data_library_names, dir_cases, case_names, exp_names):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        dir_exp=attributes[(dir_case, case_name)]['dir_exp']
        dir_ScientificColourMaps7=attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        itime=attributes[(dir_case, case_name)]['itime']
        initial_time = datetime(*itime)
        total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
        cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
        history_interval=attributes[(dir_case, case_name)]['history_interval']
        forecast_domains=attributes[(dir_case, case_name)]['forecast_domains']
        forecast_hours=attributes[(dir_case, case_name)]['forecast_hours']
        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))

        for da_cycle in tqdm(range(1, total_da_cycles+1), desc='DA Cycles', leave=False):
            for dom in tqdm(forecast_domains, desc='DA Domains', leave=False):

                dir_weather_map = os.path.join(dir_exp, 'weather_map')
                os.makedirs(dir_weather_map, exist_ok=True)
                dir_weather_map = os.path.join(dir_weather_map, 'slp_rain')
                os.makedirs(dir_weather_map, exist_ok=True)
                specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
                dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                os.makedirs(dir_weather_map_case, exist_ok=True)
                dir_bkg = os.path.join(dir_exp, 'cycling_da', specific_case, 'bkg')

                for idt in range(0, int(forecast_hours/history_interval+1)):

                    anl_end_time = initial_time + timedelta(hours=cycling_interval*da_cycle)
                    forecast_start_time = anl_end_time
                    time_last = forecast_start_time + timedelta(hours = idt*history_interval)
                    time_now = forecast_start_time + timedelta(hours = (idt+1)*history_interval)
                    time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')

                    wrfout_last = f"wrfout_{dom}_{time_last.strftime('%Y-%m-%d_%H:00:00')}"
                    wrfout = f"wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:00:00')}"

                    filename_last = os.path.join(dir_bkg, wrfout_last)
                    ncfile_last = Dataset(filename_last)
                    rain_exp_last = getvar(ncfile_last, 'RAINNC')
                    rain_con_last = getvar(ncfile_last, 'RAINC')
                    rain_tot_last = rain_exp_last + rain_con_last

                    filename = os.path.join(dir_bkg, wrfout)
                    ncfile = Dataset(filename)
                    lat = ncfile.variables['XLAT'][0,:,:]
                    lon = ncfile.variables['XLONG'][0,:,:]
                    rain_exp = getvar(ncfile, 'RAINNC')
                    rain_con = getvar(ncfile, 'RAINC')
                    rain_tot = rain_exp + rain_con
                    slp = getvar(ncfile, 'slp', units='hPa')
                    (u10, v10) = getvar(ncfile, 'uvmet10', units='ms-1')
                    ncfile.close()

                    rain_rate = rain_tot - rain_tot_last
                    if time_last == forecast_start_time: rain_rate = rain_tot

                    extent = [lon[0,0], lon[-1,-1], lat[0,0], lat[-1,-1]]
                    fig_width = 2.75*np.abs(lon[-1,-1]-lon[0,0])/np.abs(lat[-1,-1]-lat[0,0])
                    fig_height = 2.75+0.75
                    clb_aspect = 25*np.abs(lon[-1,-1]-lon[0,0])/np.abs(lat[-1,-1]-lat[0,0])

                    pdfname = os.path.join(dir_weather_map_case, '_'.join([time_now_YYYYMMDDHH, 'slp_rain', dom+'.pdf']))
                    pngname = os.path.join(dir_weather_map_case, '_'.join([time_now_YYYYMMDDHH, 'slp_rain', dom+'.png']))

                    with PdfPages(pdfname) as pdf:

                        fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                        ax = axs

                        m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                        m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                        mlon, mlat = m(lon, lat)

                        space = 20
                        pcm1 = ax.contourf(mlon, mlat, rain_rate, levels=np.arange(0, 55.1, 1), cmap=cmaps.hawaii, extend='both', zorder=1)
                        ax.quiver(mlon[::space, ::space], mlat[::space, ::space], u10[::space, ::space], v10[::space, ::space],                                                                                                                                                                                                                                                                                                
                                  width=0.001, headwidth=5.0, headlength=7.5, scale=75.0, scale_units='inches', zorder=1)
                        ax.contour(mlon, mlat, slp, levels=np.arange(900, 1100.1, 5.0), colors='k', linewidths=1.0, zorder=0)

                        ax.set_xticks(np.arange(-180, 181, 10))
                        ax.set_yticks(np.arange(-90, 91, 10))
                        ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                        ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                        ax.tick_params('both', direction='in', labelsize=10.0)
                        ax.axis(extent)
                        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                        clb = fig.colorbar(pcm1, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                        clb.set_label("6-hr accumulated precipitation (mm)", fontsize=10.0, labelpad=4.0)
                        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                        clb.ax.minorticks_off()
                        clb.set_ticks(range(0, 56, 10))
                        clb.set_ticklabels(range(0, 56, 10))

                        plt.tight_layout()
                        plt.savefig(pngname, dpi=600)
                        pdf.savefig(fig)
                        plt.cla()
                        plt.clf()
                        plt.close()

                    command = f"convert {pngname} -trim {pngname}"
                    subprocess.run(command, shell=True)
