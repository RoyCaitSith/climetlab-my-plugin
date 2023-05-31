import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/08_CPEX/01_CV_RF07_AEW06_IAN', 'Ian')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN',
    'dir_data': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN/data',
    'dir_GFS': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN/data/GFS',
    'itime': (2022, 9, 16,  0, 0, 0),
    'forecast_hours': 240,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 4,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 3,
    'cycling_interval': 6,
    'history_interval': 6,
    'hwrf_header': 'hwrf.18x18.AL132020.2020082406',
    'dir_track_intensity': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN/track_intensity/best_track',
    'NHC_best_track': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN/track_intensity/best_track/2022_09L_Ian.csv',
    'ibtracs': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN/track_intensity/best_track/ibtracs.ALL.list.v04r00.csv',
    'ibtracs_case': 'IAN',
    'ibtracs_season': 2022,
    'dir_IMERG': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/08_CPEX/01_CV_RF07_AEW06_IAN/Data/IMERG',
    'dir_ScientificColourMaps7': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/01_CV_RF07_AEW06_IAN/cycling_da/namelists',
}
