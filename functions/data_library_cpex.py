import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/08_CPEX/01_CV_RF07_AEW06_IAN', 'Ian')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN',
    'dir_ScientificColourMaps7': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/01_CV_RF07_AEW06_IAN/cycling_da/namelists',
    'NHC_best_track': '2022_09L_Ian.csv',
    'hwrf_header': 'hwrf.18x18.AL092022.2022092218',
    'ibtracs': {'filename': 'ibtracs.ALL.list.v04r00.csv', 'season': 2022, 'name': 'IAN'},
    'itime': (2022, 9, 16,  0, 0, 0),
    'forecast_hours': 240,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 4,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GEFS',
    'ensemble_members': 60,
}

attributes[('/08_CPEX/02_AW_RF01_AEW01', 'AEW01')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/02_AW_RF01_AEW01',
    'dir_ScientificColourMaps7': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/02_AW_RF01_AEW01/cycling_da/namelists',
    'itime': (2021, 8, 20,  0, 0, 0),
    'forecast_hours': 24,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 4,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GEFS',
    'ensemble_members': 60,
}

attributes[('/08_CPEX/03_AW_RF02_AEW02', 'AEW02')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/03_AW_RF02_AEW02',
    'dir_ScientificColourMaps7': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/03_AW_RF02_AEW02/cycling_da/namelists',
    'itime': (2021, 8, 21,  0, 0, 0),
    'forecast_hours': 24,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 4,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GEFS',
    'ensemble_members': 60,
}

attributes[('/08_CPEX/04_AW_RF07_Larry', 'Larry')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/04_AW_RF07_Larry',
    'dir_ScientificColourMaps7': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/04_AW_RF07_Larry/cycling_da/namelists',
    'itime': (2021, 9,  4,  0, 0, 0),
    'forecast_hours': 48,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 4,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GEFS',
    'ensemble_members': 60,
}

compare_schemes['Ian_scheme_01'] = {
    'cases': [('/08_CPEX/01_CV_RF07_AEW06_IAN', 'Ian', 'CTRL'), \
              ('/08_CPEX/01_CV_RF07_AEW06_IAN', 'Ian', 'CONV'), \
              ('/08_CPEX/01_CV_RF07_AEW06_IAN', 'Ian', 'DAWN'), \
              ('/08_CPEX/01_CV_RF07_AEW06_IAN', 'Ian', 'HALO')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN/track_intensity/figures',
    'labels': ['CTRL', 'CONV', 'DAWN', 'HALO'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2],  sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-'],
}
