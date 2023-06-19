import os
import shutil
import datetime
import importlib
import subprocess
import file_operations as fo
from tqdm.notebook import tqdm
from cycling_da import submit_job, check_file_existence, update_namelist_time_control

def download_gefs_ensemble(data_library_name, dir_case, case_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    dir_GEFS = attributes[(dir_case, case_name)]['dir_GEFS']
    itime = attributes[(dir_case, case_name)]['itime']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    initial_time = datetime.datetime(*itime)
    anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)
    anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(total_da_cycles-1))
    download_stime = initial_time - datetime.timedelta(hours=cycling_interval)
    download_etime = anl_end_time
    n_download_time = int((download_etime - download_stime).total_seconds()/cycling_interval/3600 + 1)
    os.makedirs(dir_GEFS, exist_ok=True)

    aws_s3_cp = 'aws s3 cp --no-sign-request '
    aws_s3_bucket = 's3://noaa-gefs-pds/'
    download_interval = cycling_interval
    forecast_interval = cycling_interval
    forecast_period = 12
    n_ensemble = 30

    for idx in tqdm(range(n_download_time), desc='Time', unit="files", bar_format="{desc}: {n}/{total} cycling_interval | {elapsed}<{remaining}"):
        download_ntime = download_stime + datetime.timedelta(hours = idx*cycling_interval)
        YYYYMMDD = download_ntime.strftime('%Y%m%d')
        HH = download_ntime.strftime('%H')
        dir_download = '/'.join([dir_GEFS, YYYYMMDD])
        os.makedirs(dir_download, exist_ok=True)
        dir_download = '/'.join([dir_download, HH])
        os.makedirs(dir_download, exist_ok=True)

        for idn in tqdm(range(n_ensemble+1), desc='Ensembles', leave=False, unit="files", bar_format="{desc}: {n}/{total} ensembles | {elapsed}<{remaining}"):

            forecast_ntime = 0
            while forecast_ntime <= forecast_period:

                #if idn == 0:
                    #file_name_avg_a = 'geavg.t' + HH + 'z.pgrb2a.0p50.f' + str(forecast_ntime).zfill(3)
                    #file_name_avg_b = 'geavg.t' + HH + 'z.pgrb2b.0p50.f' + str(forecast_ntime).zfill(3)
                    #file_name_avg_c = 'geavg.t' + HH + 'z.pgrb2c.0p50.f' + str(forecast_ntime).zfill(3)
                    #download_file_name_avg_a = '/'.join([dir_download, file_name_avg_a])
                    #download_file_name_avg_b = '/'.join([dir_download, file_name_avg_b])
                    #download_file_name_avg_c = '/'.join([dir_download, file_name_avg_c])
                    #aws_directory_avg_a = '/'.join(['gefs.'+YYYYMMDD, HH, 'atmos', 'pgrb2ap5/'])
                    #aws_directory_avg_b = '/'.join(['gefs.'+YYYYMMDD, HH, 'atmos', 'pgrb2bp5/'])
                    #aws_command_avg_a = aws_s3_cp + aws_s3_bucket + aws_directory_avg_a + file_name_avg_a + ' ' + download_file_name_avg_a
                    #aws_command_avg_b = aws_s3_cp + aws_s3_bucket + aws_directory_avg_b + file_name_avg_b + ' ' + download_file_name_avg_b
                    #combine_command_avg = ' '.join(['grib_copy', download_file_name_avg_a, download_file_name_avg_b, download_file_name_avg_c])
                    ##print(aws_command_avg_a)
                    #output = subprocess.check_output(aws_command_avg_a, shell=True)
                    ##print(aws_command_avg_b)
                    #output = subprocess.check_output(aws_command_avg_b, shell=True)
                    ##print(combine_command_avg)
                    #output = subprocess.check_output(combine_command_avg, shell=True)

                file_type = 'gep'
                if idn == 0: file_type = 'gec'

                file_name_a = file_type + str(idn).zfill(2) + '.t' + HH + 'z.pgrb2a.0p50.f' + str(forecast_ntime).zfill(3)
                file_name_b = file_type + str(idn).zfill(2) + '.t' + HH + 'z.pgrb2b.0p50.f' + str(forecast_ntime).zfill(3)
                file_name_c = file_type + str(idn).zfill(2) + '.t' + HH + 'z.pgrb2c.0p50.f' + str(forecast_ntime).zfill(3)
                download_file_name_a = '/'.join([dir_download, file_name_a])
                download_file_name_b = '/'.join([dir_download, file_name_b])
                download_file_name_c = '/'.join([dir_download, file_name_c])

                aws_directory_a = '/'.join(['gefs.'+YYYYMMDD, HH, 'atmos', 'pgrb2ap5/'])
                aws_directory_b = '/'.join(['gefs.'+YYYYMMDD, HH, 'atmos', 'pgrb2bp5/'])
                aws_command_a = aws_s3_cp + aws_s3_bucket + aws_directory_a + file_name_a + ' ' + download_file_name_a
                aws_command_b = aws_s3_cp + aws_s3_bucket + aws_directory_b + file_name_b + ' ' + download_file_name_b
                combine_command = ' '.join(['grib_copy', download_file_name_a, download_file_name_b, download_file_name_c])

                #print(aws_command_a)
                output = subprocess.check_output(aws_command_a, shell=True)
                #print(aws_command_b)
                pipe = subprocess.check_output(aws_command_b, shell=True)
                #print(combine_command)
                pipe = subprocess.check_output(combine_command, shell=True)

                forecast_ntime += forecast_interval

