import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/02_GOES_Bias_Correction/27_ChCor', 'Laura')] = {
    'itime': (2020, 8, 24,  0, 0, 0),
    'forecast_hours': 54,
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor',
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 12,
    'time_window_max': 1.5,
    'da_domains': ['d01'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'cycling_interval': 6,
    'history_interval': 6,
    'hwrf_header': 'hwrf.18x18.AL132020.2020082406',
    'NHC_best_track': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/2020_13L_Laura.csv',
    'ibtracs': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/ibtracs.ALL.list.v04r00.csv',
    'ibtracs_case': 'LAURA',
    'ibtracs_season': 2020,
    'product': 'GOES-R',
    'dir_IMERG': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/IMERG',
    'dir_ScientificColourMaps7': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7',
}
compare_schemes['GOES_Laura_scheme_01'] = {
    'cases': [('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_ALL'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'PB'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_09'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'ASRBC4CLD_CLD_10')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor/track_intensity/Laura/Figures',
    'labels': ['ASRBC4CLD_CLD_ALL', 'PB', 'ASRBC4CLD_CLD_08', 'ASRBC4CLD_CLD_09', 'ASRBC4CLD_CLD_10'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4]],
    'linestyles': ['-', '-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_02'] = {
    'cases': [('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_ALL'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_08'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_09'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor/track_intensity/Laura/Figures',
    'labels': ['NPB_ASRBC4CLD_CLD_ALL', 'NPB', 'NPB_ASRBC4CLD_08', 'NPB_ASRBC4CLD_CLD_08', 'NPB_ASRBC4CLD_CLD_09', 'NPB_ASRBC4CLD_CLD_10'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], sns_bright_cmap[5]],
    'linestyles': ['-', '-', '-', '-', '-', '-'],
}
compare_schemes['GOES_Laura_scheme_03'] = {
    'cases': [('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10_V1'), \
              ('/02_GOES_Bias_Correction/27_ChCor', 'Laura', 'NPB_ASRBC4CLD_CLD_10_V2')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor/track_intensity/Laura/Figures',
    'labels': ['NPB_ASRBC4CLD_CLD_10', 'NPB_ASRBC4CLD_CLD_10_V1', 'NPB_ASRBC4CLD_CLD_10_V2'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2]],
    'linestyles': ['-', '-', '-'],
}
