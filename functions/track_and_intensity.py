import os
import math
import datetime
import numpy as np
import pandas as pd
import climetlab as cml
import matplotlib.pyplot as plt
from data_library import attributes, compare_track_intensity_schemes
from tqdm.notebook import tqdm
from geopy.distance import great_circle
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
from IPython.display import Image, display

def calculate_track_intensity_errors(dir_case, case_name, exp_name):

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

    data = cml.load_source('file', NHC_best_track)
    bt_df = data.to_pandas()

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        for dom in GFDL_domains:

            case = '_'.join([case_name, exp_name, 'C' + str(da_cycle).zfill(2)])
            file_track_intensity = os.path.join(dir_exp, 'track_intensity', case_name, exp_name+'_C'+str(da_cycle).zfill(2), 'multi', 'fort.69')
            df = pd.read_csv(file_track_intensity, header=None, usecols=[2, 5, 6, 7, 8, 9])
            df.columns = ['Initial_Time', 'Forecast_Hour', 'LAT', 'LON', 'MWS (Knot)', 'MSLP (hPa)']
            df.drop_duplicates(subset=['Forecast_Hour'], keep='last', inplace=True)

            df.insert(loc=0, column='Date_Time', value=df.apply(lambda row: datetime.datetime.strptime(str(row['Initial_Time']), '%Y%m%d%H') +
                                                     datetime.timedelta(hours=row['Forecast_Hour'] / 100.0), axis=1))
            df.drop(columns=['Initial_Time', 'Forecast_Hour'], inplace=True)
            df['LAT'] = df['LAT'].str.extract('(\d+\.?\d*)N', expand=False).astype(float) * 0.1
            df['LON'] = df['LON'].str.extract('(\d+\.?\d*)W', expand=False).astype(float) * -0.1
            df.reset_index(drop=True, inplace=True)
            df.to_csv(dir_track_intensity + '/' + case + '_' + dom + '.csv', index=False)

            anl_start_time = datetime.datetime(*itime) + datetime.timedelta(hours=6.0)
            total_simulation_hours = forecast_hours + cycling_interval*(int(da_cycle-1))
            n_lead_time = int(total_simulation_hours/history_interval + 1)
            error_df = pd.DataFrame(0.0, index=np.arange(n_lead_time), columns=['Forecast_Hour', 'Track_Error (km)', 'MSLP_Error (hPa)', 'MWS_Error (Knot)'])
            error_df['Forecast_Hour'] = df['Date_Time'].apply(lambda x: (datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')-initial_time).total_seconds()/3600 if not pd.isna(x) else x)
            bt_df_Forecast_Hour = bt_df['Date_Time'].apply(lambda x: (datetime.datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')-initial_time).total_seconds()/3600 if not pd.isna(x) else x)

            bt_df_lat = np.interp(np.array(error_df['Forecast_Hour']), np.array(bt_df_Forecast_Hour), np.array(bt_df['LAT']))
            bt_df_lon = np.interp(np.array(error_df['Forecast_Hour']), np.array(bt_df_Forecast_Hour), np.array(bt_df['LON']))
            bt_df_MSLP = np.interp(np.array(error_df['Forecast_Hour']), np.array(bt_df_Forecast_Hour), np.array(bt_df['MSLP (hPa)']))
            bt_df_MWS = np.interp(np.array(error_df['Forecast_Hour']), np.array(bt_df_Forecast_Hour), np.array(bt_df['MWS (Knot)']))
            for idl in range(n_lead_time):
                loc = (df['LAT'][idl], df['LON'][idl])
                bt_loc = (bt_df_lat[idl], bt_df_lon[idl])
                error_df['Track_Error (km)'][idl] = great_circle(loc, bt_loc).kilometers
            error_df['MSLP_Error (hPa)'] = df['MSLP (hPa)'] - bt_df_MSLP
            error_df['MWS_Error (Knot)'] = df['MWS (Knot)'] - bt_df_MWS
            error_df.to_csv(dir_track_intensity + '/Error_' + case + '_' + dom + '.csv', index=False)

def compare_track(scheme):

    dir_grayC = '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7/grayC'
    grayC_cm_data = np.loadtxt(dir_grayC + '/grayC.txt')
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

    total_da_cycles = compare_track_intensity_schemes[scheme]['total_da_cycles']
    GFDL_domains = compare_track_intensity_schemes[scheme]['GFDL_domains']
    dir_save = compare_track_intensity_schemes[scheme]['dir_save']
    labels = compare_track_intensity_schemes[scheme]['labels']
    colors = compare_track_intensity_schemes[scheme]['colors']
    linestyles = compare_track_intensity_schemes[scheme]['linestyles']

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        for dom in GFDL_domains:

            pdfname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_track.pdf"
            pngname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_track.png"

            with PdfPages(pdfname) as pdf:

                fig, axs   = plt.subplots(1, 1, figsize=(3.25, 3.0))
                fig.subplots_adjust(left=0.125, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.100)

                (dir_case, case_name, exp_name) = compare_track_intensity_schemes[scheme]['cases'][0]
                itime = attributes[(dir_case, case_name)]['itime']
                forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                history_interval = attributes[(dir_case, case_name)]['history_interval']
                dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']

                initial_time = datetime.datetime(*itime)
                anl_start_time = initial_time + datetime.timedelta(hours=6.0)
                anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
                forecast_start_time = anl_end_time
                forecast_end_time = forecast_start_time + datetime.timedelta(hours=forecast_hours)

                NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']
                df = pd.read_csv(NHC_best_track)
                index = [idx for idx, Date_Time in enumerate(df['Date_Time']) if forecast_start_time <= datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S') <= forecast_end_time]
                lat = list(df['LAT'][index])
                lon = list(df['LON'][index])
                dt = list(df['Date_Time'][index])
                idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

                clon = 5*(lon[0]+lon[-1])/2.0//5
                clat = 5*(lat[0]+lat[-1])/2.0//5
                half_extent = np.max([5*abs(lon[-1]-clon)//5+5, 5*abs(lat[-1]-clat)//5+5, 15])
                extent = [clon-half_extent+5.0, clon+half_extent, clat-half_extent+5.0, clat+half_extent]

                ax = axs
                m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='h', ax=ax)
                m.drawcoastlines(linewidth=0.2, color='k')
                # Draw best track
                ax.plot(lon, lat, 'o', color='k', ls='-', ms=4.00, linewidth=2.50, label='NHC', zorder=3)
                ax.plot(lon[idx_forecast_start_time::4], lat[idx_forecast_start_time::4], 'o', color='w', ms=1.50, zorder=3)
                for idx in range(idx_forecast_start_time, len(lon), 4):
                    ax.text(lon[idx]+0.50, lat[idx]+0.50, dt[idx][8:10], ha='center', va='center', color='k', fontsize=10.0, zorder=4)

                for idc, (dir_case, case_name, exp_name) in enumerate(compare_track_intensity_schemes[scheme]['cases']):

                    itime = attributes[(dir_case, case_name)]['itime']
                    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                    history_interval = attributes[(dir_case, case_name)]['history_interval']
                    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']

                    initial_time = datetime.datetime(*itime)
                    anl_start_time = initial_time + datetime.timedelta(hours=6.0)
                    anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
                    forecast_start_time = anl_end_time
                    forecast_end_time = forecast_start_time + datetime.timedelta(hours=forecast_hours)

                    case = '_'.join([case_name, exp_name + '_C' + str(da_cycle).zfill(2)])
                    filename = f"{dir_track_intensity}/{case}_{dom}.csv"
                    df = pd.read_csv(filename)
                    index = [idx for idx, Date_Time in enumerate(df['Date_Time']) if forecast_start_time <= datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S') <= forecast_end_time]
                    lat = list(df['LAT'][index])
                    lon = list(df['LON'][index])

                    idx_forecast_start_time = int(int((24-float(forecast_start_time.strftime('%H')))%24/6)*(6/history_interval))
                    ax.plot(lon, lat, color=colors[idc], ls=linestyles[idc], ms=2.00, linewidth=1.25, label=labels[idc], zorder=3)
                    ax.plot(lon[::int(6/history_interval)], lat[::int(6/history_interval)], 'o', color=colors[idc], ms=2.00, zorder=3)
                    ax.plot(lon[idx_forecast_start_time::int(24/history_interval)], lat[idx_forecast_start_time::int(24/history_interval)], 'o', color='w', ms=0.75, zorder=3)

                ax.set_xticks(np.arange(extent[0], extent[1]+1, 10))
                ax.set_yticks(np.arange(extent[2]+5.0, extent[3]+1, 10))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(extent[0]), int(extent[1])+1, 10)])
                ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(extent[2]+5.0), int(extent[3])+1, 10)])
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                ax.legend(loc='upper right', fontsize=5.0, handlelength=2.5).set_zorder(102)

                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

                img = Image(filename=pngname)
                display(img)

def compare_MSLP(scheme):

    total_da_cycles = compare_track_intensity_schemes[scheme]['total_da_cycles']
    GFDL_domains = compare_track_intensity_schemes[scheme]['GFDL_domains']
    dir_save = compare_track_intensity_schemes[scheme]['dir_save']
    labels = compare_track_intensity_schemes[scheme]['labels']
    colors = compare_track_intensity_schemes[scheme]['colors']
    linestyles = compare_track_intensity_schemes[scheme]['linestyles']

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        for dom in GFDL_domains:

            pdfname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_MSLP.pdf"
            pngname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_MSLP.png"

            with PdfPages(pdfname) as pdf:

                fig = plt.figure(1, [7.5, 9.0])
                fig.subplots_adjust(left=0.100, bottom=0.050, right=0.950, top=0.975, wspace=0.000, hspace=0.150)

                ax = fig.add_subplot(211)
                for idc, (dir_case, case_name, exp_name) in enumerate(compare_track_intensity_schemes[scheme]['cases']):

                    itime = attributes[(dir_case, case_name)]['itime']
                    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                    history_interval = attributes[(dir_case, case_name)]['history_interval']
                    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']

                    initial_time = datetime.datetime(*itime)
                    anl_start_time = initial_time + datetime.timedelta(hours=6.0)
                    anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
                    forecast_start_time = anl_end_time
                    forecast_end_time = forecast_start_time + datetime.timedelta(hours=forecast_hours)

                    if idc == 0:
                        NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']
                        df = pd.read_csv(NHC_best_track)

                        index = []
                        formatted_date_labels = []
                        for idx, Date_Time in enumerate(df['Date_Time']):
                            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                            if time_now >= forecast_start_time and time_now <= forecast_end_time:
                                index = index + [idx]
                                formatted_date_labels = formatted_date_labels + [time_now.strftime("%H UTC\n%d %b")]

                        MSLP_bt = list(df['MSLP (hPa)'][index])
                        MWS_bt = list(df['MWS (Knot)'][index])
                        idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

                        extent = [0, len(MSLP_bt)-1, 940.0, 1020.0]
                        x_tick_labels = ['']*len(MSLP_bt)
                        x_tick_labels[idx_forecast_start_time::4] = formatted_date_labels[idx_forecast_start_time::4]

                        # Draw best track
                        ax.plot(np.arange(len(MSLP_bt)), MSLP_bt, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
                        ax.plot(np.arange(idx_forecast_start_time, len(MSLP_bt), 4), MSLP_bt[idx_forecast_start_time::4], 'o', color='w', ms=1.00, zorder=3)

                    case = '_'.join([case_name, exp_name + '_C' + str(da_cycle).zfill(2)])
                    filename = f"{dir_track_intensity}/{case}_{dom}.csv"
                    df = pd.read_csv(filename)

                    index = []
                    for idx, Date_Time in enumerate(df['Date_Time']):
                        time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                        if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]

                    MSLP = list(df['MSLP (hPa)'][index])

                    idx_forecast_start_time = int(int((24-float(forecast_start_time.strftime('%H')))%24/6)*(6/history_interval))
                    ax.plot(np.arange(0, len(MSLP))/(6.0/history_interval), MSLP, color=colors[idc], ls=linestyles[idc], ms=2.00, linewidth=1.20, label=labels[idc], zorder=3)
                    ax.plot(np.arange(0, len(MSLP), 6/history_interval)/(6.0/history_interval), MSLP[::int(6/history_interval)], 'o', color=colors[idc], ms=2.00, zorder=3)
                    ax.plot(np.arange(idx_forecast_start_time, len(MSLP), 24/history_interval)/(6.0/history_interval), MSLP[idx_forecast_start_time::int(24/history_interval)], 'o', color='w', ms=0.80, zorder=3)

                ax.set_xticks(np.arange(0, len(MSLP_bt), 1))
                ax.set_xticklabels(x_tick_labels)
                ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
                ax.set_ylabel('Time', fontsize=10.0)
                ax.set_ylabel('MSLP (hPa)', fontsize=10.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5)
                ax.legend(loc='lower left', fontsize=10.0, handlelength=2.5)

                ax = fig.add_subplot(212)
                for idc, (dir_case, case_name, exp_name) in enumerate(compare_track_intensity_schemes[scheme]['cases']):

                    itime = attributes[(dir_case, case_name)]['itime']
                    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                    history_interval = attributes[(dir_case, case_name)]['history_interval']
                    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']

                    initial_time = datetime.datetime(*itime)
                    anl_start_time = initial_time + datetime.timedelta(hours=6.0)
                    anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
                    forecast_start_time = anl_end_time
                    forecast_end_time = forecast_start_time + datetime.timedelta(hours=forecast_hours)

                    if idc == 0:
                        NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']
                        df = pd.read_csv(NHC_best_track)

                        index = []
                        formatted_date_labels = []
                        for idx, Date_Time in enumerate(df['Date_Time']):
                            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                            if time_now >= forecast_start_time and time_now <= forecast_end_time:
                                index = index + [idx]
                                formatted_date_labels = formatted_date_labels + [time_now.strftime("%H UTC\n%d %b")]

                        MSLP_bt = list(df['MSLP (hPa)'][index])
                        MWS_bt = list(df['MWS (Knot)'][index])
                        idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

                        extent = [0, len(MWS_bt)-1, 20.0, 120.0]
                        x_tick_labels = ['']*len(MWS_bt)
                        x_tick_labels[idx_forecast_start_time::4] = formatted_date_labels[idx_forecast_start_time::4]

                        # Draw best track
                        ax.plot(np.arange(len(MWS_bt)), MWS_bt, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
                        ax.plot(np.arange(idx_forecast_start_time, len(MWS_bt), 4), MWS_bt[idx_forecast_start_time::4], 'o', color='w', ms=1.00, zorder=3)

                    case = '_'.join([case_name, exp_name + '_C' + str(da_cycle).zfill(2)])
                    filename = f"{dir_track_intensity}/{case}_{dom}.csv"
                    df = pd.read_csv(filename)

                    index = []
                    for idx, Date_Time in enumerate(df['Date_Time']):
                        time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                        if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]

                    MWS = list(df['MWS (Knot)'][index])

                    idx_forecast_start_time = int(int((24-float(forecast_start_time.strftime('%H')))%24/6)*(6/history_interval))
                    ax.plot(np.arange(0, len(MWS))/(6.0/history_interval), MWS, color=colors[idc], ls=linestyles[idc], ms=2.00, linewidth=1.20, label=labels[idc], zorder=3)
                    ax.plot(np.arange(0, len(MWS), 6/history_interval)/(6.0/history_interval), MWS[::int(6/history_interval)], 'o', color=colors[idc], ms=2.00, zorder=3)
                    ax.plot(np.arange(idx_forecast_start_time, len(MWS), 24/history_interval)/(6.0/history_interval), MWS[idx_forecast_start_time::int(24/history_interval)], 'o', color='w', ms=0.80, zorder=3)

                ax.set_xticks(np.arange(0, len(MWS_bt), 1))
                ax.set_xticklabels(x_tick_labels)
                ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
                ax.set_ylabel('Time', fontsize=10.0)
                ax.set_ylabel('MWS (Knot)', fontsize=10.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5)
                ax.legend(loc='upper left', fontsize=10.0, handlelength=2.5)

                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

                img = Image(filename=pngname)
                display(img)

def compare_intensity(scheme):

    total_da_cycles = compare_track_intensity_schemes[scheme]['total_da_cycles']
    GFDL_domains = compare_track_intensity_schemes[scheme]['GFDL_domains']
    dir_save = compare_track_intensity_schemes[scheme]['dir_save']
    labels = compare_track_intensity_schemes[scheme]['labels']
    colors = compare_track_intensity_schemes[scheme]['colors']
    linestyles = compare_track_intensity_schemes[scheme]['linestyles']

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        for dom in GFDL_domains:

            pdfname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_intensity.pdf"
            pngname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_intensity.png"

            with PdfPages(pdfname) as pdf:

                fig = plt.figure(1, [7.5, 9.0])
                fig.subplots_adjust(left=0.100, bottom=0.050, right=0.950, top=0.975, wspace=0.000, hspace=0.150)

                ax = fig.add_subplot(211)
                for idc, (dir_case, case_name, exp_name) in enumerate(compare_track_intensity_schemes[scheme]['cases']):

                    itime = attributes[(dir_case, case_name)]['itime']
                    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                    history_interval = attributes[(dir_case, case_name)]['history_interval']
                    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']

                    initial_time = datetime.datetime(*itime)
                    anl_start_time = initial_time + datetime.timedelta(hours=6.0)
                    anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
                    forecast_start_time = anl_end_time
                    forecast_end_time = forecast_start_time + datetime.timedelta(hours=forecast_hours)

                    if idc == 0:
                        NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']
                        df = pd.read_csv(NHC_best_track)

                        index = []
                        formatted_date_labels = []
                        for idx, Date_Time in enumerate(df['Date_Time']):
                            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                            if time_now >= forecast_start_time and time_now <= forecast_end_time:
                                index = index + [idx]
                                formatted_date_labels = formatted_date_labels + [time_now.strftime("%H UTC\n%d %b")]

                        MSLP_bt = list(df['MSLP (hPa)'][index])
                        MWS_bt = list(df['MWS (Knot)'][index])
                        idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

                        extent = [0, len(MSLP_bt)-1, 940.0, 1020.0]
                        x_tick_labels = ['']*len(MSLP_bt)
                        x_tick_labels[idx_forecast_start_time::4] = formatted_date_labels[idx_forecast_start_time::4]

                        # Draw best track
                        ax.plot(np.arange(len(MSLP_bt)), MSLP_bt, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
                        ax.plot(np.arange(idx_forecast_start_time, len(MSLP_bt), 4), MSLP_bt[idx_forecast_start_time::4], 'o', color='w', ms=1.00, zorder=3)

                    case = '_'.join([case_name, exp_name + '_C' + str(da_cycle).zfill(2)])
                    filename = f"{dir_track_intensity}/{case}_{dom}.csv"
                    df = pd.read_csv(filename)

                    index = []
                    for idx, Date_Time in enumerate(df['Date_Time']):
                        time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                        if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]

                    MSLP = list(df['MSLP (hPa)'][index])

                    idx_forecast_start_time = int(int((24-float(forecast_start_time.strftime('%H')))%24/6)*(6/history_interval))
                    ax.plot(np.arange(0, len(MSLP))/(6.0/history_interval), MSLP, color=colors[idc], ls=linestyles[idc], ms=2.00, linewidth=1.20, label=labels[idc], zorder=3)
                    ax.plot(np.arange(0, len(MSLP), 6/history_interval)/(6.0/history_interval), MSLP[::int(6/history_interval)], 'o', color=colors[idc], ms=2.00, zorder=3)
                    ax.plot(np.arange(idx_forecast_start_time, len(MSLP), 24/history_interval)/(6.0/history_interval), MSLP[idx_forecast_start_time::int(24/history_interval)], 'o', color='w', ms=0.80, zorder=3)

                ax.set_xticks(np.arange(0, len(MSLP_bt), 1))
                ax.set_xticklabels(x_tick_labels)
                ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
                ax.set_ylabel('Time', fontsize=10.0)
                ax.set_ylabel('MSLP (hPa)', fontsize=10.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5)
                ax.legend(loc='lower left', fontsize=10.0, handlelength=2.5)

                ax = fig.add_subplot(212)
                for idc, (dir_case, case_name, exp_name) in enumerate(compare_track_intensity_schemes[scheme]['cases']):

                    itime = attributes[(dir_case, case_name)]['itime']
                    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                    history_interval = attributes[(dir_case, case_name)]['history_interval']
                    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']

                    initial_time = datetime.datetime(*itime)
                    anl_start_time = initial_time + datetime.timedelta(hours=6.0)
                    anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
                    forecast_start_time = anl_end_time
                    forecast_end_time = forecast_start_time + datetime.timedelta(hours=forecast_hours)

                    if idc == 0:
                        NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']
                        df = pd.read_csv(NHC_best_track)

                        index = []
                        formatted_date_labels = []
                        for idx, Date_Time in enumerate(df['Date_Time']):
                            time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                            if time_now >= forecast_start_time and time_now <= forecast_end_time:
                                index = index + [idx]
                                formatted_date_labels = formatted_date_labels + [time_now.strftime("%H UTC\n%d %b")]

                        MSLP_bt = list(df['MSLP (hPa)'][index])
                        MWS_bt = list(df['MWS (Knot)'][index])
                        idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)

                        extent = [0, len(MWS_bt)-1, 20.0, 120.0]
                        x_tick_labels = ['']*len(MWS_bt)
                        x_tick_labels[idx_forecast_start_time::4] = formatted_date_labels[idx_forecast_start_time::4]

                        # Draw best track
                        ax.plot(np.arange(len(MWS_bt)), MWS_bt, 'o', color='k', ls='-', ms=2.50, linewidth=1.50, label='NHC', zorder=3)
                        ax.plot(np.arange(idx_forecast_start_time, len(MWS_bt), 4), MWS_bt[idx_forecast_start_time::4], 'o', color='w', ms=1.00, zorder=3)

                    case = '_'.join([case_name, exp_name + '_C' + str(da_cycle).zfill(2)])
                    filename = f"{dir_track_intensity}/{case}_{dom}.csv"
                    df = pd.read_csv(filename)

                    index = []
                    for idx, Date_Time in enumerate(df['Date_Time']):
                        time_now = datetime.datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                        if time_now >= forecast_start_time and time_now <= forecast_end_time: index = index + [idx]

                    MWS = list(df['MWS (Knot)'][index])

                    idx_forecast_start_time = int(int((24-float(forecast_start_time.strftime('%H')))%24/6)*(6/history_interval))
                    ax.plot(np.arange(0, len(MWS))/(6.0/history_interval), MWS, color=colors[idc], ls=linestyles[idc], ms=2.00, linewidth=1.20, label=labels[idc], zorder=3)
                    ax.plot(np.arange(0, len(MWS), 6/history_interval)/(6.0/history_interval), MWS[::int(6/history_interval)], 'o', color=colors[idc], ms=2.00, zorder=3)
                    ax.plot(np.arange(idx_forecast_start_time, len(MWS), 24/history_interval)/(6.0/history_interval), MWS[idx_forecast_start_time::int(24/history_interval)], 'o', color='w', ms=0.80, zorder=3)

                ax.set_xticks(np.arange(0, len(MWS_bt), 1))
                ax.set_xticklabels(x_tick_labels)
                ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
                ax.set_ylabel('Time', fontsize=10.0)
                ax.set_ylabel('MWS (Knot)', fontsize=10.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5)
                ax.legend(loc='upper left', fontsize=10.0, handlelength=2.5)

                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

                img = Image(filename=pngname)
                display(img)
