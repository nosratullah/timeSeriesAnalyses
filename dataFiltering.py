import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert,find_peaks,correlate
from time import gmtime as gmt
import os
import seaborn as sns
import pandas as pd
import timeSeriesAnalysis as lc


date = '2020/1/31/22/'
sns.set_style('darkgrid')

fileList = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5 ,4.0]
for j in fileList:
    # Data Importing
    data = pd.read_csv('{}/lfp_{}.csv'.format(date,j))
    ex_lfp = np.array(data['ex_lfp'])
    in_lfp = np.array(data['in_lfp'])
    time = np.array(data['time'])
    lfp = lc.combining(ex_lfp, in_lfp)
    # The Furiertransform Part
    lfp_fft, time_domain = lc.manualFFT(lfp, time, 'one')
    first_fft_peak = find_peaks(lfp_fft)[0]
    lfp_inverse = lc.filtering(lfp, time, 150)
    lfp_filtered_fft, time_domain1 = lc.manualFFT(lfp_filtered, time, 'two')
    # Excitatory Furiertransform Filtering
    ex_lfp_fft, ex_time_domain = lc.manualFFT(ex_lfp, time, 'one')
    ex_first_fft_peak = find_peaks(ex_lfp_fft)[0]
    ex_lfp_inverse = lc.filtering(ex_lfp, time, 150)
    ex_lfp_filtered_fft, time_domain1 = lc.manualFFT(ex_lfp_inverse, time, 'two')
    # Inhibitory Furiertransform Filtering
    in_lfp_fft, in_time_domain = lc.manualFFT(in_lfp, time, 'one')
    in_first_fft_peak = find_peaks(in_lfp_fft)[0]
    in_lfp_inverse = lc.filtering(in_lfp, time, 150)
    in_lfp_filtered_fft, time_domain1 = lc.manualFFT(in_lfp_inverse, time, 'two')
    # The Plotting Part
    '''
    plt.figure(figsize=(20,17))
    plt.subplot(411)
    plt.plot(time[1000:2000],lfp[1000:2000],label='LFP',color=u'#86232F');
    plt.ylabel('mV')
    #plt.grid(alpha=1,color='w',linestyle='--')
    plt.legend(loc=1)
    plt.subplot(412)
    plt.plot(time_domain[1:],lfp_fft[1:], label='LFP frequency',color=u'#86232F')
    plt.legend(loc=1)
    plt.ylabel('Amplitude')
    plt.xlim(0,300)
    plt.subplot(413)
    plt.plot(time[1000:2000],lfp_inverse[1000:2000],label='LFP filtered',color=u'#949494');
    plt.legend(loc=1)
    plt.subplot(414)
    plt.plot(time_domain1[1:],lfp_filtered_fft[1:], label='LFP filtered frequency',color=u'#949494')
    plt.legend(loc=1)
    plt.xlim(0,300)
    plt.xlabel('Frequency')
    plt.ylabel('Amplitude')
    '''
    # Saving Plot Part
    '''
    corrsAddress = date + '/lfp_fft_filtering'
    if (os.path.isdir(corrsAddress)):
        pass
    else:
        os.makedirs(corrsAddress)
    plt.savefig('{}/lfp_{}.pdf'.format(corrsAddress,j))
    '''
    # Saving Plot Part
    saveAdress = date + '/fft_filtered'
    if (os.path.isdir(saveAdress)):
        pass
    else:
        os.makedirs(saveAdress)
    with open('{}/lfp_{}.csv'.format(saveAdress,j), 'w') as file:
        writer = csv.writer(file)
        for i in range(len(time)):
            if (i == 0):
                writer.writerow(('time','ex_lfp','in_lfp', 'LFP'))
            else:
                writer.writerow((time[i],ex_lfp_filtered_fft[i],in_lfp_filtered_fft[i],lfp_filtered_fft[i]))
