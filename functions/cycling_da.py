import os
import re
import time
import shutil
import requests
import importlib
import subprocess
import file_operations as fo
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from IPython.display import display
from IPython.display import Image as IPImage

def check_file_existence(time_start, time_end, directories, file_format, domains, history_interval):

    ctime = time_start
    while ctime <= time_end:
        for dom in domains:
            file_name = file_format.format(dom=dom, ctime=ctime)
            if not any(os.path.exists(os.path.join(directory, file_name)) for directory in directories):
                return False
        ctime = ctime + timedelta(hours=history_interval)
    return True

def copy_files(time_start, time_end, dir_src, file_format_src, dir_dst, file_format_dst, domains, history_interval):

    n_time = int((time_end-time_start).total_seconds()/3600/history_interval+1)
    for idt in tqdm(range(n_time), desc='Time', unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        ctime = time_start + timedelta(hours=idt*history_interval)
        for dom in domains:
            file_name_src = file_format_src.format(dom=dom, ctime=ctime)
            file_name_dst = file_format_dst.format(dom=dom, ctime=ctime)
            src = os.path.join(dir_src, file_name_src)
            dst = os.path.join(dir_dst, file_name_dst)
            os.system(f'cp {src} {dst}')

def move_files(time_start, time_end, dir_src, file_format_src, dir_dst, file_format_dst, domains, history_interval):

    n_time = int((time_end-time_start).total_seconds()/3600/history_interval+1)
    for idt in tqdm(range(n_time), desc='Time', unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        ctime = time_start + timedelta(hours=idt*history_interval)
        for dom in domains:
            file_name_src = file_format_src.format(dom=dom, ctime=ctime)
            file_name_dst = file_format_dst.format(dom=dom, ctime=ctime)
            src = os.path.join(dir_src, file_name_src)
            dst = os.path.join(dir_dst, file_name_dst)
            if os.path.exists(src) and not os.path.exists(dst):
                os.system(f'mv {src} {dst}')
            else:
                print(f'{file_name_dst} already exists in {dir_dst}')

def copy_files_after_gsi(dir_option, run_gsi_dir, dir_da, time_now_string, domains):

    for dom in domains:

        diag_conv_ges    = os.path.join(dir_da, '.'.join(['diag_conv_ges', time_now_string, dom]))
        results_conv_ges = os.path.join(dir_da, '.'.join(['results_conv_ges', time_now_string, dom]))
        f = open(os.path.join(dir_option, 'namelist.conv'), 'w')
        f.write(f"&iosetup\n")
        f.write(f" infilename='{diag_conv_ges}',\n")
        f.write(f" outfilename='{results_conv_ges}',\n")
        f.write(f"/")
        f.close()

        print(f"Copy diag conv ges files")
        os.system(f"cp {dir_option}/namelist.conv {dir_da}")
        os.system(f"cp {dir_option}/read_diag_conv.x {dir_da}")
        os.system(f"cp {run_gsi_dir}/case_{dom}/diag_conv_ges.* {diag_conv_ges}")

        print(f"Run read_diag_conv.x")
        os.system(f"cd {dir_da} && ./read_diag_conv.x")
        os.system(f"rm -rf {dir_da}/namelist.conv")
        os.system(f"rm -rf {dir_da}/read_diag_conv.x")

        diag_conv_anl    = os.path.join(dir_da, '.'.join(['diag_conv_anl', time_now_string, dom]))
        results_conv_anl = os.path.join(dir_da, '.'.join(['results_conv_anl', time_now_string, dom]))
        f = open(os.path.join(dir_option, 'namelist.conv'), 'w')
        f.write(f"&iosetup\n")
        f.write(f" infilename='{diag_conv_anl}',\n")
        f.write(f" outfilename='{results_conv_anl}',\n")
        f.write(f"/")
        f.close()

        print(f"Copy diag conv anl files")
        os.system(f"cp {dir_option}/namelist.conv {dir_da}")
        os.system(f"cp {dir_option}/read_diag_conv.x {dir_da}")
        os.system(f"cp {run_gsi_dir}/case_{dom}/diag_conv_anl.* {diag_conv_anl}")

        print(f"Run read_diag_conv.x")
        os.system(f"cd {dir_da} && ./read_diag_conv.x")
        os.system(f"rm -rf {dir_da}/namelist.conv")
        os.system(f"rm -rf {dir_da}/read_diag_conv.x")

        print(f"Save ens_spread.grd")
        ens_spread = os.path.join(dir_da, '_'.join(['ens', 'spread', time_now_string, f"{dom}.grd"]))
        os.system(f"cp {run_gsi_dir}/case_{dom}/ens_spread.grd {ens_spread}")

        print(f"Copy satbias_out")
        satbias_out = os.path.join(dir_da, '.'.join(['satbias_out', time_now_string, dom]))
        os.system(f"cp {run_gsi_dir}/case_{dom}/satbias_out {satbias_out}")

        print(f"Copy satbias_pc.out")
        satbias_pc_out = os.path.join(dir_da, '.'.join(['satbias_pc', 'out', time_now_string, dom]))
        os.system(f"cp {run_gsi_dir}/case_{dom}/satbias_pc.out {satbias_pc_out}")

        print(f"Save wrf_inout of domain {dom}")
        os.system(f"cp {run_gsi_dir}/case_{dom}/wrf_inout {dir_da}/wrf_inout.{time_now_string}.{dom}")

def submit_job(dir_script, script_name, whether_wait, nodes, ntasks, account, partition, nodelist='', user_id='u1237353', sleep_interval=15):

    script_name_dir = os.path.join(dir_script, script_name)
    script = fo.change_content(script_name_dir)
    script.substitude_string('#SBATCH --nodes', '=', str(nodes))
    script.substitude_string('#SBATCH --ntasks', '=', str(ntasks))
    script.substitude_string('#SBATCH --account', '=', account)
    script.substitude_string('#SBATCH --partition', '=', partition)
    script.substitude_string('#SBATCH --nodelist', '=', nodelist)
    script.save_content()

    info = os.popen(f'cd {dir_script} && sbatch {script_name}').read()
    jobid = re.findall(r"\d+\.?\d*", info)
    print(f'jobid: {jobid}')

    # Wait for the WRF job to complete
    if whether_wait:
        while any(num == jobid[0] for num in re.findall(r"\d+\.?\d*", os.popen(f'squeue -u {user_id}').read())):
            time.sleep(sleep_interval)
        print(f'Finish running the job')

def run_wps_and_real(data_library_name, dir_case, case_name, exp_name, wps_version, period, whether_wait, nodes, ntasks, account, partition, nodelist=''):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    # Set the directories of the input files or procedures
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_namelists = attributes[(dir_case, case_name)]['dir_namelists']
    dir_scratch = attributes[(dir_case, case_name)]['dir_scratch']
    itime = attributes[(dir_case, case_name)]['itime']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    history_interval = attributes[(dir_case, case_name)]['history_interval']
    boundary_data_deterministic = attributes[(dir_case, case_name)]['boundary_data_deterministic']
    da_domains = attributes[(dir_case, case_name)]['da_domains']
    forecast_domains = attributes[(dir_case, case_name)]['forecast_domains']
    wps_interval = attributes[(dir_case, case_name)]['wps_interval']
    forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']

    dir_data = os.path.join(dir_exp, 'data')
    dir_GFS = os.path.join(dir_data, 'GFS')
    os.makedirs(dir_data, exist_ok=True)
    os.makedirs(dir_GFS, exist_ok=True)

    # I do not need to set the directories of these files
    specific_case_name = f"{case_name}_{exp_name}_C{str(total_da_cycles).zfill(2)}"
    dir_namelists      = os.path.join(dir_namelists, specific_case_name)
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

        initial_time     = datetime(*itime)
        initial_time_str = initial_time.strftime('%Y%m%d%H')
        anl_start_time   = initial_time + timedelta(hours=cycling_interval)
        anl_end_time     = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
        analysis_hours   = da_cycle*cycling_interval

        if period == 'cycling_da':
            max_dom = len(da_domains)
            start_date = initial_time
            total_hours = analysis_hours
            if boundary_data_deterministic == 'GFS': wps_interval = 6
        if period == 'forecast':
            max_dom = len(forecast_domains)
            start_date = anl_end_time
            total_hours = forecast_hours + 6
        end_date = start_date + timedelta(hours = total_hours)
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

        if period == 'cycling_da':
            wps_show_dom = os.path.join(dir_namelists, 'wps_show_dom.png')
            # os.system(f"ncl {dir_namelists}/plotgrids_new.ncl")
            subprocess.run(f"convert {wps_show_dom} -trim {wps_show_dom}", shell=True)
            image = IPImage(filename=wps_show_dom)
            display(image)

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
        namelist_input.substitude_string('history_interval', ' = ', f'{history_interval*60}, ' * max_dom)
        namelist_input.substitude_string('history_outname',  ' = ', f"'{folder_dir}/{initial_time_str}/wrfout_d<domain>_<date>'")
        namelist_input.substitude_string('rst_outname',      ' = ', f"'{folder_dir}/{initial_time_str}/wrfrst_d<domain>_<date>'")

        if boundary_data_deterministic == 'GFS':
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
            time_now = initial_time + timedelta(hours = idth)
            if period == 'cycling_da': fhours = 0
            if period == 'forecast':
                time_now = anl_end_time
                fhours = idth

            time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')
            time_now_YYYYMMDD = time_now.strftime('%Y%m%d')
            time_now_YYYY = time_now.strftime('%Y')

            if boundary_data_deterministic == 'GFS':
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
        if boundary_data_deterministic == 'GFS': vtable = 'Vtable.GFS'
        print(f"Vtable of Boundary Condition: {vtable}")

        run_wps = fo.change_content(run_wps_dir)
        run_wps.substitude_string('#SBATCH -J', ' ', initial_time_str[2::])
        run_wps.substitude_string('export SCRATCH_DIRECTORY', '=', folder_dir)
        run_wps.substitude_string(f"ln -sf $WORK_DIRECTORY/{wps_version}/ungrib/Variable_Tables", '/', f"{vtable} $RUN_WRF_DIRECTORY/Vtable")

        if boundary_data_deterministic == 'GFS':
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
                   partition=partition,
                   nodelist=nodelist)
        print('\n')

def run_cycling_da(data_library_name, dir_case, case_name, exp_name, \
                   gsi_nodes, gsi_ntasks, gsi_account, gsi_partition, \
                   wrf_nodes, wrf_ntasks, wrf_account, wrf_partition, \
                   gsi_nodelist='', wrf_nodelist=''):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    itime = attributes[(dir_case, case_name)]['itime']
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_scratch = attributes[(dir_case, case_name)]['dir_scratch']
    da_domains = attributes[(dir_case, case_name)]['da_domains']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
    boundary_data_ensemble = attributes[(dir_case, case_name)]['boundary_data_ensemble']
    ensemble_members = attributes[(dir_case, case_name)]['ensemble_members']
    dir_namelists = attributes[(dir_case, case_name)]['dir_namelists']

    specific_case_name = f"{case_name}_{exp_name}_C{str(total_da_cycles).zfill(2)}"
    dir_namelists = os.path.join(dir_namelists, specific_case_name)
    dir_data = os.path.join(dir_exp, 'data')
    dir_gefs_wrf_ensemble = os.path.join(dir_data, 'GEFS_WRF_Ensemble')
    dir_gfs_ensemble = os.path.join(dir_data, 'GFS_Ensemble')
    dir_cycling_da = os.path.join(dir_exp, 'cycling_da', specific_case_name)
    dir_scratch_case = os.path.join(dir_scratch, specific_case_name)
    dir_prepbufr = os.path.join(dir_data, 'PREPBUFR')
    dir_goesbufr = os.path.join(dir_data, 'GOES', 'bufr')
    dir_dawnbufr = os.path.join(dir_data, 'DAWN', 'bufr')
    dir_halobufr = os.path.join(dir_data, 'HALO', 'bufr')
    dir_cygnssbufr = os.path.join(dir_data, 'CYGNSS', 'bufr')
    if 'OLD' in exp_name or 'old' in exp_name:
        if 'V1_AS' in exp_name: dir_tropicsbufr = os.path.join(dir_data, 'TROPICS_V1_AS', 'bufr_old')
        if 'V2_AS' in exp_name: dir_tropicsbufr = os.path.join(dir_data, 'TROPICS_V2_AS', 'bufr_old')
        if 'V1_CS' in exp_name: dir_tropicsbufr = os.path.join(dir_data, 'TROPICS_V1_CS', 'bufr_old')
        if 'V2_CS' in exp_name: dir_tropicsbufr = os.path.join(dir_data, 'TROPICS_V2_CS', 'bufr_old')
    else:
        if 'V1_AS' in exp_name: dir_tropicsbufr = os.path.join(dir_data, 'TROPICS_V1_SEA_AS', 'bufr')
        if 'V2_AS' in exp_name: dir_tropicsbufr = os.path.join(dir_data, 'TROPICS_V2_SEA_AS', 'bufr')
        if 'V1_CS' in exp_name: dir_tropicsbufr = os.path.join(dir_data, 'TROPICS_V1_SEA_CS', 'bufr')
        if 'V2_CS' in exp_name: dir_tropicsbufr = os.path.join(dir_data, 'TROPICS_V2_SEA_CS', 'bufr')

    dir_da = os.path.join(dir_cycling_da, 'da')
    dir_bkg = os.path.join(dir_cycling_da, 'bkg')
    dir_gsi = os.path.join(dir_cycling_da, 'gsi')
    dir_option = os.path.join(dir_cycling_da, 'option')
    os.makedirs(dir_cycling_da, exist_ok=True)
    os.makedirs(dir_da, exist_ok=True)
    os.makedirs(dir_bkg, exist_ok=True)
    os.makedirs(dir_gsi, exist_ok=True)
    os.makedirs(dir_option, exist_ok=True)

    option_filelist = ['anavinfo_arw_netcdf_glbe', 'cloudy_radiance_info.txt', 'comgsi_namelist.sh', 'comgsi_satbias_in', 'comgsi_satbias_pc_in', \
                       'global_convinfo.txt', 'global_satinfo.txt', 'gsi.x', 'namelist.conv', 'namelist.rad', 'prepobs_errtable.global', \
                       'read_diag_conv.x', 'read_diag_rad_anl.x', 'read_diag_rad_ges_jacobian.x', 'read_diag_rad_ges.x', 'run_gsi.sh', 'run_GSI.sh']
    print(f"Copy files to dir_option")
    for option_file in option_filelist:
        os.system(f"cp {dir_namelists}/{option_file} {dir_option}/{option_file}")

    initial_time = datetime(*itime)
    initial_time_YYYYMMDDHH = initial_time.strftime('%Y%m%d%H')
    time_last = initial_time
    time_last_YYYYMMDDHH = time_last.strftime('%Y%m%d%H')
    time_last_YYYYMMDD = time_last.strftime('%Y%m%d')
    time_last_HH = time_last.strftime('%H')

    for idc in tqdm(range(1, total_da_cycles+1), desc='DA Cycle', unit="files", bar_format="{desc}: {n}/{total} DA Cycles | {elapsed}<{remaining}"):

        time_now = initial_time + timedelta(hours=idc*cycling_interval)
        time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')
        time_now_YYYYMMDD = time_now.strftime('%Y%m%d')
        time_now_HH = time_now.strftime('%H')
        print(f"Run GSI at {time_now_YYYYMMDDHH}")

        for dom in da_domains:

            print(f"Check wrfinput file for {dom}")
            wrf_inout = os.path.join(dir_da, f"wrf_inout.{time_now_YYYYMMDDHH}.{dom}")
            if not os.path.exists(wrf_inout):

                print(f"Copy satbias_out to satbias_out")
                satbias_out = os.path.join(dir_da, '.'.join(['satbias_out', time_last_YYYYMMDDHH, dom]))
                os.system(f"cp {satbias_out} {dir_option}/comgsi_satbias_in")

                print(f"Copy satbias_pc.out to satbias_pc.out")
                satbias_pc_out = os.path.join(dir_da, '.'.join(['satbias_pc', 'out', time_last_YYYYMMDDHH, dom]))
                os.system(f"cp {satbias_pc_out} {dir_option}/comgsi_satbias_pc_in")

                print(time_now_YYYYMMDDHH)
                run_gsi_dir = os.path.join(dir_gsi, time_now_YYYYMMDDHH)
                os.makedirs(run_gsi_dir, exist_ok=True)

                print(f"Create bkg folder, and copy wrfout to bkg")
                bkg_dir = os.path.join(run_gsi_dir, 'bkg')
                wrfout  = os.path.join(dir_bkg, '_'.join(['wrfout', dom, time_now.strftime('%Y-%m-%d_%H:00:00')]))
                os.makedirs(bkg_dir, exist_ok=True)
                os.system(f"cp {wrfout} {bkg_dir}")

                print(f"Create obs folder, and copy bufr to obs")
                obs_dir = os.path.join(run_gsi_dir, 'obs')
                os.makedirs(obs_dir, exist_ok=True)
                if 'CTRL' not in exp_name and 'NPB' not in exp_name: os.system(f"cp {dir_prepbufr}/{time_now_YYYYMMDD}/prepbufr.gdas.{time_now_YYYYMMDD}.t{time_now_HH}z.nr.48h {obs_dir}/gdas.t{time_now_HH}z.prepbufr")
                if 'ASRBC4CLD' in exp_name: os.system(f"cp {dir_goesbufr}/{time_now_YYYYMMDD}/gdas.t{time_now_HH}z.goesrabi.tm00.bufr_d {obs_dir}/gdas.t{time_now_HH}z.goesrabi.tm00.bufr_d ")
                if 'DAWN' in exp_name: os.system(f"cp {dir_dawnbufr}/{time_now_YYYYMMDD}/gdas.t{time_now_HH}z.dawn.tm00.bufr_d {obs_dir}/gdas.t{time_now_HH}z.dawn.tm00.bufr_d ")
                if 'HALO' in exp_name: os.system(f"cp {dir_halobufr}/{time_now_YYYYMMDD}/gdas.t{time_now_HH}z.halo.tm00.bufr_d {obs_dir}/gdas.t{time_now_HH}z.halo.tm00.bufr_d ")
                if 'CYG' in exp_name: os.system(f"cp {dir_cygnssbufr}/{time_now_YYYYMMDD}/gdas.t{time_now_HH}z.cygnss.tm00.bufr_d {obs_dir}/gdas.t{time_now_HH}z.cygnss.tm00.bufr_d ")
                if 'V1_AS' in exp_name or 'V2_AS' in exp_name or 'V1_CS' in exp_name or 'V2_CS' in exp_name:
                    os.system(f"cp {dir_tropicsbufr}/{time_now_YYYYMMDD}/gdas.t{time_now_HH}z.tropics.tm00.bufr_d {obs_dir}/gdas.t{time_now_HH}z.tropics.tm00.bufr_d ")

                print(f"Create ens folder, and copy wrfout to ens")
                ens_dir = os.path.join(run_gsi_dir, 'ens')
                os.makedirs(ens_dir, exist_ok=True)
                if boundary_data_ensemble == 'GEFS':
                    for idens in range(1, int(ensemble_members+1)):
                        ens_in  = f"{dir_gefs_wrf_ensemble}/{time_now_YYYYMMDD}/{time_now_HH}/wrfout_{dom}_{str(idens).zfill(3)}"
                        if os.path.exists(ens_in):
                            ens_out = f"{ens_dir}/wrf_en{str(idens).zfill(3)}"
                            os.system(f"ln -sf {ens_in} {ens_out}")
                elif boundary_data_ensemble == 'GFS':
                    for idens in range(1, int(ensemble_members+1)):
                        ens_in = f"{dir_gfs_ensemble}/{time_last_YYYYMMDD}/{time_last_HH}/mem{str(idens).zfill(3)}/gdas.t{time_last_HH}z.atmf006.nc"
                        # print(ens_in)
                        if os.path.exists(ens_in):
                            ens_out = f"{ens_dir}/gdas.t{time_last_HH}z.atmf006s.mem{str(idens).zfill(3)}"
                            os.system(f"ln -sf {ens_in} {ens_out}")
                        ens_in = f"{dir_gfs_ensemble}/{time_last_YYYYMMDD}/{time_last_HH}/gdas.t{time_last_HH}z.atmf006s.mem{str(idens).zfill(3)}"
                        # print(ens_in)
                        if os.path.exists(ens_in):
                            ens_out = f"{ens_dir}/gdas.t{time_last_HH}z.atmf006s.mem{str(idens).zfill(3)}"
                            os.system(f"ln -sf {ens_in} {ens_out}")

                print(f"Copy, revise, and the script of running gsi at {time_now_YYYYMMDDHH}")
                run_gsi_input = fo.change_content(os.path.join(dir_option, 'run_GSI.sh'))
                run_gsi_input.substitude_string('DATA_DIR', '=', dir_gsi)
                run_gsi_input.substitude_string('OPTION_ROOT', '=', dir_option)
                run_gsi_input.substitude_string('ANAL_TIME', '=', time_now_YYYYMMDDHH)
                run_gsi_input.substitude_string('DOMAIN_NAME', '=', dom)
                run_gsi_input.substitude_string('GSIPROC', '=', str(gsi_ntasks))
                run_gsi_input.save_content()

                print(f"Run gsi for domain {dom} at {time_now_YYYYMMDDHH}")
                submit_job(dir_script=dir_option,
                           script_name='run_GSI.sh',
                           whether_wait=True,
                           nodes=gsi_nodes,
                           ntasks=gsi_ntasks,
                           account=gsi_account,
                           partition=gsi_partition,
                           nodelist=gsi_nodelist)

                info = os.popen(f"grep 'ENDING DATE-TIME' {run_gsi_dir}/case_{dom}/stdout").readlines()
                if len(info) == 1:

                    print(f"Finish running gsi at {time_now_YYYYMMDDHH} for {dom}")
                    copy_files_after_gsi(dir_option=dir_option,
                                         run_gsi_dir=run_gsi_dir,
                                         dir_da=dir_da,
                                         time_now_string=time_now_YYYYMMDDHH,
                                         domains=[dom])
                    print(f"Delete slurm...")
                    os.system(f"rm -rf {dir_option}/slurm*")

                else:

                    print(f"GSI failed at {time_now_YYYYMMDDHH} exit!")
                    print(f"Delete slurm...")
                    os.system(f"rm -rf {dir_option}/slurm*")
                    os._exit(0)

        time_last = time_now
        time_now = time_now + timedelta(hours = cycling_interval)
        time_last_YYYYMMDDHH = time_last.strftime('%Y%m%d%H')
        time_last_YYYYMMDD = time_last.strftime('%Y%m%d')
        time_last_HH = time_last.strftime('%H')
        time_now_YYYYMMDDHH  = time_now.strftime('%Y%m%d%H')

        #Run WRF
        print(f"Check wrfout at {dir_scratch_case}/{initial_time_YYYYMMDDHH} and dir_bkg")
        wrfout_exist = check_file_existence(time_start=time_last,
                                            time_end=time_now,
                                            directories=[dir_bkg, os.path.join(dir_scratch_case, initial_time_YYYYMMDDHH)],
                                            file_format='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                                            domains=da_domains,
                                            history_interval=cycling_interval)

        if not wrfout_exist and idc < total_da_cycles:

            namelist_input_dir = os.path.join(dir_scratch_case, 'Run_WRF', 'namelist.input')
            namelist_input = fo.change_content(namelist_input_dir)
            max_dom = len(da_domains)

            #Time_Control
            start_YYYY_str = max_dom * f"{time_last.strftime('%Y')}, "
            start_MM_str   = max_dom * f"{time_last.strftime('%m')}, "
            start_DD_str   = max_dom * f"{time_last.strftime('%d')}, "
            start_HH_str   = max_dom * f"{time_last.strftime('%H')}, "
            end_YYYY_str   = max_dom * f"{time_now.strftime('%Y')}, "
            end_MM_str     = max_dom * f"{time_now.strftime('%m')}, "
            end_DD_str     = max_dom * f"{time_now.strftime('%d')}, "
            end_HH_str     = max_dom * f"{time_now.strftime('%H')}, "

            namelist_input.substitude_string('max_dom', ' = ', str(max_dom))
            namelist_input.substitude_string('run_days',  ' = ', str(cycling_interval//24) + ',')
            namelist_input.substitude_string('run_hours', ' = ', str(cycling_interval%24) + ',')
            namelist_input.substitude_string('start_year', ' = ', start_YYYY_str)
            namelist_input.substitude_string('start_month', ' = ', start_MM_str)
            namelist_input.substitude_string('start_day', ' = ', start_DD_str)
            namelist_input.substitude_string('start_hour', ' = ', start_HH_str)
            namelist_input.substitude_string('end_year', ' = ', end_YYYY_str)
            namelist_input.substitude_string('end_month', ' = ', end_MM_str)
            namelist_input.substitude_string('end_day', ' = ', end_DD_str)
            namelist_input.substitude_string('end_hour', ' = ', end_HH_str)
            namelist_input.substitude_string('history_interval', ' = ', max_dom * f"{str(cycling_interval*60)}, ")
            namelist_input.save_content()

            print('Copy wrfinput to Run_WRF')
            copy_files(time_start=time_last,
                       time_end=time_last,
                       dir_src=dir_da,
                       file_format_src='wrf_inout.{ctime:%Y%m%d%H}.{dom}',
                       dir_dst=os.path.join(dir_scratch_case, 'Run_WRF'),
                       file_format_dst='wrfinput_{dom}',
                       domains=da_domains,
                       history_interval=cycling_interval)

            #run wrf to get the forecast
            print(f"Run wrf from {time_last} to {time_now}")
            submit_job(dir_script=os.path.join(dir_scratch_case, 'Run_WRF'),
                       script_name='run_wrf.sh',
                       whether_wait=True,
                       nodes=wrf_nodes,
                       ntasks=wrf_ntasks,
                       account=wrf_account,
                       partition=wrf_partition,
                       nodelist=wrf_nodelist)

            print(f"Finish running wrf from {time_last} to {time_now}")

        #move the forecast files to the bkg folder
        print(f"move the forecast files to the bkg folder at {time_now}")
        move_files(time_start=time_last,
                   time_end=time_now,
                   dir_src=os.path.join(dir_scratch_case, initial_time_YYYYMMDDHH),
                   file_format_src='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                   dir_dst=dir_bkg,
                   file_format_dst='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                   domains=da_domains,
                   history_interval=cycling_interval)

        print('remove wrfout files')
        for dom in da_domains:
            wrfout_at_dir_case = f"{dir_scratch_case}/{initial_time_YYYYMMDDHH}/wrfout_{dom}_{time_last.strftime('%Y-%m-%d_%H:%M:00')}"
            if os.path.exists(wrfout_at_dir_case): os.system(f"rm -rf {wrfout_at_dir_case}")

def prepare_wrf_forecast(data_library_name, dir_case, case_name, exp_name):

    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')
    itime = attributes[(dir_case, case_name)]['itime']
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    da_domains = attributes[(dir_case, case_name)]['da_domains']
    cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    initial_time = datetime(*itime)
    anl_start_time = initial_time + timedelta(hours=cycling_interval)
    anl_end_time = anl_start_time + timedelta(hours=(total_da_cycles-1)*cycling_interval)
    dir_cycling_da = os.path.join(dir_exp, 'cycling_da', f"{case_name}_{exp_name}_C{str(total_da_cycles).zfill(2)}")
    dir_da_in = os.path.join(dir_cycling_da, 'da')
    dir_bkg_in = os.path.join(dir_cycling_da, 'bkg')

    for idc in tqdm(range(1, total_da_cycles), desc='DA Cycle', unit="files", bar_format="{desc}: {n}/{total} DA Cycles | {elapsed}<{remaining}"):

        anl_end_time = anl_start_time + timedelta(hours=(idc-1)*cycling_interval)
        dir_cycling_da = os.path.join(dir_exp, 'cycling_da', f"{case_name}_{exp_name}_C{str(idc).zfill(2)}")
        dir_da_out = os.path.join(dir_cycling_da, 'da')
        dir_bkg_out = os.path.join(dir_cycling_da, 'bkg')
        os.makedirs(dir_cycling_da, exist_ok=True)
        os.makedirs(dir_da_out, exist_ok=True)
        os.makedirs(dir_bkg_out, exist_ok=True)

        copy_files(time_start=anl_start_time,
                   time_end=anl_end_time,
                   dir_src=dir_da_in,
                   file_format_src='wrf_inout.{ctime:%Y%m%d%H}.{dom}',
                   dir_dst=dir_da_out,
                   file_format_dst='wrf_inout.{ctime:%Y%m%d%H}.{dom}',
                   domains=da_domains,
                   history_interval=cycling_interval)

        copy_files(time_start=initial_time,
                   time_end=anl_end_time,
                   dir_src=dir_bkg_in,
                   file_format_src='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                   dir_dst=dir_bkg_out,
                   file_format_dst='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                   domains=da_domains,
                   history_interval=cycling_interval)

def run_wrf_forecast(data_library_name, dir_case, case_name, exp_name, da_cycle, whether_wait, nodes, ntasks, account, partition, nodelist=''):

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
    wps_interval = attributes[(dir_case, case_name)]['wps_interval']
    boundary_data_deterministic = attributes[(dir_case, case_name)]['boundary_data_deterministic']

    case = '_'.join([case_name, exp_name, f"C{str(da_cycle).zfill(2)}", 'Forecast'])
    initial_time = datetime(*itime)
    initial_time_str = initial_time.strftime('%Y%m%d%H')
    anl_start_time = initial_time + timedelta(hours=cycling_interval)
    anl_end_time = anl_start_time + timedelta(hours=cycling_interval*(da_cycle-1))
    time_start = anl_end_time
    if boundary_data_deterministic == 'GFS': time_end = time_start + timedelta(hours=forecast_hours+6)

    dir_da = os.path.join(dir_exp, 'cycling_da', f"{case_name}_{exp_name}_C{str(da_cycle).zfill(2)}", 'da')
    dir_bkg = os.path.join(dir_exp, 'cycling_da', f"{case_name}_{exp_name}_C{str(da_cycle).zfill(2)}", 'bkg')
    dir_scratch_case = os.path.join(dir_scratch, case)

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
                                         directories=[dir_bkg, os.path.join(dir_scratch_case, initial_time_str)],
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
                   dir_dst=os.path.join(dir_scratch_case, 'Run_WRF'),
                   file_format_dst='wrfinput_{dom}',
                   domains=da_domains,
                   history_interval=cycling_interval)

        # Run wrf to get the forecast
        print(f'Cycle {da_cycle}: Run wrf from {time_start} to {time_end}')
        submit_job(dir_script=os.path.join(dir_scratch_case, 'Run_WRF'),
                   script_name='run_wrf.sh',
                   whether_wait=whether_wait,
                   nodes=nodes,
                   ntasks=ntasks,
                   account=account,
                   partition=partition,
                   nodelist=nodelist)

        if whether_wait:
            # Check the existence of wrfout while finishing
            print('Check wrfout files after running forecast')
            result_wrfout = check_file_existence(time_start=time_start,
                                                 time_end=time_end,
                                                 directories=[dir_bkg, os.path.join(dir_scratch_case, initial_time_str)],
                                                 file_format='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                                                 domains=forecast_domains,
                                                 history_interval=history_interval)
            if not result_wrfout: print('Fail to run wrf forecast')

    if result_wrfout:
        print(f'Move wrf forecasts from {time_start} to {time_end}')
        move_files(time_start=time_start,
                   time_end=time_end,
                   dir_src=os.path.join(dir_scratch_case, initial_time_str),
                   file_format_src='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                   dir_dst=dir_bkg,
                   file_format_dst='wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}',
                   domains=forecast_domains,
                   history_interval=history_interval)
