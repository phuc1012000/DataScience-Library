from statsmodels.tsa.tsatools import lagmat

import pandas as pd
import numpy as np

def lag_func(df,columns,lag):
    for column in columns:
        lag_0_col = column + "_lag_0"
        df[lag_0_col] = 0
        df.loc[1:, lag_0_col] = df[column][1:].values - df[column][:-1].values

        X = lagmat(df[lag_0_col], lag)

        for c in range(1,lag+1):
            df["lag_%d" % c] = X[:, c-1]
