import os
import re
import glob
import datetime
import importlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

    dir_data = attributes[(dir_case, case_name)]['dir_data']
    filenames = glob.glob(os.path.join(dir_data, '*MetNav*ict'))
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
                day = datetime.datetime(int(items[0]), int(items[1]), int(items[2]), 0, 0, 0)
                day_str = day.strftime('%Y%m%d')

                time_list = []
                lat_list = []
                lon_list = []
                for line in lines[first_line:]:
                    line = line.rstrip('\n')
                    items = line.split(',')
                    time_now = day + datetime.timedelta(seconds = float(items[0]))
                    time_now_str = int(time_now.strftime('%Y%m%d%H%M%S'))
                    time_list += [time_now_str]
                    lat_list += [float(items[2])]
                    lon_list += [float(items[3])]

            row = pd.DataFrame({'Time': time_list, \
                                'LAT': lat_list, \
                                'LON': lon_list})
            df = pd.concat([df, row], ignore_index=True)

            filename_flight_track = '_'.join(['CPEXCV-MetNav', 'DC8', 'flight', 'track', day_str+'.csv'])
            save_file = os.path.join(dir_data, filename_flight_track)
            df.to_csv(save_file, index=False)
            print(filename_flight_track)

def draw_metnav_dc8(data_library_name, dir_case, case_name):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    dir_data = attributes[(dir_case, case_name)]['dir_data']
    dir_ScientificColourMaps7 = attributes[(dir_case, case_name)]['dir_ScientificColourMaps7']
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    grayC_map = LinearSegmentedColormap.from_list('grayC', grayC_cm_data[::1])
    filenames = glob.glob(os.path.join(dir_data, '*flight_track*csv'))

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

        clon = 5*(min_flight_lon + max_flight_lon)/2.0//5
        clat = 5*(min_flight_lat + max_flight_lat)/2.0//5
        half_extent = np.max([5*abs(max_flight_lon - clon)//5+5, 5*abs(max_flight_lat - clat)//5+5, 15])
        extent = [clon-half_extent+5.0, clon+half_extent, clat-half_extent+5.0, clat+half_extent]

        numbers = re.findall(r'\d+', filename)
        day_str = numbers[-1]
        pdfname = os.path.join(dir_data, '_'.join(['CPEXCV-MetNav', 'DC8', 'flight', 'track', day_str+'.pdf']))
        pngname = os.path.join(dir_data, '_'.join(['CPEXCV-MetNav', 'DC8', 'flight', 'track', day_str+'.png']))

        print('_'.join(['CPEXCV-MetNav', 'DC8', 'flight', 'track', day_str+'.csv']))
        print(f"Time: from {min_flight_time} to {max_flight_time}")
        print(f"LAT: from {min_flight_lat} to {max_flight_lat}")
        print(f"LON: from {min_flight_lon} to {max_flight_lon}")

        with PdfPages(pdfname) as pdf:

            fig, axs = plt.subplots(1, 1, figsize=(3.25, 3.0))

            ax = axs
            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='h', ax=ax)
            m.drawcoastlines(linewidth=0.2, color='k')
            ax.plot(flight_lon, flight_lat, '-', color='k', linewidth=2.50, label='DC8', zorder=3)

            ax.set_xticks(np.arange(-180, 181, 5))
            ax.set_yticks(np.arange(-90, 91, 5))
            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 5)])
            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  5)])
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.axis(extent)
            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
            ax.legend(loc='upper right', fontsize=5.0, handlelength=2.5).set_zorder(102)

            plt.tight_layout()
            plt.savefig(pngname, dpi=600)
            pdf.savefig(fig)
            plt.cla()
            plt.clf()
            plt.close()

            image = IPImage(filename=pngname)
            display(image)
