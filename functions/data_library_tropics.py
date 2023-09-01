import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/05_TROPICS/05_cycling_da', 'Ida')] = {
    'itime': (2021, 8, 26,  0, 0, 0),
    'forecast_hours': 78,
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/05_cycling_da',
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 3,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'cycling_interval': 6,
    'history_interval': 6,
    'hwrf_header': 'hwrf.18x18.AL092021.2021082606',
    'dir_track_intensity': '/uufs/chpc.utah.edu/common/home/u1237353/TROPICS/05_cycling_da/track_intensity/best_track',
    'NHC_best_track': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/2021_09L_Ida.csv',
    'ibtracs': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/ibtracs.ALL.list.v04r00.csv',
    'ibtracs_case': 'IDA',
    'ibtracs_season': 2021,
    'product': 'TROPICS V1',
    'dir_tropics': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/Data/TROPICS',
    'dir_cygnss': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/CYGNSS',
    'dir_IMERG': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/IMERG',
    'dir_ScientificColourMaps7': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7',
}

attributes[('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida')] = {
    'itime': (2021, 8, 26,  0, 0, 0),
    'forecast_hours': 78,
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3',
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 3,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'cycling_interval': 6,
    'history_interval': 6,
    'hwrf_header': 'hwrf.18x18.AL092021.2021082606',
    'dir_track_intensity': '/uufs/chpc.utah.edu/common/home/u1237353/TROPICS/10_cycling_da_tropics_v3/track_intensity/best_track',
    'NHC_best_track': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/2021_09L_Ida.csv',
    'ibtracs': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/ibtracs.ALL.list.v04r00.csv',
    'ibtracs_case': 'IDA',
    'ibtracs_season': 2021,
    'product': 'TROPICS V3',
    'dir_tropics': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/Data/TROPICS_V3',
    'dir_cygnss': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/CYGNSS',
    'dir_IMERG': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/IMERG',
    'dir_ScientificColourMaps7': '/uufs/chpc.utah.edu/common/home/u1237353/climetlab-my-plugin/colormaps/ScientificColourMaps7',
}

