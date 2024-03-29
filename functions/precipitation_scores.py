import os
import math
import importlib
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import colormaps as cmaps
from datetime import datetime, timedelta
from combine_and_show_images import combine_images_grid
from tqdm.notebook import tqdm
from wrf import getvar
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import Image as IPImage
from IPython.display import display

def ETS_6h(data_library_names, dir_cases, case_names, exp_names,
           observations=['CMORPH', 'GSMaP', 'IMERG'],
           resolutions={'d01':12, 'd02':4},
           thresholds=[1.0, 5.0, 10.0, 15.0],
           tc_box_range=300,
           region_types=['tc', 'domain']):

    time_interval = 6

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        module = importlib.import_module(f"set_parameters_{data_library_name}")

        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        initial_time = datetime(*itime)

        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        dir_best_track = os.path.join(dir_exp, 'track_intensity', 'best_track')
        dir_score = os.path.join(dir_exp, 'score')
        dir_ETS_6h = os.path.join(dir_score, 'ETS_6h')
        os.makedirs(dir_score, exist_ok=True)
        os.makedirs(dir_ETS_6h, exist_ok=True)

        n_observation = len(observations)
        n_forecast_hour = total_da_cycles+int(forecast_hours/time_interval)
        n_threshold = len(thresholds)
        n_region_type = len(region_types)
        n_total = n_observation*total_da_cycles*n_forecast_hour*n_threshold*n_region_type

        for dom in tqdm(resolutions.keys(), desc='Domains', position=0, leave=True):

            columns_lists = ['Observation', 'DA_Cycle', 'Forecast_Hour', 'Date_Time', 'Threshold', 'Region_Type', 'ETS']
            df = pd.DataFrame(index=np.arange(n_total), columns=columns_lists)

            iddf = 0
            for observation in tqdm(observations, desc='Observations', position=0, leave=True):
                for da_cycle in range(1, total_da_cycles+1):
                    for fhour in range(time_interval, da_cycle*cycling_interval+forecast_hours+1, time_interval):
                    
                        time_now = initial_time + timedelta(hours=fhour)
                        var_time = int(time_now.strftime('%Y%m%d%H%M00'))
                            
                        specific_case = '_'.join([case_name, observation, 'C'+str(da_cycle).zfill(2)])
                        dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                        reanl_filename = os.path.join(dir_weather_map_case, f"rain_6h_9999_{dom}.nc")

                        specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
                        dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                        wrfanl_filename = os.path.join(dir_weather_map_case, f"rain_6h_9999_{dom}.nc")

                        if os.path.exists(reanl_filename) and os.path.exists(wrfanl_filename):
                            
                            reanl_ncfile = Dataset(reanl_filename)
                            reanl_times = reanl_ncfile.variables['time'][:]
                            idt = np.where(reanl_times == var_time)[0][0]
                            reanl_var = reanl_ncfile.variables['rain_6h'][idt,:,:]/time_interval
                            reanl_ncfile.close()

                            wrfanl_ncfile = Dataset(wrfanl_filename)
                            wrfanl_times = wrfanl_ncfile.variables['time'][:]
                            idt = np.where(wrfanl_times == var_time)[0][0]
                            wrfanl_var = wrfanl_ncfile.variables['rain_6h'][idt,:,:]/time_interval
                            wrfanl_lat = wrfanl_ncfile.variables['lat'][:,:]
                            wrfanl_lon = wrfanl_ncfile.variables['lon'][:,:]
                            wrfanl_ncfile.close()

                            for thres in thresholds:
                                for rtype in region_types:

                                    if rtype == 'tc':
                                        best_track = os.path.join(dir_best_track, attributes[(dir_case, case_name)]['NHC_best_track'])
                                        bt_df = pd.read_csv(best_track)
                                        bt_lats = list(bt_df['LAT'][:])
                                        bt_lons = list(bt_df['LON'][:])
                                        bt_dates = list(bt_df['Date_Time'][:])
                                        del bt_df

                                        var_time_datetime = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')
                                        for id_bt, bt_date in enumerate(bt_dates):
                                            bt_datetime = datetime.strptime(bt_date, '%Y-%m-%d %H:%M:%S')
                                            if bt_datetime == var_time_datetime:
                                                bt_lat = bt_lats[id_bt]
                                                bt_lon = bt_lons[id_bt]

                                        bt_dlon = wrfanl_lon - bt_lon
                                        bt_dlat = wrfanl_lat - bt_lat
                                        bt_distrance_square = np.square(bt_dlon) + np.square(bt_dlat)
                                        bt_min_pos = np.unravel_index(np.argmin(bt_distrance_square, axis=None), bt_distrance_square.shape)
                                        tc_box_index = math.floor(tc_box_range/resolutions[dom])
                                        reanl_rain = reanl_var[bt_min_pos[0]-tc_box_index:bt_min_pos[0]+tc_box_index+1, bt_min_pos[1]-tc_box_index:bt_min_pos[1]+tc_box_index+1]

                                        best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", f"{dom}.csv"]))
                                        if not os.path.exists(best_track):
                                            best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", 'd01.csv']))
                                        wrf_df = pd.read_csv(best_track)
                                        wrf_lats = list(wrf_df['LAT'][:])
                                        wrf_lons = list(wrf_df['LON'][:])
                                        wrf_dates = list(wrf_df['Date_Time'][:])
                                        del wrf_df

                                        var_time_datetime = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')
                                        for id_wrf, wrf_date in enumerate(wrf_dates):
                                            wrf_datetime = datetime.strptime(wrf_date, '%Y-%m-%d %H:%M:%S')
                                            if wrf_datetime == var_time_datetime:
                                                wrf_lat = wrf_lats[id_wrf]
                                                wrf_lon = wrf_lons[id_wrf]

                                        wrf_dlon = wrfanl_lon - wrf_lon
                                        wrf_dlat = wrfanl_lat - wrf_lat
                                        wrf_distrance_square = np.square(wrf_dlon) + np.square(wrf_dlat)
                                        wrf_min_pos = np.unravel_index(np.argmin(wrf_distrance_square, axis=None), wrf_distrance_square.shape)
                                        tc_box_index = math.floor(tc_box_range/resolutions[dom])
                                        wrfanl_rain = wrfanl_var[wrf_min_pos[0]-tc_box_index:wrf_min_pos[0]+tc_box_index+1, wrf_min_pos[1]-tc_box_index:wrf_min_pos[1]+tc_box_index+1]

                                    elif rtype == 'domain':
                                        reanl_rain = reanl_var
                                        wrfanl_rain = wrfanl_var

                                    Hit         = (reanl_rain >= thres) & (wrfanl_rain >= thres)
                                    False_Alarm = (reanl_rain  < thres) & (wrfanl_rain >= thres)
                                    Miss        = (reanl_rain >= thres) & (wrfanl_rain  < thres)
                                    Correct_Neg = (reanl_rain  < thres) & (wrfanl_rain  < thres)

                                    N_H  = len(wrfanl_rain[Hit])
                                    N_FA = len(wrfanl_rain[False_Alarm])
                                    N_M  = len(wrfanl_rain[Miss])
                                    N_CN = len(wrfanl_rain[Correct_Neg])
                                    Total = N_H + N_FA + N_M + N_CN

                                    ref = (N_H + N_FA)*(N_H + N_M)/Total
                                    ETS = (N_H - ref)/(N_H + N_FA + N_M - ref)
                                    
                                    df['Observation'][iddf] = observation
                                    df['DA_Cycle'][iddf] = int(da_cycle)
                                    df['Forecast_Hour'][iddf] = int(fhour)
                                    df['Date_Time'][iddf] = time_now
                                    df['Threshold'][iddf] = int(thres)
                                    df['Region_Type'][iddf] = rtype
                                    df['ETS'][iddf] = ETS

                                    iddf += 1

            df.to_csv(f"{dir_ETS_6h}/{case_name}_{exp_name}_{dom}.csv", index=False)
            print(df)

