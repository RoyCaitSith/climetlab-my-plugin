import os
import importlib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from netCDF4 import Dataset

def comapre_wrfanl_reanl(data_library_names, dir_cases, case_names, exp_names,
                         models=['ERA5', 'GFS'],
                         variables=['u_anl', 'v_anl', 't_anl', 'q_anl'],
                         levels=[1000, 900, 800, 700, 600, 500, 400, 300, 200, 100]):
    
    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        module = importlib.import_module(f"set_parameters_{data_library_name}")

        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        da_domains = attributes[(dir_case, case_name)]['da_domains']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        initial_time = datetime(*itime)

        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        dir_score = os.path.join(dir_exp, 'score')
        dir_wrfanl_reanl = os.path.join(dir_score, 'wrfanl_reanl')
        os.makedirs(dir_score, exist_ok=True)
        os.makedirs(dir_wrfanl_reanl, exist_ok=True)

        n_model = len(models)
        n_variable = len(variables)
        n_level = len(levels)
        n_total = n_model*total_da_cycles*n_variable*n_level

        for dom in tqdm(da_domains, desc='Domains', position=0, leave=True):

            columns_lists = ['Model', 'Date_Time', 'DA_Cycle', 'Variable', 'Level', 'MBE', 'MAE', 'MSE', 'RMSE']
            df = pd.DataFrame(index=np.arange(n_total), columns=columns_lists)

            idc = 0
            for model in tqdm(models, desc='Models', position=0, leave=True):
                print(model)
                for da_cycle in range(1, total_da_cycles+1):
                    for var in variables:
                        for lev in levels:
                # for da_cycle in tqdm(range(1, total_da_cycles+1), desc='Times', position=0, leave=False):
                #     for var in tqdm(variables, desc='Variables', position=0, leave=False):
                #         for lev in tqdm(levels, desc='Levels', position=0, leave=False):

                            time_now = initial_time + timedelta(hours=da_cycle*cycling_interval)
                            var_time = int(time_now.strftime('%Y%m%d%H%M00'))

                            df['Model'][idc] = model
                            df['Date_Time'][idc] = time_now
                            df['DA_Cycle'][idc] = int(da_cycle)
                            df['Variable'][idc] = var
                            df['Level'][idc] = int(lev)
                            
                            specific_case = '_'.join([case_name, model, 'C'+str(total_da_cycles).zfill(2)])
                            dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                            reanl_filename = os.path.join(dir_weather_map_case, f"{var}_{lev}_{dom}.nc")
                            reanl_ncfile = Dataset(reanl_filename)
                            reanl_times = reanl_ncfile.variables['time'][:]
                            idt = np.where(reanl_times == var_time)[0][0]
                            reanl_var = reanl_ncfile.variables[var][idt,:,:]
                            reanl_ncfile.close()

                            specific_case = '_'.join([case_name, exp_name, 'C'+str(total_da_cycles).zfill(2)])
                            dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
                            wrfanl_filename = os.path.join(dir_weather_map_case, f"{var}_{lev}_{dom}.nc")
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

                            df['MBE'][idc] = MBE
                            df['MAE'][idc] = MAE
                            df['MSE'][idc] = MSE
                            df['RMSE'][idc] = RMSE

                            idc += 1

            df.to_csv(f"{dir_wrfanl_reanl}/{case_name}_{exp_name}_{dom}.csv", index=False)