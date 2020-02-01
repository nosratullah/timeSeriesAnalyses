import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert,find_peaks
from statsmodels.tsa.stattools import acf,ccf
from time import gmtime as gmt
import os

#date = str('{}/{}/{}/{}'.format(gmt()[0],gmt()[1],gmt()[2],int(gmt()[3]+3.5)))


date = '2020/1/20/21/'
plt.figure(figsize=(25,12))
fileList = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
for j in fileList:
    data = pd.read_csv('{}/lfp_{}.csv'.format(date,j))
    ex_data = np.array(data['ex_lfp'])
    in_data = np.array(data['in_lfp'])
    ex_data = lc.smooth(ex_data,5)
    in_data = lc.smooth(in_data,5)
    ex_peak_values = lc.extract_peaks(ex_data)
    in_peak_values = lc.extract_peaks(in_data)
    ex_amps_correlation = acf(ex_peak_values,fft=True)
    in_amps_correlation = acf(in_peak_values,fft=True)
    np.random.shuffle(ex_peak_values)
    np.random.shuffle(in_peak_values)
    ex_amps_shuffs = acf(ex_peak_values,fft=True)
    in_amps_shuffs = acf(in_peak_values,fft=True)
    plt.subplot(1,2,1)
    plt.plot(ex_amps_correlation[:20],'.-',label='excitatory amp acf_{}'.format(j/10),
    alpha = (1 if ex_amps_correlation[1] > 0.4 else 0.2))
    plt.text(0,ex_amps_correlation[1],'{}'.format(round(ex_amps_correlation[1],3)),
    alpha = (1 if ex_amps_correlation[1] > 0.4 else 0.2))
    plt.fill_between(range(0,len(ex_amps_shuffs[1:21])),y1=ex_amps_shuffs[1:21],alpha=0.4,label='shuffled area')
    plt.title('amplitude correlation')
    plt.xlabel('steps')
    plt.ylabel('correlation')
    plt.legend(loc='best')
    plt.subplot(1,2,2)
    plt.plot(in_amps_correlation[1:20],'.-',label='inhibitory amp acf_{}'.format(j/10),
    alpha = (1 if in_amps_correlation[1] > 0.4 else 0.2))
    plt.text(0,in_amps_correlation[1],'{}'.format(round(in_amps_correlation[1],3)),
    alpha = (1 if in_amps_correlation[1] > 0.4 else 0.2))
    plt.fill_between(range(0,len(in_amps_shuffs[1:21])),y1=in_amps_shuffs[1:21],alpha=0.4,label='shuffled area')
    plt.title('amplitude correlation')
    plt.xlabel('steps')
    plt.ylabel('correlation')
    plt.legend(loc='best')

corrsAddress = date + '/correlations'
if (os.path.isdir(corrsAddress)):
    pass
else:
    os.makedirs(corrsAddress)
plt.savefig('{}/amp_acf.png'.format(corrsAddress))
