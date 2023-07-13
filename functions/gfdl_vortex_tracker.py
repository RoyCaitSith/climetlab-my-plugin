import os
import glob
import shutil
import importlib
from datetime import datetime, timedelta
from netCDF4 import Dataset
from tqdm.notebook import tqdm

def link_wrfout(data_library_name, dir_case, case_name, exp_name, \
                input_anl_start_time=datetime(2000, 1, 1, 0, 0, 0), \
                input_forecast_end_time=datetime(2000, 1, 1, 0, 0, 0)):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    forecast_hours=attributes[(dir_case, case_name)]['forecast_hours']
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    history_interval=attributes[(dir_case, case_name)]['history_interval']
    GFDL_domains=attributes[(dir_case, case_name)]['GFDL_domains']

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc="DA Cycle"):

        case = '_'.join([case_name, exp_name, 'C' + str(da_cycle).zfill(2)])
        initial_time = datetime(*itime)
        if input_anl_start_time == datetime(2000, 1, 1, 0, 0, 0):
            anl_start_time = initial_time + timedelta(hours=cycling_interval)
        else:
            anl_start_time = input_anl_start_time
        if input_forecast_end_time == datetime(2000, 1, 1, 0, 0, 0):
            forecast_end_time = initial_time + timedelta(hours=cycling_interval*da_cycle + forecast_hours)
        else:
            forecast_end_time = input_forecast_end_time
        dir_in = os.path.join(dir_exp, 'cycling_da', case, 'bkg')
        dir_out = os.path.join(dir_exp, 'track_intensity', case, 'wrfprd')
        os.makedirs(dir_out, exist_ok=True)

        n_time = int((forecast_end_time - anl_start_time).total_seconds() / 3600 / history_interval) + 1

        print(f'Link wrfout files from {anl_start_time} to {forecast_end_time}')
        for item in tqdm(range(n_time), desc="Processing files", leave=False):
            for dom in GFDL_domains:
                forecast_time_now = anl_start_time + timedelta(hours=history_interval * item)
                wrfout_time = forecast_time_now.strftime('%Y-%m-%d_%H:00:00')
                wrfout_name = f'wrfout_{dom}_{wrfout_time}'
                wrfout = os.path.join(dir_in, wrfout_name)
                if os.path.islink(os.path.join(dir_out, wrfout_name)): os.unlink(os.path.join(dir_out, wrfout_name))
                os.symlink(wrfout, os.path.join(dir_out, wrfout_name))

                with Dataset(os.path.join(dir_out, wrfout_name), 'r+') as wrfout_read:
                    wrfout_read.START_DATE = anl_start_time.strftime('%Y-%m-%d_%H:00:00')
                    wrfout_read.SIMULATION_START_DATE = anl_start_time.strftime('%Y-%m-%d_%H:00:00')

def setup_gfdl_folder(data_library_name, dir_case, case_name, exp_name, copy_exp_name):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc="DA Cycle"):
        case = '_'.join([case_name, exp_name, 'C' + str(da_cycle).zfill(2)])
        copy_case = '_'.join([case_name, copy_exp_name, 'C' + str(da_cycle).zfill(2)])

        folder_in = os.path.join(dir_exp, 'track_intensity', copy_case)
        folder_out = os.path.join(dir_exp, 'track_intensity', case)
        folder_multi_in = os.path.join(folder_in, 'multi')
        folder_multi_out = os.path.join(folder_out, 'multi')
        os.makedirs(folder_multi_out, exist_ok=True)

        for file_name in ['gettrk.exe', 'grbindex.exe', 'input.nml', 'tcvit_rsmc_storms.txt']:
            shutil.copy(os.path.join(folder_multi_in, file_name), os.path.join(folder_multi_out, file_name))

        for file_name in glob.glob(os.path.join(folder_multi_in, 'fort.*')):
            shutil.copy(file_name, folder_multi_out)

        folder_parm_in = os.path.join(folder_in, 'parm')
        folder_parm_out = os.path.join(folder_out, 'parm')
        os.makedirs(folder_parm_out, exist_ok=True)
        os.system(f'cp {os.path.join(folder_parm_in, "wrf_cntrl.parm")} {os.path.join(folder_parm_out, "wrf_cntrl.parm")}')

        folder_postprd_in = os.path.join(folder_in, 'postprd')
        folder_postprd_out = os.path.join(folder_out, 'postprd')
        os.makedirs(folder_postprd_out, exist_ok=True)
        os.system(f'cp {os.path.join(folder_postprd_in, "run_unipost")} {os.path.join(folder_postprd_out, "run_unipost")}')

        print("Please revise fort.15 in multi")
        print("Please revise input.nml in multi")
        print("Please revise tcvit_rsmc_storms.txt in multi")
        print("Please revise run_unipost in postprd")
        print("Please run run_unipost!")

def process_gfdl_files(data_library_name, dir_case, case_name, exp_name, \
                       input_anl_start_time=datetime(2000, 1, 1, 0, 0, 0), \
                       input_forecast_end_time=datetime(2000, 1, 1, 0, 0, 0)):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
    itime=attributes[(dir_case, case_name)]['itime']
    forecast_hours=attributes[(dir_case, case_name)]['forecast_hours']
    dir_exp=attributes[(dir_case, case_name)]['dir_exp']
    GFDL_domains=attributes[(dir_case, case_name)]['GFDL_domains']
    cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
    history_interval=attributes[(dir_case, case_name)]['history_interval']
    hwrf_header=attributes[(dir_case, case_name)]['hwrf_header']
    initial_time = datetime(*itime)
    dtime = history_interval * 60

    for da_cycle in tqdm(range(1, total_da_cycles+1), desc="DA Cycle"):
        case = '_'.join([case_name, exp_name, 'C' + str(da_cycle).zfill(2)])
        files_exp = os.path.join(dir_exp, 'track_intensity', case)
        files_dir = os.path.join(files_exp, 'postprd')
        files_out = os.path.join(files_exp, 'multi')
        
        if input_anl_start_time == datetime(2000, 1, 1, 0, 0, 0):
            anl_start_time = initial_time + timedelta(hours=cycling_interval)
        else:
            anl_start_time = input_anl_start_time

        if input_forecast_end_time == datetime(2000, 1, 1, 0, 0, 0):
            forecast_end_time = initial_time + timedelta(hours=cycling_interval*da_cycle + forecast_hours)
        else:
            forecast_end_time = input_forecast_end_time

        n_time = int((forecast_end_time - anl_start_time).total_seconds() / 3600 / history_interval) + 1

        for item in tqdm(range(n_time), desc="Processing files", leave=False):
            for dom in GFDL_domains:
                input_file = os.path.join(files_dir, f'FINAL_{dom}.{str(item * history_interval).zfill(2)}')
                flnm_hwrf = f'{files_out}/{hwrf_header}.f{str(item * dtime).zfill(5)}'
                flnm_hwrf_ix = f'{flnm_hwrf}.ix'
                if os.path.islink(flnm_hwrf): os.unlink(flnm_hwrf)
                os.symlink(input_file, flnm_hwrf, target_is_directory=False)
                os.system(f'{files_out}/grbindex.exe {flnm_hwrf} {flnm_hwrf_ix}')