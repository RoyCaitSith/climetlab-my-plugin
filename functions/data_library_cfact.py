import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

# attributes[('/CFACT/01_IOP8', 'IOP8')] = {
#     'dir_exp': '/glade/work/royfeng/CFACT/01_IOP8',
#     'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
#     'dir_namelists': '/glade/u/home/royfeng/CFACT/01_IOP8/namelists',
#     'itime': (2022, 2, 18, 12, 0, 0),
#     'forecast_hours': 24,
#     'dir_scratch': '/glade/derecho/scratch/royfeng',
#     'total_da_cycles': 13,
#     'time_window_max': 0.5,
#     'da_domains': ['d01', 'd02', 'd03', 'd04'],
#     'forecast_domains': ['d01', 'd02', 'd03', 'd04'],
#     'wps_interval': 6,
#     'cycling_interval': 1,
#     'history_interval': 1,
#     'boundary_data_deterministic': 'GFS',
#     'boundary_data_ensemble': 'SELF',
#     'ensemble_members': 60,
# }

attributes[('/CFACT/01_IOP8', 'IOP8')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CFACT/01_IOP8',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CFACT/01_IOP8/namelists',
    'itime': (2022, 2, 18, 18, 0, 0),
    'forecast_hours': 30,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 4,
    'time_window_max': 1.0,
    'da_domains': ['d01', 'd02', 'd03'],
    'forecast_domains': ['d01', 'd02', 'd03'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 0.25,
    'boundary_data_deterministic': 'NAM',
    'boundary_data_ensemble': 'NAM',
    'ensemble_members': 60,
}

attributes[('/CFACT/02_IOP8_TEST_CTRL_Sensitivity_Study', 'IOP8')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CFACT/02_IOP8_TEST_CTRL_Sensitivity_Study',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CFACT/02_IOP8_TEST_CTRL_Sensitivity_Study/namelists',
    'itime': (2022, 2, 18, 18, 0, 0),
    'forecast_hours': 24,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 0,
    'time_window_max': 1.0,
    'da_domains': ['d01', 'd02', 'd03', 'd04'],
    'forecast_domains': ['d01', 'd02', 'd03', 'd04'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 0.25,
    'boundary_data_deterministic': 'NAM_HIRES',
    'boundary_data_ensemble': 'NAM_HIRES',
    'ensemble_members': 60,
}

attributes[('/CFACT/03_IOP8', 'IOP8')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CFACT/03_IOP8',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CFACT/03_IOP8/namelists',
    'itime': (2022, 2, 17, 18, 0, 0),
    'forecast_hours': 24,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 9,
    'time_window_max': 1.0,
    'da_domains': ['d01', 'd02', 'd03', 'd04'],
    'forecast_domains': ['d01', 'd02', 'd03', 'd04'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 0.25,
    'boundary_data_deterministic': 'GDAS',
    'boundary_data_ensemble': 'GDAS',
    'ensemble_members': 60,
}