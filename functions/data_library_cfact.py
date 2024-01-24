import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/CFACT/01_IOP8', 'IOP8')] = {
    'dir_exp': '/glade/work/royfeng/CFACT/01_IOP8',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/glade/u/home/royfeng/CFACT/01_IOP8/namelists',
    'itime': (2022, 2, 18, 12, 0, 0),
    'forecast_hours': 24,
    'dir_scratch': '/glade/derecho/scratch/royfeng',
    'total_da_cycles': 13,
    'time_window_max': 0.5,
    'da_domains': ['d01', 'd02', 'd03', 'd04'],
    'forecast_domains': ['d01', 'd02', 'd03', 'd04'],
    'wps_interval': 6,
    'cycling_interval': 1,
    'history_interval': 1,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'SELF',
    'ensemble_members': 60,
}