import os
import re
import glob
import importlib
import subprocess
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from netCDF4 import Dataset
from tqdm.notebook import tqdm
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from combine_and_show_images import combine_images_grid
from IPython.display import Image as IPImage

def metnav_to_csv(data_library_name, dir_case, case_name):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_data = os.path.join(dir_exp, 'data')
    dir_MetNav = os.path.join(dir_data, 'MetNav')

    filenames = glob.glob(os.path.join(dir_MetNav, '*MetNav*ict'))
    for filename in tqdm(filenames, desc='Files', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        if filename != '':
            df = pd.DataFrame(columns=['Time', 'LAT', 'LON'])
            with open(filename) as f:
                lines = f.readlines()

                #Get the first line of the record
                line = lines[0:1][0].rstrip('\n')
                items = line.split(',')
                first_line = int(items[0])

                #Get the date
                line = lines[6:7][0].rstrip('\n')
                items = line.split(',')
                day = datetime(int(items[0]), int(items[1]), int(items[2]), 0, 0, 0)
                day_str = day.strftime('%Y%m%d')

                time_list = []
                lat_list = []
                lon_list = []
                for line in lines[first_line:]:
                    line = line.rstrip('\n')
                    items = line.split(',')
                    time_now = day + timedelta(seconds = float(items[0]))
                    time_now_str = int(time_now.strftime('%Y%m%d%H%M%S'))
                    time_list += [time_now_str]
                    lat_list += [float(items[2])]
                    lon_list += [float(items[3])]

            row = pd.DataFrame({'Time': time_list, \
                                'LAT': lat_list, \
                                'LON': lon_list})
            df = pd.concat([df, row], ignore_index=True)

            filename_flight_track = '_'.join(['CPEXCV-MetNav', 'DC8', 'flight', 'track', day_str+'.csv'])
            save_file = os.path.join(dir_MetNav, filename_flight_track)
            df.to_csv(save_file, index=False)
            print(filename_flight_track)

def draw_metnav_dc8(data_library_name, dir_case, case_name, wrf_domain=False, wrf_domain_exp_name='CTRL'):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_MetNav = os.path.join(dir_data, 'MetNav')
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    filenames = glob.glob(os.path.join(dir_MetNav, '*flight_track*csv'))

    if wrf_domain:

        dir_wrfout = os.path.join(dir_exp, 'cycling_da', f"{case_name}_{wrf_domain_exp_name}_C{str(total_da_cycles).zfill(2)}", 'bkg')
        wrfout_format = 'wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}'
        file_wrfout_d01 = os.path.join(dir_wrfout, wrfout_format.format(dom='d01', ctime=initial_time))
        file_wrfout_d02 = os.path.join(dir_wrfout, wrfout_format.format(dom='d02', ctime=initial_time))

        wrfout_d01 = Dataset(file_wrfout_d01)
        lat_d01 = wrfout_d01.variables['XLAT'][0,:,:]
        lon_d01 = wrfout_d01.variables['XLONG'][0,:,:]
        wrfout_d01.close()

        lat_d02 = []
        lon_d02 = []
        wrfout_d02 = Dataset(file_wrfout_d02)
        lat_temp = wrfout_d02.variables['XLAT'][0,:,:]
        lon_temp = wrfout_d02.variables['XLONG'][0,:,:]
        n_we_d02 = len(lat_temp[0, :])
        n_sn_d02 = len(lat_temp[:, 0])
        lat_d02.extend(list(lat_temp[0, 0:n_we_d02-1:1]))
        lat_d02.extend(list(lat_temp[0:n_sn_d02-1, n_we_d02-1]))
        lat_d02.extend(list(lat_temp[n_sn_d02-1, n_we_d02-1:0:-1]))
        lat_d02.extend(list(lat_temp[n_sn_d02-1:0:-1, 0]))
        lon_d02.extend(list(lon_temp[0, 0:n_we_d02-1:1]))
        lon_d02.extend(list(lon_temp[0:n_sn_d02-1, n_we_d02-1]))
        lon_d02.extend(list(lon_temp[n_sn_d02-1, n_we_d02-1:0:-1]))
        lon_d02.extend(list(lon_temp[n_sn_d02-1:0:-1, 0]))
        lat_d02.append(lat_temp[0, 0])
        lon_d02.append(lon_temp[0, 0])
        wrfout_d02.close()

    for filename in tqdm(filenames, desc='Files', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        df = pd.read_csv(filename)
        flight_time = df['Time']
        flight_lat = df['LAT']
        flight_lon = df['LON']
        min_flight_time = np.min(flight_time)
        max_flight_time = np.max(flight_time)
        min_flight_lat  = np.min(flight_lat)
        max_flight_lat  = np.max(flight_lat)
        min_flight_lon  = np.min(flight_lon)
        max_flight_lon  = np.max(flight_lon)

        if wrf_domain:
            domain = 'd01_d02'
            extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
        else:
            domain = 'auto'
            clon = 5*(min_flight_lon + max_flight_lon)/2.0//5
            clat = 5*(min_flight_lat + max_flight_lat)/2.0//5
            half_extent = np.max([5*abs(max_flight_lon - clon)//5+5, 5*abs(max_flight_lat - clat)//5+5, 15])
            extent = [clon-half_extent+5.0, clon+half_extent, clat-half_extent+5.0, clat+half_extent]
        
        fig_width = 3.00*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])+0.5
        fig_height = 3.00

        numbers = re.findall(r'\d+', filename)
        day_str = numbers[-1]
        pdfname = os.path.join(dir_MetNav, '_'.join([day_str, 'CPEXCV-MetNav', 'DC8', 'flight', 'track', domain+'.pdf']))
        pngname = os.path.join(dir_MetNav, '_'.join([day_str, 'CPEXCV-MetNav', 'DC8', 'flight', 'track', domain+'.png']))

        print('_'.join(['CPEXCV-MetNav', 'DC8', 'flight', 'track', day_str+'.csv']))
        print(f"Time: from {min_flight_time} to {max_flight_time}")
        print(f"LAT: from {min_flight_lat} to {max_flight_lat}")
        print(f"LON: from {min_flight_lon} to {max_flight_lon}")

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))

            ax = axs
            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='h', ax=ax)
            m.drawcoastlines(linewidth=0.2, color='k')
            ax.plot(flight_lon, flight_lat, '-', color='k', linewidth=1.00, label='DC8', zorder=3)

            if wrf_domain:
                x_lon_d02, y_lat_d02 = m(lon_d02, lat_d02, inverse=False)
                ax.plot(x_lon_d02, y_lat_d02, '-', color='k', linewidth=1.00, zorder=7)
                ax.text(np.max(lon_d01)-2.00, np.min(lat_d01)+1.50, 'D01', ha='right', va='bottom', color='k', fontsize=10.0, zorder=7)
                ax.text(np.max(lon_d02)-2.00, np.min(lat_d02)+1.50, 'D02', ha='right', va='bottom', color='k', fontsize=10.0, zorder=7)
                ax.set_xticks(np.arange(-180, 181, 10))
                ax.set_yticks(np.arange(-90, 91, 10))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
                ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
            else:
                ax.set_xticks(np.arange(-180, 181, 5))
                ax.set_yticks(np.arange(-90, 91, 5))
                ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 5)])
                ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  5)])
            
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.axis(extent)
            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
            ax.legend(loc='best', fontsize=5.0, handlelength=2.5).set_zorder(102)

            plt.tight_layout()
            plt.savefig(pngname, dpi=600)
            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()

            command = f"convert {pngname} -trim {pngname}"
            subprocess.run(command, shell=True)
            image = IPImage(filename=pngname)
            display(image)
