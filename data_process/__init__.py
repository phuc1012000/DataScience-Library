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

def reduce_mem_usage(df, verbose = False):
    start_mem_usg = df.memory_usage().sum() / 1024**2
    print("Memory usage of properties dataframe is :",start_mem_usg," MB")
    NAlist = [] # Keeps track of columns that have missing values filled in.
    for col in df.columns:
        if df[col].dtype != object:  # Exclude strings

            # Print current column type
            if verbose:
                print("Column: ",col)
                print("dtype before: ",df[col].dtype)

            # make variables for Int, max and min
            IsInt = False
            mx = df[col].max()
            mn = df[col].min()

            # Integer does not support NA, therefore, NA needs to be filled
            if not np.isfinite(df[col]).all():
                NAlist.append(col)
                df[col].fillna(mn-1,inplace=True)

            # test if column can be converted to an integer
            asint = df[col].fillna(0).astype(np.int64)
            result = (df[col] - asint)
            result = result.sum()
            if result > -0.01 and result < 0.01:
                IsInt = True


            # Make Integer/unsigned Integer datatypes
            if IsInt:
                if mn >= 0:
                    if mx < 255:
                        df[col] = df[col].astype(np.uint8)
                    elif mx < 65535:
                        df[col] = df[col].astype(np.uint16)
                    elif mx < 4294967295:
                        df[col] = df[col].astype(np.uint32)
                    else:
                        df[col] = df[col].astype(np.uint64)
                else:
                    if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                        df[col] = df[col].astype(np.int64)

            # Make float datatypes 32 bit
            else:
                df[col] = df[col].astype(np.float32)

            # Print new column type
            if verbose:
                print("dtype after: ",df[col].dtype)
                print("******************************")

    # Print final result
    print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = df.memory_usage().sum() / 1024**2
    print("Memory usage is: ",mem_usg," MB")
    print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")

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