compare_schemes['TROPICS_Ida_scheme_01'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['V1_CONTROL', 'V1_TROPICS_Q_ENS', 'V1_TROPICS_T_ENS', 'V1_TROPICS_Q_T_ENS', 'V3_TROPICS_Q_ENS', 'V3_TROPICS_T_ENS', 'V3_TROPICS_Q_T_ENS'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-', '--', '--', '--'],
}
compare_schemes['TROPICS_Ida_scheme_02'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['V1_CONTROL', 'V1_TROPICS_T_ENS', 'V1_TROPICS_T_CLR_ENS', 'V3_TROPICS_T_ENS', 'V3_TROPICS_T_CLR_ENS'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[1], sns_bright_cmap[2]],
    'linestyles': ['-', '--', '--', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_03'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_T_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_T_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['V1_CON_ENS', 'V1_CON_TROPICS_T_ENS', 'V1_CON_TROPICS_T_CLR_ENS', 'V3_CON_TROPICS_T_ENS', 'V3_CON_TROPICS_T_CLR_ENS'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[1], sns_bright_cmap[2]],
    'linestyles': ['-', '--', '--', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_04'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CONTROL', 'V1_Q_CLR', 'V1_T_CLR', 'V1_Q_T_CLR', 'V3_Q_CLR', 'V3_T_CLR', 'V3_Q_T_CLR'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], \
                                   sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3]],
    'linestyles': ['-', '--', '--', '--', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_05'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CYG_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CONTROL', 'CYG', 'V1_Q_T_CLR', 'CYG_V1_Q_T_CLR', 'V3_Q_T_CLR', 'CYG_V3_Q_T_CLR'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[3],  sns_bright_cmap[4], \
                                                       sns_bright_cmap[3],  sns_bright_cmap[4]],
    'linestyles': ['-', '-', '--', '--', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_06'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CON', 'CON_V1_Q_CLR', 'CON_V1_T_CLR', 'CON_V1_Q_T_CLR', 'CON_V3_Q_CLR', 'CON_V3_T_CLR', 'CON_V3_Q_T_CLR'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], \
                                   sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3]],
    'linestyles': ['-', '--', '--', '--', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_07'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_CYG_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CON', 'CON_CYG', 'CON_V3_Q_T_CLR', 'CON_CYG_V3_Q_T_CLR', 'CON_V3_Q_T_CLR', 'CON_CYG_V3_Q_T_CLR'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[3],  sns_bright_cmap[4], \
                                                       sns_bright_cmap[3],  sns_bright_cmap[4]],
    'linestyles': ['-', '-', '--', '--', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_08'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_TROPICS_Q_T_V1_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/05_cycling_da/track_intensity/Ida/Figures',
    'labels': ['CONTROL', 'CYG', 'V1_Q', 'V1_T', 'V1_Q_T', 'CYG_V1_Q_T', 'V1_Q_CLR', 'V1_T_CLR', 'V1_Q_T_CLR', 'CYG_V1_Q_T_CLR'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], \
                                                       sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4]],
    'linestyles': ['-', '-', '-', '-', '-', '-', '--', '--', '--', '--'],
}
compare_schemes['TROPICS_Ida_scheme_09'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_TROPICS_Q_T_V1_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/05_cycling_da/track_intensity/Ida/Figures',
    'labels': ['CON', 'CON_CYG', 'CON_V1_Q', 'CON_V1_T', 'CON_V1_Q_T', 'CON_CYG_V1_Q_T', 'CON_V1_Q_CLR', 'CON_V1_T_CLR', 'CON_V1_Q_T_CLR', 'CON_CYG_V1_Q_T_CLR'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], \
                                                       sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4]],
    'linestyles': ['-', '-', '-', '-', '-', '-', '--', '--', '--', '--'],
}
compare_schemes['TROPICS_Ida_scheme_10'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CYG_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CYG_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CONTROL', 'CYG', 'V3_Q', 'V3_T', 'V3_Q_T', 'CYG_V3_Q_T', 'V3_Q_CLR', 'V3_T_CLR', 'V3_Q_T_CLR', 'CYG_V3_Q_T_CLR'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], \
                                                       sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4]],
    'linestyles': ['-', '-', '-', '-', '-', '-', '--', '--', '--', '--'],
}
compare_schemes['TROPICS_Ida_scheme_11'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_CYG_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_CYG_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CON', 'CON_CYG', 'CON_V3_Q', 'CON_V3_T', 'CON_V3_Q_T', 'CON_CYG_V3_Q_T', 'CON_V3_Q_CLR', 'CON_V3_T_CLR', 'CON_V3_Q_T_CLR', 'CON_CYG_V3_Q_T_CLR'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4], \
                                                       sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4]],
    'linestyles': ['-', '-', '-', '-', '-', '-', '--', '--', '--', '--'],
}
compare_schemes['TROPICS_Ida_scheme_12'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CONTROL', 'V1_Q', 'V1_T', 'V1_Q_T', 'V3_Q', 'V3_T', 'V3_Q_T'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], \
                                   sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3]],
    'linestyles': ['-', '--', '--', '--', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_13'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CYG_TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CONTROL', 'CYG', 'V1_Q_T', 'CYG_V1_Q_T', 'V3_Q_T', 'CYG_V3_Q_T'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[3],  sns_bright_cmap[4], \
                                                       sns_bright_cmap[3],  sns_bright_cmap[4]],
    'linestyles': ['-', '-', '--', '--', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_14'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CONTROL', 'CON_V1_Q', 'CON_V1_T', 'CON_V1_Q_T', 'CON_V3_Q', 'CON_V3_T', 'CON_V3_Q_T'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], \
                                   sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3]],
    'linestyles': ['-', '--', '--', '--', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_15'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_CYG_TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CON', 'CON_CYG', 'CON_V3_Q_T', 'CON_CYG_V3_Q_T', 'CON_V3_Q_T', 'CON_CYG_V3_Q_T'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[3],  sns_bright_cmap[4], \
                                                       sns_bright_cmap[3],  sns_bright_cmap[4]],
    'linestyles': ['-', '-', '--', '--', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_16'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CYG_TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CTRL', 'CYG', 'V1', 'CYG_V1', 'V3', 'CYG_V3'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[3],  sns_bright_cmap[4], sns_bright_cmap[1],  sns_bright_cmap[2]],
    'linestyles': ['-', '-', '-', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_17'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_CYG_TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CON', 'CYG', 'V1', 'CYG_V1', 'V3', 'CYG_V3'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[3],  sns_bright_cmap[4], sns_bright_cmap[1],  sns_bright_cmap[2]],
    'linestyles': ['-', '-', '-', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_18'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CYG_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CTRL', 'CYG', 'V1', 'CYG_V1', 'V3', 'CYG_V3'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[3],  sns_bright_cmap[4], sns_bright_cmap[1],  sns_bright_cmap[2]],
    'linestyles': ['-', '-', '-', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_19'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_TROPICS_Q_T_V1_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_CYG_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CON', 'CYG', 'V1', 'CYG_V1', 'V3', 'CYG_V3'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[5], sns_bright_cmap[3],  sns_bright_cmap[4], sns_bright_cmap[1],  sns_bright_cmap[2]],
    'linestyles': ['-', '-', '-', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_20'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CYG_TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CTRL', 'CYG', 'V3', 'CYG_V3'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2],  sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_21'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_CYG_TROPICS_Q_T_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CON', 'CYG', 'V3', 'CYG_V3'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2],  sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_22'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CYG_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CYG_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CTRL', 'CYG', 'V3', 'CYG_V3'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2],  sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-'],
}
compare_schemes['TROPICS_Ida_scheme_23'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_CYG_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_Q_T_V3_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_CYG_TROPICS_Q_T_V3_CLR_ENS')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['CON', 'CYG', 'V3', 'CYG_V3'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2],  sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-'],
}
