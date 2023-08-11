import os
import re
import glob
import importlib
import subprocess
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cpt_convert import loadCPT
from netCDF4 import Dataset
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from google.cloud import storage
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.basemap import Basemap
from IPython.display import Image as IPImage
from matplotlib.colors import LinearSegmentedColormap

def download_goes_date(download_start_time, n_days, dir_GOES, data_set='ABI-L2-CMIPF'):
    """
    Download GOES-R data for a specified number of days and store it locally.

    Args:
    download_start_time (datetime): The start date and time for downloading the data.
    n_days (int): The number of days for which to download the data.
    data_set (str): The name of the data set in the GCP bucket.
    dir_GOES (str): The local directory where the downloaded files will be stored.
    """
    bucket_name = "gcp-public-data-goes-16"
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)

    for idx in tqdm(range(n_days), desc='Day', unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        time_now = download_start_time + timedelta(days=idx)
        time_str = time_now.strftime('%Y%m%d')
        year = time_now.strftime('%Y').zfill(4)
        start_time = datetime(int(year)-1, 12, 31, 0, 0, 0)
        time_dif = time_now - start_time
        day = str(time_dif.days).zfill(3)
        dir_day = f"{dir_GOES}/{time_str}"

        os.makedirs(dir_day, exist_ok=True)

        for hour in tqdm(range(24), desc='Hours', leave=False, unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
            dir_hour = f"{dir_day}/{str(hour).zfill(2)}"
            os.makedirs(dir_hour, exist_ok=True)
            dir_in = f"{data_set}/{year}/{day}/{str(hour).zfill(2)}/"
            blobs = bucket.list_blobs(prefix=dir_in)

            for blob in tqdm(blobs, desc='Files', leave=False, unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
                file_name = os.path.basename(blob.name)
                # Check if the file corresponds to channels 7 to 16
                channel_number = int(file_name.split("_")[1][-2:])
                if 7 <= channel_number <= 16:
                    local_path = os.path.join(dir_hour, file_name)
                    # Download the file from GCS to the local machine
                    with open(local_path, "wb") as f:
                        blob.download_to_file(f)

def download_goes_case(data_library_names, dir_cases, case_names, data_sets=['ABI-L2-CMIPF']):

    bucket_name = "gcp-public-data-goes-16"
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)

    for idc in tqdm(range(len(dir_cases)), desc='Cases', unit='files', bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):

        (data_library_name, dir_case, case_name) = (data_library_names[idc], dir_cases[idc], case_names[idc])

        module=importlib.import_module(f"data_library_{data_library_name}")
        attributes=getattr(module, 'attributes')
    
        itime = attributes[(dir_case, case_name)]['itime']
        dir_exp = attributes[(dir_case, case_name)]['dir_exp']
        total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']
        forecast_hours = attributes[(dir_case, case_name)]['forecast_hours']
        cycling_interval = attributes[(dir_case, case_name)]['cycling_interval']
        history_interval = attributes[(dir_case, case_name)]['history_interval']
        initial_time = datetime(*itime)

        dir_data = os.path.join(dir_exp, 'data')        
        dir_GOES = os.path.join(dir_data, 'GOES')
        os.makedirs(dir_GOES, exist_ok=True)

        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        n_time = int((cycling_interval*(total_da_cycles-1) + forecast_hours + 6)/history_interval + 1)

        for da_cycle in tqdm(range(0, total_da_cycles+1), desc='DA Cycles', leave=False, unit="files", bar_format="{desc}: {n}/{total} da cycles | {elapsed}<{remaining}"):
            
            time_now = initial_time + timedelta(hours=cycling_interval*da_cycle)
            time_now_str = time_now.strftime('%Y%m%d')
            time_now_year = time_now.strftime('%Y').zfill(4)
            time_now_hour = time_now.strftime('%H').zfill(2)

            start_time = datetime(int(time_now_year)-1, 12, 31, 0, 0, 0)
            time_dif = time_now - start_time
            day = str(time_dif.days).zfill(3)
            dir_day = os.path.join(dir_GOES, time_now_str)
            os.makedirs(dir_day, exist_ok=True)

            for data_set in data_sets:
                dir_in = f"{data_set}/{time_now_year}/{day}/{time_now_hour}/"
                blobs = bucket.list_blobs(prefix=dir_in)

                for blob in tqdm(blobs, desc='Files', leave=False, unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
                    file_name = os.path.basename(blob.name)
                    # Check if the file corresponds to channels 7 to 16
                    channel_number = int(file_name.split("_")[1][-2:])
                    if 7 <= channel_number <= 16:
                        local_path = os.path.join(dir_day, file_name)
                        # Download the file from GCS to the local machine
                        with open(local_path, "wb") as f:
                            blob.download_to_file(f)

        for idt in tqdm(range(n_time), desc='Forecasts', leave=False, unit="files", bar_format="{desc}: {n}/{total} forecasts | {elapsed}<{remaining}"):
            
            time_now = anl_start_time + timedelta(hours=history_interval*idt)
            time_now_str = time_now.strftime('%Y%m%d')
            time_now_year = time_now.strftime('%Y').zfill(4)
            time_now_hour = time_now.strftime('%H').zfill(2)

            start_time = datetime(int(time_now_year)-1, 12, 31, 0, 0, 0)
            time_dif = time_now - start_time
            day = str(time_dif.days).zfill(3)
            dir_day = os.path.join(dir_GOES, time_now_str)
            os.makedirs(dir_day, exist_ok=True)

            for data_set in data_sets:
                dir_in = f"{data_set}/{time_now_year}/{day}/{time_now_hour}/"
                blobs = bucket.list_blobs(prefix=dir_in)

                for blob in tqdm(blobs, desc='Files', leave=False, unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
                    file_name = os.path.basename(blob.name)
                    # Check if the file corresponds to channels 7 to 16
                    channel_number = int(file_name.split("_")[1][-2:])
                    if 7 <= channel_number <= 16:
                        local_path = os.path.join(dir_day, file_name)
                        # Download the file from GCS to the local machine
                        with open(local_path, "wb") as f:
                            blob.download_to_file(f)

def draw_goes_images(data_library_name, dir_case, case_name, channel=8, goes_levels=np.arange(190.0, 270.1, 1.0),
                     flight_track=False, dropsonde=False, tc_track=False, aew_track=False,
                     anl_start_time=datetime(2022, 9, 16, 0, 0, 0), anl_end_time=datetime(2022, 9, 16, 0, 0, 0), time_interval=1.0,
                     region_type='d01', wrf_domain_exp_name='CTRL', domain_specified=[-60, -10, -10, 30]):

    # Import the necessary library
    module = importlib.import_module(f"data_library_{data_library_name}")
    attributes = getattr(module, 'attributes')

    itime = attributes[(dir_case, case_name)]['itime']
    initial_time = datetime(*itime)
    dir_exp = attributes[(dir_case, case_name)]['dir_exp']
    dir_colormaps = attributes[(dir_case, case_name)]['dir_colormaps']
    total_da_cycles = attributes[(dir_case, case_name)]['total_da_cycles']

    dir_data = os.path.join(dir_exp, 'data')
    dir_MetNav = os.path.join(dir_data, 'MetNav')
    dir_abi = os.path.join(dir_data, 'GOES')
    dir_goes = os.path.join(dir_exp, 'goes')
    dir_ScientificColourMaps7 = os.path.join(dir_colormaps, 'ScientificColourMaps7')
    grayC_cm_data = np.loadtxt(os.path.join(dir_ScientificColourMaps7, 'grayC', 'grayC.txt'))
    cpt, cpt_r = loadCPT(os.path.join(dir_colormaps, 'GOES-R_BT.rgb'))
    cpt_convert = LinearSegmentedColormap('cpt', cpt)
    
    if region_type == 'd01' or region_type == 'd02':

        dir_wrfout = os.path.join(dir_exp, 'cycling_da', f"{case_name}_{wrf_domain_exp_name}_C{str(total_da_cycles).zfill(2)}", 'bkg')
        wrfout_format = 'wrfout_{dom}_{ctime:%Y-%m-%d_%H:%M:00}'
        file_wrfout_d01 = os.path.join(dir_wrfout, wrfout_format.format(dom='d01', ctime=initial_time))
        file_wrfout_d02 = os.path.join(dir_wrfout, wrfout_format.format(dom='d02', ctime=initial_time))

        wrfout_d01 = Dataset(file_wrfout_d01)
        lat_d01 = wrfout_d01.variables['XLAT'][0,:,:]
        lon_d01 = wrfout_d01.variables['XLONG'][0,:,:]
        wrfout_d01.close()

        lat_d02_box = []
        lon_d02_box = []
        wrfout_d02 = Dataset(file_wrfout_d02)
        lat_d02 = wrfout_d02.variables['XLAT'][0,:,:]
        lon_d02 = wrfout_d02.variables['XLONG'][0,:,:]
        n_we_d02 = len(lat_d02[0, :])
        n_sn_d02 = len(lat_d02[:, 0])
        lat_d02_box.extend(list(lat_d02[0, 0:n_we_d02-1:1]))
        lat_d02_box.extend(list(lat_d02[0:n_sn_d02-1, n_we_d02-1]))
        lat_d02_box.extend(list(lat_d02[n_sn_d02-1, n_we_d02-1:0:-1]))
        lat_d02_box.extend(list(lat_d02[n_sn_d02-1:0:-1, 0]))
        lon_d02_box.extend(list(lon_d02[0, 0:n_we_d02-1:1]))
        lon_d02_box.extend(list(lon_d02[0:n_sn_d02-1, n_we_d02-1]))
        lon_d02_box.extend(list(lon_d02[n_sn_d02-1, n_we_d02-1:0:-1]))
        lon_d02_box.extend(list(lon_d02[n_sn_d02-1:0:-1, 0]))
        lat_d02_box.append(lat_d02[0, 0])
        lon_d02_box.append(lon_d02[0, 0])
        wrfout_d02.close()
    
    if region_type == 'flight' or flight_track:
        filenames = glob.glob(os.path.join(dir_MetNav, '*flight_track*csv'))
        for filename in filenames:
            df = pd.read_csv(filename)
            flight_time = df['Time']
            flight_lat = df['LAT']
            flight_lon = df['LON']
            min_flight_lat = np.min(flight_lat)
            max_flight_lat = np.max(flight_lat)
            min_flight_lon = np.min(flight_lon)
            max_flight_lon = np.max(flight_lon)
            numbers = re.findall(r'\d+', filename)
            index_flight_time = flight_time%10000 == 0
            index_flight_time_00 = flight_time%1000000 == 0                                                                         
            del df

    if region_type == 'd01': extent = [lon_d01[0,0], lon_d01[-1,-1], lat_d01[0,0], lat_d01[-1,-1]]
    if region_type == 'd02': extent = [lon_d02[0,0], lon_d02[-1,-1], lat_d02[0,0], lat_d02[-1,-1]]
    if region_type == 'specified': extent = [domain_specified[0], domain_specified[1], domain_specified[2], domain_specified[3]]
    if region_type == 'flight':
        clon = 5*(min_flight_lon + max_flight_lon)/2.0//5
        clat = 5*(min_flight_lat + max_flight_lat)/2.0//5
        half_extent = np.max([5*abs(max_flight_lon - clon)//5+5, 5*abs(max_flight_lat - clat)//5+5, 15])
        extent = [clon-half_extent+5.0, clon+half_extent, clat-half_extent+5.0, clat+half_extent]

    duration = anl_end_time - anl_start_time
    duration_in_second = duration.total_seconds()
    duration_in_hour = duration_in_second/3600
    n_time = int(duration_in_hour/time_interval)+1

    for idt in tqdm(range(n_time), desc='Times', unit='files', bar_format="{desc}: {n}/{total} | {elapsed}<{remaining}"):

        time_now = anl_start_time + timedelta(hours=idt*time_interval)
        time_now_str = time_now.strftime('%Y%m%d%H%M%S')
        time_now_YYYYMMDD = time_now.strftime('%Y%m%d')
        time_now_HH = time_now.strftime('%H')

        output_filename = (
            f"{time_now_str}_ch{str(channel).zfill(2)}_"
            f"flight_track_{flight_track}_dropsonde_{dropsonde}_"
            f"tc_track_{tc_track}_aew_track_{aew_track}_"
            f"{region_type}"
        )

        pdfname = os.path.join(dir_goes, output_filename+'.pdf')
        pngname = os.path.join(dir_goes, output_filename+'.png')

        with PdfPages(pdfname) as pdf:

            fig_width = 2.75*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])
            fig_height = 2.75+0.75
            clb_aspect = 25*np.abs(extent[1]-extent[0])/np.abs(extent[3]-extent[2])

            fig, axs = plt.subplots(1, 1, figsize=(fig_width, fig_height))

            ax = axs
            m = Basemap(projection='cyl', llcrnrlat=extent[2], llcrnrlon=extent[0], urcrnrlat=extent[3], urcrnrlon=extent[1], resolution='h', ax=ax)
            m.drawcoastlines(linewidth=0.2, color='k')

            abiname = f"OR_ABI-L2-CMIPF-M6C{str(channel).zfill(2)}_G16_s*{time_now_HH}00*"
            abi = '/'.join([dir_abi, time_now_YYYYMMDD, abiname])
            fileabi = os.popen('ls ' + abi).read().split()

            ncfile = Dataset(fileabi[0])
            CMI = ncfile.variables['CMI'][:,:]
            x = ncfile.variables['x'][:]
            y = ncfile.variables['y'][:]

            gip      = ncfile.variables['goes_imager_projection']
            r_eq     = gip.semi_major_axis
            r_pol    = gip.semi_minor_axis
            H        = gip.perspective_point_height + gip.semi_major_axis
            phi_0    = gip.latitude_of_projection_origin
            lambda_0 = gip.longitude_of_projection_origin

            x, y    = np.meshgrid(x, y, indexing='xy')
            sin_x   = np.sin(x)
            cos_x   = np.cos(x)
            sin_y   = np.sin(y)
            cos_y   = np.cos(y)
            a       = np.power(sin_x, 2) + np.power(cos_x, 2)*(np.power(cos_y, 2)+np.power(r_eq*sin_y/r_pol, 2))
            b       = -2.0*H*cos_x*cos_y
            c       = np.power(H, 2) - np.power(r_eq, 2)
            r_s     = (-1.0*b - np.sqrt(np.power(b, 2)-4*a*c))/(2*a)
            s_x     = r_s*cos_x*cos_y
            s_y     = -1.0*r_s*sin_x
            s_z     = r_s*cos_x*sin_y
            abi_lat = np.degrees(np.arctan(np.power(r_eq/r_pol, 2)*s_z/np.sqrt(np.power(H-s_x, 2)+np.power(s_y, 2))))
            abi_lon = lambda_0 - np.degrees(np.arctan(s_y/(H-s_x)))

            x_abi_lon, y_abi_lat = m(abi_lon, abi_lat, inverse=False)
            pcm = ax.contourf(x_abi_lon, y_abi_lat, CMI, levels=goes_levels, cmap=cpt_convert, extend='both', zorder=1)            

            if flight_track: ax.plot(flight_lon, flight_lat, '-', color='k', linewidth=1.00, label='DC8', zorder=3)

            if region_type == 'd01':
                x_lon_d02_box, y_lat_d02_box = m(lon_d02_box, lat_d02_box, inverse=False)
                ax.plot(x_lon_d02_box, y_lat_d02_box, '-', color='k', linewidth=1.00, zorder=7)
                ax.text(np.max(lon_d01)-2.00, np.min(lat_d01)+1.50, 'D01', ha='right', va='bottom', color='k', fontsize=10.0, zorder=7)
                ax.text(np.max(lon_d02)-2.00, np.min(lat_d02)+1.50, 'D02', ha='right', va='bottom', color='k', fontsize=10.0, zorder=7)

            ax.set_xticks(np.arange(-180, 181, 10))
            ax.set_yticks(np.arange(-90, 91, 10))
            ax.set_xticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "W" if x < 0 else ("E" if x > 0 else "")) for x in range(int(-180), int(180)+1, 10)])
            ax.set_yticklabels(["$\\mathrm{{{0}^\\circ {1}}}$".format(abs(x), "S" if x < 0 else ("N" if x > 0 else "")) for x in range(int(-90),  int(90)+1,  10)])
            ax.tick_params('both', direction='in', labelsize=10.0)
            ax.axis(extent)
            ax.grid(True, linewidth=0.5, color=grayC_cm_data[53])
            ax.legend(loc='best', fontsize=5.0, handlelength=2.5).set_zorder(102)

            # if tc_track:
            #     clb1 = fig.colorbar(pcm, ax=axs, ticks=np.arange(190, 250.1, 5.0), orientation='horizontal', pad=-0.025, aspect=50, shrink=1.00)
            #     clb1.set_label('GOES-R Channel 8 BTs (K) at ' + time_now.strftime('%H UTC %d Aug %Y'), fontsize=10.0, labelpad=4.0)
            #     clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

            #     grade = [20, 33, 63, 82, 95, 112, 125]
            #     cat = ['TD', 'TS', 'Cat1', 'Cat2', 'Cat3', 'Cat4']
            #     clb2 = plt.colorbar(sc2, ticks=grade, orientation='horizontal', pad=0.050, aspect=50, shrink=1.00)
            #     clb2.set_ticklabels(grade)
            #     clb2.set_label('MWS (Knot)', fontsize=10.0)
            #     clb2.ax.tick_params(axis='both', direction='in', labelsize=10.0)
            #     for idx, lab in enumerate(cat):
            #         clb2.ax.text(0.5*(grade[idx+1]+grade[idx]), -95.0, lab, ha='center', va='center', color='k', fontsize=10.0)
            # else:
                # clb1 = fig.colorbar(pcm, ax=axs, ticks=goes_levels[::10], orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
                # clb1.set_label(f"BTs of channel {str(channel)} (K)", fontsize=10.0, labelpad=4.0)
                # clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)
            
            clb1 = fig.colorbar(pcm, ax=axs, ticks=goes_levels[::10], orientation='horizontal', pad=0.075, aspect=clb_aspect, shrink=1.00)
            clb1.set_label(f"BTs of channel {str(channel)} (K)", fontsize=10.0, labelpad=4.0)
            clb1.ax.tick_params(axis='both', direction='in', pad=4.0, length=3.0, labelsize=10.0)

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
