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
           observations=['IMERG', 'CMORPH', 'GSMaP'],
           resolutions=[12, 4],
           thresholds=[1.0, 5.0, 10.0, 15.0],
           region_types=['tc', 'domain']):

    time_interval = 6
    tc_box_range = 500

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        module = importlib.import_module(f"set_parameters_{data_library_name}")

        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        da_domains = attributes[(dir_case, case_name)]['da_domains']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
        initial_time = datetime(*itime)

        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        dir_best_track = os.path.join(dir_exp, 'track_intensity', 'best_track')
        dir_score = os.path.join(dir_exp, 'score')
        dir_ETS_6h = os.path.join(dir_score, 'ETS_6h')
        os.makedirs(dir_score, exist_ok=True)
        os.makedirs(dir_ETS_6h, exist_ok=True)

        for idd, dom in tqdm(enumerate(da_domains), desc='Domains', position=0, leave=True):

            columns_lists = ['Observation', 'DA_Cycle', 'Forecast_Hour', 'Date_Time', 'Threshold', 'Region_type', 'ETS']
            df = pd.DataFrame(columns=columns_lists)

            idc = 0
            for observation in tqdm(observations, desc='Observations', position=0, leave=True):
                for da_cycle in range(1, total_da_cycles+1):
                    for fhour in range(0, forecast_hours+1, time_interval):
                    
                        time_now = initial_time + timedelta(hours=da_cycle*time_interval+fhour)
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
                            reanl_var = reanl_ncfile.variables['rain_6h'][idt,:,:]
                            reanl_ncfile.close()

                            wrfanl_ncfile = Dataset(wrfanl_filename)
                            wrfanl_times = wrfanl_ncfile.variables['time'][:]
                            idt = np.where(wrfanl_times == var_time)[0][0]
                            wrfanl_var = wrfanl_ncfile.variables['rain_6h'][idt,:,:]
                            wrfanl_lat = wrfanl_ncfile.variables['lat'][:,:]
                            wrfanl_lon = wrfanl_ncfile.variables['lon'][:,:]
                            wrfanl_ncfile.close()

                            for thres in thresholds:
                                for rtype in region_types:

                                    if rtype == 'tc':
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

                                        bt_dlon = wrfanl_lon - bt_lon
                                        bt_dlat = wrfanl_lat - bt_lat
                                        bt_distrance_square = np.square(bt_dlon) + np.square(bt_dlat)
                                        bt_min_pos = np.unravel_index(np.argmin(bt_distrance_square, axis=None), bt_distrance_square.shape)
                                        tc_box_index = math.floor(tc_box_range/resolutions[idd])
                                        reanl_var = reanl_var[bt_min_pos[0]-tc_box_index:bt_min_pos[0]+tc_box_index+1, bt_min_pos[1]-tc_box_index:bt_min_pos[1]+tc_box_index+1]

                                        best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", f"{dom}.csv"]))
                                        if not os.path.exists(best_track):
                                            best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", 'd01.csv']))
                                        df = pd.read_csv(best_track)
                                        wrf_lats = list(df['LAT'][:])
                                        wrf_lons = list(df['LON'][:])
                                        wrf_dates = list(df['Date_Time'][:])
                                        del df

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
                                        tc_box_index = math.floor(tc_box_range/resolutions[idd])
                                        wrfanl_var = wrfanl_var[wrf_min_pos[0]-tc_box_index:wrf_min_pos[0]+tc_box_index+1, wrf_min_pos[1]-tc_box_index:wrf_min_pos[1]+tc_box_index+1]
                                        wrfanl_lat = wrfanl_lat[wrf_min_pos[0]-tc_box_index:wrf_min_pos[0]+tc_box_index+1, wrf_min_pos[1]-tc_box_index:wrf_min_pos[1]+tc_box_index+1]
                                        wrfanl_lon = wrfanl_lon[wrf_min_pos[0]-tc_box_index:wrf_min_pos[0]+tc_box_index+1, wrf_min_pos[1]-tc_box_index:wrf_min_pos[1]+tc_box_index+1]

                                    Hit         = (reanl_var >= thres) & (wrfanl_var >= thres)
                                    False_Alarm = (reanl_var  < thres) & (wrfanl_var >= thres)
                                    Miss        = (reanl_var >= thres) & (wrfanl_var  < thres)
                                    Correct_Neg = (reanl_var  < thres) & (wrfanl_var  < thres)

                                    N_H  = len(wrfanl_var[Hit])
                                    N_FA = len(wrfanl_var[False_Alarm])
                                    N_M  = len(wrfanl_var[Miss])
                                    N_CN = len(wrfanl_var[Correct_Neg])
                                    Total = N_H + N_FA + N_M + N_CN

                                    ref = (N_H + N_FA)*(N_H + N_M)/Total
                                    ETS = (N_H - ref)/(N_H + N_FA + N_M - ref)

                                    df['Observation'][idc] = observation
                                    df['DA_Cycle'][idc] = int(da_cycle)
                                    df['Forecast_Hour'][idc] = int(fhour)
                                    df['Date_Time'][idc] = time_now
                                    df['Threshold'][idc] = int(thres)
                                    df['Region_type'][idc] = rtype
                                    df['ETS'][idc] = ETS

                                    idc += 1

            df.to_csv(f"{dir_ETS_6h}/{case_name}_{exp_name}_{dom}.csv", index=False)