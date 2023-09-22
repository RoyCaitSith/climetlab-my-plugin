import os
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

def calculate_ETS(data_library_names, dir_cases, case_names, exp_names, ref_exp_names, domain, region_type):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        data_library_name = data_library_names[idc]
        dir_case = dir_cases[idc]
        case_name = case_names[idc]
        exp_name = exp_names[idc]
        ref_exp_name = ref_exp_names[idc]

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')

        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        itime = attributes[(dir_case, case_name)]['itime']
        initial_time = datetime(*itime)
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_track_intensity = os.path.join(dir_exp, 'track_intensity')
        dir_best_track = os.path.join(dir_track_intensity, 'best_track')

        for da_cycle in range(1, total_da_cycles+1, 1):

            

        if region_type == 'tc':
            NHC_best_track = attributes[(dir_case, case_name)]['NHC_best_track']
            ref_best_track = os.path.join(dir_best_track, NHC_best_track)
            ref_df = pd.read_csv(ref_best_track)
            ref_bt_lats = list(ref_df['LAT'][:])
            ref_bt_lons = list(ref_df['LON'][:])
            ref_bt_dates = list(ref_df['Date_Time'][:])
            del ref_df

            best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", f"{dom}.csv"]))
            if not os.path.exists(best_track):
                best_track = os.path.join(dir_best_track, '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", 'd01.csv']))
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
                        if region_type == 'tc':
                            extent = [bt_lon-5.0, bt_lon+5.0, bt_lat-5.0, bt_lat+5.0]



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