def run_wps_and_real_gefs(data_library_name, dir_case, case_name, exp_name, whether_wait, nodes, ntasks, account, partition):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    # Set the directories of the input files or procedures
    dir_GEFS = attributes[(dir_case, case_name)]['dir_GEFS']
    dir_namelists = attributes[(dir_case, case_name)]['dir_namelists']
    dir_scratch = attributes[(dir_case, case_name)]['dir_scratch']
    itime = attributes[(dir_case, case_name)]['itime']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    boundary_data_ensemble = attributes[(dir_case, case_name)]['boundary_data_ensemble']
    ensemble_members = attributes[(dir_case, case_name)]['ensemble_members']
    da_domains = attributes[(dir_case, case_name)]['da_domains']
    forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
    wps_interval = attributes[(dir_case, case_name)]['wps_interval']
    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']

    # I do not need to set the directories of these files
    namelist_wps_dir   = os.path.join(dir_namelists, 'namelist.wps')
    namelist_input_dir = os.path.join(dir_namelists, 'namelist.input')
    run_wps_dir        = os.path.join(dir_namelists, 'run_wps.sh')
    run_wrf_dir        = os.path.join(dir_namelists, 'run_wrf.sh')

    #print(f'Generate 6 and 12 hour ensemble forecasts for each cycles')
    ensemble_forecast_hours = [6, 12]
    for ens_hours in ensemble_forecast_hours:
        for idens in range(1, int(ensemble_members/2)+1):
            for da_cycle in range(1, total_da_cycles+1):

                # Set the folder name of the new case
                case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2), 'GEFS', f'f{str(ens_hours).zfill(3)}', f'mem{str(idens).zfill(2)}'])
                folder_dir = os.path.join(dir_scratch, case)
                os.system(f"rm -rf {folder_dir}")
                fo.create_new_case_folder(folder_dir)
                #print(folder_dir)

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

                max_dom = len(da_domains)
                wps_interval = cycling_interval
                start_date = anl_end_time - datetime.timedelta(hours = ens_hours)
                end_date = anl_end_time
                #print(f"domains: {max_dom}")
                #print(f"start_date: {start_date}")
                #print(f"end_date: {end_date}")
                #print(f"ens_hours: {ens_hours}")

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
                run_days_str   = f"{str(ens_hours//24)}, "
                run_hours_str  = f"{str(ens_hours %24)}, "
                start_YYYY_str = max_dom * f"{start_date.strftime('%Y')}, "
                start_MM_str   = max_dom * f"{start_date.strftime('%m')}, "
                start_DD_str   = max_dom * f"{start_date.strftime('%d')}, "
                start_HH_str   = max_dom * f"{start_date.strftime('%H')}, "
                end_YYYY_str   = max_dom * f"{end_date.strftime('%Y')}, "
                end_MM_str     = max_dom * f"{end_date.strftime('%m')}, "
                end_DD_str     = max_dom * f"{end_date.strftime('%d')}, "
                end_HH_str     = max_dom * f"{end_date.strftime('%H')}, "

                namelist_input.substitude_string('run_days',                ' = ', run_days_str)
                namelist_input.substitude_string('run_hours',               ' = ', run_hours_str)
                namelist_input.substitude_string('start_year',              ' = ', start_YYYY_str)
                namelist_input.substitude_string('start_month',             ' = ', start_MM_str)
                namelist_input.substitude_string('start_day',               ' = ', start_DD_str)
                namelist_input.substitude_string('start_hour',              ' = ', start_HH_str)
                namelist_input.substitude_string('end_year',                ' = ', end_YYYY_str)
                namelist_input.substitude_string('end_month',               ' = ', end_MM_str)
                namelist_input.substitude_string('end_day',                 ' = ', end_DD_str)
                namelist_input.substitude_string('end_hour',                ' = ', end_HH_str)
                namelist_input.substitude_string('interval_seconds',        ' = ', str(3600*wps_interval))
                namelist_input.substitude_string('max_dom',                 ' = ', f"{str(max_dom)}, ")
                namelist_input.substitude_string('history_interval',        ' = ', f'{wps_interval*60}, ' * max_dom)
                namelist_input.substitude_string('history_outname',         ' = ', f"'{folder_dir}/{initial_time_str}/wrfout_d<domain>_<date>'")
                namelist_input.substitude_string('rst_outname',             ' = ', f"'{folder_dir}/{initial_time_str}/wrfrst_d<domain>_<date>'")
                namelist_input.substitude_string('num_metgrid_levels',      ' = ', '32, ')
                namelist_input.substitude_string('num_metgrid_soil_levels', ' = ', '4, ')
                namelist_input.save_content()

                #print(f"Create Geogrid_Data in {folder_dir}")
                os.mkdir(os.path.join(folder_dir, 'Geogrid_Data'))
                #print(f"Create Boundary_Condition_Data in {folder_dir}")
                os.mkdir(os.path.join(folder_dir, 'Boundary_Condition_Data'))
                #print(f"Create Metgrid_Data in {folder_dir}")
                os.mkdir(os.path.join(folder_dir, 'Metgrid_Data'))
                #print(f"Create Run_WRF in {folder_dir}")
                os.mkdir(os.path.join(folder_dir, 'Run_WRF'))
                #print(f"Create {initial_time_str} in {folder_dir}")
                os.mkdir(os.path.join(folder_dir, initial_time_str))
                #print('Copy the boundary condition data into Boundary_Condition_Data')

                time_now = start_date
                time_now_YYYYMMDD = time_now.strftime('%Y%m%d')
                time_now_HH = time_now.strftime('%H')
                for idth in range(0, ens_hours + wps_interval, wps_interval):
                    bc_filename = f'gep{str(idens).zfill(2)}.t{time_now_HH}z.pgrb2c.0p50.f{str(idth).zfill(3)}'
                    dir_bc_filename = os.path.join(dir_GEFS, time_now_YYYYMMDD, time_now_HH, bc_filename)
                    os.system(f"cp {dir_bc_filename} {folder_dir}/Boundary_Condition_Data")
                    #print(dir_bc_filename)

                # Set the variable in the run_wps.sh
                if boundary_data_ensemble == 'GEFS': vtable = 'Vtable.GFSENS'
                #print(f"Vtable of Boundary Condition: {vtable}")

                run_wps = fo.change_content(run_wps_dir)
                run_wps.substitude_string('#SBATCH -J', ' ', initial_time_str[2::])
                run_wps.substitude_string('export SCRATCH_DIRECTORY', '=', folder_dir)
                run_wps.substitude_string('ln -sf $WORK_DIRECTORY/WPS/ungrib/Variable_Tables', '/', f"{vtable} $RUN_WRF_DIRECTORY/Vtable")
                run_wps.substitude_string('$RUN_WRF_DIRECTORY/link_grib.csh $SCRATCH_DIRECTORY/Boundary_Condition_Data', '/', 'gep* $RUN_WRF_DIRECTORY')
                run_wps.save_content()

                # Set the variable in the run_wrf.sh
                run_wrf = fo.change_content(run_wrf_dir)
                run_wrf.substitude_string('#SBATCH -J', ' ', initial_time_str[2::])
                run_wrf.substitude_string('export SCRATCH_DIRECTORY', '=', folder_dir)
                run_wrf.save_content()

                #print('Copy namelist.wps into Run_WRF')
                shutil.copy(namelist_wps_dir, folder_dir)
                #print('Copy namelist.input into Run_WRF')
                shutil.copy(namelist_input_dir, folder_dir)
                #print('Copy run_wps.sh into Run_WRF')
                shutil.copy(run_wps_dir, os.path.join(folder_dir, 'Run_WRF'))
                #print('Copy run_wrf.sh into Run_WRF')
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

