import os
import importlib
import requests
import pygrib
import subprocess
import metpy.calc
import numpy as np
import matplotlib.pyplot as plt
import colormaps as cmaps
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from wrf import getvar, latlon_coords, interplevel, g_geoht, CoordPair, vertcross
from netCDF4 import Dataset, num2date
from scipy.interpolate import griddata
from metpy.units import units
from combine_and_show_images import combine_images_grid
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import Image as IPImage
from IPython.display import display

def extract_cross_section(data_library_names, dir_cases, case_names, exp_names,
                          da_cycle=4, domain='d01', var_time=20000101010000, 
                          lat_start=0, lon_start=-70, lat_end=0, lon_end=-50,
                          ref_exp_name='CTRL', variables=['u']):

    start_point = CoordPair(lat=lat_start, lon=lon_start)
    end_point = CoordPair(lat=lat_end, lon=lon_end)
    level_1d = np.arange(1000, 4, -5)+1.0
    n_level = len(level_1d)
    n_latlon = int(20*np.sqrt((lat_end-lat_start)*(lat_end-lat_start)+(lon_end-lon_start)*(lon_end-lon_start))+1)
    lat_1d = np.linspace(lat_start, lat_end, n_latlon)
    lon_1d = np.linspace(lon_start, lon_end, n_latlon)
    lon_360_1d = np.linspace(lon_start, lon_end, n_latlon)
    lon_360_1d[lon_360_1d<0] = lon_360_1d[lon_360_1d<0] + 360.0
    latlon_idx_1d = np.arange(0, n_latlon, 1)
    lat_2d, level_2d = np.meshgrid(lat_1d, level_1d, sparse=False, indexing='xy')
    lon_2d, level_2d = np.meshgrid(lon_1d, level_1d, sparse=False, indexing='xy')
    latlon_idx_2d, level_2d = np.meshgrid(latlon_idx_1d, level_1d, sparse=False, indexing='xy')

    time_now = datetime.strptime(str(var_time), '%Y%m%d%H%M%S')

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        module = importlib.import_module(f"set_parameters_{data_library_name}")
        set_variables = getattr(module, 'set_variables')

        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        dir_cycling_da = os.path.join(dir_exp, 'cycling_da')
        dir_cross_section = os.path.join(dir_exp, 'cross_section')
        dir_data = os.path.join(dir_exp, 'data')
        dir_ERA5 = os.path.join(dir_data, 'ERA5')
        dir_GFS = os.path.join(dir_data, 'GFS')
        os.makedirs(dir_cross_section, exist_ok=True)

        specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
        dir_cross_section_case = os.path.join(dir_cross_section, specific_case)
        os.makedirs(dir_cross_section_case, exist_ok=True)

        if 'IMERG'  in exp_name or \
           'CMORPH' in exp_name or \
           'GSMaP'  in exp_name or \
           'GFS'    in exp_name or \
           'ERA5'   in exp_name:
            dir_wrfout = os.path.join(dir_cycling_da, f"{case_name}_{ref_exp_name}_C{str(da_cycle).zfill(2)}", 'bkg')
        else:
            dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'bkg')

        for var in tqdm(variables, desc='Variables', position=0, leave=True):

            (information, levels) = set_variables(var)

            output_filename = (
                f"{str(var_time)}_{var}_"
                f"{str(int(lat_start*10))}_{str(int(lon_start*10))}_"
                f"{str(int(lat_end*10))}_{str(int(lon_end*10))}_"
                f"{domain}_C{str(da_cycle).zfill(2)}.nc"
            )
            filename = os.path.join(dir_cross_section_case, output_filename)
            os.system(f"rm -rf {filename}")

            ncfile_output = Dataset(filename, 'w', format='NETCDF4')
            ncfile_output.createDimension('n_level', n_level)
            ncfile_output.createDimension('n_latlon', n_latlon)
            ncfile_output.createVariable('level', 'f8', ('n_level', 'n_latlon'))
            ncfile_output.createVariable('lat',   'f8', ('n_level', 'n_latlon'))
            ncfile_output.createVariable('lon',   'f8', ('n_level', 'n_latlon'))
            ncfile_output.createVariable(var,     'f8', ('n_level', 'n_latlon'))
            ncfile_output.variables['level'][:,:] = level_2d
            ncfile_output.variables['lat'][:,:] = lat_2d
            ncfile_output.variables['lon'][:,:] = lon_2d
            ncfile_output.variables[var][:,:] = 0.0

            if 'inc' in var:

                var_bkg = var.replace('_inc', '')
                var_anl = var.replace('_inc', '_anl')
                filename_bkg = filename.replace('_inc', '')
                filename_anl = filename.replace('_inc', '_anl')

                ncfile_bkg = Dataset(filename_bkg)
                ncfile_anl = Dataset(filename_anl)
                ncfile_output.variables[var][:,:] = ncfile_anl.variables[var_anl][:,:] - ncfile_bkg.variables[var_bkg][:,:]
                ncfile_bkg.close()
                ncfile_anl.close()
                        
            else:

                if 'GFS' in exp_name:

                    if 'anl' in var:
                                    
                        var_bkg = var.replace('_anl', '')
                        filename_bkg = filename.replace('_anl', '')

                        ncfile_bkg = Dataset(filename_bkg)
                        ncfile_output.variables[var][:,:] = ncfile_bkg.variables[var_bkg][:,:]
                        ncfile_bkg.close()
                                
                    else:

                        YYYY = time_now.strftime('%Y')
                        YYMMDDHH = time_now.strftime('%Y%m%d%H')
                        YYYYMMDD = time_now.strftime('%Y%m%d')
                                
                        dir_rda = 'https://data.rda.ucar.edu/ds084.1'
                        GFS_filename = f"gfs.0p25.{YYMMDDHH}.f000.grib2"
                        GFS_file = os.path.join(dir_GFS, GFS_filename)

                        if not os.path.exists(GFS_file):

                            GFS_rda_filename = os.path.join(dir_rda, YYYY, YYYYMMDD, GFS_filename)
                            response = requests.get(GFS_rda_filename, stream=True)
                            with open(GFS_file, "wb") as f:
                                f.write(response.content)

                        GFS_pygrib = pygrib.open(GFS_file)
                        # for grb in GFS_pygrib:
                        #     print(grb)
                        
                        GFS_temp_select = GFS_pygrib.select(name=information['GFS'], typeOfLevel='isobaricInhPa')[:]
                        GFS_temp, GFS_lat, GFS_lon = GFS_temp_select[0].data(lat1=np.min(lat_1d)-15.0, \
                                                                             lat2=np.max(lat_1d)+15.0, \
                                                                             lon1=np.min(lon_360_1d)-15.0, \
                                                                             lon2=np.max(lon_360_1d)+15.0)
                        
                        n_GFS_level = len(GFS_temp_select)
                        n_GFS_lat = GFS_lat.shape[0]
                        n_GFS_lon = GFS_lon.shape[1]
                        GFS_p = np.zeros((n_GFS_level, n_GFS_lat, n_GFS_lon))
                        GFS_temp = np.zeros((n_GFS_level, n_GFS_lat, n_GFS_lon))

                        for idl in range(n_GFS_level):
                            GFS_temp_data = GFS_temp_select[idl]
                            GFS_p[idl,:,:] = GFS_temp_data.level
                            GFS_temp[idl,:,:], GFS_lat, GFS_lon = GFS_temp_data.data(lat1=np.min(lat_1d)-15.0, \
                                                                                     lat2=np.max(lat_1d)+15.0, \
                                                                                     lon1=np.min(lon_360_1d)-15.0, \
                                                                                     lon2=np.max(lon_360_1d)+15.0)
                        
                        GFS_temp_level = interplevel(GFS_temp, GFS_p, level_1d)
                        GFS_lon[GFS_lon>180.0] = GFS_lon[GFS_lon>180.0] - 360.0
                        GFS_lat_1d = np.array(GFS_lat).ravel()
                        GFS_lon_1d = np.array(GFS_lon).ravel()
                        
                        for idl, lev in enumerate(level_1d):
                            GFS_temp_1d = np.array(GFS_temp_level[idl,:,:]).ravel()
                            if var == 'q': GFS_temp_1d = GFS_temp_1d/(1.0-GFS_temp_1d)
                            if var == 'avo': GFS_temp_1d = GFS_temp_1d*100000.0
                            ncfile_output.variables[var][idl,:] = griddata((GFS_lon_1d, GFS_lat_1d), GFS_temp_1d, (lon_1d, lat_1d), method='linear')

                        GFS_pygrib.close()

                elif 'ERA5' in exp_name:
                    
                    if 'anl' in var:
                                    
                        var_bkg = var.replace('_anl', '')
                        filename_bkg = filename.replace('_anl', '')

                        ncfile_bkg = Dataset(filename_bkg)
                        ncfile_output.variables[var][:,:] = ncfile_bkg.variables[var_bkg][:,:]
                        ncfile_bkg.close()
                                
                    else:

                        ERA5_filename = os.path.join(dir_ERA5, 'ERA5_pressure_levels.nc')
                        ERA5_ncfile = Dataset(ERA5_filename)
                                        
                        ERA5_hour = ERA5_ncfile.variables['time']
                        ERA5_level = ERA5_ncfile.variables['level'][:]
                        ERA5_time = num2date(ERA5_hour, ERA5_hour.units, ERA5_hour.calendar)
                        ERA5_idt = np.where(ERA5_time == time_now)[0][0]
                        ERA5_lat = ERA5_ncfile.variables['latitude'][:]
                        ERA5_lon = ERA5_ncfile.variables['longitude'][:]
                        ERA5_lat_sidx = np.where(ERA5_lat < np.max(lat_1d) + 15.0)[0][0]
                        ERA5_lon_sidx = np.where(ERA5_lon > np.min(lon_360_1d) - 15.0)[0][0]
                        ERA5_lat_eidx = np.where(ERA5_lat > np.min(lat_1d) - 15.0)[0][-1]
                        ERA5_lon_eidx = np.where(ERA5_lon < np.max(lon_360_1d) + 15.0)[0][-1]
                        ERA5_lon[ERA5_lon>180.0] = ERA5_lon[ERA5_lon>180.0] - 360.0                        
                        ERA5_lat = ERA5_lat[ERA5_lat_sidx:ERA5_lat_eidx]
                        ERA5_lon = ERA5_lon[ERA5_lon_sidx:ERA5_lon_eidx]
                        n_ERA5_level = len(ERA5_level)
                        n_ERA5_lat = len(ERA5_lat)
                        n_ERA5_lon = len(ERA5_lon)

                        ERA5_temp = ERA5_ncfile.variables[information['ERA5']][ERA5_idt,:,ERA5_lat_sidx:ERA5_lat_eidx,ERA5_lon_sidx:ERA5_lon_eidx]
                        ERA5_lat = np.transpose(np.tile(ERA5_lat, (n_ERA5_lon, 1)))
                        ERA5_lon = np.tile(ERA5_lon, (n_ERA5_lat, 1))
                        ERA5_p = np.zeros((n_ERA5_level, n_ERA5_lat, n_ERA5_lon))
                        for idl, lev in enumerate(ERA5_level):
                            ERA5_p[idl,:,:] = lev

                        ERA5_temp_level = interplevel(ERA5_temp, ERA5_p, level_1d)
                        ERA5_lat_1d = np.array(ERA5_lat).ravel()
                        ERA5_lon_1d = np.array(ERA5_lon).ravel()

                        for idl, lev in enumerate(level_1d):
                            ERA5_temp_1d = np.array(ERA5_temp_level[idl,:,:]).ravel()
                            if var == 'q': ERA5_temp_1d = ERA5_temp_1d/(1.0-ERA5_temp_1d)
                            if var == 'avo':
                                ERA5_coriolis_parameter = metpy.calc.coriolis_parameter(np.deg2rad(ERA5_lat_1d))
                                ERA5_temp_1d = ERA5_temp_1d+ERA5_coriolis_parameter
                                ERA5_temp_1d = ERA5_temp_1d*100000.0
                            if var == 'geopt':
                                ERA5_temp_1d = ERA5_temp_1d/9.80665
                            ncfile_output.variables[var][idl,:] = griddata((ERA5_lon_1d, ERA5_lat_1d), ERA5_temp_1d, (lon_1d, lat_1d), method='linear')

                        ERA5_ncfile.close()

                else:
                    wrfout = os.path.join(dir_wrfout, f"wrfout_{domain}_{time_now.strftime('%Y-%m-%d_%H:%M:00')}")
                    if 'anl' in var:
                        dir_wrfout = os.path.join(dir_cycling_da, specific_case, 'da')
                        wrfout = os.path.join(dir_wrfout, f"wrf_inout.{time_now.strftime('%Y%m%d%H')}.{domain}")

                    if os.path.exists(wrfout):

                        ncfile = Dataset(wrfout)
                        p = getvar(ncfile, 'pressure')
                        if 'index' in information.keys():
                            if information['unit'] == 'null':
                                var_value = getvar(ncfile, information['name'])[information['index']]
                            else:
                                var_value = getvar(ncfile, information['name'], units=information['unit'])[information['index']]
                        else:
                            if information['unit'] == 'null':
                                var_value = getvar(ncfile, information['name'])
                                if var == 'geopt': var_value = g_geoht.get_height(ncfile, msl=True)
                            else:
                                var_value = getvar(ncfile, information['name'], units=information['unit'])
                        
                        temp_cs_2d = vertcross(var_value, p, wrfin=ncfile, levels=level_1d, \
                                               start_point=start_point, end_point=end_point, \
                                               latlon=True, meta=True)
                        ncfile.close()

                        coord_pairs = np.array(temp_cs_2d.coords['xy_loc'])
                        n_latlon_cs = len(coord_pairs)
                        latlon_idx_cs_1d = np.arange(0, n_latlon_cs, 1)*(n_latlon-1.0)/(n_latlon_cs-1.0)
                        latlon_idx_cs_2d, level_cs_2d = np.meshgrid(latlon_idx_cs_1d, level_1d, sparse=False, indexing='xy')
                        latlon_idx_cs_2d_1d = np.reshape(latlon_idx_cs_2d, -1)
                        level_cs_2d_1d = np.reshape(level_cs_2d, -1)
                        temp_cs_2d_1d = np.reshape(temp_cs_2d.data, -1)
                        ncfile_output.variables[var][:,:] = griddata((latlon_idx_cs_2d_1d, level_cs_2d_1d), temp_cs_2d_1d, \
                                                              (latlon_idx_2d, level_2d), method='linear')

                ncfile_output.close()

