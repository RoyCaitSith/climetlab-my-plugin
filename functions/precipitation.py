import os
import h5py
import datetime
import importlib
import subprocess
import numpy as np
import pandas as pd
import cal_polar_to_latlon as clatlon
import matplotlib.pyplot as plt
from combine_and_show_images import combine_images_grid
from mpl_toolkits.basemap import Basemap
from tqdm.notebook import tqdm
from wrf import getvar, latlon_coords
from netCDF4 import Dataset
from scipy.interpolate import griddata
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import Image as IPImage

def calculate_6h_accumulated_precipitation(data_library_names, dir_cases, case_names, exp_names, imerg_exp_name='CONV'):

    accumulated_hours = 6.0
    IMERG_time_resolution = 0.5
    n_cases = len(dir_cases)

    for idc in tqdm(range(n_cases), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
        itime=attributes[(dir_case, case_name)]['itime']
        initial_time = datetime.datetime(*itime)
        forecast_hours=attributes[(dir_case, case_name)]['forecast_hours']
        dir_data=attributes[(dir_case, case_name)]['dir_data']
        dir_exp=attributes[(dir_case, case_name)]['dir_exp']
        GFDL_domains=attributes[(dir_case, case_name)]['GFDL_domains']
        cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
        history_interval=attributes[(dir_case, case_name)]['history_interval']
        dir_IMERG=os.path.join(dir_data, 'IMERG')

        for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', leave=False):

            anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)
            anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
            forecast_start_time = anl_end_time
            forecast_end_time = forecast_start_time + datetime.timedelta(hours=forecast_hours)
            n_time = int(forecast_hours/accumulated_hours)

            dir_rainfall = '/'.join([dir_exp, 'rainfall', case_name, exp_name+'_C'+str(da_cycle).zfill(2)])
            os.makedirs(dir_rainfall, exist_ok=True)

            for dom in tqdm(GFDL_domains, desc='GFDL Domains', leave=False):

                if 'IMERG' in exp_name:
                    dir_wrfout = '/'.join([dir_exp, 'cycling_da', f"{case_name}_{imerg_exp_name}_C{str(da_cycle).zfill(2)}", 'bkg'])
                else:
                    dir_wrfout = '/'.join([dir_exp, 'cycling_da', f"{case_name}_{exp_name}_C{str(da_cycle).zfill(2)}", 'bkg'])
                wrfout = dir_wrfout + f'/wrfout_{dom}_' + initial_time.strftime('%Y-%m-%d_%H:%M:00')
                ncfile = Dataset(wrfout)
                RAINNC = getvar(ncfile, 'RAINNC')
                ncfile.close()

                lat, lon = latlon_coords(RAINNC)
                (n_lat, n_lon) = lat.shape

                filename = dir_rainfall + f'/rainfall_6h_{dom}.nc'
                ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                ncfile_output.createDimension('n_time', n_time)
                ncfile_output.createDimension('n_lat',  n_lat)
                ncfile_output.createDimension('n_lon',  n_lon)
                ncfile_output.createVariable('lat',      'f8', ('n_lat', 'n_lon'))
                ncfile_output.createVariable('lon',      'f8', ('n_lat', 'n_lon'))
                ncfile_output.createVariable('rainfall', 'f8', ('n_time', 'n_lat', 'n_lon'))

                ncfile_output.variables['lat'][:,:] = lat
                ncfile_output.variables['lon'][:,:] = lon
                ncfile_output.variables['rainfall'][:,:,:] = 0.0

                for idt in tqdm(range(n_time), desc="Time", leave=False):

                    time_now = forecast_start_time + datetime.timedelta(hours = idt*6.0)

                    if 'IMERG' in exp_name:

                        IMERG_prep = np.zeros((3600, 1800), dtype=float)

                        for dh in np.arange(0.0, accumulated_hours, IMERG_time_resolution):

                            time_IMERG = time_now + datetime.timedelta(hours=dh)
                            YYMMDD = time_IMERG.strftime('%Y%m%d')
                            HHMMSS = time_IMERG.strftime('%H%M%S')

                            info = os.popen(f'ls {dir_IMERG}/{YYMMDD}/3B-HHR.MS.MRG.3IMERG.{YYMMDD}-S{HHMMSS}*').readlines()
                            file_IMERG = info[0].strip()
                            f = h5py.File(file_IMERG)
                            IMERG_prep = IMERG_prep + IMERG_time_resolution*f['Grid']['precipitationCal'][0,:,:]

                        IMERG_prep  = IMERG_prep/accumulated_hours
                        IMERG_lat   = np.tile(f['Grid']['lat'][:], (3600, 1))
                        IMERG_lon   = np.transpose(np.tile(f['Grid']['lon'][:], (1800, 1)))
                        IMERG_index = (IMERG_lat < np.array(lat[-1, -1]) + 15.0) & (IMERG_lat > np.array(lat[0, 0]) - 15.0) & \
                                      (IMERG_lon < np.array(lon[-1, -1]) + 15.0) & (IMERG_lon > np.array(lon[0, 0]) - 15.0)

                        IMERG_prep_1d = IMERG_prep[IMERG_index]
                        IMERG_lat_1d  = IMERG_lat[IMERG_index]
                        IMERG_lon_1d  = IMERG_lon[IMERG_index]
                        ncfile_output.variables['rainfall'][idt,:,:] = griddata((IMERG_lon_1d, IMERG_lat_1d), IMERG_prep_1d, (lon, lat), method='linear')

                    else:

                        for idx in range(0, int(accumulated_hours), history_interval):

                            time_0 = time_now + datetime.timedelta(hours = idx)
                            time_1 = time_now + datetime.timedelta(hours = idx+history_interval)

                            wrfout_0 = dir_wrfout + '/wrfout_' + dom + '_' + time_0.strftime('%Y-%m-%d_%H:%M:00')
                            wrfout_1 = dir_wrfout + '/wrfout_' + dom + '_' + time_1.strftime('%Y-%m-%d_%H:%M:00')

                            ncfile   = Dataset(wrfout_0)
                            RAINNC_0 = getvar(ncfile, 'RAINNC')
                            RAINC_0  = getvar(ncfile, 'RAINC')
                            ncfile.close()

                            ncfile   = Dataset(wrfout_1)
                            RAINNC_1 = getvar(ncfile, 'RAINNC')
                            RAINC_1  = getvar(ncfile, 'RAINC')
                            ncfile.close()

                            if time_0 == anl_end_time:
                                RAINNC_0 = 0.0
                                RAINC_0 = 0.0

                            rainfall = RAINNC_1 + RAINC_1 - RAINNC_0 - RAINC_0
                            ncfile_output.variables['rainfall'][idt,:,:] = ncfile_output.variables['rainfall'][idt,:,:] + rainfall

                        ncfile_output.variables['rainfall'][idt,:,:] = ncfile_output.variables['rainfall'][idt,:,:]/accumulated_hours

                ncfile_output.close()

