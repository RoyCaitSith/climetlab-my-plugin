import os
import re
import time
import shutil
import datetime
import file_operations as fo
from tqdm.notebook import tqdm

def check_file_existence(time_start, time_end, directories, file_format, domains, history_interval):

    ctime = time_start
    while ctime <= time_end:
        for dom in domains:
            file_name = file_format.format(dom=dom, ctime=ctime)
            if not any(os.path.exists(os.path.join(directory, file_name)) for directory in directories):
                return False
        ctime = ctime + datetime.timedelta(hours=history_interval)
    return True

def copy_files(time_start, time_end, dir_src, file_format_src, dir_dst, file_format_dst, domains, history_interval):

    n_time = int((time_end-time_start).total_seconds()/3600/history_interval+1)
    for idt in tqdm(range(n_time), desc='Files', unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        ctime = time_start + datetime.timedelta(hours=idt*history_interval)
        for dom in domains:
            file_name_src = file_format_src.format(dom=dom, ctime=ctime)
            file_name_dst = file_format_dst.format(dom=dom, ctime=ctime)
            src = os.path.join(dir_src, file_name_src)
            dst = os.path.join(dir_dst, file_name_dst)
            os.system(f'cp {src} {dst}')

def move_files(time_start, time_end, dir_src, file_format_src, dir_dst, file_format_dst, domains, history_interval):

    n_time = int((time_end-time_start).total_seconds()/3600/history_interval+1)
    for idt in tqdm(range(n_time), desc='Files', unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        ctime = time_start + datetime.timedelta(hours=idt*history_interval)
        for dom in domains:
            file_name_src = file_format_src.format(dom=dom, ctime=ctime)
            file_name_dst = file_format_dst.format(dom=dom, ctime=ctime)
            src = os.path.join(dir_src, file_name_src)
            dst = os.path.join(dir_dst, file_name_dst)
            if os.path.exists(src) and not os.path.exists(dst):
                os.system(f'mv {src} {dst}')
            else:
                print(f'{file_name_dst} already exists in {dir_dst}')

def update_namelist_time_control(time_start, time_end, forecast_hours, dir_case, forecast_domains, history_interval):

    def update_time_parts(dt, max_dom):
        time_parts = ['%Y', '%m', '%d', '%H']
        return [dt.strftime(time_part) + ', ' for time_part in time_parts]

    namelist_input_dir = os.path.join(dir_case, 'Run_WRF', 'namelist.input')
    namelist_input = fo.change_content(namelist_input_dir)
    max_dom = len(forecast_domains)
    start_parts = update_time_parts(time_start, max_dom)
    end_parts = update_time_parts(time_end, max_dom)
    for idx, time_part in enumerate(['start_year', 'start_month', 'start_day', 'start_hour']):
        namelist_input.substitude_string(time_part, ' = ', start_parts[idx] * max_dom)
    for idx, time_part in enumerate(['end_year', 'end_month', 'end_day', 'end_hour']):
        namelist_input.substitude_string(time_part, ' = ', end_parts[idx] * max_dom)

    namelist_input.substitude_string('max_dom', ' = ', str(max_dom))
    namelist_input.substitude_string('run_days', ' = ', f'{forecast_hours // 24},')
    namelist_input.substitude_string('run_hours', ' = ', f'{forecast_hours % 24},')
    namelist_input.substitude_string('input_from_file', ' = ', '.true., ' + '.false., ' * (max_dom - 1))
    namelist_input.substitude_string('history_interval', ' = ', f'{history_interval*60}, ' * max_dom)
    namelist_input.save_content()

def submit_job(dir_script, script_name, whether_wait, nodes, ntasks, account, partition, user_id='u1237353', sleep_interval=15):

    script_name_dir = os.path.join(dir_script, script_name)
    script = fo.change_content(script_name_dir)
    script.substitude_string('#SBATCH --nodes', '=', str(nodes))
    script.substitude_string('#SBATCH --ntasks', '=', str(ntasks))
    script.substitude_string('#SBATCH --account', '=', account)
    script.substitude_string('#SBATCH --partition', '=', partition)
    script.save_content()

    info = os.popen(f'cd {dir_script} && sbatch {script_name}').read()
    jobid = re.findall(r"\d+\.?\d*", info)
    print(f'jobid: {jobid}')

    # Wait for the WRF job to complete
    if whether_wait:
        while any(num == jobid[0] for num in re.findall(r"\d+\.?\d*", os.popen(f'squeue -u {user_id}').read())):
            time.sleep(sleep_interval)
        print(f'Finish running the job')

    return

def run_wrf_forecast(case_name, exp_name, da_cycle, itime, forecast_hours, dir_exp, dir_scratch, da_domains, forecast_domains, cycling_interval, history_interval, whether_wait, nodes, ntasks, account, partition):

    exp_name = exp_name + '_C' + str(da_cycle).zfill(2)
    case = '_'.join([case_name, exp_name])
    initial_time = datetime.datetime(*itime)
    initial_time_str = initial_time.strftime('%Y%m%d%H')
    anl_start_time = initial_time + datetime.timedelta(hours=6.0)
    anl_end_time = anl_start_time + datetime.timedelta(hours=6.0*(da_cycle-1))
    time_start = anl_end_time
    time_end = time_start + datetime.timedelta(hours=forecast_hours)
    dir_da = os.path.join(dir_exp, 'cycling_da', 'Data', case_name, exp_name, 'da')
    dir_bkg = os.path.join(dir_exp, 'cycling_da', 'Data', case_name, exp_name, 'bkg')
    dir_case = os.path.join(dir_scratch, case)

    # Check the existence of wrf_inout
    result_wrf_inout = check_file_existence(time_start=time_start,
                                            time_end=time_start,
                                            directories=[dir_da],
                                            file_format='wrf_inout.{ctime:%Y%m%d%H}.{dom}',
                                            domains=da_domains,
                                            history_interval=cycling_interval)
    if not result_wrf_inout:
        print('No wrf_inout file')
        return
    print('Finsh checking the existence of wrf_inout')

    # Check the existence of wrfout
    print('Check wrfout files')
    result_wrfout = check_file_existence(time_start=time_start,
                                         time_end=time_end,
                                         directories=[dir_bkg, os.path.join(dir_case, initial_time_str)],
                                         file_format='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                                         domains=forecast_domains,
                                         history_interval=history_interval)

    if not result_wrfout:
        # Copy wrfinput
        print('Wrfout does not exist! Start to copy wrf_inout to run the forecast')
        copy_files(time_start=time_start,
                   time_end=time_start,
                   dir_src=dir_da,
                   file_format_src='wrf_inout.{ctime:%Y%m%d%H}.{dom}',
                   dir_dst=os.path.join(dir_case, 'Run_WRF'),
                   file_format_dst='wrfinput_{dom}',
                   domains=da_domains,
                   history_interval=cycling_interval)

        # Time_Control
        print('Revise namelist.input')
        update_namelist_time_control(time_start, time_end, forecast_hours, dir_case, forecast_domains, history_interval)

        # Run wrf to get the forecast
        print(f'Run wrf from {time_start} to {time_end}')
        submit_job(dir_script=os.path.join(dir_case, 'Run_WRF'),
                   script_name='run_wrf.sh',
                   whether_wait=whether_wait,
                   nodes=nodes,
                   ntasks=ntasks,
                   account=account,
                   partition=partition)

        if whether_wait:
            # Check the existence of wrfout while finishing
            print('Check wrfout files after running forecast')
            result_wrfout = check_file_existence(time_start=time_start,
                                                 time_end=time_end,
                                                 directories=[dir_bkg, os.path.join(dir_case, initial_time_str)],
                                                 file_format='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                                                 domains=forecast_domains,
                                                 history_interval=history_interval)
            if not result_wrfout: print('Fail to run wrf forecast')

    if result_wrfout:
        print(f'Move wrf forecasts from {time_start} to {time_end}')
        move_files(time_start=time_start,
                   time_end=time_end,
                   dir_src=os.path.join(dir_case, initial_time_str),
                   file_format_src='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                   dir_dst=dir_bkg,
                   file_format_dst='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                   domains=forecast_domains,
                   history_interval=history_interval)
