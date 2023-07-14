import os
import importlib
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from google.cloud import storage

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

        dir_data=os.path.join(dir_exp, 'data')        
        dir_GOES = os.path.join(dir_data, 'GOES')
        os.makedirs(dir_GOES, exist_ok=True)

        anl_start_time = initial_time + timedelta(hours=cycling_interval)
        n_time = (cycling_interval*(total_da_cycles-1) + forecast_hours + 6)/history_interval + 1

        for da_cycle in tqdm(range(1, total_da_cycles+1), desc='DA Cycles', leave=False, unit="files", bar_format="{desc}: {n}/{total} da cycles | {elapsed}<{remaining}"):
            
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
        
        print(maio)

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