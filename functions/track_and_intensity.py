import os
import math
import importlib
import subprocess
import numpy as np
import pandas as pd
import climetlab as cml
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from combine_and_show_images import combine_images_grid
from tqdm.notebook import tqdm
from geopy.distance import great_circle
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.basemap import Basemap
from IPython.display import Image as IPImage

def display_ibtracs_climetlab(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    ibtracs=attributes[(dir_case, case_name)]['ibtracs']
    dir_best_track=os.path.join(dir_exp, 'track_intensity', 'best_track')

    ibtracs_cml = cml.load_source('file', os.path.join(dir_best_track, ibtracs['filename']))
    ibtracs_pd = ibtracs_cml.to_pandas()
    ibtracs_pd = ibtracs_pd[(ibtracs_pd.NAME == ibtracs['name']) & (ibtracs_pd.SEASON == ibtracs['season'])]
    cml.plot_map(ibtracs_pd, style="cyclone-track")
    print(ibtracs_pd)

def display_NHC_best_track_climetlab(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    NHC_best_track=attributes[(dir_case, case_name)]['NHC_best_track']
    dir_best_track=os.path.join(dir_exp, 'track_intensity', 'best_track')

    NHC_cml = cml.load_source('file', os.path.join(dir_best_track, NHC_best_track))
    NHC_pd = NHC_cml.to_pandas()
    cml.plot_map(NHC_pd, style="cyclone-track")
    print(NHC_pd)

def calculate_track_intensity_errors(data_library_name, dir_case, case_name, exp_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    initial_time=datetime(*itime)
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    GFDL_domains=attributes[(dir_case, case_name)]['GFDL_domains']
    NHC_best_track=attributes[(dir_case, case_name)]['NHC_best_track']

    dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
    dir_best_track = os.path.join(dir_track_intensity, 'best_track')
    data = cml.load_source('file', os.path.join(dir_best_track, NHC_best_track))
    bt_df = data.to_pandas()

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        for dom in GFDL_domains:

            case = '_'.join([case_name, exp_name, 'C' + str(da_cycle).zfill(2)])
            file_track_intensity = os.path.join(dir_exp, 'track_intensity', case, 'multi', 'fort.69')
            df = pd.read_csv(file_track_intensity, header=None, usecols=[2, 5, 6, 7, 8, 9])
            df.columns = ['Initial_Time', 'Forecast_Hour', 'LAT', 'LON', 'MWS (Knot)', 'MSLP (hPa)']
            df.drop_duplicates(subset=['Forecast_Hour'], keep='last', inplace=True)

            df.insert(loc=0, column='Date_Time', value=df.apply(lambda row: datetime.strptime(str(row['Initial_Time']), '%Y%m%d%H') +
                                                     timedelta(hours=row['Forecast_Hour'] / 100.0), axis=1))
            df.drop(columns=['Initial_Time', 'Forecast_Hour'], inplace=True)
            df['LAT'] = df['LAT'].str.extract('(\d+\.?\d*)N', expand=False).astype(float) * 0.1
            df['LON'] = df['LON'].str.extract('(\d+\.?\d*)W', expand=False).astype(float) * -0.1
            df.reset_index(drop=True, inplace=True)
            df.to_csv(dir_best_track + '/' + case + '_' + dom + '.csv', index=False)

            n_lead_time = df.shape[0]
            error_df = pd.DataFrame(0.0, index=np.arange(n_lead_time), columns=['Forecast_Hour', 'Track_Error (km)', 'MSLP_Error (hPa)', 'MWS_Error (Knot)'])
            error_df['Forecast_Hour'] = df['Date_Time'].apply(lambda x: (datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')-initial_time).total_seconds()/3600 if not pd.isna(x) else x)
            bt_df_Forecast_Hour = bt_df['Date_Time'].apply(lambda x: (datetime.strptime(str(x), '%Y-%m-%d %H:%M:%S')-initial_time).total_seconds()/3600 if not pd.isna(x) else x)

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
            error_df.to_csv(dir_best_track + '/Error_' + case + '_' + dom + '.csv', index=False)

def compare_track_scheme(data_library_name, scheme):

    module = importlib.import_module(f"data_library_{data_library_name}")
    compare_schemes = getattr(module, 'compare_schemes')
    attributes = getattr(module, 'attributes')

    (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][0]
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    GFDL_domains = attributes[(dir_case, case_name)]['GFDL_domains']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
    dir_save = compare_schemes[scheme]['dir_save']
    labels = compare_schemes[scheme]['labels']
    colors = compare_schemes[scheme]['colors']
    linestyles = compare_schemes[scheme]['linestyles']

    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        for dom in GFDL_domains:

            pdfname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_track.pdf"
            pngname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_track.png"

            with PdfPages(pdfname) as pdf:

                fig, axs   = plt.subplots(1, 1, figsize=(3.25, 3.0))
                #fig.subplots_adjust(left=0.125, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.100)

                (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][0]
                itime = attributes[(dir_case, case_name)]['itime']
                dir_exp = attributes[(dir_case, case_name)]['dir_exp']
                forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                history_interval = attributes[(dir_case, case_name)]['history_interval']
                NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']

                dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
                dir_best_track = os.path.join(dir_track_intensity, 'best_track')

                initial_time = datetime(*itime)
                anl_start_time = initial_time + timedelta(hours=cycling_interval)
                anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
                forecast_start_time = anl_end_time
                forecast_end_time = forecast_start_time + timedelta(hours=forecast_hours)
                
                df = pd.read_csv(os.path.join(dir_best_track, NHC_best_track))
                index = [idx for idx, Date_Time in enumerate(df['Date_Time']) if forecast_start_time <= datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S') <= forecast_end_time]
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

                for idc, (dir_case, case_name, exp_name) in enumerate(compare_schemes[scheme]['cases']):

                    itime = attributes[(dir_case, case_name)]['itime']
                    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
                    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                    history_interval = attributes[(dir_case, case_name)]['history_interval']
                    dir_track_intensity = os.path.join(dir_exp, 'track_intensity')

                    initial_time = datetime(*itime)
                    anl_start_time = initial_time + timedelta(hours=cycling_interval)
                    anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
                    forecast_start_time = anl_end_time
                    forecast_end_time = forecast_start_time + timedelta(hours=forecast_hours)

                    case = '_'.join([case_name, exp_name + '_C' + str(da_cycle).zfill(2)])
                    filename = f"{dir_best_track}/{case}_{dom}.csv"
                    df = pd.read_csv(filename)
                    index = []
                    time_now = forecast_start_time
                    while time_now <= forecast_end_time:
                        for idx, Date_Time in enumerate(df['Date_Time']):
                            if time_now == datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S'): index.append(idx)
                        time_now = time_now + timedelta(hours=history_interval)
                    lat = list(df['LAT'][index])
                    lon = list(df['LON'][index])

                    idx_forecast_start_time = int(int((24-float(forecast_start_time.strftime('%H')))%24/6)*(6/history_interval))
                    ax.plot(lon, lat, color=colors[idc], ls=linestyles[idc], ms=2.00, linewidth=1.25, label=labels[idc]+'_C'+str(da_cycle).zfill(2), zorder=3)
                    ax.plot(lon[::int(6/history_interval)], lat[::int(6/history_interval)], 'o', color=colors[idc], ms=2.00, zorder=3)
                    ax.plot(lon[idx_forecast_start_time::int(24/history_interval)], lat[idx_forecast_start_time::int(24/history_interval)], 'o', color='w', ms=0.75, zorder=3)

                ax.set_xticks(np.arange(-180, 181, 5))
                ax.set_yticks(np.arange(-90, 91, 5))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 5)])
                ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  5)])
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                ax.legend(loc='upper right', fontsize=5.0, handlelength=2.5).set_zorder(102)

                plt.tight_layout()
                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

    for dom in GFDL_domains:
        image_files = []
        output_file = dir_save + f"/{scheme}_{dom}_all_track.png"
        for da_cycle in range(1, total_da_cycles+1):
            image_files.append(dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_track.png")

        combine_images_grid(image_files, output_file)
        command = f"convert {output_file} -trim {output_file}"
        subprocess.run(command, shell=True)
        image = IPImage(filename=output_file)
        display(image)

def compare_intensity_scheme(data_library_name, scheme, variable):

    module = importlib.import_module(f"data_library_{data_library_name}")
    compare_schemes = getattr(module, 'compare_schemes')
    attributes = getattr(module, 'attributes')

    (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][0]
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    GFDL_domains = attributes[(dir_case, case_name)]['GFDL_domains']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
    dir_save = compare_schemes[scheme]['dir_save']
    labels = compare_schemes[scheme]['labels']
    colors = compare_schemes[scheme]['colors']
    linestyles = compare_schemes[scheme]['linestyles']

    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Cycles', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        for dom in GFDL_domains:

            if 'MSLP' in variable: varname = 'MSLP'
            if 'MWS' in variable:  varname = 'MWS'

            pdfname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_{varname}.pdf"
            pngname = dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_{varname}.png"

            with PdfPages(pdfname) as pdf:

                fig, axs   = plt.subplots(1, 1, figsize=(3.25, 3.0))
                #fig.subplots_adjust(left=0.125, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.100)

                (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][0]
                itime = attributes[(dir_case, case_name)]['itime']
                forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']
                dir_exp = attributes[(dir_case, case_name)]['dir_exp']
                dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
                dir_best_track = os.path.join(dir_track_intensity, 'best_track')

                initial_time = datetime(*itime)
                anl_start_time = initial_time + timedelta(hours=cycling_interval)
                anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
                forecast_start_time = anl_end_time
                forecast_end_time = forecast_start_time + timedelta(hours=forecast_hours)

                df = pd.read_csv(os.path.join(dir_best_track, NHC_best_track))

                index = []
                formatted_date_labels = []
                for idx, Date_Time in enumerate(df['Date_Time']):
                    time_now = datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S')
                    if time_now >= forecast_start_time and time_now <= forecast_end_time:
                        index.append(idx)
                        #formatted_date_labels.append(time_now.strftime("%H UTC\n%d %b"))
                        formatted_date_labels.append(time_now.strftime("%d"))

                var_bt = list(df[variable][index])

                idx_forecast_start_time = int((24-float(forecast_start_time.strftime('%H')))%24/6)
                extent = [0, len(var_bt)-1, 10.0*math.floor(min(var_bt)/10.0)-10.0, 10.0*math.ceil(max(var_bt)/10.0)+10.0]
                x_tick_labels = ['']*len(var_bt)
                x_tick_labels[idx_forecast_start_time::4] = formatted_date_labels[idx_forecast_start_time::4]

                # Draw best track
                ax = axs
                ax.plot(np.arange(len(var_bt)), var_bt, 'o', color='k', ls='-', ms=4.00, linewidth=2.50, label='NHC', zorder=3)
                ax.plot(np.arange(idx_forecast_start_time, len(var_bt), 4), var_bt[idx_forecast_start_time::4], 'o', color='w', ms=1.50, zorder=3)

                for idc, (dir_case, case_name, exp_name) in enumerate(compare_schemes[scheme]['cases']):

                    itime = attributes[(dir_case, case_name)]['itime']
                    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
                    history_interval = attributes[(dir_case, case_name)]['history_interval']

                    initial_time = datetime(*itime)
                    anl_start_time = initial_time + timedelta(hours=cycling_interval)
                    anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
                    forecast_start_time = anl_end_time
                    forecast_end_time = forecast_start_time + timedelta(hours=forecast_hours)

                    case = '_'.join([case_name, exp_name + '_C' + str(da_cycle).zfill(2)])
                    filename = f"{dir_best_track}/{case}_{dom}.csv"
                    df = pd.read_csv(filename)
                    index = []
                    time_now = forecast_start_time
                    while time_now <= forecast_end_time:
                        for idx, Date_Time in enumerate(df['Date_Time']):
                            if time_now == datetime.strptime(Date_Time, '%Y-%m-%d %H:%M:%S'): index.append(idx)
                        time_now = time_now + timedelta(hours=history_interval)
                    var = list(df[variable][index])

                    idx_forecast_start_time = int(int((24-float(forecast_start_time.strftime('%H')))%24/6)*(6/history_interval))
                    ax.plot(np.arange(0, len(var))/(6.0/history_interval), var, color=colors[idc], ls=linestyles[idc], ms=2.00, linewidth=1.25, label=labels[idc]+'_C'+str(da_cycle).zfill(2), zorder=3)
                    ax.plot(np.arange(0, len(var), 6/history_interval)/(6.0/history_interval), var[::int(6/history_interval)], 'o', color=colors[idc], ms=2.00, zorder=3)
                    ax.plot(np.arange(idx_forecast_start_time, len(var), 24/history_interval)/(6.0/history_interval), var[idx_forecast_start_time::int(24/history_interval)], 'o', color='w', ms=0.75, zorder=3)

                ax.set_xticks(np.arange(0, len(var_bt), 1))
                ax.set_xticklabels(x_tick_labels)
                ax.set_yticks(np.arange(extent[2], extent[3]+1, 10))
                ax.set_ylabel(variable, fontsize=10.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis(extent)
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                if 'MSLP' in variable: ax.legend(loc='lower left', fontsize=5.0, handlelength=2.5).set_zorder(102)
                if 'MWS' in variable:  ax.legend(loc='upper left', fontsize=5.0, handlelength=2.5).set_zorder(102)

                plt.tight_layout()
                plt.savefig(pngname, dpi=600)
                pdf.savefig(fig)
                plt.cla()
                plt.clf()
                plt.close()

    for dom in GFDL_domains:
        image_files = []
        if 'MSLP' in variable: output_file = dir_save + f"/{scheme}_{dom}_all_MSLP.png"
        if 'MWS' in variable:  output_file = dir_save + f"/{scheme}_{dom}_all_MWS.png"
        for da_cycle in range(1, total_da_cycles+1):
            if 'MSLP' in variable: image_files.append(dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_MSLP.png")
            if 'MWS' in variable:  image_files.append(dir_save + f"/{scheme}_{dom}_C{da_cycle:02}_MWS.png")

        combine_images_grid(image_files, output_file)
        command = f"convert {output_file} -trim {output_file}"
        subprocess.run(command, shell=True)
        image = IPImage(filename=output_file)
        display(image)

def compare_averaged_RMSE_time_series_scheme(data_library_name, scheme, variable):

    module = importlib.import_module(f"data_library_{data_library_name}")
    compare_schemes = getattr(module, 'compare_schemes')
    attributes = getattr(module, 'attributes')

    dir_save = compare_schemes[scheme]['dir_save']
    labels = compare_schemes[scheme]['labels']
    colors = compare_schemes[scheme]['colors']
    linestyles = compare_schemes[scheme]['linestyles']

    (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][0]
    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
    history_interval = attributes[(dir_case, case_name)]['history_interval']
    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    GFDL_domains = attributes[(dir_case, case_name)]['GFDL_domains']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']

    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

    for dom in GFDL_domains:

        if 'Track' in variable: varname = 'track'
        if 'MSLP' in variable:  varname = 'MSLP'
        if 'MWS' in variable:   varname = 'MWS'

        pdfname = dir_save + f"/{scheme}_{dom}_{varname}_averaged_RMSE_time_series.pdf"
        pngname = dir_save + f"/{scheme}_{dom}_{varname}_averaged_RMSE_time_series.png"

        n_lead_time = int((forecast_hours-6.0)/history_interval+1)
        RMSE_ref = np.zeros(n_lead_time)
        for da_cycle in range(0, total_da_cycles):
            filename = f"{dir_track_intensity}/Error_{case_name}_{exp_name}_C{str(da_cycle+1).zfill(2)}_{dom}.csv"
            df = pd.read_csv(filename)
            mask = (df['Forecast_Hour'] >= (da_cycle + 1) * 6.0) & (df['Forecast_Hour'] <= (da_cycle + 1) * 6.0 + forecast_hours - 6.0) & (df['Forecast_Hour']%6 == 0)
            RMSE_ref += np.square(df.loc[mask, variable].to_numpy())
        RMSE_ref = np.sqrt(RMSE_ref/total_da_cycles)

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.0))
            #fig.subplots_adjust(left=0.125, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.100)

            n_case = len(compare_schemes[scheme]['cases'])
            width = 0.618/n_case
            ymin = 0
            ymax = 0
            ax = axs

            for idc, (dir_case, case_name, exp_name) in enumerate(compare_schemes[scheme]['cases'][1:]):

                itime = attributes[(dir_case, case_name)]['itime']
                forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                history_interval = attributes[(dir_case, case_name)]['history_interval']
                dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']

                RMSE = np.zeros(n_lead_time)
                for da_cycle in range(total_da_cycles):
                    filename = f"{dir_track_intensity}/Error_{case_name}_{exp_name}_C{str(da_cycle+1).zfill(2)}_{dom}.csv"
                    df = pd.read_csv(filename)
                    mask = (df['Forecast_Hour'] >= (da_cycle + 1) * 6.0) & (df['Forecast_Hour'] <= (da_cycle + 1) * 6.0 + forecast_hours - 6.0) & (df['Forecast_Hour']%6 == 0)
                    RMSE += np.square(df.loc[mask, variable].to_numpy())

                RMSE = np.sqrt(RMSE/total_da_cycles)
                RMSE = RMSE_ref-RMSE
                ymin = np.min([ymin, np.min(RMSE)])
                ymax = np.max([ymax, np.max(RMSE)])

                for idl in range(0, n_lead_time):
                    if idl == 1:
                        ax.bar(idl + idc*width-0.3+width, RMSE[idl], width, color=colors[idc+1], label=labels[idc+1], zorder=3)
                    else:
                        ax.bar(idl + idc*width-0.3+width, RMSE[idl], width, color=colors[idc+1], zorder=3)

            ymin = ymin*1.25
            ymax = ymax*1.25
            ax.set_xticks(np.arange(0, n_lead_time, 6/history_interval))
            ax.set_xticklabels([str(idx) for idx in range(0, forecast_hours, 6)])
            ax.set_xlabel('Forecast Hours', fontsize=10.0)
            if 'Track' in variable: ax.set_ylabel('Improvement of Track (km)', fontsize=10.0)
            if 'MSLP' in variable:  ax.set_ylabel('Improvement of MSLP (hPa)', fontsize=10.0)
            if 'MWS' in variable:   ax.set_ylabel('Improvement of MWS (Knot)', fontsize=10.0)
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.axis([-0.5, n_lead_time-0.5, ymin, ymax])
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

def compare_averaged_RMSE_each_cycle_scheme(data_library_name, scheme, variable):

    module = importlib.import_module(f"data_library_{data_library_name}")
    compare_schemes = getattr(module, 'compare_schemes')
    attributes = getattr(module, 'attributes')

    dir_save = compare_schemes[scheme]['dir_save']
    labels = compare_schemes[scheme]['labels']
    colors = compare_schemes[scheme]['colors']
    linestyles = compare_schemes[scheme]['linestyles']

    (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][0]
    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
    history_interval = attributes[(dir_case, case_name)]['history_interval']
    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    GFDL_domains = attributes[(dir_case, case_name)]['GFDL_domains']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']

    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

    for dom in GFDL_domains:

        if 'Track' in variable: varname = 'track'
        if 'MSLP' in variable:  varname = 'MSLP'
        if 'MWS' in variable:   varname = 'MWS'

        pdfname = dir_save + f"/{scheme}_{dom}_{varname}_averaged_RMSE_each_cycle.pdf"
        pngname = dir_save + f"/{scheme}_{dom}_{varname}_averaged_RMSE_each_cycle.png"

        RMSE_ref = np.zeros(total_da_cycles)
        for da_cycle in range(0, total_da_cycles):
            filename = f"{dir_track_intensity}/Error_{case_name}_{exp_name}_C{str(da_cycle+1).zfill(2)}_{dom}.csv"
            df = pd.read_csv(filename)
            mask = (df['Forecast_Hour'] >= (da_cycle + 1) * 6.0) & (df['Forecast_Hour'] <= (da_cycle + 1) * 6.0 + forecast_hours - 6.0) & (df['Forecast_Hour']%6 == 0)
            RMSE_ref[da_cycle] = np.sqrt(np.average(np.square(df.loc[mask, variable].to_numpy())))

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.0))
            #fig.subplots_adjust(left=0.125, bottom=0.075, right=0.975, top=0.975, wspace=0.250, hspace=0.100)

            n_case = len(compare_schemes[scheme]['cases'])
            width = 0.618/n_case
            ymin = 0
            ymax = 0
            ax = axs

            for idc, (dir_case, case_name, exp_name) in enumerate(compare_schemes[scheme]['cases'][1:]):

                itime = attributes[(dir_case, case_name)]['itime']
                forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
                history_interval = attributes[(dir_case, case_name)]['history_interval']
                dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']

                RMSE = np.zeros(total_da_cycles)
                for da_cycle in range(total_da_cycles):
                    filename = f"{dir_track_intensity}/Error_{case_name}_{exp_name}_C{str(da_cycle+1).zfill(2)}_{dom}.csv"
                    df = pd.read_csv(filename)
                    mask = (df['Forecast_Hour'] >= (da_cycle + 1) * 6.0) & (df['Forecast_Hour'] <= (da_cycle + 1) * 6.0 + forecast_hours - 6.0) & (df['Forecast_Hour']%6 == 0)
                    RMSE[da_cycle] = np.sqrt(np.average(np.square(df.loc[mask, variable].to_numpy())))

                RMSE = RMSE_ref-RMSE
                ymin = np.min([ymin, np.min(RMSE)])
                ymax = np.max([ymax, np.max(RMSE)])

                for idl in range(0, total_da_cycles):
                    if idl == 0:
                        ax.bar(idl + idc*width-0.3+width, RMSE[idl], width, color=colors[idc+1], label=labels[idc+1], zorder=3)
                    else:
                        ax.bar(idl + idc*width-0.3+width, RMSE[idl], width, color=colors[idc+1], zorder=3)

            ymin = ymin*1.25
            ymax = ymax*1.25
            ax.set_xticks(np.arange(0, total_da_cycles, 4))
            ax.set_xticklabels(['C' + str(idx).zfill(2) for idx in np.arange(1, total_da_cycles+1, 4)])
            if 'Track' in variable: ax.set_ylabel('Improvement of Track (km)', fontsize=10.0)
            if 'MSLP' in variable:  ax.set_ylabel('Improvement of MSLP (hPa)', fontsize=10.0)
            if 'MWS' in variable:   ax.set_ylabel('Improvement of MWS (Knot)', fontsize=10.0)
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.axis([-0.5, total_da_cycles-0.5, ymin, ymax])
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

