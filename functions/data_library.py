import seaborn as sns

attributes = {}
compare_track_intensity_schemes = {}
sns_bright_cmap = sns.color_palette('bright')

attributes[('/05_TROPICS/05_cycling_da', 'Ida')] = {
    'itime': (2021, 8, 26,  0, 0, 0),
    'forecast_hours': 78,
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/05_cycling_da',
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 3,
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
}
attributes[('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida')] = {
    'itime': (2021, 8, 26,  0, 0, 0),
    'forecast_hours': 78,
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3',
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 3,
    'da_domains': ['d01', 'd02'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'cycling_interval': 6,
    'history_interval': 1,
    'hwrf_header': 'hwrf.18x18.AL092021.2021082606',
    'dir_track_intensity': '/uufs/chpc.utah.edu/common/home/u1237353/TROPICS/10_cycling_da_tropics_v3/track_intensity/best_track',
    'NHC_best_track': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/2021_09L_Ida.csv',
    'ibtracs': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/ibtracs.ALL.list.v04r00.csv',
    'ibtracs_case': 'IDA',
    'ibtracs_season': 2021,
}
attributes[('/02_GOES_Bias_Correction/27_ChCor', 'Laura')] = {
    'itime': (2020, 8, 24,  0, 0, 0),
    'forecast_hours': 54,
    'dir_exp': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/27_ChCor',
    'dir_scratch': '/scratch/general/nfs1/u1237353',
    'total_da_cycles': 12,
    'da_domains': ['d01'],
    'forecast_domains': ['d01', 'd02'],
    'GFDL_domains': ['d01'],
    'cycling_interval': 6,
    'history_interval': 6,
    'hwrf_header': 'hwrf.18x18.AL132020.2020082406',
    'dir_track_intensity': '/uufs/chpc.utah.edu/common/home/u1237353/GOES-R-observation-error-covariance/track_intensity/best_track',
    'NHC_best_track': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/2021_09L_Ida.csv',
    'ibtracs': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/02_GOES_Bias_Correction/Data/best_track/ibtracs.ALL.list.v04r00.csv',
    'ibtracs_case': 'LAURA',
    'ibtracs_season': 2020,
}
compare_track_intensity_schemes['TROPICS_Ida_scheme_01'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_Q_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_Q_T_ENS')],
    'total_da_cycles': 3,
    'extents': [(-95.0, -70.0, 10.0, 35.0), (-95.0, -70.0, 12.5, 35.0), (-95.0, -70.0, 12.5, 35.0)],
    'GFDL_domains': ['d01'],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['V1_CONTROL', 'V1_TROPICS_Q_ENS', 'V1_TROPICS_T_ENS', 'V1_TROPICS_Q_T_ENS', 'V3_TROPICS_Q_ENS', 'V3_TROPICS_T_ENS', 'V3_TROPICS_Q_T_ENS'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[3]],
    'linestyles': ['-', '-', '-', '-', '--', '--', '--'],
}
compare_track_intensity_schemes['TROPICS_Ida_scheme_02'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CONTROL'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'TROPICS_T_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'TROPICS_T_CLR_ENS')],
    'total_da_cycles': 3,
    'extents': [(-95.0, -70.0, 10.0, 35.0), (-95.0, -70.0, 12.5, 35.0), (-95.0, -70.0, 12.5, 35.0)],
    'GFDL_domains': ['d01'],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['V1_CONTROL', 'V1_TROPICS_T_ENS', 'V1_TROPICS_T_CLR_ENS', 'V3_TROPICS_T_ENS', 'V3_TROPICS_T_CLR_ENS'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[1], sns_bright_cmap[2]],
    'linestyles': ['-', '--', '--', '-', '-'],
}
compare_track_intensity_schemes['TROPICS_Ida_scheme_03'] = {
    'cases': [('/05_TROPICS/05_cycling_da', 'Ida', 'CON_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_T_ENS'), \
              ('/05_TROPICS/05_cycling_da', 'Ida', 'CON_TROPICS_T_CLR_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_T_ENS'), \
              ('/05_TROPICS/10_cycling_da_tropics_v3', 'Ida', 'CON_TROPICS_T_CLR_ENS')],
    'total_da_cycles': 3,
    'GFDL_domains': ['d01'],
    'dir_save': '/uufs/chpc.utah.edu/common/home/zpu-group16/cfeng/05_TROPICS/10_cycling_da_tropics_v3/track_intensity/Ida/Figures',
    'labels': ['V1_CON_ENS', 'V1_CON_TROPICS_T_ENS', 'V1_CON_TROPICS_T_CLR_ENS', 'V3_CON_TROPICS_T_ENS', 'V3_CON_TROPICS_T_CLR_ENS'],
    'colors': [sns_bright_cmap[0], sns_bright_cmap[1], sns_bright_cmap[2], sns_bright_cmap[1], sns_bright_cmap[2]],
    'linestyles': ['-', '--', '--', '-', '-'],
}