def draw_cross_section(data_library_names, dir_cases, case_names, exp_names,
                       contourf_var, contourf_var_levels, contourf_var_cmap,
                       contour_var='null', contour_var_ref_exp_name='ERA5',
                       contour_positive_clabel=False, contour_positive_levels=[0.75], contour_positive_color='w',
                       contour_negative_clabel=False, contour_negative_levels=[-0.75], contour_negative_color='w',
                       quiver_vars=['null', 'null'], quiver_var_ref_exp_name='ERA5', quiver_var_color='w',
                       quiver_var_x_space=10, quiver_var_y_space=10, quiver_var_scale=25,
                       lat_start=0, lon_start=-70, lat_end=0, lon_end=-50,
                       domain='d01', da_cycle=4, var_time=20000101010000, x_display_mode='lat'):
    
    quiver_var_1 = quiver_vars[0]
    quiver_var_2 = quiver_vars[1]
    if x_display_mode == 'lon': extent = [lon_start, lon_end, 100, 1000]
    if x_display_mode == 'lat': extent = [lat_start, lat_end, 100, 1000]

    # Import the necessary library
    (data_library_name, dir_case, case_name, exp_name) = (data_library_names[0], dir_cases[0], case_names[0], exp_names[0])
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')
    module = importlib.import_module(f"set_parameters_{data_library_name}")
    set_variables = getattr(module, 'set_variables')

    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_colormaps = attributes[(dir_case, case_name)]['dir_colormaps']
    dir_cross_section = os.path.join(dir_exp, 'cross_section')
    dir_ScientificColourMaps7 = os.path.join(dir_colormaps, 'ScientificColourMaps7')
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))    
 
    image_files = []
    dir_save = os.path.join(dir_cross_section, 'figures')
    output_filename = (
        f"{str(var_time)}_{contourf_var}_{contour_var}_"
        f"{quiver_var_1}_{quiver_var_2}_"
        f"{str(int(lat_start*10))}_{str(int(lon_start*10))}_"
        f"{str(int(lat_end*10))}_{str(int(lon_end*10))}_"
        f"{domain}_C{str(da_cycle).zfill(2)}"
    )
    output_file = os.path.join(dir_save, output_filename+'.png')

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])
        specific_case = '_'.join([case_name, exp_name, 'C'+str(da_cycle).zfill(2)])
        dir_cross_section_case = os.path.join(dir_cross_section, specific_case)

        filename = (
            f"{str(var_time)}_{contourf_var}_{contour_var}_"
            f"{quiver_var_1}_{quiver_var_2}_"
            f"{str(int(lat_start*10))}_{str(int(lon_start*10))}_"
            f"{str(int(lat_end*10))}_{str(int(lon_end*10))}_"
            f"{domain}_C{str(da_cycle).zfill(2)}"
        )    
        pdfname = os.path.join(dir_cross_section_case, filename+'.pdf')
        pngname = os.path.join(dir_cross_section_case, filename+'.png')
        image_files.append(pngname)

        contourf_filename = (
                f"{str(var_time)}_{contourf_var}_"
                f"{str(int(lat_start*10))}_{str(int(lon_start*10))}_"
                f"{str(int(lat_end*10))}_{str(int(lon_end*10))}_"
                f"{domain}_C{str(da_cycle).zfill(2)}.nc"
            )
        contourf_var_filename = os.path.join(dir_cross_section_case, contourf_filename)
        contourf_var_ncfile = Dataset(contourf_var_filename)
        contourf_level = contourf_var_ncfile.variables['level'][:,:]
        contourf_lat = contourf_var_ncfile.variables['lat'][:,:]
        contourf_lon = contourf_var_ncfile.variables['lon'][:,:]
        contourf_var_value = contourf_var_ncfile.variables[contourf_var][:,:]
        contourf_var_ncfile.close()

        if 'null' not in contour_var:
            dir_cross_section_case = os.path.join(dir_cross_section, specific_case)
            contour_filename = (
                f"{str(var_time)}_{contour_var}_"
                f"{str(int(lat_start*10))}_{str(int(lon_start*10))}_"
                f"{str(int(lat_end*10))}_{str(int(lon_end*10))}_"
                f"{domain}_C{str(da_cycle).zfill(2)}.nc"
            )
            contour_var_filename = os.path.join(dir_cross_section_case, contour_filename)
            contour_var_ncfile = Dataset(contour_var_filename)
            contour_level = contour_var_ncfile.variables['level'][:,:]
            contour_lat = contour_var_ncfile.variables['lat'][:,:]
            contour_lon = contour_var_ncfile.variables['lon'][:,:]
            contour_var_value = contour_var_ncfile.variables[contour_var][:,:]
            contour_var_ncfile.close()
            
        if 'null' not in quiver_vars:
            dir_cross_section_case = os.path.join(dir_cross_section, specific_case)
            quiver_var_1_filename = (
                f"{str(var_time)}_{quiver_var_1}_"
                f"{str(int(lat_start*10))}_{str(int(lon_start*10))}_"
                f"{str(int(lat_end*10))}_{str(int(lon_end*10))}_"
                f"{domain}_C{str(da_cycle).zfill(2)}.nc"
            )            
            quiver_var_1_filename = os.path.join(dir_cross_section_case, quiver_var_1_filename)
            quiver_var_1_ncfile = Dataset(quiver_var_1_filename)
            quiver_var_1_level = quiver_var_1_ncfile.variables['level'][:,:]
            quiver_var_1_lat = quiver_var_1_ncfile.variables['lat'][:,:]
            quiver_var_1_lon = quiver_var_1_ncfile.variables['lon'][:,:]
            quiver_var_1_value = quiver_var_1_ncfile.variables[quiver_var_1][:,:]
            quiver_var_1_ncfile.close()
            quiver_var_2_filename = (
                f"{str(var_time)}_{quiver_var_2}_"
                f"{str(int(lat_start*10))}_{str(int(lon_start*10))}_"
                f"{str(int(lat_end*10))}_{str(int(lon_end*10))}_"
                f"{domain}_C{str(da_cycle).zfill(2)}.nc"
            )            
            quiver_var_2_filename = os.path.join(dir_cross_section_case, quiver_var_2_filename)
            quiver_var_2_ncfile = Dataset(quiver_var_2_filename)
            quiver_var_2_level = quiver_var_2_ncfile.variables['level'][:,:]
            quiver_var_2_lat = quiver_var_2_ncfile.variables['lat'][:,:]
            quiver_var_2_lon = quiver_var_2_ncfile.variables['lon'][:,:]
            quiver_var_2_value = quiver_var_2_ncfile.variables[quiver_var_2][:,:]
            quiver_var_2_ncfile.close()

        fig_width = 2.75*1.5
        fig_height = 2.75+0.75
        clb_aspect = 25*1.5

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
            ax = axs

            (contourf_information, contourf_levels) = set_variables(contourf_var)

            if x_display_mode == 'lon':
                pcm = ax.contourf(contourf_lon, contourf_level, contourf_information['factor']*contourf_var_value, \
                      levels=contourf_var_levels, cmap=contourf_var_cmap, extend=contourf_information['extend'], zorder=1)
            elif x_display_mode == 'lat':
                pcm = ax.contourf(contourf_lat, contourf_level, contourf_information['factor']*contourf_var_value, \
                      levels=contourf_var_levels, cmap=contourf_var_cmap, extend=contourf_information['extend'], zorder=1)
            # print(np.nanmax(contourf_var_value))
            # print(np.nanmin(contourf_var_value))
                
            if 'null' not in contour_var:
                (contour_information, contour_levels) = set_variables(contour_var)
                if contour_positive_clabel == True:
                    if x_display_mode == 'lon':
                        CS1 = ax.contour(contour_lon, contour_level, contour_information['factor']*contour_var_value, \
                                         levels=contour_positive_levels, linestyles='solid',  colors=contour_positive_color, linewidths=1.0, zorder=1)
                    elif x_display_mode == 'lat':
                        CS1 = ax.contour(contour_lat, contour_level, contour_information['factor']*contour_var_value, \
                                         levels=contour_positive_levels, linestyles='solid',  colors=contour_positive_color, linewidths=1.0, zorder=1)
                    ax.clabel(CS1, inline=True, fontsize=5.0)
                if contour_negative_clabel == True:
                    if x_display_mode == 'lon':
                        CS2 = ax.contour(contour_lon, contour_level, contour_information['factor']*contour_var_value, \
                                         levels=contour_negative_levels, linestyles='dashed',  colors=contour_negative_color, linewidths=1.0, zorder=1)
                    elif x_display_mode == 'lat':
                        CS2 = ax.contour(contour_lat, contour_level, contour_information['factor']*contour_var_value, \
                                         levels=contour_negative_levels, linestyles='dashed',  colors=contour_negative_color, linewidths=1.0, zorder=1)
                    ax.clabel(CS2, inline=True, fontsize=5.0)
                # print(np.nanmax(contour_var_value))
                # print(np.nanmin(contour_var_value))

            if 'null' not in quiver_vars:
                (quiver_1_information, quiver_1_levels) = set_variables(quiver_var_1)
                (quiver_2_information, quiver_2_levels) = set_variables(quiver_var_2)
                if x_display_mode == 'lon':
                    ax.quiver(quiver_var_1_lon[::quiver_var_y_space, ::quiver_var_x_space], \
                              quiver_var_1_level[::quiver_var_y_space, ::quiver_var_x_space], \
                              quiver_1_information['factor']*quiver_var_1_value[::quiver_var_y_space, ::quiver_var_x_space], \
                              quiver_2_information['factor']*quiver_var_2_value[::quiver_var_y_space, ::quiver_var_x_space], \
                              width=0.0025, headwidth=5.0, headlength=7.5, \
                              color=quiver_var_color, scale=quiver_var_scale, scale_units='inches', zorder=1)
                elif x_display_mode == 'lat':
                    ax.quiver(quiver_var_1_lat[::quiver_var_y_space, ::quiver_var_x_space], \
                              quiver_var_1_level[::quiver_var_y_space, ::quiver_var_x_space], \
                              quiver_1_information['factor']*quiver_var_1_value[::quiver_var_y_space, ::quiver_var_x_space], \
                              quiver_2_information['factor']*quiver_var_2_value[::quiver_var_y_space, ::quiver_var_x_space], \
                              width=0.0025, headwidth=5.0, headlength=7.5, \
                              color=quiver_var_color, scale=quiver_var_scale, scale_units='inches', zorder=1)

            if x_display_mode == 'lon':
                ax.set_xticks(np.arange(-180, 181, 5))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 5)])
            elif x_display_mode == 'lat':
                ax.set_xticks(np.arange(-90, 91, 5))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90), int(90)+1, 5)])
            
            ax.set_yticks(np.arange(200, 1001, 200))
            ax.set_ylabel('Pressure (hPa)', fontsize=10.0)
            ax.text(extent[0], extent[2], exp_name, ha='left', va='top', color='k', fontsize=10.0, bbox=dict(boxstyle='round', ec=grayC_cm_data[53], fc=grayC_cm_data[0]), zorder=7)
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.axis(extent)
            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
            clb.set_label(f"{contourf_information['lb_title']}", fontsize=10.0, labelpad=4.0)
            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
            clb.ax.minorticks_off()
            clb.set_ticks(list(map(float, contourf_var_levels[0::2])))
            clb.set_ticklabels(contourf_var_levels[0::2])

            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig(pngname, dpi=600)
            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()

            command = f"convert {pngname} -trim {pngname}"
            subprocess.run(command, shell=True)

    combine_images_grid(image_files, output_file)
    command = f"convert {output_file} -trim {output_file}"
    subprocess.run(command, shell=True)
    image = IPImage(filename=output_file)
    display(image)
