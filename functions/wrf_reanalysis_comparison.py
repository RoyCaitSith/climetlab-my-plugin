import os
import panda as pd
from datetime import timedelta
from tqdm.notebook import tqdm

def wrf_reanalysis_comparison_6h(data_library_names, dir_cases, case_names, exp_names,
                                 models=['ERA5', 'GFS'],
                                 variables=['u', 'v', 't', 'q'],
                                 levels=[1000, 975, 950, 925, 900, 850, 800, 700, 600, 500, 400, 300, 200, 100]):
    
    time_interval = 6

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        module = importlib.import_module(f"set_parameters_{data_library_name}")
        set_variables = getattr(module, 'set_variables')

        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        da_domains = attributes[(dir_case, case_name)]['da_domains']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        initial_time = datetime(*itime)

        dir_weather_map = os.path.join(dir_exp, 'weather_map')
        dir_reanalysis = os.path.join(dir_exp, 'reanalysis')
        os.makedirs(dir_reanalysis, exist_ok=True)

        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
        n_time = int(total_da_cycles*cycling_interval/time_interval)
        n_level = len(levels)

        for dom in tqdm(da_domains, desc='Domains', leave=False):

            columns_lists = ['Date_Time', 'DA_Cycle', 'Variables', 'Level', 'Bias', 'RMSE']
            for lev in levels: columns_lists += str(lev)
            df = pd.DataFrame(0.0, index=n_variables*n_time*n_level, \
                columns=columns_lists)

            idc = 0
            for idt in tqdm(range(n_time), desc='Times', leave=False):
                for var in tqdm(variables, desc='Variables', leave=False):
                    for lev in tqdm(levels, desc='Levels', leave=False):

                        df['Date_Time'][idc] = anl_start_time + timedelta(hours=idt*time_interval)
                        df['DA_Cycle'][idc] = int((idt+1)*time_interval/cycling_interval)
                        df[str(lev)][idc] = 
                        idc += 1


            # Import the necessary library
            (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])
            specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
            dir_weather_map_case = os.path.join(dir_weather_map, specific_case)
            
            # print(exp_name)

            filename = (
                f"{str(var_time)}_{contourf_var}_{str(contour_var_level)}_"
                f"{contour_var}_{str(contour_var_level)}_"
                f"{quiver_var_1}_{quiver_var_2}_{str(quiver_var_level)}_"
                f"{region_type}_{dom}_C{str(da_cycle).zfill(2)}"
            )
            pdfname = os.path.join(dir_weather_map_case, filename+'.pdf')
            pngname = os.path.join(dir_weather_map_case, filename+'.png')
            image_files.append(pngname)

            contourf_var_filename = os.path.join(dir_weather_map_case, f"{contourf_var}_{contourf_var_level}_{dom}.nc")
            contourf_var_ncfile = Dataset(contourf_var_filename)
            contourf_var_times = contourf_var_ncfile.variables['time'][:]
            idt = np.where(contourf_var_times == var_time)[0][0]
            lat = contourf_var_ncfile.variables['lat'][:,:]
            lon = contourf_var_ncfile.variables['lon'][:,:]
            contourf_var_value = contourf_var_ncfile.variables[contourf_var][idt,:,:]
            contourf_var_ncfile.close()

            contourf_var_filename = os.path.join(dir_weather_map_case, f"{contourf_var}_{contourf_var_level}_d01.nc")
            contourf_var_ncfile = Dataset(contourf_var_filename)
            lat_d01 = contourf_var_ncfile.variables['lat'][:,:]
            lon_d01 = contourf_var_ncfile.variables['lon'][:,:]
            contourf_var_ncfile.close()

            contourf_var_filename = os.path.join(dir_weather_map_case, f"{contourf_var}_{contourf_var_level}_d02.nc")
            contourf_var_ncfile = Dataset(contourf_var_filename)
            lat_d02 = contourf_var_ncfile.variables['lat'][:,:]
            lon_d02 = contourf_var_ncfile.variables['lon'][:,:]
            contourf_var_ncfile.close()



            error_df.to_csv(f"{dir_reanalysis}/{case_name}_{exp_name}_{dom}.csv", index=False)