from scipy.signal import hilbert,find_peaks,correlate
import numpy as np
from statsmodels.tsa.stattools import acf,ccf

def extract_peaks(data):
    amps = np.abs(hilbert(data))
    peaks_times = find_peaks(amps)
    peaks_times = peaks_times[0]
    peaks = []
    for i in peaks_times:
        peaks.append(amps[i])
    peaks = peaks[:-1]
    return peaks

def time_diffrences(data):
    amps = np.abs(hilbert(data))
    peaks_times = find_peaks(amps)
    peaks_times = peaks_times[0]
    diff_list = np.diff(peaks_times)
    diff_list = np.array(diff_list)

    return diff_list

def amps_detection(data):
    amps_data = np.abs(hilbert(data))
    amps_times = find_peaks(amps_data)
    amps_times = list(amps_times[0])
    amps_peak_values = []
    for l in amps_times:
        amps_peak_values.append(amps_data[l])
    amps_peak_values = amps_peak_values[:-1]
    amps_peak_values = np.array(amps_peak_values)
    return amps_peak_values

def shuff_corr(data1, data2):
    np.random.shuffle(data1)
    np.random.shuffle(data2)
    shuff_corr = ccf(data1,data2,unbiased=False)
    return shuff_corr

def shuff_acf(data):
    np.random.shuffle(data)
    shuff_corr = acf(data,fft=True)
    return shuff_corr

def smooth(y, box_pts=3):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth
