from scipy.fftpack import fft

import pandas as pd
import numpy as np

from matplotlib import pyplot as plt

from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import acf

def plot_with_fft(time_index,df, label,periods ,figsize=(15,5),color = ['r','b']):

    fig = plt.figure(1,figsize=figsize)
    plt.title(label)
    plt.plot(time_index, df, label = label,color = color[0] )
    fig = plt.figure(2,figsize=figsize)
    fft_complex = fft(df)

    fft_mag = [np.sqrt(np.real(x)*np.real(x)+np.imag(x)*np.imag(x)) for x in fft_complex]
    fft_xvals = [day / time_index[-1] for day in time_index]

    npts = len(fft_xvals) // 2 + 1
    fft_mag = fft_mag[:npts]
    fft_xvals = fft_xvals[:npts]

    plt.ylabel('FFT Magnitude')
    plt.title('Fourier Transform')
    plt.plot(fft_xvals[1:],fft_mag[1:],label =label,color = color[0] )
    # Draw lines at 1, 1/2, and 1/3 week periods
    for period in periods:
        plt.axvline(x=period,color=color[1],alpha=0.3)

    plt.legend()
    plt.show()


def autocorrelation_plot(data,title = 'autocorrelation',figsize=(10,5)):
    fig = plt.figure(1,figsize=figsize)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    data_diff = [data[i] - data[i-1] for i in range(1,len(data))]
    autocorr = acf(data_diff)
    pac = pacf(data_diff)

    x = [x for x in range(len(pac))]
    ax1.plot(x[1:],autocorr[1:])

    ax2.plot(x[1:],pac[1:])
    ax1.set_xlabel('Lag')
    ax1.set_ylabel('Autocorrelation')
    ax1.set_title(title)

    ax2.set_xlabel('Lag')
    ax2.set_ylabel('Partial Autocorrelation')
    plt.show()
