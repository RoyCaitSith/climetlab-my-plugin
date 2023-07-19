import os
import h5py
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

def draw_sfc_wind_individual(data_library_names, dir_cases, case_names, exp_names):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')

        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        itime = attributes[(dir_case, case_name)]['itime']
        initial_time = datetime(*itime)
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        history_interval = attributes[(dir_case, case_name)]['history_interval']
        forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
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
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        itime = attributes[(dir_case, case_name)]['itime']
        initial_time = datetime(*itime)
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        history_interval = attributes[(dir_case, case_name)]['history_interval']
        forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
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

def draw_6h_accumulated_precipitation_box_scheme(data_library_name, scheme, type='tc'):

    accumulated_hours = 6.0
    radii = [150.0, 300.0, 450.0]
    angles = np.arange(0.0, 360.0, 2.0)

    dir_grayC = '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7/grayC'
    grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

    module = importlib.import_module(f"data_library_{data_library_name}")
    compare_schemes = getattr(module, 'compare_schemes')
    attributes = getattr(module, 'attributes')

    n_cases = len(compare_schemes[scheme]['cases'])
    (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][-1]
    labels = compare_schemes[scheme]['labels']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    GFDL_domains = attributes[(dir_case, case_name)]['GFDL_domains']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']
    NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']

    for dom in tqdm(GFDL_domains, desc='GFDL Domains', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        for da_cycle in tqdm(range(1, total_da_cycles+1), desc="Cycles", leave=False):

            anl_start_time = initial_time + timedelta(hours=cycling_interval)
            anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
            forecast_start_time = anl_end_time
            n_time = int(forecast_hours/accumulated_hours)

            for idt in tqdm(range(n_time), desc="Time", leave=False):

                time_now = forecast_start_time + timedelta(hours=idt*accumulated_hours)
                time_label = time_now + timedelta(hours=accumulated_hours/2.0)
                time_now_str = time_now.strftime('%Y%m%d%H')
                time_label_str = time_label.strftime('%H UTC %d %b')

                image_files = []
                dir_rainfall = '/'.join([dir_exp, 'rainfall', case_name, 'Figures'])
                output_file = os.path.join(dir_rainfall, '_'.join([time_now_str, 'rainfall', '6h', scheme, 'C'+str(da_cycle).zfill(2), dom+'.png']))

                observations = ['IMERG']
                n_observations = len(observations)

                for ido in tqdm(range(n_observations), desc="Observations", leave=False):

                    dir_rainfall = '/'.join([dir_exp, 'rainfall', case_name, observations[ido]+'_C'+str(da_cycle).zfill(2)])
                    filename = dir_rainfall + f'/rainfall_6h_{dom}.nc'
                    ncfile   = Dataset(filename)
                    rain = ncfile.variables['rainfall'][idt,:,:]*accumulated_hours
                    rain_lat = ncfile.variables['lat'][:,:]
                    rain_lon = ncfile.variables['lon'][:,:]
                    ncfile.close()

                    df = pd.read_csv(NHC_best_track)
                    TC_lats = list(df['LAT'][:])
                    TC_lons = list(df['LON'][:])
                    TC_dates = list(df['Date_Time'][:])
                    del df

                    pdfname = dir_rainfall + '/' + '_'.join([time_label_str, 'rainfall', '6h', dom+'.pdf'])
                    pngname = dir_rainfall + '/' + '_'.join([time_label_str, 'rainfall', '6h', dom+'.png'])
                    image_files.append(pngname)

                    with PdfPages(pdfname) as pdf:

                        fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))

                        time_end = time_now + timedelta(hours = accumulated_hours)
                        for id_TC, TC_date in enumerate(TC_dates):
                            TC_datetime = datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                            if TC_datetime == time_end:
                                TC_lat = 0.5*(TC_lats[id_TC] + TC_lats[id_TC-1])
                                TC_lon = 0.5*(TC_lons[id_TC] + TC_lons[id_TC-1])
                                extent = [TC_lon-5.0, TC_lon+5.0, TC_lat-5.0, TC_lat+5.0]

                        ax = axs
                        m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                        m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                        mlons, mlats = m(rain_lon, rain_lat)

                        extend_label = observations[ido]+': '+time_label_str

                        rain_masked = np.ma.masked_where(rain <= 0, rain)
                        #pcm = ax.contourf(rain_lon, rain_lat, rain_masked, locator=ticker.LogLocator(), levels=rain_levels, cmap='jet', extend='max', zorder=1)
                        pcm = ax.contourf(rain_lon, rain_lat, rain_masked, levels=np.arange(0, 55.1, 1.0), cmap='jet', extend='max', zorder=1)
                        ax.plot([-180.0, 180.0], [TC_lat, TC_lat], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                        ax.plot([TC_lon, TC_lon], [-90.0, 90.0],   '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                        ax.text(TC_lon-4.6, TC_lat+4.4, extend_label, ha='left', va='center', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

                        lat_polar = np.zeros((len(radii), len(angles)))
                        lon_polar = np.zeros((len(radii), len(angles)))
                        for idr in range(0, len(radii)):
                            for ida in range(0, len(angles)):
                                lat_polar[idr,ida], lon_polar[idr,ida] = clatlon.Cal_LatLon(TC_lat, TC_lon, radii[idr], angles[ida])
                            ax.plot(lon_polar[idr,:], lat_polar[idr,:], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)

                        ax.set_xticks(np.arange(-180, 181, 5))
                        ax.set_yticks(np.arange(-90, 91, 5))
                        ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 5)])
                        ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  5)])
                        ax.tick_params('both', direction='in', labelsize=10.0)
                        ax.axis(extent)
                        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                        clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
                        clb.set_label('6-hr Accumulated Precipitation (mm)', fontsize=10.0, labelpad=4.0)
                        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                        clb.ax.minorticks_off()
                        #clb.set_ticks(rain_levels)
                        #clb.set_ticklabels(rain_labels)
                        clb.set_ticks(range(0, 56, 10))
                        clb.set_ticklabels(range(0, 56, 10))

                        plt.tight_layout()
                        plt.savefig(pngname, dpi=600)
                        pdf.savefig(fig)
                        plt.cla()
                        plt.clf()
                        plt.close()

                for idc in tqdm(range(n_cases), desc="Cases", leave=False):

                    (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][idc]
                    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
                    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']
                    dir_rainfall = '/'.join([dir_exp, 'rainfall', case_name, exp_name+'_C'+str(da_cycle).zfill(2)])
                    filename = dir_rainfall + f'/rainfall_6h_{dom}.nc'
                    ncfile   = Dataset(filename)
                    rain = ncfile.variables['rainfall'][idt,:,:]*accumulated_hours
                    rain_lat = ncfile.variables['lat'][:,:]
                    rain_lon = ncfile.variables['lon'][:,:]
                    ncfile.close()

                    case = '_'.join([case_name, exp_name, 'C' + str(da_cycle).zfill(2)])
                    df = pd.read_csv(dir_track_intensity + '/' + case + '_' + dom + '.csv')
                    TC_lats = list(df['LAT'][:])
                    TC_lons = list(df['LON'][:])
                    TC_dates = list(df['Date_Time'][:])
                    del df

                    pdfname = dir_rainfall + '/' + '_'.join([time_now.strftime('%Y%m%d%H'), 'rainfall', '6h', dom+'.pdf'])
                    pngname = dir_rainfall + '/' + '_'.join([time_now.strftime('%Y%m%d%H'), 'rainfall', '6h', dom+'.png'])
                    image_files.append(pngname)

                    with PdfPages(pdfname) as pdf:

                        fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))

                        time_end = time_now + timedelta(hours = accumulated_hours)
                        for id_TC, TC_date in enumerate(TC_dates):
                            TC_datetime = datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
                            if TC_datetime == time_end:
                                TC_lat = 0.5*(TC_lats[id_TC] + TC_lats[id_TC-1])
                                TC_lon = 0.5*(TC_lons[id_TC] + TC_lons[id_TC-1])
                                extent = [TC_lon-5.0, TC_lon+5.0, TC_lat-5.0, TC_lat+5.0]

                        ax = axs
                        m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                        m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                        mlons, mlats = m(rain_lon, rain_lat)

                        extend_label = labels[idc]
                        if 'CON' in exp_name and 'CON' not in labels[idc] and 'CTRL' not in labels[idc]: extend_label = 'CON_' + extend_label
                        if 'CLR' in exp_name and 'CLR' not in labels[idc]: extend_label = extend_label + '_CLR'

                        rain_masked = np.ma.masked_where(rain <= 0, rain)
                        #pcm = ax.contourf(rain_lon, rain_lat, rain_masked, locator=ticker.LogLocator(), levels=rain_levels, cmap='jet', extend='max', zorder=1)
                        pcm = ax.contourf(rain_lon, rain_lat, rain_masked, levels=np.arange(0, 55.1, 1.0), cmap='jet', extend='max', zorder=1)
                        ax.plot([-180.0, 180.0], [TC_lat, TC_lat], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                        ax.plot([TC_lon, TC_lon], [-90.0, 90.0],   '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)
                        ax.text(TC_lon-4.6, TC_lat+4.4, extend_label, ha='left', va='center', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)

                        lat_polar = np.zeros((len(radii), len(angles)))
                        lon_polar = np.zeros((len(radii), len(angles)))
                        for idr in range(0, len(radii)):
                            for ida in range(0, len(angles)):
                                lat_polar[idr,ida], lon_polar[idr,ida] = clatlon.Cal_LatLon(TC_lat, TC_lon, radii[idr], angles[ida])
                            ax.plot(lon_polar[idr,:], lat_polar[idr,:], '--', color=grayC_cm_data[53], linewidth=0.5, zorder=3)

                        ax.set_xticks(np.arange(-180, 181, 5))
                        ax.set_yticks(np.arange(-90, 91, 5))
                        ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 5)])
                        ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  5)])
                        ax.tick_params('both', direction='in', labelsize=10.0)
                        ax.axis(extent)
                        ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                        clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
                        clb.set_label('6-hr Accumulated Precipitation (mm)', fontsize=10.0, labelpad=4.0)
                        clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                        clb.ax.minorticks_off()
                        #clb.set_ticks(rain_levels)
                        #clb.set_ticklabels(rain_labels)
                        clb.set_ticks(range(0, 56, 20))
                        clb.set_ticklabels(range(0, 56, 20))

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

