import os

import pandas as pd
import numpy as np


#-------------------- READ CSV FILE ----------------------
def read_csv(csv_file_path,frac = False,random_state =42,drop_index= False):

    dataset_name = csv_file_path.split('/')[-1]

    if os.path.isfile(csv_file_path) and dataset_name[-3:] == 'csv':
        df = pd.read_csv(csv_file_path)

        if frac:
            df = df.sample(frac =frac,random_state=random_state)
            df.reset_index(drop=drop_index, inplace = True)

        print("{} 's information:".format(dataset_name))
        print(df.info())
        print()

        return df
    else:
        print("Missing csv file")


def print_df(df, _list = None, index = True):

    if _list is None:
        _list = range(len(df))

    try:
        if  index:
            for i in _list:
                print('{:6} :   {}'.format(df.index[i], df.iloc[i]))
        else:
            for i in _list:
                print(df.iloc[i])
    except:
        print(f'{i} is out of index')


def safe_get(data, *keys):
    try:
        current = data
        for key in keys:
            current = current[key]
    except:
        current = None
    return current
#------------------- Anomalies ---------------------#

def _std_cut_off(df, return_outliers = False):
    df_std = df.std()
    df_mean = df.mean()
    anomaly_cut_off = df_std * 3

    lower_limit  = df_mean - anomaly_cut_off
    upper_limit = df_mean + anomaly_cut_off

    if return_outliers:
        return df[df <= lower_limit], df[df <= upper_limit]
    else:
        return df[(df >= lower_limit) & (df <= upper_limit)]

def find_anomalies(df, columns = None, return_outliers = False):
    # Set upper and lower limit to 3 standard deviation
    if columns is None:
        return _std_cut_off(df,return_outliers)
    else:
        for column in columns:
            _std_cut_off(df[column], return_outliers)

# ------------------------ Create BINS -------------------------

def _create_bins(df,category,n_bins):
    global bins

    bins = np.unique(df.quantile(np.linspace(0, 1, n_bins)).values.astype(int))

    if category > len(bins) -1:
        n_bins += 5
        _create_bins(df,category,n_bins)
    elif category < len(bins) -1:
        n_bins -= 1
        _create_bins(df,category,n_bins)

    return bins, n_bins

def create_bins(df,bins = None ,n_bins = 3,right = False, return_bins = False):

    if bins is None:
        category = n_bins
        bins = []
        df_sorted = df.sort_values()

        bins, n_bins = _create_bins(df_sorted,category,n_bins)

    df = pd.cut(df, bins=bins, right=right, duplicates='drop').cat.codes

    if return_bins:
        return df, bins, n_bins
    else:
        return df
