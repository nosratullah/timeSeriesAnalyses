import numpy as np
#import matplotlib.pyplot as plt
import pylab as plt
from scipy.signal import hilbert,find_peaks,correlate
from statsmodels.tsa.stattools import acf,ccf
from time import gmtime as gmt
import os
import seaborn as sns
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import pandas as pd
import libraries as lc

#date = str('{}/{}/{}/{}'.format(gmt()[0],gmt()[1],gmt()[2],int(gmt()[3]+3.5)))

#checking whether a directory exist or not:
colorPallete = [u'#86232F',u'#50151C',u'#7C7C7C',u'#7F222E',u'#7C7C7C']
fileList = [0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
plt.figure(figsize=(20,10))
sns.set_style("dark")

date = '2020/1/20/21/'
firstValueCorr = np.zeros(len(fileList))
firstValueCorr_rev = np.zeros(len(fileList))
secondValueCorr = np.zeros(len(fileList))
secondValueCorr_rev = np.zeros(len(fileList))
xlim = np.linspace(-0.3, +0.5, 9)
counter = 0
threshold = 0.613
for j in fileList:
    data = pd.read_csv('{}/lfp_{}.csv'.format(date,j))
    ex_lfp = np.array(data['ex_lfp'])
    time = np.array(data['time'])
    ex_lfp = lc.smooth(ex_lfp,5)
    #in_lfp = lc.smooth(in_lfp)
    periods_data = lc.time_diffrences(ex_lfp)
    amplitude_data = lc.amps_detection(ex_lfp)
    crossCorrelation = ccf(amplitude_data,periods_data,unbiased=False)
    crossCorrelation_rev = ccf(periods_data,amplitude_data,unbiased=False)
    shuffling1 = lc.shuff_corr(amplitude_data,periods_data)
    shuffling2 = lc.shuff_corr(amplitude_data,periods_data)

    # Extracting First Correlation Term
    firstValueCorr[counter] = crossCorrelation[0]
    firstValueCorr_rev[counter] = crossCorrelation_rev[0]
    secondValueCorr[counter] = crossCorrelation[1]
    secondValueCorr_rev[counter] = crossCorrelation_rev[1]
    counter += 1

    # Ploting Part
    plt.subplot(1,2,1)
    plt.plot(crossCorrelation_rev[:20],'.-',label='PAC {} '.format(round(j - 0.5,2)),
    alpha=(1 if (crossCorrelation[0] >= threshold) else 0.1),color=np.random.choice(colorPallete))
    plt.fill_between(range(0,20),y1=shuffling1[:20],alpha=0.1,color=u'#86232F')
    plt.fill_between(range(0,20),y1=shuffling2[:20],alpha=0.05,color=u'#86232F')
    plt.text(0,crossCorrelation[0],'{}'.format(round(crossCorrelation[0],3)),
    alpha=(1 if (crossCorrelation[0] >= threshold) else 0))
    plt.ylim(-0.2,1)
    plt.title('Period-Amplitude Correlation')
    plt.xlabel('Steps')
    plt.ylabel('Correlation')
    plt.legend(loc='best')
    plt.grid(alpha=1,color='w',linestyle='--')
    if (j == fileList[-1]):
        ax = inset_axes(plt.gca(),width='45%',height='30%',loc='upper center')
        ax.grid(alpha=1,color='w',linestyle='--')
        #ax.set_ylim(0.2,0.7)
        #ax.set_xlim(-0.3,+0.5)
        ax.plot(xlim,firstValueCorr_rev,'.-',color=u'#86232F',label='1st')
        #ax.plot(xlim,secondValueCorr_rev,'.-',color=u'#7C7C7C',label='2nd')
        ax.legend(loc=2)

    # Plotting First Correlation Term
    plt.subplot(1,2,2)
    plt.plot(crossCorrelation[:20],'.-',label='APC {} '.format(round(j - 0.5,2)),
    alpha=(1 if (crossCorrelation[0] >= threshold) else 0.1),color=np.random.choice(colorPallete))
    plt.fill_between(range(0,20),y1=shuffling1[:20],alpha=0.05,color=u'#86232F')
    plt.fill_between(range(0,20),y1=shuffling2[:20],alpha=0.1,color=u'#86232F')
    plt.text(0,crossCorrelation[0],'{}'.format(round(crossCorrelation[0],3)),
    alpha=(1 if (crossCorrelation[0] >= threshold) else 0))
    plt.ylim(-0.2,1)
    plt.title('Amplitude-Period Correlation')
    plt.xlabel('Steps')
    plt.ylabel('Correlation')
    plt.legend(loc='best')
    plt.grid(alpha=1,color='w',linestyle='--')
    if (j == fileList[-1]):
        ax = inset_axes(plt.gca(),width='45%',height='30%',loc='upper center')
        ax.grid(alpha=1,color='w',linestyle='--')
        #ax.set_xlim(-0.3,+0.5)
        ax.plot(xlim,firstValueCorr,'.-',color=u'#86232F',label='1st')
        #ax.plot(xlim,secondValueCorr,'.-',color=u'#7C7C7C',label='2nd')
        ax.legend(loc=2)


corrsAddress = date + '/correlations_smooth'
if (os.path.isdir(corrsAddress)):
    pass
else:
    os.makedirs(corrsAddress)
plt.savefig('{}/crossCorr_shuffs.pdf'.format(corrsAddress))
