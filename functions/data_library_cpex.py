import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/CPEX/01_CV_RF07_AEW06_IAN', 'Ian')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/01_CV_RF07_AEW06_IAN',
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

attributes[('/CPEX/02_AW_RF01_AEW01', 'AEW01')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/02_AW_RF01_AEW01',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/02_AW_RF01_AEW01/namelists',
    'AEW_best_track': '2021_AEW01.csv',
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
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

attributes[('/CPEX/03_AW_RF02_AEW02', 'AEW02')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/03_AW_RF02_AEW02',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/03_AW_RF02_AEW02/namelists',
    'AEW_best_track': '2021_AEW02.csv',
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
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

attributes[('/CPEX/04_AW_RF07_Larry', 'Larry')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/04_AW_RF07_Larry',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/04_AW_RF07_Larry/namelists',
    'NHC_best_track': '2021_12L_Larry.csv',
    'hwrf_header': 'hwrf.18x18.AL122021.2021090406',
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
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

attributes[('/CPEX/05_CV_RF07_AEW06', 'AEW06')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/05_CV_RF07_AEW06',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/05_CV_RF07_AEW06/namelists',
    'AEW_best_track': '2022_AEW06.csv',
    'IMERG_version': {'run': 'HHR-L', 'version': 'V06C'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '05A',
    'itime': (2022, 9, 16,  0, 0, 0),
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

attributes[('/CPEX/06_CV_RF01_AEW03', 'AEW03')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/06_CV_RF01_AEW03',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/06_CV_RF01_AEW03/namelists',
    'AEW_best_track': '2022_AEW03.csv',
    'IMERG_version': {'run': 'HHR-L', 'version': 'V06C'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '05A',
    'itime': (2022, 9,  6,  0, 0, 0),
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

attributes[('/CPEX/07_CV_RF02_AEW03', 'AEW03')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/07_CV_RF02_AEW03',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/07_CV_RF02_AEW03/namelists',
    'AEW_best_track': '2022_AEW03.csv',
    'IMERG_version': {'run': 'HHR-L', 'version': 'V06C'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '05A',
    'itime': (2022, 9,  7,  0, 0, 0),
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

attributes[('/CPEX/08_CV_RF03_AEW04', 'AEW04')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/08_CV_RF03_AEW04',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/08_CV_RF03_AEW04/namelists',
    'AEW_best_track': '2022_AEW04.csv',
    'IMERG_version': {'run': 'HHR-L', 'version': 'V06C'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '05A',
    'itime': (2022, 9,  9,  0, 0, 0),
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

attributes[('/CPEX/09_CV_RF04_AEW04', 'AEW04')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/09_CV_RF04_AEW04',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/CPEX/09_CV_RF04_AEW04/namelists',
    'AEW_best_track': '2022_AEW04.csv',
    'IMERG_version': {'run': 'HHR-L', 'version': 'V06C'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '05A',
    'itime': (2022, 9, 10,  0, 0, 0),
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
    'cases': [('/CPEX/01_CV_RF07_AEW06_IAN', 'Ian', 'CTRL'), \
              ('/CPEX/01_CV_RF07_AEW06_IAN', 'Ian', 'CONV'), \
              ('/CPEX/01_CV_RF07_AEW06_IAN', 'Ian', 'DAWN'), \
              ('/CPEX/01_CV_RF07_AEW06_IAN', 'Ian', 'HALO')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/CPEX/01_CV_RF07_AEW06_IAN/track_intensity/figures',
    'labels': ['CTRL', 'CONV', 'DAWN', 'HALO'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2],  sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-'],
}
