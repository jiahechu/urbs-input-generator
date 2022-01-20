import os
import pandas as pd 


def find_all_file(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            if f.endswith('.csv'):
                fullname = os.path.join(root, f)
                yield fullname


def read_csv_file(csv_file_name, needed_info_name, sep):
    csv_data = pd.read_csv(csv_file_name, sep=sep)
    return csv_data[needed_info_name]


def read_whole_folder_csv(base_folder, needed_info_name, sep):
    needed_info_list = []
    for file in find_all_file(base_folder):
        needed_info_list.append(read_csv_file(file, needed_info_name, sep))
    return(needed_info_list)

def read_xls_file(xls_file_name, sheet_name):