def draw_6h_accumulated_precipitation(data_library_name, scheme):

    accumulated_hours = 6.0

    #rain_levels = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4, 0.6, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, \
                   #6.0, 8.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0]
    #rain_labels = ['0.1', '0.15', '0.2', '0.25', '0.3', '0.4', '0.6', '1.0', '1.5', \
                   #'2', '3', '4', '5', '6', '8', '10', '15', '20', '25', '30', '35', '40']

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
    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time = datetime.datetime(*itime)
    forecast_hours=attributes[(dir_case, case_name)]['forecast_hours']
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    GFDL_domains=attributes[(dir_case, case_name)]['GFDL_domains']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    history_interval=attributes[(dir_case, case_name)]['history_interval']
    dir_track_intensity=attributes[(dir_case, case_name)]['dir_track_intensity']
    NHC_best_track=attributes[(dir_case, case_name)]['NHC_best_track']

    for dom in tqdm(GFDL_domains, desc='GFDL Domains', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        for da_cycle in tqdm(range(1, total_da_cycles+1), desc="Cycles", leave=False):

            anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)
            anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
            forecast_start_time = anl_end_time
            forecast_end_time = forecast_start_time + datetime.timedelta(hours=forecast_hours)
            n_time = int(forecast_hours/accumulated_hours)

            for idt in tqdm(range(n_time), desc="Time", leave=False):

                time_now = forecast_start_time + datetime.timedelta(hours=idt*accumulated_hours)
                time_label = time_now + datetime.timedelta(hours=accumulated_hours/2.0)
                time_now_str = time_now.strftime('%Y%m%d%H')
                time_label_str = time_label.strftime('%H UTC %d %b')

                image_files = []
                dir_rainfall = '/'.join([dir_exp, 'rainfall', case_name, 'Figures'])
                output_file = dir_rainfall + '/' + '_'.join([time_now_str, 'rainfall', '6h', scheme, 'C'+str(da_cycle).zfill(2), dom+'.png'])

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

                        time_end = time_now + datetime.timedelta(hours = accumulated_hours)
                        for id_TC, TC_date in enumerate(TC_dates):
                            TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
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
                        pcm = ax.contourf(rain_lon, rain_lat, rain_masked, levels=range(5, 56, 5), cmap='jet', extend='max', zorder=1)
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
                        clb.set_ticks(range(5, 56, 10))
                        clb.set_ticklabels(range(5, 56, 10))

                        plt.tight_layout()
                        plt.savefig(pngname, dpi=600)
                        pdf.savefig(fig)
                        plt.cla()
                        plt.clf()
                        plt.close()

                for idc in tqdm(range(n_cases), desc="Cases", leave=False):

                    (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][idc]
                    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
                    dir_track_intensity=attributes[(dir_case, case_name)]['dir_track_intensity']
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

                        time_end = time_now + datetime.timedelta(hours = accumulated_hours)
                        for id_TC, TC_date in enumerate(TC_dates):
                            TC_datetime = datetime.datetime.strptime(TC_date, '%Y-%m-%d %H:%M:%S')
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
                        pcm = ax.contourf(rain_lon, rain_lat, rain_masked, levels=range(5, 56, 5), cmap='jet', extend='max', zorder=1)
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
                        clb.set_ticks(range(5, 56, 10))
                        clb.set_ticklabels(range(5, 56, 10))

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
