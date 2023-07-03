import os
import datetime
import importlib
import subprocess
import numpy as np
import colormaps as cmaps
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from tqdm.notebook import tqdm
from wrf import getvar, interplevel, latlon_coords
from combine_and_show_images import combine_images_grid
from mpl_toolkits.basemap import Basemap
from matplotlib.backends.backend_pdf import PdfPages
from IPython.display import Image as IPImage

def set_parameters_variables(var):

    information = {}
    levels = {}

    information.update({'ua':     {'unit': 'ms-1', 'lb_title': 'ua (m/s)', 'factor': 1.0}})
    information.update({'va':     {'unit': 'ms-1', 'lb_title': 'va (m/s)', 'factor': 1.0}})
    information.update({'temp':   {'unit': 'K', 'lb_title': 'T (K)', 'factor': 1.0}})
    information.update({'QVAPOR': {'unit': 'null', 'lb_title': "QVAPOR " + "($\mathregular{gkg^{-1}}$)", 'factor': 1000.0}})

    if 'ua' in var:
        levels.update({925: [-18.0, 20.0, 4.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({850: [-18.0, 20.0, 4.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({700: [-22.5, 25.0, 5.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({500: [-22.5, 25.0, 5.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({300: [-36.0, 40.0, 8.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({200: [-36.0, 40.0, 8.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
    if 'va' in var:
        levels.update({925: [-18.0, 20.0, 4.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({850: [-18.0, 20.0, 4.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({700: [-13.5, 15.0, 3.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({500: [-13.5, 15.0, 3.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({300: [-18.0, 20.0, 4.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({200: [-18.0, 20.0, 4.0, cmaps.vik, -3.5, 4.0, 1.0, cmaps.vik]})
    if 'temp' in var:
        levels.update({925: [285, 305, 2.0, cmaps.lajolla, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({850: [280, 300, 2.0, cmaps.lajolla, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({700: [275, 290, 1.5, cmaps.lajolla, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({500: [260, 270, 1.0, cmaps.lajolla, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({300: [230, 250, 2.0, cmaps.lajolla, -3.5, 4.0, 1.0, cmaps.vik]})
        levels.update({200: [210, 225, 1.5, cmaps.lajolla, -3.5, 4.0, 1.0, cmaps.vik]})
    if 'QVAPOR' in var:
        levels.update({925: [0.0, 20.0, 2.00, cmaps.imola, -3.5, 4.0, 1.0, cmaps.cork]})
        levels.update({850: [0.0, 15.0, 1.50, cmaps.imola, -3.5, 4.0, 1.0, cmaps.cork]})
        levels.update({700: [0.0, 10.0, 1.00, cmaps.imola, -3.5, 4.0, 1.0, cmaps.cork]})
        levels.update({500: [0.0, 5.00, 0.50, cmaps.imola, -3.5, 4.0, 1.0, cmaps.cork]})
        levels.update({300: [0.0, 1.00, 0.10, cmaps.imola, -3.5, 4.0, 1.0, cmaps.cork]})
        levels.update({200: [0.0, 0.10, 0.01, cmaps.imola, -3.5, 4.0, 1.0, cmaps.cork]})

    return (information[var], levels)

def calculate_analysis_increment(data_library_names, dir_cases, case_names, exp_names, variables = ['ua']):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        dir_exp=attributes[(dir_case, case_name)]['dir_exp']
        total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
        itime=attributes[(dir_case, case_name)]['itime']
        initial_time = datetime.datetime(*itime)
        da_domains=attributes[(dir_case, case_name)]['da_domains']
        cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']

        anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)
        dir_cycling_da = os.path.join(dir_exp, 'cycling_da')
        dir_increment = os.path.join(dir_exp, 'increment')
        specific_case = '_'.join([case_name, exp_name, 'C'+str(total_da_cycles).zfill(2)])
        dir_increment_case = os.path.join(dir_increment, specific_case)
        os.makedirs(dir_increment, exist_ok=True)
        os.makedirs(dir_increment_case, exist_ok=True)

        for dom in tqdm(da_domains, desc='DA Domains', leave=False):
            for var in tqdm(variables, desc='Variables', leave=False):

                (information, levels) = set_parameters_variables(var)
                n_level = len(levels.keys())

                filename = os.path.join(dir_increment_case, '_'.join([var, 'analysis', 'increment', dom+'.nc']))
                os.system('rm -rf ' + filename)
                # print(filename)

                for idt in range(0, total_da_cycles):

                    time_now = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
                    # print(time_now)

                    wrfout_bkg = f"{dir_cycling_da}/{specific_case}/bkg/wrfout_{dom}_{time_now.strftime('%Y-%m-%d_%H:00:00')}"
                    wrfout_anl = f"{dir_cycling_da}/{specific_case}/da/wrf_inout.{time_now.strftime('%Y%m%d%H')}.{dom}"

                    if os.path.exists(wrfout_bkg) and os.path.exists(wrfout_anl):

                        ncfile = Dataset(wrfout_bkg)
                        p_bkg  = getvar(ncfile, 'pressure')
                        if information['unit'] == 'null':
                            var_bkg = getvar(ncfile, var)
                        else:
                            var_bkg = getvar(ncfile, var, units=information['unit'])
                        ncfile.close()

                        ncfile = Dataset(wrfout_anl)
                        p_anl  = getvar(ncfile, 'pressure')
                        if information['unit'] == 'null':
                            var_anl = getvar(ncfile, var)
                        else:
                            var_anl = getvar(ncfile, var, units=information['unit'])
                        ncfile.close()

                        lat, lon = latlon_coords(p_bkg)
                        (n_lat, n_lon) = lat.shape

                        if idt == 0:
                            ncfile_output = Dataset(filename, 'w', format='NETCDF4')
                            ncfile_output.createDimension('n_time',  total_da_cycles)
                            ncfile_output.createDimension('n_level', n_level)
                            ncfile_output.createDimension('n_wrf',   2)
                            ncfile_output.createDimension('n_lat',   n_lat)
                            ncfile_output.createDimension('n_lon',   n_lon)
                            ncfile_output.createVariable('level', 'f8', ('n_level'))
                            ncfile_output.createVariable('lat',   'f8', ('n_lat',  'n_lon'))
                            ncfile_output.createVariable('lon',   'f8', ('n_lat',  'n_lon'))
                            ncfile_output.createVariable(var,     'f8', ('n_time', 'n_level', 'n_wrf', 'n_lat', 'n_lon'))
                            ncfile_output.variables['level'][:] = list(levels.keys())
                            ncfile_output.variables['lat'][:,:] = lat
                            ncfile_output.variables['lon'][:,:] = lon
                            ncfile_output.description           = var

                        if 0 in levels:
                            ncfile_output.variables[var][idt,0,0,:,:] = var_bkg
                            ncfile_output.variables[var][idt,0,1,:,:] = var_anl
                        else:
                            temp_bkg = interplevel(var_bkg, p_bkg, list(levels.keys()))
                            temp_anl = interplevel(var_anl, p_anl, list(levels.keys()))
                            for idl in range(len(levels)):
                                ncfile_output.variables[var][idt,idl,0,:,:] = temp_bkg[idl,:,:]
                                ncfile_output.variables[var][idt,idl,1,:,:] = temp_anl[idl,:,:]
                        
                    else:

                        ncfile_output.variables[var][idt,:,:,:,:] = 0.0

                ncfile_output.close()

def draw_analysis_increment(data_library_names, dir_cases, case_names, exp_names, variables = ['ua']):

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        # Import the necessary library
        (data_library_name, dir_case, case_name, exp_name) = (data_library_names[idc], dir_cases[idc], case_names[idc], exp_names[idc])

        module = importlib.import_module(f"data_library_{data_library_name}")
        attributes = getattr(module, 'attributes')
        dir_exp=attributes[(dir_case, case_name)]['dir_exp']
        dir_ScientificColourMaps7=attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
        total_da_cycles=attributes[(dir_case, case_name)]['total_da_cycles']
        itime=attributes[(dir_case, case_name)]['itime']
        initial_time = datetime.datetime(*itime)
        da_domains=attributes[(dir_case, case_name)]['da_domains']
        cycling_interval=attributes[(dir_case, case_name)]['cycling_interval']
        grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))

        anl_start_time = initial_time + datetime.timedelta(hours=cycling_interval)
        dir_increment = os.path.join(dir_exp, 'increment')
        specific_case = '_'.join([case_name, exp_name, 'C'+str(total_da_cycles).zfill(2)])
        dir_increment_case = os.path.join(dir_increment, specific_case)
        os.makedirs(dir_increment, exist_ok=True)
        os.makedirs(dir_increment_case, exist_ok=True)

        for dom in tqdm(da_domains, desc='DA Domains', leave=False):
            for var in tqdm(variables, desc='Variables', leave=False):
                (information, levels) = set_parameters_variables(var)
                filename = os.path.join(dir_increment_case, '_'.join([var, 'analysis', 'increment', dom+'.nc']))
                ncfile = Dataset(filename)
                lat = ncfile.variables['lat'][:,:]
                lon = ncfile.variables['lon'][:,:]
                extent = [lon[0,0], lon[-1,-1], lat[0,0], lat[-1,-1]]
                
                for idt in range(0, total_da_cycles):
                    time_now = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
                    time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')
                    # print(time_now)

                    for lev in levels.keys():

                        idl = list(levels).index(lev)
                        (vmin1, vmax1, vint1, cmap1, vmin2, vmax2, vint2, cmap2) = levels[lev]

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.png']))
                        with PdfPages(pdfname) as pdf:
                    
                            # fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))
                            fig, axs = plt.subplots(1, 1, figsize=(6.00, 3.50))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*ncfile.variables[var][idt,idl,0,:,:], levels=np.arange(vmin1, vmax1+0.5*vint1, vint1), cmap=cmap1, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
                            clb.set_label(information['lb_title'], fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(np.arange(vmin1, vmax1+0.5*vint1, vint1))
                            clb.set_ticklabels(np.arange(vmin1, vmax1+0.5*vint1, vint1))

                            plt.tight_layout()
                            plt.savefig(pngname, dpi=600)
                            pdf.savefig(fig)
                            plt.cla()
                            plt.clf()
                            plt.close()
                        
                        command = f"convert {pngname} -trim {pngname}"
                        subprocess.run(command, shell=True)

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'anl', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'anl', str(lev).zfill(3)+'hPa', dom+'.png']))
                        with PdfPages(pdfname) as pdf:
                    
                            # fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))
                            fig, axs = plt.subplots(1, 1, figsize=(6.00, 3.50))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*ncfile.variables[var][idt,idl,1,:,:], levels=np.arange(vmin1, vmax1+0.5*vint1, vint1), cmap=cmap1, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
                            clb.set_label(information['lb_title'], fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(np.arange(vmin1, vmax1+0.5*vint1, vint1))
                            clb.set_ticklabels(np.arange(vmin1, vmax1+0.5*vint1, vint1))

                            plt.tight_layout()
                            plt.savefig(pngname, dpi=600)
                            pdf.savefig(fig)
                            plt.cla()
                            plt.clf()
                            plt.close()

                        command = f"convert {pngname} -trim {pngname}"
                        subprocess.run(command, shell=True)

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'inc', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'inc', str(lev).zfill(3)+'hPa', dom+'.png']))
                        with PdfPages(pdfname) as pdf:
                    
                            # fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.50))
                            fig, axs = plt.subplots(1, 1, figsize=(6.00, 3.50))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*(ncfile.variables[var][idt,idl,1,:,:]-ncfile.variables[var][idt,idl,0,:,:]), levels=np.arange(vmin2, vmax2+0.5*vint2, vint2), cmap=cmap2, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=25, shrink=1.00)
                            clb.set_label(information['lb_title'], fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(np.arange(vmin2, vmax2+0.5*vint2, vint2))
                            clb.set_ticklabels(np.arange(vmin2, vmax2+0.5*vint2, vint2))

                            plt.tight_layout()
                            plt.savefig(pngname, dpi=600)
                            pdf.savefig(fig)
                            plt.cla()
                            plt.clf()
                            plt.close()

                        command = f"convert {pngname} -trim {pngname}"
                        subprocess.run(command, shell=True)

                ncfile.close()