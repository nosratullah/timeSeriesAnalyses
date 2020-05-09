import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert,find_peaks,correlate
from time import gmtime as gmt
import os
import seaborn as sns
import pandas as pd
import timeSeriesAnalysis as lc


date = 'data'
sns.set_style('darkgrid')

fileList = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
for j in fileList:
    data = pd.read_csv('{}/lfp_{}.csv'.format(date,j))
    ex_lfp = np.array(data['ex_lfp'])
    in_lfp = np.array(data['in_lfp'])
    time = np.array(data['time'])
    #ex_lfp = lc.smooth(ex_lfp,5)
    #in_lfp = lc.smooth(in_lfp,5)
    # The Furiertransform Part
    ex_fft, time_domain = lc.manualFFT(ex_lfp,time)
    in_fft, time_domain = lc.manualFFT(in_lfp,time)
    # The Plotting Part
    plt.figure(figsize=(20,15))
    plt.subplot(411)
    plt.plot(time[20:1020],ex_lfp[20:1020],label='excitatory lfp',color=u'#86232F');
    plt.ylabel('mV')
    #plt.grid(alpha=1,color='w',linestyle='--')
    plt.legend(loc=1)
    plt.subplot(412)
    plt.plot(time_domain[1:],ex_fft[1:], label='excitatory frequency',color=u'#86232F')
    plt.legend(loc=1)
    plt.ylabel('Amplitude')
    plt.xlim(0,300)
    plt.subplot(413)
    plt.plot(time[20:1020],in_lfp[20:1020],label='inhibitory lfp',color=u'#949494');
    plt.legend(loc=1)
    plt.subplot(414)
    plt.plot(time_domain[1:],in_fft[1:], label='excitatory frequency',color=u'#949494')
    plt.legend(loc=1)
    plt.xlim(0,300)
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')

    corrsAddress = date + '/lfp'
    if (os.path.isdir(corrsAddress)):
        pass
    else:
        os.makedirs(corrsAddress)
    plt.savefig('{}/lfp_{}.png'.format(corrsAddress,j))
