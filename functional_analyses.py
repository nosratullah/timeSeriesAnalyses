import pandas as pd
import numpy as np
import crosscorrelations as cc
import amplitudeCorrolation as ac
import periodCorrelation as pc
import smoothing as sm
import histogram as hs

date = '2020/2/3/12/'
filtered_data = date + '/fft_filtered'
fileList = [2.0, 2.5, 3.0, 3.5 ,4.0, 4.5]
parameters = pd.read_csv('{}/NetworkParameters_{}.csv'.format(date,fileList[0]))
ex_tauSyn = parameters['ex_tauSyn'][0]

sm.smoothing(date, fileList)
cc.crossCorrelation(filtered_data, fileList, ex_tauSyn)
ac.amplitude_acf(filtered_data, fileList, ex_tauSyn)
pc.periods_acf(filtered_data, fileList, ex_tauSyn)
hs.histogram(filtered_data, fileList)