def run_wrf_forecast_gefs(data_library_name, dir_case, case_name, exp_name, whether_wait, nodes, ntasks, account, partition):

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
    boundary_data_ensemble = attributes[(dir_case, case_name)]['boundary_data_ensemble']
    ensemble_members = attributes[(dir_case, case_name)]['ensemble_members']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    initial_time = datetime.datetime(*itime)
    initial_time_str = initial_time.strftime('%Y%m%d%H')
    anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)

    ensemble_forecast_hours = [6, 12]
    for ens_hours in ensemble_forecast_hours:
        for idens in range(1, int(ensemble_members/2)+1):
            for da_cycle in range(1, total_da_cycles+1):

                # Set the folder name of the new case
                case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2), 'GEFS', f'f{str(ens_hours).zfill(3)}', f'mem{str(idens).zfill(2)}'])
                anl_end_time = anl_start_time + datetime.timedelta(hours=cycling_interval*(da_cycle-1))
                time_start = anl_end_time - datetime.timedelta(hours = ens_hours)
                time_end = anl_end_time
                dir_case = os.path.join(dir_scratch, case)

                # Check the existence of wrfinput
                result_wrfinput = check_file_existence(time_start=time_start,
                                                       time_end=time_start,
                                                       directories=[os.path.join(dir_case, 'Run_WRF')],
                                                       file_format='wrfinput_{dom}',
                                                       domains=da_domains,
                                                       history_interval=cycling_interval)
                print(f'Check wrfinput: {result_wrfinput}')

                # Check the existence of wrfout
                result_wrfout = check_file_existence(time_start=time_start,
                                                     time_end=time_end,
                                                     directories=[os.path.join(dir_case, initial_time_str)],
                                                     file_format='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                                                     domains=da_domains,
                                                     history_interval=cycling_interval)
                print(f'Check wrfout files: {result_wrfout}')

                if result_wrfinput and not result_wrfout:
                    # Run wrf to get the forecast
                    print(f'Run wrf from {time_start} to {time_end}')
                    submit_job(dir_script=os.path.join(dir_case, 'Run_WRF'),
                               script_name='run_wrf.sh',
                               whether_wait=whether_wait,
                               nodes=nodes,
                               ntasks=ntasks,
                               account=account,
                               partition=partition)