def ETS_24h(data_library_names, dir_cases, case_names, exp_names,
            observations=['CMORPH', 'GSMaP', 'IMERG'],
            resolutions={'d01':12, 'd02':4},
            thresholds=[10.0, 15.0, 20.0, 25.0, 30.0],
            tc_box_range=300,
            region_types=['tc', 'domain']):

    # A threshold-based approach was used to examine changes in rainfall intensities in four categories of daily rainfall intensity
    # (1) moderately heavy precipitation (12.7–25.4 mm/day range)
    # (2) heavy precipitation (25.4–76.2 mm/day range)
    # (3) very heavy precipitation (>76.2 mm/day)
    # (4) extreme precipitation (>152.4 mm/day)
    
    time_interval = 24

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        module = importlib.import_module(f"set_parameters_{data_library_name}")

        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        initial_time = datetime(*itime)

        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        dir_best_track = os.path.join(dir_exp, 'track_intensity', 'best_track')
        dir_score = os.path.join(dir_exp, 'score')
        dir_ETS_24h = os.path.join(dir_score, 'ETS_24h')
        os.makedirs(dir_score, exist_ok=True)
        os.makedirs(dir_ETS_24h, exist_ok=True)

        n_observation = len(observations)
        n_forecast_hour = int(forecast_hours/time_interval)
        n_threshold = len(thresholds)
        n_region_type = len(region_types)
        n_total = n_observation*total_da_cycles*n_forecast_hour*n_threshold*n_region_type

        for dom in tqdm(resolutions.keys(), desc='Domains', position=0, leave=True):

            columns_lists = ['Observation', 'DA_Cycle', 'Forecast_Hour', 'Date_Time', 'Threshold', 'Region_Type', 'ETS']
            df = pd.DataFrame(index=np.arange(n_total), columns=columns_lists)

            iddf = 0
            for observation in tqdm(observations, desc='Observations', position=0, leave=True):
                for da_cycle in range(1, total_da_cycles+1):
                    for fhour in range(da_cycle*cycling_interval, da_cycle*cycling_interval+forecast_hours, time_interval):
                    
                        specific_case = '_'.join([case_name, observation, 'C'+str(da_cycle).zfill(2)])
                        dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                        reanl_filename = os.path.join(dir_weather_map_case, f"rain_6h_9999_{dom}.nc")

                        specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
                        dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                        wrfanl_filename = os.path.join(dir_weather_map_case, f"rain_6h_9999_{dom}.nc")

                        if os.path.exists(reanl_filename) and os.path.exists(wrfanl_filename):
                            for thres in thresholds:
                                for rtype in region_types:
                                    for dt in range(0, time_interval, 6):
                                        time_now = initial_time + timedelta(hours=fhour+dt)
                                        var_time = int(time_now.strftime('%Y%m%d%H%M00'))

                                        reanl_ncfile = Dataset(reanl_filename)
                                        reanl_times = reanl_ncfile.variables['time'][:]
                                        idt = np.where(reanl_times == var_time)[0][0]
                                        reanl_var = reanl_ncfile.variables['rain_6h'][idt,:,:]
                                        reanl_ncfile.close()

                                        wrfanl_ncfile = Dataset(wrfanl_filename)
                                        wrfanl_times = wrfanl_ncfile.variables['time'][:]
                                        idt = np.where(wrfanl_times == var_time)[0][0]
                                        wrfanl_var = wrfanl_ncfile.variables['rain_6h'][idt,:,:]
                                        wrfanl_lat = wrfanl_ncfile.variables['lat'][:,:]
                                        wrfanl_lon = wrfanl_ncfile.variables['lon'][:,:]
                                        wrfanl_ncfile.close()

                                        if rtype == 'tc':
                                            best_track = os.path.join(dir_best_track, attributes[(dir_case, case_name)]['NHC_best_track'])
                                            bt_df = pd.read_csv(best_track)
                                            bt_lats = list(bt_df['LAT'][:])
                                            bt_lons = list(bt_df['LON'][:])
                                            bt_dates = list(bt_df['Date_Time'][:])
                                            del bt_df

                                            var_time_datetime = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')
                                            for id_bt, bt_date in enumerate(bt_dates):
                                                bt_datetime = datetime.strptime(bt_date, '%Y-%m-%d %H:%M:%S')
                                                if bt_datetime == var_time_datetime:
                                                    bt_lat = bt_lats[id_bt]
                                                    bt_lon = bt_lons[id_bt]

                                            bt_dlon = wrfanl_lon - bt_lon
                                            bt_dlat = wrfanl_lat - bt_lat
                                            bt_distrance_square = np.square(bt_dlon) + np.square(bt_dlat)
                                            bt_min_pos = np.unravel_index(np.argmin(bt_distrance_square, axis=None), bt_distrance_square.shape)
                                            tc_box_index = math.floor(tc_box_range/resolutions[dom])
                                            if dt == 0:
                                                reanl_rain = reanl_var[bt_min_pos[0]-tc_box_index:bt_min_pos[0]+tc_box_index+1, bt_min_pos[1]-tc_box_index:bt_min_pos[1]+tc_box_index+1]
                                            else:
                                                reanl_rain += reanl_var[bt_min_pos[0]-tc_box_index:bt_min_pos[0]+tc_box_index+1, bt_min_pos[1]-tc_box_index:bt_min_pos[1]+tc_box_index+1]

                                            best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", f"{dom}.csv"]))
                                            if not os.path.exists(best_track):
                                                best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", 'd01.csv']))
                                            wrf_df = pd.read_csv(best_track)
                                            wrf_lats = list(wrf_df['LAT'][:])
                                            wrf_lons = list(wrf_df['LON'][:])
                                            wrf_dates = list(wrf_df['Date_Time'][:])
                                            del wrf_df

                                            var_time_datetime = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')
                                            for id_wrf, wrf_date in enumerate(wrf_dates):
                                                wrf_datetime = datetime.strptime(wrf_date, '%Y-%m-%d %H:%M:%S')
                                                if wrf_datetime == var_time_datetime:
                                                    wrf_lat = wrf_lats[id_wrf]
                                                    wrf_lon = wrf_lons[id_wrf]

                                            wrf_dlon = wrfanl_lon - wrf_lon
                                            wrf_dlat = wrfanl_lat - wrf_lat
                                            wrf_distrance_square = np.square(wrf_dlon) + np.square(wrf_dlat)
                                            wrf_min_pos = np.unravel_index(np.argmin(wrf_distrance_square, axis=None), wrf_distrance_square.shape)
                                            tc_box_index = math.floor(tc_box_range/resolutions[dom])
                                            if dt == 0:
                                                wrfanl_rain = wrfanl_var[wrf_min_pos[0]-tc_box_index:wrf_min_pos[0]+tc_box_index+1, wrf_min_pos[1]-tc_box_index:wrf_min_pos[1]+tc_box_index+1]
                                            else:
                                                wrfanl_rain += wrfanl_var[wrf_min_pos[0]-tc_box_index:wrf_min_pos[0]+tc_box_index+1, wrf_min_pos[1]-tc_box_index:wrf_min_pos[1]+tc_box_index+1]

                                        elif rtype == 'domain':

                                            if dt == 0:
                                                reanl_rain = reanl_var
                                                wrfanl_rain = wrfanl_var
                                            else:
                                                reanl_rain += reanl_var
                                                wrfanl_rain += wrfanl_var

                                    Hit         = (reanl_rain >= thres) & (wrfanl_rain >= thres)
                                    False_Alarm = (reanl_rain  < thres) & (wrfanl_rain >= thres)
                                    Miss        = (reanl_rain >= thres) & (wrfanl_rain  < thres)
                                    Correct_Neg = (reanl_rain  < thres) & (wrfanl_rain  < thres)

                                    N_H   = len(wrfanl_rain[Hit])
                                    N_FA  = len(wrfanl_rain[False_Alarm])
                                    N_M   = len(wrfanl_rain[Miss])
                                    N_CN  = len(wrfanl_rain[Correct_Neg])
                                    Total = N_H + N_FA + N_M + N_CN

                                    # print(N_CN)
                                    # print(observation)
                                    # print(da_cycle)
                                    # print(fhour)
                                    # print(time_now)
                                    # print(thres)
                                    # print(rtype)

                                    ref = (N_H + N_FA)*(N_H + N_M)/Total
                                    ETS = (N_H - ref)/(N_H + N_FA + N_M - ref)
                                    
                                    df['Observation'][iddf] = observation
                                    df['DA_Cycle'][iddf] = int(da_cycle)
                                    df['Forecast_Hour'][iddf] = int(fhour)
                                    df['Date_Time'][iddf] = time_now
                                    df['Threshold'][iddf] = int(thres)
                                    df['Region_Type'][iddf] = rtype
                                    df['ETS'][iddf] = ETS

                                    iddf += 1

            df.to_csv(f"{dir_ETS_24h}/{case_name}_{exp_name}_{dom}.csv", index=False)
            print(df)

