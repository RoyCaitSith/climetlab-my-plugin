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
        levels.update({925: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({850: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({700: [['-20', '-15', '-10', '-5', '0', '5', '10', '15', '20'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({500: [['-20', '-15', '-10', '-5', '0', '5', '10', '15', '20'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({300: [['-32', '-24', '-16', '-8', '0', '8', '16', '24', '32'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({200: [['-32', '-24', '-16', '-8', '0', '8', '16', '24', '32'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
    if 'va' in var:
        levels.update({925: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({850: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({700: [['-12',  '-9',  '-6', '-3', '0', '3',  '6',  '9', '12'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({500: [['-12',  '-9',  '-6', '-3', '0', '3',  '6',  '9', '12'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({300: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
        levels.update({200: [['-16', '-12',  '-8', '-4', '0', '4',  '8', '12', '16'], cmaps.vik, ['-4', '-3', '-2', '-1', '0', '1', '2', '3', '4'], cmaps.vik]})
    if 'temp' in var:
        levels.update({925: [[  '284',   '287',   '290',   '293',   '296',   '299',   '302',   '305',   '308'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({850: [[  '284',   '287',   '290',   '293',   '296',   '299',   '302',   '305',   '308'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({700: [[  '274',   '276',   '278',   '280',   '282',   '284',   '286',   '288',   '290'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({500: [[  '262',   '263',   '264',   '265',   '266',   '267',   '268',   '269',   '270'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({300: [['232.0', '233.5', '235.0', '236.5', '238.0', '239.5', '241.0', '242.5', '244.0'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
        levels.update({200: [['212.0', '213.5', '215.0', '216.5', '218.0', '219.5', '221.0', '222.5', '224.0'], cmaps.lajolla, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.vik]})
    if 'QVAPOR' in var:
        levels.update({925: [['0',    '2',    '4',    '6',    '8',   '10',   '12',   '14',   '16'], cmaps.imola, ['-3.2', '-2.4', '-1.6', '-0.8', '0', '0.8', '1.6', '2.4', '3.2'], cmaps.cork]})
        levels.update({850: [['0',    '2',    '4',    '6',    '8',   '10',   '12',   '14',   '16'], cmaps.imola, ['-2.0', '-1.5', '-1.0', '-0.5', '0', '0.5', '1.0', '1.5', '2.0'], cmaps.cork]})
        levels.update({700: [['0',  '1.5',    '3',  '4.5',    '6',  '7.5',    '9', '10.5',   '12'], cmaps.imola, ['-1.2', '-0.9', '-0.6', '-0.3', '0', '0.3', '0.6', '0.9', '1.2'], cmaps.cork]})
        levels.update({500: [['0',    '1',    '2',    '3',    '4',    '5',    '6',    '7',    '8'], cmaps.imola, ['-0.8', '-0.6', '-0.4', '-0.2', '0', '0.2', '0.4', '0.6', '0.8'], cmaps.cork]})
        levels.update({300: [['0',  '0.1',  '0.2',  '0.3',  '0.4',  '0.5',  '0.6',  '0.7',  '0.8'], cmaps.imola, ['-0.4', '-0.3', '-0.2', '-0.1', '0', '0.1', '0.2', '0.3', '0.4'], cmaps.cork]})
        levels.update({200: [['0',  '0.1',  '0.2',  '0.3',  '0.4',  '0.5',  '0.6',  '0.7',  '0.8'], cmaps.imola, ['-0.4', '-0.3', '-0.2', '-0.1', '0', '0.1', '0.2', '0.3', '0.4'], cmaps.cork]})

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
                fig_width = 2.75*np.abs(lon[-1,-1]-lon[0,0])/np.abs(lat[-1,-1]-lat[0,0])
                fig_height = 2.75+0.75
                clb_aspect = 25*np.abs(lon[-1,-1]-lon[0,0])/np.abs(lat[-1,-1]-lat[0,0])
                
                for idt in range(0, total_da_cycles):
                    time_now = anl_start_time + datetime.timedelta(hours = idt*cycling_interval)
                    time_now_YYYYMMDDHH = time_now.strftime('%Y%m%d%H')
                    image_files = []
                    output_file = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, dom+'.png']))

                    for lev in levels.keys():

                        idl = list(levels).index(lev)
                        (clblabels1, cmap1, clblabels2, cmap2) = levels[lev]

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.png']))
                        image_files.append(pngname)
                        with PdfPages(pdfname) as pdf:
                    
                            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*ncfile.variables[var][idt,idl,0,:,:], levels=list(map(float, clblabels1)), cmap=cmap1, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                            clb.set_label(f"{information['lb_title']} of bkg at {lev} hPa", fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(list(map(float, clblabels1)))
                            clb.set_ticklabels(clblabels1)

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
                        image_files.append(pngname)
                        with PdfPages(pdfname) as pdf:

                            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*ncfile.variables[var][idt,idl,1,:,:], levels=list(map(float, clblabels1)), cmap=cmap1, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                            clb.set_label(f"{information['lb_title']} of anl at {lev} hPa", fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(list(map(float, clblabels1)))
                            clb.set_ticklabels(clblabels1)

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
                        image_files.append(pngname)
                        with PdfPages(pdfname) as pdf:

                            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))
                            ax = axs

                            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='i', ax=ax)
                            m.drawcoastlines(linewidth=0.5, color='k', zorder=2)
                            mlon, mlat = m(lon, lat)
                            pcm = ax.contourf(mlon, mlat, information['factor']*(ncfile.variables[var][idt,idl,1,:,:]-ncfile.variables[var][idt,idl,0,:,:]), levels=list(map(float, clblabels2)), cmap=cmap2, extend='both', zorder=1)

                            ax.set_xticks(np.arange(-180, 181, 10))
                            ax.set_yticks(np.arange(-90, 91, 10))
                            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
                            ax.tick_params('both', direction='in', labelsize=10.0)
                            ax.axis(extent)
                            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])

                            clb = fig.colorbar(pcm, ax=axs, orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                            clb.set_label(f"{information['lb_title']} of inc at {lev} hPa", fontsize=10.0, labelpad=4.0)
                            clb.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
                            clb.ax.minorticks_off()
                            clb.set_ticks(list(map(float, clblabels2)))
                            clb.set_ticklabels(clblabels2)

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

                    for lev in levels.keys():

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'bkg', str(lev).zfill(3)+'hPa', dom+'.png']))
                        os.system(f"rm -rf {pdfname}")
                        os.system(f"rm -rf {pngname}")

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'anl', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'anl', str(lev).zfill(3)+'hPa', dom+'.png']))
                        os.system(f"rm -rf {pdfname}")
                        os.system(f"rm -rf {pngname}")

                        pdfname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'inc', str(lev).zfill(3)+'hPa', dom+'.pdf']))
                        pngname = os.path.join(dir_increment_case, '_'.join([time_now_YYYYMMDDHH, var, 'inc', str(lev).zfill(3)+'hPa', dom+'.png']))
                        os.system(f"rm -rf {pdfname}")
                        os.system(f"rm -rf {pngname}")

                ncfile.close()