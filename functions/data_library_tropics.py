import seaborn as sns

attributes = {}
compare_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/TROPICS/12_Sam_Cycling_DA', 'Sam')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/TROPICS/12_Sam_Cycling_DA',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/TROPICS/12_Sam_Cycling_DA/namelists',
    'NHC_best_track': '2021_18L_Sam.csv',
    'hwrf_header': 'hwrf.18x18.AL182021.2021092318',
    'ibtracs': {'filename': 'ibtracs.ALL.list.v04r00.csv', 'season': 2021, 'name': 'SAM'},
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
    'itime': (2021, 9, 23, 12, 0, 0),
    'forecast_hours': 72,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 8,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    # 'boundary_data_ensemble': 'GFS',
    # 'ensemble_members': 80,
    'boundary_data_ensemble': 'GEFS',
    'ensemble_members': 60,
}

attributes[('/05_TROPICS/05_cycling_da', 'Ida')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/05_cycling_da',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/TROPICS/05_cycling_da/namelists',
    'NHC_best_track': '2021_09L_Ida.csv',
    'hwrf_header': 'hwrf.18x18.AL092021.2021082606',
    'ibtracs': {'filename': 'ibtracs.ALL.list.v04r00.csv', 'season': 2021, 'name': 'IDA'},
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
    'itime': (2021, 8, 26,  0, 0, 0),
    'forecast_hours': 78,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 3,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GFS',
    'ensemble_members': 80,
}

attributes[('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/TROPICS/05_cycling_da/namelists',
    'NHC_best_track': '2021_09L_Ida.csv',
    'hwrf_header': 'hwrf.18x18.AL092021.2021082606',
    'ibtracs': {'filename': 'ibtracs.ALL.list.v04r00.csv', 'season': 2021, 'name': 'IDA'},
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
    'itime': (2021, 8, 26,  0, 0, 0),
    'forecast_hours': 78,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 3,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GFS',
    'ensemble_members': 80,
}

attributes[('/05_TROPICS/11_cycling_da_tropics', 'Ida')] = {
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/11_cycling_da_tropics',
    'dir_colormaps': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/software/colormaps/colormaps/colormaps',
    'dir_namelists': '/uufs/chpc.utah.edu/common/home/u1237353/TROPICS/11_cycling_da_tropics/namelists',
    'NHC_best_track': '2021_09L_Ida.csv',
    'hwrf_header': 'hwrf.18x18.AL092021.2021082606',
    'ibtracs': {'filename': 'ibtracs.ALL.list.v04r00.csv', 'season': 2021, 'name': 'IDA'},
    'IMERG_version': {'run': 'HHR', 'version': 'V06B'},
    'CMORPH_version': '8km-30min',
    'GSMaP_version': '04G',
    'itime': (2021, 8, 26,  0, 0, 0),
    'forecast_hours': 72,
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 6,
    'time_window_max': 3.0,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'wps_interval': 6,
    'cycling_interval': 6,
    'history_interval': 6,
    'boundary_data_deterministic': 'GFS',
    'boundary_data_ensemble': 'GFS',
    'ensemble_members': 80,
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
compare_schemes['TROPICS_Sam_scheme_01'] = {
    'cases': [('/TROPICS/12_Sam_Cycling_DA', 'Sam', 'CONV'), \
              ('/TROPICS/12_Sam_Cycling_DA', 'Sam', 'V1_AS_Q'), \
            #   ('/TROPICS/12_Sam_Cycling_DA', 'Sam', 'V1_AS_T'), \
              ('/TROPICS/12_Sam_Cycling_DA', 'Sam', 'V1_AS_QT'), \
              ('/TROPICS/12_Sam_Cycling_DA', 'Sam', 'CYG_V1_AS_QT')],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group30/cfeng/TROPICS/12_Sam_Cycling_DA/track_intensity/figures',
    'labels': ['CONV', 'V1_AS_Q', 'V1_AS_QT', 'CYG_V1_AS_QT'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[4]],
    'linestyles': ['-', '-', '-', '-', '-'],
}