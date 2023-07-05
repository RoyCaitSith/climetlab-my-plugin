from weather_map_forecast import draw_sfc_wind_individual

data_library_names = ['cpex']
dir_cases = ['/08_CPEX/01_CV_RF07_AEW06_IAN']
case_names = ['Ian']
exp_names = ['DAWN']

draw_sfc_wind_individual(data_library_names=data_library_names,
                         dir_cases=dir_cases,
                         case_names=case_names,
                         exp_names=exp_names)