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

def ETS_6h(data_library_names, dir_cases, case_names, exp_names,
           observations=['IMERG', 'CMORPH', 'GSMaP'],
           thresholds=[1.0, 5.0, 10.0, 15.0],
           region_types=['domain', 'tc']):

    time_interval = 6

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
        dir_score = os.path.join(dir_exp, 'score')
        dir_ETS_6h = os.path.join(dir_score, 'ETS_6h')
        os.makedirs(dir_score, exist_ok=True)
        os.makedirs(dir_ETS_6h, exist_ok=True)

        for dom in tqdm(da_domains, desc='Domains', position=0, leave=True):

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
                            wrfanl_lat = wrfanl_ncfile.variables['lat'][idt,:,:]
                            wrfanl_lon = wrfanl_ncfile.variables['lon'][idt,:,:]
                            wrfanl_ncfile.close()

                            for thres in thresholds:
                                for rtype in region_types:

                                    if rtype == 'tc':
                                        reanl_var 

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