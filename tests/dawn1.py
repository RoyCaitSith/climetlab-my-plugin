from dawn import wrf_extract_DAWN

n_exp_name = 1
wrf_extract_DAWN(data_library_names=['cpex']*n_exp_name,
                 dir_cases=['/08_CPEX/01_CV_RF07_AEW06_IAN']*n_exp_name,
                 case_names=['Ian']*n_exp_name,
                 exp_names=['HALO_OE15'])
