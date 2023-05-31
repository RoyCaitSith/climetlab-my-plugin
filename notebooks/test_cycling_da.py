from cycling_da import run_wps_and_real

run_wps_and_real(data_library_name='cpex',
                 dir_case='/08_CPEX/01_CV_RF07_AEW06_IAN',
                 case_name='Ian',
                 exp_name='CON',
                 period='cycling_da',
                 whether_wait=False, nodes=1, ntasks=16, account='zpu-kp', partition='zpu-kp')
