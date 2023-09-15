from halo import wrf_extract_HALO

n_exp_name = 4
wrf_extract_HALO(data_library_names=['cpex']*n_exp_name,
                 dir_cases=['/08_CPEX/01_CV_RF07_AEW06_IAN']*n_exp_name,
                 case_names=['Ian']*n_exp_name,
                 exp_names=['HALO_OE10', 'HALO_OE15', 'HALO_OE25', 'HALO_OE30'])
