import os
import glob
import datetime
import pandas as pd
from data_library import attributes
from tqdm.notebook import tqdm

def metnav_to_csv(dir_case, case_name):

    dir_data = attributes[(dir_case, case_name)]['dir_data']
    filenames = glob.glob(os.path.join(dir_data, '*MetNav*'))
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

            filename_flight_track = '_'.join(['flight', 'track', day_str+'.csv'])
            save_file = os.path.join(dir_data, filename_flight_track)
            df.to_csv(save_file, index=False)
            print(save_file)
