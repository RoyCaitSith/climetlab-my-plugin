import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/GOES-R-observation-error-covariance/01_Laura', 'Laura')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/01_Laura',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/GOES-R-observation-error-covariance/01_Laura/namelists',
    'NHC_best_track': '2020_13L_Laura.csv',
    'hwrf_header': 'hwrf.18x18.AL132020.2020082406',
    'ibtracs': {'filename': 'ibtracs.ALL.list.v04r00.csv', 'season': 2020, 'name': 'LAURA'},
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
    'itime': (2020, 8, 24,  0, 0, 0),
    'forecast_hours': 48,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 12,
    'time_window_max': 1.5,
    'da_domains': ['d01'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GFS',
    'ensemble_members': 80,
}

attributes[('/GOES-R-observation-error-covariance/02_Ida', 'Ida')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/02_Ida',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/GOES-R-observation-error-covariance/02_Ida/namelists',
    'NHC_best_track': '2021_09L_Ida.csv',
    'hwrf_header': 'hwrf.18x18.AL092021.2021082606',
    'ibtracs': {'filename': 'ibtracs.ALL.list.v04r00.csv', 'season': 2021, 'name': 'IDA'},
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
    'itime': (2021, 8, 26,  0, 0, 0),
    'forecast_hours': 48,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 12,
    'time_window_max': 1.5,
    'da_domains': ['d01'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GFS',
    'ensemble_members': 80,
}

compare_schemes['GOES_Laura_scheme_01'] = {
    'cases': [('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/01_Laura/track_intensity/figures',
    'labels': ['NPB'],
    'colors': [sns_bright_cmap[0]],
    'linestyles': ['-'],
}
compare_schemes['GOES_Laura_scheme_02'] = {
    'cases': [('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_08'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_09'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_10'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_08'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_09'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/01_Laura/track_intensity/figures',
    'labels': ['NPB', 'NPB_ASRBC4CLD_08', 'NPB_ASRBC4CLD_09', 'NPB_ASRBC4CLD_10', 'NPB_ASRBC4CLD_CLD_08', 'NPB_ASRBC4CLD_CLD_09', 'NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], sns_bright_cmap[5], sns_bright_cmap[6], sns_bright_cmap[7]],
    'linestyles': ['-', '-', '-', '-', '-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_03'] = {
    'cases': [('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'ASRBC4CLD_CLD_08'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'ASRBC4CLD_CLD_09'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'ASRBC4CLD_CLD_10'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/01_Laura/track_intensity/figures',
    'labels': ['ASRBC4CLD_CLD_08', 'ASRBC4CLD_CLD_09', 'ASRBC4CLD_CLD_10', 'ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_04'] = {
    'cases': [('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_08'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_09'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_10'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_08'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_09'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/01_Laura/track_intensity/figures',
    'labels': ['NPB_ASRBC4CLD_08', 'NPB_ASRBC4CLD_09', 'NPB_ASRBC4CLD_10', 'NPB_ASRBC4CLD_CLD_08', 'NPB_ASRBC4CLD_CLD_09', 'NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], sns_bright_cmap[5], sns_bright_cmap[6], sns_bright_cmap[7]],
    'linestyles': ['-', '-', '-', '-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_05'] = {
    'cases': [('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_10_V1'), \
              ('/GOES-R-observation-error-covariance/01_Laura', 'Laura', 'NPB_ASRBC4CLD_CLD_10_V2')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/01_Laura/track_intensity/figures',
    'labels': ['NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_10_V1', 'NPB_ASRBC4CLD_CLD_10_V2'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2]],
    'linestyles': ['-', '-', '-'],
}
compare_schemes['GOES_Ida_scheme_01'] = {
    'cases': [('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'CTRL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/02_Ida/track_intensity/figures',
    'labels': ['CTRL'],
    'colors': [sns_bright_cmap[0]],
    'linestyles': ['-'],
}
compare_schemes['GOES_Ida_scheme_02'] = {
    'cases': [('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_08'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_09'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_10'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_CLD_08'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_CLD_09'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/02_Ida/track_intensity/figures',
    'labels': ['NPB', 'NPB_ASRBC4CLD_08', 'NPB_ASRBC4CLD_09', 'NPB_ASRBC4CLD_10', 'NPB_ASRBC4CLD_CLD_08', 'NPB_ASRBC4CLD_CLD_09', 'NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], sns_bright_cmap[5], sns_bright_cmap[6], sns_bright_cmap[7]],
    'linestyles': ['-', '-', '-', '-', '-', '-', '-', '-'],
}
compare_schemes['GOES_Ida_scheme_04'] = {
    'cases': [('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_08'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_09'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_10'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_CLD_08'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_CLD_09'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/GOES-R-observation-error-covariance/02_Ida', 'Ida', 'NPB_ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/GOES-R-observation-error-covariance/02_Ida/track_intensity/figures',
    'labels': ['NPB_ASRBC4CLD_08', 'NPB_ASRBC4CLD_09', 'NPB_ASRBC4CLD_10', 'NPB_ASRBC4CLD_CLD_08', 'NPB_ASRBC4CLD_CLD_09', 'NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], sns_bright_cmap[5], sns_bright_cmap[6], sns_bright_cmap[7]],
    'linestyles': ['-', '-', '-', '-', '-', '-', '-'],
}
