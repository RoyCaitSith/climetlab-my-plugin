import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/02_GOES_Bias_Correction/27_ChCor', 'Laura')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/GOES-R-observation-error-covariance/01_Laura/cycling_da/namelists',
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

compare_schemes['GOES_Laura_scheme_01'] = {
    'cases': [('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'PB'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_09'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_10'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor/track_intensity/figures',
    'labels': ['PB', 'ASRBC4CLD_CLD_08', 'ASRBC4CLD_CLD_09', 'ASRBC4CLD_CLD_10', 'ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4]],
    'linestyles': ['-', '-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_02'] = {
    'cases': [('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_09'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor/track_intensity/figures',
    'labels': ['NPB', 'NPB_ASRBC4CLD_08', 'NPB_ASRBC4CLD_CLD_08', 'NPB_ASRBC4CLD_CLD_09', 'NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], sns_bright_cmap[5]],
    'linestyles': ['-', '-', '-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_03'] = {
    'cases': [('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_09'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_10'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor/track_intensity/figures',
    'labels': ['ASRBC4CLD_CLD_08', 'ASRBC4CLD_CLD_09', 'ASRBC4CLD_CLD_10', 'ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_04'] = {
    'cases': [('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_09'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_ALL')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor/track_intensity/figures',
    'labels': ['NPB_ASRBC4CLD_08', 'NPB_ASRBC4CLD_CLD_08', 'NPB_ASRBC4CLD_CLD_09', 'NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_ALL'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4]],
    'linestyles': ['-', '-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_05'] = {
    'cases': [('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10_V1'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10_V2')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor/track_intensity/figures',
    'labels': ['NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_10_V1', 'NPB_ASRBC4CLD_CLD_10_V2'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2]],
    'linestyles': ['-', '-', '-'],
}