def compare_ETS_6h(data_library_names, dir_cases, case_names, exp_names, ref_exp_name,
                   domains=['d01', 'd02'], observation='IMERG', threshold=10,
                   region_type='domain', display_mode='lead_time'):

    time_interval = 6
    
    for domain in domains:

        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[0], dir_cases[0], case_names[0], exp_names[0])
        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')

        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

        dir_score = os.path.join(dir_exp, 'score')
        dir_ETS_6h = os.path.join(dir_score, 'ETS_6h')

        pdfname = os.path.join(dir_ETS_6h, f"{observation}_{str(int(threshold))}_{display_mode}_{region_type}_{domain}.pdf")
        pngname = os.path.join(dir_ETS_6h, f"{observation}_{str(int(threshold))}_{display_mode}_{region_type}_{domain}.png")

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(6.0, 3.50))
            # fig.subplots_adjust(left=0.050, bottom=0.100, right=0.975, top=0.975, wspace=0.300, hspace=0.225)
            cmap_tableau_20 = cmaps.tableau_20.colors
            n_case = len(case_names)
            width = 0.618/n_case

            ax = axs

            if display_mode == 'lead_time':
                n_lead_time = int(forecast_hours/time_interval + 1)
                ETS_ref = np.zeros(n_lead_time)
                filename = f"{dir_ETS_6h}/{case_name}_{ref_exp_name}_{domain}.csv"
                df = pd.read_csv(filename)

                for da_cycle in range(1, total_da_cycles+1):
                    mask = (df['Forecast_Hour'] >= da_cycle * cycling_interval) & (df['Forecast_Hour'] <= da_cycle * cycling_interval + forecast_hours) & (df['DA_Cycle'] == da_cycle) & \
                           (df['Threshold'] == threshold) & (df['Region_Type'] == region_type) & (df['Observation'] == observation)
                    ETS_ref += df.loc[mask, 'ETS'].to_numpy()
                ETS_ref = ETS_ref/total_da_cycles

            elif display_mode == 'da_cycle':
                ETS_ref = np.zeros(total_da_cycles)
                filename = f"{dir_ETS_6h}/{case_name}_{ref_exp_name}_{domain}.csv"
                df = pd.read_csv(filename)

                for da_cycle in range(1, total_da_cycles+1):
                    mask = (df['Forecast_Hour'] >= da_cycle * cycling_interval) & (df['Forecast_Hour'] <= da_cycle * cycling_interval + forecast_hours) & (df['DA_Cycle'] == da_cycle) & \
                           (df['Threshold'] == threshold) & (df['Region_Type'] == region_type) & (df['Observation'] == observation)
                    ETS_ref[da_cycle-1] = np.average(df.loc[mask, 'ETS'].to_numpy())

            for idc in range(n_case):
                (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

                if display_mode == 'lead_time':
                    ETS_exp = np.zeros(n_lead_time)
                    ETS_dif = np.zeros(n_lead_time)
                    filename = f"{dir_ETS_6h}/{case_name}_{exp_name}_{domain}.csv"
                    df = pd.read_csv(filename)

                    for da_cycle in range(1, total_da_cycles+1):
                        mask = (df['Forecast_Hour'] >= da_cycle * cycling_interval) & (df['Forecast_Hour'] <= da_cycle * cycling_interval + forecast_hours) & (df['DA_Cycle'] == da_cycle) & \
                               (df['Threshold'] == threshold) & (df['Region_Type'] == region_type) & (df['Observation'] == observation)
                        ETS_exp += df.loc[mask, 'ETS'].to_numpy()
                    ETS_exp = ETS_exp/total_da_cycles
                    ETS_dif = ETS_exp - ETS_ref

                    for idl in range(n_lead_time):
                        if idl == 0:
                            ax.bar(idl+(idc-1)*width-0.5*(n_case-1)*width, ETS_dif[idl], width, color=cmap_tableau_20[idc], label=exp_name, zorder=3)
                            ax.text(idl, 0.0, str(np.around(ETS_ref[idl], 3)), ha='center', va='center', color='black', fontsize=7.5)
                        else:
                            ax.bar(idl+(idc-1)*width-0.5*(n_case-1)*width, ETS_dif[idl], width, color=cmap_tableau_20[idc], zorder=3)
                            ax.text(idl, 0.0, str(np.around(ETS_ref[idl], 3)), ha='center', va='center', color='black', fontsize=7.5)
                
                    ax.set_xticks(np.arange(0, n_lead_time, 1))
                    ax.set_xlabel('Forecast Hours', fontsize=10.0)
                    ax.set_xticklabels([str(x) for x in range(0, n_lead_time*time_interval, time_interval)])

                elif display_mode == 'da_cycle':
                    ETS_exp = np.zeros(total_da_cycles)
                    ETS_dif = np.zeros(total_da_cycles)

                    filename = f"{dir_ETS_6h}/{case_name}_{exp_name}_{domain}.csv"
                    df = pd.read_csv(filename)

                    for da_cycle in range(1, total_da_cycles+1):
                        mask = (df['Forecast_Hour'] >= da_cycle * cycling_interval) & (df['Forecast_Hour'] <= da_cycle * cycling_interval + forecast_hours) & (df['DA_Cycle'] == da_cycle) & \
                               (df['Threshold'] == threshold) & (df['Region_Type'] == region_type) & (df['Observation'] == observation)
                        ETS_exp[da_cycle-1] = np.average(df.loc[mask, 'ETS'].to_numpy())
                        ETS_dif[da_cycle-1] = ETS_exp[da_cycle-1] - ETS_ref[da_cycle-1]
                    
                    for idt in range(1, total_da_cycles+1, 1):
                        if idt == 1:
                            ax.bar(idt+(idc-1)*width-0.5*(n_case-1)*width, ETS_dif[idt-1], width, color=cmap_tableau_20[idc], label=exp_name, zorder=3)
                            ax.text(idt, 0.0, str(np.around(ETS_ref[idt-1], 3)), ha='center', va='center', color='black', fontsize=7.5)
                        else:
                            ax.bar(idt+(idc-1)*width-0.5*(n_case-1)*width, ETS_dif[idt-1], width, color=cmap_tableau_20[idc], zorder=3)
                            ax.text(idt, 0.0, str(np.around(ETS_ref[idt-1], 3)), ha='center', va='center', color='black', fontsize=7.5)

                    ax.set_xticks(np.arange(1, total_da_cycles+1, 1))
                    ax.set_xlabel('DA Cycle', fontsize=10.0)

            ax.set_ylabel('Improvement of ETS', fontsize=10.0)
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.grid(linewidth=0.5, color='gray', axis='y')
            ax.legend(loc='best', fontsize=7.5, handlelength=2.5).set_zorder(102)

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