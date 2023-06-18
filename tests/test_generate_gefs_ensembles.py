from generate_gefs_ensembles import download_gefs_ensemble
from generate_gefs_ensembles import gefs_run_wps_and_real

#download_gefs_ensemble('cpex', '/08_CPEX/01_CV_RF07_AEW06_IAN', 'Ian')

gefs_run_wps_and_real(data_library_name='cpex',
                      dir_case='/08_CPEX/01_CV_RF07_AEW06_IAN',
                      case_name='Ian',
                      exp_name='CON',
                      member=2,
                      boundary_data='GEFS',
                      whether_wait=False, nodes=1, ntasks=16, account='zpu-kp', partition='zpu-kp')