def draw_analysis_increment(data_library_names, dir_cases, case_names, exp_names, variables = ['ua']):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        itime = attributes[(dir_case, case_name)]['itime']
        initial_time = datetime(*itime)
        da_domains = attributes[(dir_case, case_name)]['da_domains']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))

        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        dir_increment = os.path.join(dir_exp, 'increment')
        specific_case = '_'.join([case_name, exp_name, 'C'+str(total_da_cycles).zfill(2)])
        dir_increment_case = os.path.join(dir_increment, specific_case)
        os.makedirs(dir_increment, exist_ok=True)
        os.makedirs(dir_increment_case, exist_ok=True)

        for dom in tqdm(da_domains, desc='DA Domains', leave=False):
            for var in tqdm(variables, desc='Variables', leave=False):
                (information, levels) = set_variables(var)
                filename = os.path.join(dir_increment_case, '_'.join([var, 'analysis', 'increment', dom+'.nc']))
                ncfile = Dataset(filename)
                lat = ncfile.variables['lat'][:,:]
                lon = ncfile.variables['lon'][:,:]
                extent = [lon[0,0], lon[-1,-1], lat[0,0], lat[-1,-1]]
                fig_width = 2.75*np.abs(lon[-1,-1]-lon[0,0])/np.abs(lat[-1,-1]-lat[0,0])
                fig_height = 2.75+0.75
                clb_aspect = 25*np.abs(lon[-1,-1]-lon[0,0])/np.abs(lat[-1,-1]-lat[0,0])

                for idt in range(0, total_da_cycles):
                    time_now = anl_start_time + timedelta(hours = idt*cycling_interval)
                    time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')
                    image_files = []
                    output_file = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, dom+'.png']))

                    for lev in levels.keys():

                        idl = list(levels).index(lev)
                        (clblabels1, cmap1, clblabels2, cmap2) = levels[lev]

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.png']))
                        image_files.append(pngname)
                        with PdfPages(pdfname) as pdf:

                            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*ncfile.variables[var][idt,idl,0,:,:], levels=list(map(float, clblabels1)), cmap=cmap1, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                            clb.set_label(f"{information['lb_title']} of bkg at {lev} hPa", fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(list(map(float, clblabels1[0::2])))
                            clb.set_ticklabels(clblabels1[0::2])

                            plt.tight_layout()
                            plt.savefig(pngname, dpi=600)
                            pdf.savefig(fig)
                            plt.cla()
                            plt.clf()
                            plt.close()

                        command = f"convert {pngname} -trim {pngname}"
                        subprocess.run(command, shell=True)

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'anl', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'anl', str(lev).zfill(3)+'hPa', dom+'.png']))
                        image_files.append(pngname)
                        with PdfPages(pdfname) as pdf:

                            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*ncfile.variables[var][idt,idl,1,:,:], levels=list(map(float, clblabels1)), cmap=cmap1, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                            clb.set_label(f"{information['lb_title']} of anl at {lev} hPa", fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(list(map(float, clblabels1[0::2])))
                            clb.set_ticklabels(clblabels1[0::2])

                            plt.tight_layout()
                            plt.savefig(pngname, dpi=600)
                            pdf.savefig(fig)
                            plt.cla()
                            plt.clf()
                            plt.close()

                        command = f"convert {pngname} -trim {pngname}"
                        subprocess.run(command, shell=True)

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'inc', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'inc', str(lev).zfill(3)+'hPa', dom+'.png']))
                        image_files.append(pngname)
                        with PdfPages(pdfname) as pdf:

                            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*(ncfile.variables[var][idt,idl,1,:,:]-ncfile.variables[var][idt,idl,0,:,:]), levels=list(map(float, clblabels2)), cmap=cmap2, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                            clb.set_label(f"{information['lb_title']} of inc at {lev} hPa", fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(list(map(float, clblabels2[0::2])))
                            clb.set_ticklabels(clblabels2[0::2])

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

                    for lev in levels.keys():

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.png']))
                        os.system(f"rm -rf {pdfname}")
                        os.system(f"rm -rf {pngname}")

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'anl', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'anl', str(lev).zfill(3)+'hPa', dom+'.png']))
                        os.system(f"rm -rf {pdfname}")
                        os.system(f"rm -rf {pngname}")

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'inc', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'inc', str(lev).zfill(3)+'hPa', dom+'.png']))
                        os.system(f"rm -rf {pdfname}")
                        os.system(f"rm -rf {pngname}")

                ncfile.close()
