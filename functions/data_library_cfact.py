import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/CFACT/01_IO8', 'IO8')] = {
    'dir_exp': '/glade/work/royfeng/CFACT/01_CV_RF07_AEW06_IAN',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/01_CV_RF07_AEW06_IAN/namelists',
    'NHC_best_track': '2022_09L_Ian.csv',
    'AEW_best_track': '2022_AEW06.csv',
    'hwrf_header': 'hwrf.18x18.AL092022.2022092218',
    'ibtracs': {'filename': 'ibtracs.ALL.list.v04r00.csv', 'season': 2022, 'name': 'IAN'},
    'IMERG_version': {'run': 'HHR-L', 'version': 'V06C'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '05A',
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