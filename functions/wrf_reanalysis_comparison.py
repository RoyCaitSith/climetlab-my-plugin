import os
import importlib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from netCDF4 import Dataset

def comapre_wrf_reanl_6h(data_library_names, dir_cases, case_names, exp_names,
                         models=['ERA5', 'GFS'],
                         variables=['u', 'v', 't', 'q', 'u_anl', 'v_anl', 't_anl', 'q_anl'],
                         levels=[1000, 900, 800, 700, 600, 500, 400, 300, 200, 100]):
    
    time_interval = 6

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        module = importlib.import_module(f"set_parameters_{data_library_name}")

        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
        initial_time = datetime(*itime)

        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        dir_score = os.path.join(dir_exp, 'score')
        dir_wrf_reanl = os.path.join(dir_score, 'wrf_reanl')
        os.makedirs(dir_score, exist_ok=True)
        os.makedirs(dir_wrf_reanl, exist_ok=True)

        n_model = len(models)
        n_forecast_hour = total_da_cycles+int(forecast_hours/time_interval)
        n_variable = len(variables)
        n_level = len(levels)
        n_total = n_model*total_da_cycles*n_forecast_hour*n_variable*n_level

        # for dom in tqdm(['d02'], desc='Domains', position=0, leave=True):
        for dom in tqdm(forecast_domains, desc='Domains', position=0, leave=True):

            columns_lists = ['Model', 'DA_Cycle', 'Forecast_Hour', 'Date_Time', 'Variable', 'Level', 'MBE', 'MAE', 'MSE', 'RMSE']
            df = pd.DataFrame(index=np.arange(n_total), columns=columns_lists)

            iddf = 0
            for model in tqdm(models, desc='Models', position=0, leave=True):
                for da_cycle in range(1, total_da_cycles+1):
                    for fhour in range(time_interval, da_cycle*cycling_interval+forecast_hours+1, time_interval):
                    
                        time_now = initial_time + timedelta(hours=fhour)
                        var_time = int(time_now.strftime('%Y%m%d%H%M00'))

                        for var in variables:
                            for lev in levels:
                            
                                specific_case = '_'.join([case_name, model, 'C'+str(da_cycle).zfill(2)])
                                dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                                reanl_filename = os.path.join(dir_weather_map_case, f"{var}_{lev}_{dom}.nc")

                                specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
                                dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                                wrfanl_filename = os.path.join(dir_weather_map_case, f"{var}_{lev}_{dom}.nc")

                                if os.path.exists(reanl_filename) and os.path.exists(wrfanl_filename):
                            
                                    reanl_ncfile = Dataset(reanl_filename)
                                    reanl_times = reanl_ncfile.variables['time'][:]
                                    idt = np.where(reanl_times == var_time)[0][0]
                                    reanl_var = reanl_ncfile.variables[var][idt,:,:]
                                    reanl_ncfile.close()

                                    wrfanl_ncfile = Dataset(wrfanl_filename)
                                    wrfanl_times = wrfanl_ncfile.variables['time'][:]
                                    idt = np.where(wrfanl_times == var_time)[0][0]
                                    wrfanl_var = wrfanl_ncfile.variables[var][idt,:,:]
                                    wrfanl_ncfile.close()

                                    diff = wrfanl_var - reanl_var
                                    diff_abs = np.abs(diff)
                                    diff_square = np.square(diff)
                                    MBE = np.nanmean(diff)
                                    MAE = np.nanmean(diff_abs)
                                    MSE = np.nanmean(diff_square)
                                    RMSE = np.sqrt(MSE)

                                    df['Model'][iddf] = model
                                    df['DA_Cycle'][iddf] = int(da_cycle)
                                    df['Forecast_Hour'][iddf] = int(fhour)
                                    df['Date_Time'][iddf] = time_now
                                    df['Variable'][iddf] = var
                                    df['Level'][iddf] = int(lev)
                                    df['MBE'][iddf] = MBE
                                    df['MAE'][iddf] = MAE
                                    df['MSE'][iddf] = MSE
                                    df['RMSE'][iddf] = RMSE

                                    iddf += 1

            df.to_csv(f"{dir_wrf_reanl}/{case_name}_{exp_name}_{dom}.csv", index=False)
            print(df)