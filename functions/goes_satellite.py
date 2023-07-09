import os
import importlib
from datetime import datetime, timedelta
from tqdm.notebook import tqdm
from google.cloud import storage

def download_goes_data_specific_days(download_start_time, n_days, data_set, dir_GOES):
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

def download_goes_data_cycling_da(data_library_name, dir_case, case_name, data_set):

    ####Unfinished

    bucket_name = "gcp-public-data-goes-16"
    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket_name)
    dir_GOES = os.path.join(dir_data, 'GOES')

    for idx in tqdm(range(n_days), desc='Day', unit="files", bar_format="{desc}: {n}/{total} files | {elapsed}<{remaining}"):
        time_now = download_start_time + timedelta(days=idx)
        time_str = time_now.strftime('%Y%m%d')
        year = time_now.strftime('%Y').zfill(4)
        start_time = datetime(int(year)-1, 12, 31, 0, 0, 0)
        time_dif = time_now - start_time
        day = str(time_dif.days).zfill(3)
        dir_day = os.path.join(dir_GOES, time_str)

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
