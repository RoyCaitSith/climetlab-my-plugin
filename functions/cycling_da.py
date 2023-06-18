import os
import re
import sys
import time
import shutil
import datetime
import requests
import importlib
import subprocess
import file_operations as fo
import matplotlib.pyplot as plt
from tqdm.notebook import tqdm
from IPython.display import Image as IPImage

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

def run_wps_and_real(data_library_name, dir_case, case_name, exp_name, period, boundary_data, whether_wait, nodes, ntasks, account, partition):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    # Set the directories of the input files or procedures
    dir_GFS = attributes[(dir_case, case_name)]['dir_GFS']
    dir_GDAS = attributes[(dir_case, case_name)]['dir_GDAS']
    dir_namelists = attributes[(dir_case, case_name)]['dir_namelists']
    dir_scratch = attributes[(dir_case, case_name)]['dir_scratch']
    itime = attributes[(dir_case, case_name)]['itime']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    da_domains = attributes[(dir_case, case_name)]['da_domains']
    forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
    wps_interval = attributes[(dir_case, case_name)]['wps_interval']
    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']

    # I do not need to set the directories of these files
    namelist_wps_dir   = os.path.join(dir_namelists, 'namelist.wps')
    namelist_input_dir = os.path.join(dir_namelists, 'namelist.input')
    run_wps_dir        = os.path.join(dir_namelists, 'run_wps.sh')
    run_wrf_dir        = os.path.join(dir_namelists, 'run_wrf.sh')

    if period == 'cycling_da': da_cycle_start = total_da_cycles
    if period == 'forecast': da_cycle_start = 1
    for da_cycle in range(da_cycle_start, total_da_cycles+1):

        # Set the folder name of the new case
        if period == 'cycling_da': case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
        if period == 'forecast': case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2), 'Forecast'])

        folder_dir = os.path.join(dir_scratch, case)
        os.system(f"rm -rf {folder_dir}")
        fo.create_new_case_folder(folder_dir)
        print(folder_dir)

        start_date_str = ''
        end_date_str = ''
        run_days_str = ''
        run_hours_str = ''
        start_YYYY_str = ''
        start_MM_str = ''
        start_DD_str = ''
        start_HH_str = ''
        end_YYYY_str = ''
        end_MM_str = ''
        end_DD_str = ''
        end_HH_str = ''

        initial_time     = datetime.datetime(*itime)
        initial_time_str = initial_time.strftime('%Y%m%d%H')
        anl_start_time   = initial_time + datetime.timedelta(hours=cycling_interval)
        anl_end_time     = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
        analysis_hours   = da_cycle*cycling_interval

        if period == 'cycling_da':
            max_dom = len(da_domains)
            start_date = initial_time
            total_hours = analysis_hours
            wps_interval = cycling_interval
        if period == 'forecast':
            max_dom = len(forecast_domains)
            start_date = anl_end_time
            total_hours = forecast_hours + wps_interval
        end_date = start_date + datetime.timedelta(hours = total_hours)
        print(f"domains of {period} period: {max_dom}")
        print(f"start_date: {start_date}")
        print(f"end_date: {end_date}")
        print(f"total_hours: {total_hours}")

        # Set the variables in the namelist.wps
        namelist_wps = fo.change_content(namelist_wps_dir)
        # Share
        start_date_str = max_dom * f"'{start_date.strftime('%Y-%m-%d_%H:00:00')}',"
        end_date_str   = max_dom * f"'{end_date.strftime('%Y-%m-%d_%H:00:00')}',"
        namelist_wps.substitude_string('max_dom',          ' = ', str(max_dom))
        namelist_wps.substitude_string('start_date',       ' = ', start_date_str)
        namelist_wps.substitude_string('end_date',         ' = ', end_date_str)
        namelist_wps.substitude_string('interval_seconds', ' = ', str(3600*wps_interval))
        # Share
        namelist_wps.substitude_string('opt_output_from_geogrid_path', ' = ', f"'{folder_dir}/Geogrid_Data/'")
        # Metgrid
        namelist_wps.substitude_string('opt_output_from_metgrid_path', ' = ', f"'{folder_dir}/Metgrid_Data/'")
        namelist_wps.save_content()

        # Set the variables in the namelist.input
        namelist_input = fo.change_content(namelist_input_dir)
        # Time_Control
        run_days_str   = f"{str(total_hours//24)}, "
        run_hours_str  = f"{str(total_hours %24)}, "
        start_YYYY_str = max_dom * f"{start_date.strftime('%Y')}, "
        start_MM_str   = max_dom * f"{start_date.strftime('%m')}, "
        start_DD_str   = max_dom * f"{start_date.strftime('%d')}, "
        start_HH_str   = max_dom * f"{start_date.strftime('%H')}, "
        end_YYYY_str   = max_dom * f"{end_date.strftime('%Y')}, "
        end_MM_str     = max_dom * f"{end_date.strftime('%m')}, "
        end_DD_str     = max_dom * f"{end_date.strftime('%d')}, "
        end_HH_str     = max_dom * f"{end_date.strftime('%H')}, "

        namelist_input.substitude_string('run_days',         ' = ', run_days_str)
        namelist_input.substitude_string('run_hours',        ' = ', run_hours_str)
        namelist_input.substitude_string('start_year',       ' = ', start_YYYY_str)
        namelist_input.substitude_string('start_month',      ' = ', start_MM_str)
        namelist_input.substitude_string('start_day',        ' = ', start_DD_str)
        namelist_input.substitude_string('start_hour',       ' = ', start_HH_str)
        namelist_input.substitude_string('end_year',         ' = ', end_YYYY_str)
        namelist_input.substitude_string('end_month',        ' = ', end_MM_str)
        namelist_input.substitude_string('end_day',          ' = ', end_DD_str)
        namelist_input.substitude_string('end_hour',         ' = ', end_HH_str)
        namelist_input.substitude_string('interval_seconds', ' = ', str(3600*wps_interval))
        namelist_input.substitude_string('max_dom',          ' = ', f"{str(max_dom)}, ")
        namelist_input.substitude_string('history_outname',  ' = ', f"'{folder_dir}/{initial_time_str}/wrfout_d<domain>_<date>'")
        namelist_input.substitude_string('rst_outname',      ' = ', f"'{folder_dir}/{initial_time_str}/wrfrst_d<domain>_<date>'")

        if boundary_data == 'GFS':
            namelist_input.substitude_string('num_metgrid_levels',      ' = ', '34, ')
            namelist_input.substitude_string('num_metgrid_soil_levels', ' = ', '4, ')

        namelist_input.save_content()

        print(f"Create Geogrid_Data in {folder_dir}")
        os.mkdir(os.path.join(folder_dir, 'Geogrid_Data'))
        print(f"Create Boundary_Condition_Data in {folder_dir}")
        os.mkdir(os.path.join(folder_dir, 'Boundary_Condition_Data'))
        print(f"Create Metgrid_Data in {folder_dir}")
        os.mkdir(os.path.join(folder_dir, 'Metgrid_Data'))
        print(f"Create Run_WRF in {folder_dir}")
        os.mkdir(os.path.join(folder_dir, 'Run_WRF'))
        print(f"Create {initial_time_str} in {folder_dir}")
        os.mkdir(os.path.join(folder_dir, initial_time_str))
        print('Copy the boundary condition data into Boundary_Condition_Data')

        for idth in range(0, total_hours + wps_interval, wps_interval):
            time_now = initial_time + datetime.timedelta(hours = idth)
            if period == 'cycling_da': fhours = 0
            if period == 'forecast':
                time_now = anl_end_time
                fhours = idth

            time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')
            time_now_YYYYMMDD = time_now.strftime('%Y%m%d')
            time_now_YYYY = time_now.strftime('%Y')

            if boundary_data == 'GFS':
                bc_filename = f"gfs.0p25.{time_now_YYYYMMDDHH}.f{str(fhours).zfill(3)}.grib2"
                dir_bc_filename = os.path.join(dir_GFS, bc_filename)
                dir_rda = 'https://data.rda.ucar.edu/ds084.1'
            print(dir_bc_filename)

            if not os.path.exists(dir_bc_filename):
                rda_bc_filename = os.path.join(dir_rda, time_now_YYYY, time_now_YYYYMMDD, bc_filename)
                response = requests.get(rda_bc_filename, stream=True)
                with open(dir_bc_filename, "wb") as f:
                    f.write(response.content)
            os.system(f"cp {dir_bc_filename} {folder_dir}/Boundary_Condition_Data")

        # Set the variable in the run_wps.sh
        if boundary_data == 'GFS': vtable = 'Vtable.GFS'
        print(f"Vtable of Boundary Condition: {vtable}")

        run_wps = fo.change_content(run_wps_dir)
        run_wps.substitude_string('#SBATCH -J', ' ', initial_time_str[2::])
        run_wps.substitude_string('export SCRATCH_DIRECTORY', '=', folder_dir)
        run_wps.substitude_string('ln -sf $WORK_DIRECTORY/WPS/ungrib/Variable_Tables', '/', f"{vtable} $RUN_WRF_DIRECTORY/Vtable")

        if boundary_data == 'GFS':
            run_wps.substitude_string('$RUN_WRF_DIRECTORY/link_grib.csh $SCRATCH_DIRECTORY/Boundary_Condition_Data', '/', 'gfs* $RUN_WRF_DIRECTORY')

        run_wps.save_content()

        # Set the variable in the run_wrf.sh
        run_wrf = fo.change_content(run_wrf_dir)
        run_wrf.substitude_string('#SBATCH -J', ' ', initial_time_str[2::])
        run_wrf.substitude_string('export SCRATCH_DIRECTORY', '=', folder_dir)
        run_wrf.save_content()

        print('Copy namelist.wps into Run_WRF')
        shutil.copy(namelist_wps_dir, folder_dir)
        print('Copy namelist.input into Run_WRF')
        shutil.copy(namelist_input_dir, folder_dir)
        print('Copy run_wps.sh into Run_WRF')
        shutil.copy(run_wps_dir, os.path.join(folder_dir, 'Run_WRF'))
        print('Copy run_wrf.sh into Run_WRF')
        shutil.copy(run_wrf_dir, os.path.join(folder_dir, 'Run_WRF'))

        # Run WPS
        print(f'Run WPS from {start_date} to {end_date}')
        submit_job(dir_script=os.path.join(folder_dir, 'Run_WRF'),
                   script_name='run_wps.sh',
                   whether_wait=whether_wait,
                   nodes=nodes,
                   ntasks=ntasks,
                   account=account,
                   partition=partition)
        print('\n')

    os.system(f"cd {dir_namelists} && ncl plotgrids_new.ncl")
    wps_show_dom = os.path.join(dir_namelists, 'wps_show_dom.png')
    command = f"convert {wps_show_dom} -trim {wps_show_dom}"
    subprocess.run(command, shell=True)
    image = IPImage(filename=wps_show_dom)
    display(image)

def run_wrf_forecast(data_library_name, dir_case, case_name, exp_name, da_cycle, whether_wait, nodes, ntasks, account, partition):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    itime = attributes[(dir_case, case_name)]['itime']
    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_scratch = attributes[(dir_case, case_name)]['dir_scratch']
    da_domains = attributes[(dir_case, case_name)]['da_domains']
    forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    history_interval = attributes[(dir_case, case_name)]['history_interval']

    case = '_'.join([case_name, exp_name + '_C' + str(da_cycle).zfill(2)])
    initial_time = datetime.datetime(*itime)
    initial_time_str = initial_time.strftime('%Y%m%d%H')
    anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)
    anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
    time_start = anl_end_time
    time_end = time_start + datetime.timedelta(hours=forecast_hours)
    dir_da = os.path.join(dir_exp, 'cycling_da', 'Data', case_name, exp_name + '_C' + str(da_cycle).zfill(2), 'da')
    dir_bkg = os.path.join(dir_exp, 'cycling_da', 'Data', case_name, exp_name + '_C' + str(da_cycle).zfill(2), 'bkg')
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
