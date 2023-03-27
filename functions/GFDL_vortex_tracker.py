import os
import glob
import shutil
import datetime
from netCDF4 import Dataset
from tqdm.notebook import tqdm

def link_wrfout(case_name, exp_name, da_cycle, itime, forecast_hours, dir_exp, history_interval, GFDL_domains):

    exp_name = exp_name + '_C' + str(da_cycle).zfill(2)
    case = '_'.join([case_name, exp_name])
    initial_time = datetime.datetime(*itime)
    initial_time_str = initial_time.strftime('%Y%m%d%H')
    anl_start_time = initial_time + datetime.timedelta(hours=6.0)
    forecast_end_time = anl_start_time + datetime.timedelta(hours=6.0*(da_cycle-1) + forecast_hours)
    dir_in = os.path.join(dir_exp, 'cycling_da', 'Data', case_name, exp_name, 'bkg')
    dir_out = os.path.join(dir_exp, 'track_intensity', case_name, exp_name, 'wrfprd')
    os.makedirs(dir_out, exist_ok=True)

    n_time = int((forecast_end_time - anl_start_time).total_seconds() / 3600 / history_interval) + 1

    print(f'Link wrfout files from {anl_start_time} to {forecast_end_time}')
    for item in tqdm(range(n_time), desc="Processing files"):
        for dom in GFDL_domains:
            forecast_time_now = anl_start_time + datetime.timedelta(hours=history_interval * item)
            wrfout_time = forecast_time_now.strftime('%Y-%m-%d_%H:00:00')
            wrfout_name = f'wrfout_{dom}_{wrfout_time}'
            wrfout = os.path.join(dir_in, wrfout_name)
            if os.path.islink(os.path.join(dir_out, wrfout_name)): os.unlink(os.path.join(dir_out, wrfout_name))
            os.symlink(wrfout, os.path.join(dir_out, wrfout_name))

            with Dataset(os.path.join(dir_out, wrfout_name), 'r+') as wrfout_read:
                wrfout_read.START_DATE = anl_start_time.strftime('%Y-%m-%d_%H:00:00')
                wrfout_read.SIMULATION_START_DATE = anl_start_time.strftime('%Y-%m-%d_%H:00:00')

def setup_GFDL_folder(case_name, exp_name, da_cycle, dir_exp, copy_exp_name):

    exp_name = exp_name + '_C' + str(da_cycle).zfill(2)
    case = '_'.join([case_name, exp_name])
    print(case)

    folder_in = os.path.join(dir_exp, 'track_intensity', case_name, copy_exp_name)
    folder_out = os.path.join(dir_exp, 'track_intensity', case_name, exp_name)
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

def process_GFDL_files(case_name, exp_name, da_cycle, itime, forecast_hours, dir_exp, GFDL_domains, history_interval, hwrf_header):

    exp_name = exp_name + '_C' + str(da_cycle).zfill(2)
    files_exp = os.path.join(dir_exp, 'track_intensity', case_name, exp_name)
    files_hwrf = os.path.join(files_exp, 'multi', hwrf_header)
    files_dir = os.path.join(files_exp, 'postprd')
    files_out = os.path.join(files_exp, 'multi')
    dtime = history_interval * 60

    initial_time = datetime.datetime(*itime)
    anl_start_time = initial_time + datetime.timedelta(hours=6.0)
    forecast_end_time = anl_start_time + datetime.timedelta(hours=6.0*(da_cycle-1) + forecast_hours)
    n_time = int((forecast_end_time - anl_start_time).total_seconds() / 3600 / history_interval) + 1

    for item in tqdm(range(n_time), desc="Processing files"):
        for dom in GFDL_domains:
            input_file = os.path.join(files_dir, f'FINAL_{dom}.{str(item * history_interval).zfill(2)}')
            flnm_hwrf = f'{files_out}/{hwrf_header}.f{str(item * dtime).zfill(5)}'
            flnm_hwrf_ix = f'{flnm_hwrf}.ix'
            if os.path.islink(flnm_hwrf): os.unlink(flnm_hwrf)
            os.symlink(input_file, flnm_hwrf, target_is_directory=False)
            os.system(f'{files_out}/grbindex.exe {flnm_hwrf} {flnm_hwrf_ix}')