def compare_averaged_RMSE_specific_time_each_cycle_scheme(data_library_name, scheme, variable, specific_hours):

    module = importlib.import_module(f"data_library_{data_library_name}")
    compare_schemes = getattr(module, 'compare_schemes')
    attributes = getattr(module, 'attributes')

    if 'Track' in variable: varname = 'track'
    if 'MSLP' in variable:  varname = 'MSLP'
    if 'MWS' in variable:   varname = 'MWS'

    dir_save = compare_schemes[scheme]['dir_save']
    labels = compare_schemes[scheme]['labels']
    colors = compare_schemes[scheme]['colors']
    linestyles = compare_schemes[scheme]['linestyles']

    (dir_case, case_name, exp_name) = compare_schemes[scheme]['cases'][0]
    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    GFDL_domains = attributes[(dir_case, case_name)]['GFDL_domains']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']

    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])

    for dom in GFDL_domains:

        image_files = []
        output_file = dir_save + f"/{scheme}_{dom}_{varname}_averaged_RMSE_f{str(specific_hours).zfill(3)}.png"

        for da_cycle in range(0, total_da_cycles):

            pdfname = dir_save + f"/{scheme}_{dom}_{varname}_averaged_RMSE_f{str(specific_hours).zfill(3)}_C{str(da_cycle+1).zfill(2)}.pdf"
            pngname = dir_save + f"/{scheme}_{dom}_{varname}_averaged_RMSE_f{str(specific_hours).zfill(3)}_C{str(da_cycle+1).zfill(2)}.png"
            image_files.append(pngname)

            with PdfPages(pdfname) as pdf:

                fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.0))

                n_cases = len(compare_schemes[scheme]['cases'])
                width = 0.618/2
                ymin = 0
                ymax = 0
                ax = axs

                for idc, (dir_case, case_name, exp_name) in enumerate(compare_schemes[scheme]['cases']):

                    itime = attributes[(dir_case, case_name)]['itime']
                    dir_track_intensity = attributes[(dir_case, case_name)]['dir_track_intensity']
                    filename = f"{dir_track_intensity}/Error_{case_name}_{exp_name}_C{str(da_cycle+1).zfill(2)}_{dom}.csv"
                    df = pd.read_csv(filename)
                    mask = (df['Forecast_Hour'] >= (da_cycle + 1) * 6.0) & (df['Forecast_Hour'] <= (da_cycle + 1) * 6.0 + specific_hours) & (df['Forecast_Hour']%6 == 0)
                    if idc == 0:
                        RMSE_ref = np.sqrt(np.average(np.square(df.loc[mask, variable].to_numpy())))
                        RMSE_ref_str = str(round(RMSE_ref, 1)).zfill(1)
                        ax.bar(-999.0, 0.0, width, color=colors[idc], label=labels[idc]+': '+RMSE_ref_str, zorder=3)
                    else:
                        RMSE = np.sqrt(np.average(np.square(df.loc[mask, variable].to_numpy())))
                        RMSE_str = str(round(RMSE, 1)).zfill(1)
                        RMSE = RMSE_ref-RMSE
                        ymin = np.min([ymin, RMSE])
                        ymax = np.max([ymax, RMSE])
                        extend_label = labels[idc]
                        if 'CON' in exp_name and 'CON' not in labels[idc] and 'CTRL' not in labels[idc]: extend_label = 'CON_' + extend_label
                        if 'CLR' in exp_name and 'CLR' not in labels[idc]: extend_label = extend_label + '_CLR'
                        ax.bar(idc, RMSE, width, color=colors[idc], label=extend_label+': '+RMSE_str, zorder=3)

                ymin = ymin*1.25
                ymax = ymax*1.25
                ax.set_xticks(np.arange(1, n_cases, 1))
                ax.set_xticklabels(labels[1:])
                ax.set_xlabel(f'C{str(da_cycle+1).zfill(2)}: Averaged from 0 to {str(specific_hours)} Hours', fontsize=10.0)
                if 'Track' in variable: ax.set_ylabel(f'Improvement of Track (km)', fontsize=10.0)
                if 'MSLP' in variable:  ax.set_ylabel(f'Improvement of MSLP (hPa)', fontsize=10.0)
                if 'MWS' in variable:   ax.set_ylabel(f'Improvement of MWS (Knot)', fontsize=10.0)
                ax.tick_params('both', direction='in', labelsize=10.0)
                ax.axis([0.5, n_cases-0.5, ymin, ymax])
                ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
                ax.legend(loc='lower left', fontsize=5.0, handlelength=2.5).set_zorder(102)

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
