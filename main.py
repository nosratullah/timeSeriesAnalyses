import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert,find_peaks,correlate
from time import gmtime as gmt
import os
import seaborn as sns
import pandas as pd
import timeSeriesAnalysis as lc
from statsmodels.tsa.stattools import acf,ccf
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import csv

def crossCorrelation(date, fileList, ex_tauSyn):
    #checking whether a directory exist or not:
    colorPallete = [u'#86232F',u'#50151C',u'#7C7C7C',u'#7F222E',u'#7C7C7C']
    plt.figure(figsize=(20,10))
    sns.set_style("dark")
    firstValueCorr = np.zeros(len(fileList))
    firstValueCorr_rev = np.zeros(len(fileList))
    secondValueCorr = np.zeros(len(fileList))
    secondValueCorr_rev = np.zeros(len(fileList))
    xlim = np.linspace((fileList[0] - ex_tauSyn), (fileList[-1] - ex_tauSyn), len(fileList))
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


    corrsAddress = date + '/correlations'
    if (os.path.isdir(corrsAddress)):
        pass
    else:
        os.makedirs(corrsAddress)
    plt.savefig('{}/crossCorr_shuffs.pdf'.format(corrsAddress))
    plt.close()

def histogram(date, fileList):
    sns.set_style("dark")
    for j in fileList:
        data = pd.read_csv('{}/lfp_{}.csv'.format(date,j))
        ex_lfp = np.array(data['ex_lfp'])
        time = np.array(data['time'])
        ex_lfp = lc.smooth(ex_lfp,5)
        periods_data = lc.time_diffrences(ex_lfp)
        amplitude_data = lc.amps_detection(ex_lfp)
        plt.figure(figsize=(15,10))
        plt.subplot(224)
        plt.hist(periods_data,20,label='Periods',color=u'#86232F');
        plt.xlabel('ms')
        #plt.grid(alpha=1,color='w',linestyle='--')
        plt.legend(loc=1)
        plt.subplot(222)
        plt.hist(amplitude_data,20,label='Amplitudes',color=u'#86232F');
        plt.xlabel('mV')
        plt.legend(loc=1)
        #plt.grid(alpha=1,color='w',linestyle='--')
        #plt.plot(periods_data,amplitude_data,'.')
        plt.subplot(121)
        plt.hist2d(amplitude_data,periods_data,20,cmap='Greys');
        plt.grid(alpha=0.5,color='b',linestyle='--')
        plt.ylabel('IEI')
        plt.xlabel('Amplitudes')
        plt.title('{} time diffrences'.format(round(j - 0.5,2)))

        corrsAddress = date + '/histogram'
        if (os.path.isdir(corrsAddress)):
            pass
        else:
            os.makedirs(corrsAddress)
        plt.savefig('{}/histogram_{}.png'.format(corrsAddress,j))
        plt.close()

def smoothing(date, fileList):
    sns.set_style('darkgrid')
    for j in fileList:
        # Data Importing
        data = pd.read_csv('{}/lfp_{}.csv'.format(date,j))
        ex_lfp = np.array(data['ex_lfp'])
        in_lfp = np.array(data['in_lfp'])
        time = np.array(data['time'])
        lfp = lc.combining(ex_lfp, in_lfp)
        # The Furiertransform Part
        lfp_fft, time_domain = lc.manualFFT(lfp, time, 'one')
        lfp_filtered = lc.filtering(lfp, time, 300)
        lfp_filtered_fft, time_domain1 = lc.manualFFT(lfp_filtered, time, 'two')

        # The Plotting Part
        plt.figure(figsize=(20,17))
        plt.subplot(411)
        plt.plot(time[1000:2000],lfp[1000:2000],label='LFP',color=u'#86232F');
        plt.ylabel('mV')
        plt.legend(loc=1)
        plt.subplot(412)
        plt.plot(time_domain[1:],lfp_fft[1:], label='LFP frequency',color=u'#86232F')
        plt.legend(loc=1)
        plt.ylabel('Amplitude')
        plt.xlim(0,300)
        plt.subplot(413)
        plt.plot(time[1000:2000],lfp_filtered[1000:2000],label='LFP filtered',color=u'#949494');
        plt.legend(loc=1)
        plt.subplot(414)
        plt.plot(time_domain1[1:],lfp_filtered_fft[1:], label='LFP filtered frequency',color=u'#949494')
        plt.legend(loc=1)
        plt.xlim(0,300)
        plt.xlabel('Frequency')
        plt.ylabel('Amplitude')

        # Saving Part
        corrsAddress = date + '/lfp_fft_filtering'
        if (os.path.isdir(corrsAddress)):
            pass
        else:
            os.makedirs(corrsAddress)
        plt.savefig('{}/lfp_{}.pdf'.format(corrsAddress,j))
        plt.close()

def data_csv_filtered(date, fileList):
    sns.set_style('darkgrid')
    for j in fileList:
        # Data Importing
        data = pd.read_csv('{}/lfp_{}.csv'.format(date,j))
        ex_lfp = np.array(data['ex_lfp'])
        in_lfp = np.array(data['in_lfp'])
        time = np.array(data['time'])
        lfp = lc.combining(ex_lfp, in_lfp)
        # The Furiertransform Part
        lfp_fft, time_domain = lc.manualFFT(lfp, 'two')
        lfp_inverse = lc.filtering(lfp, 300)
        lfp_filtered_fft, lfp_time_domain = lc.manualFFT(lfp_inverse, 'two')
        # Excitatory Furiertransform Filtering

        ex_lfp_fft, ex_time_domain = lc.manualFFT(ex_lfp, 'two')
        ex_lfp_inverse = lc.filtering(ex_lfp, 300)
        ex_lfp_filtered_fft, ex_time_domain1 = lc.manualFFT(ex_lfp_inverse, 'two')
        # Inhibitory Furiertransform Filtering
        in_lfp_fft, in_time_domain = lc.manualFFT(in_lfp, 'two')
        in_lfp_inverse = lc.filtering(in_lfp, 300)
        in_lfp_filtered_fft, in_time_domain1 = lc.manualFFT(in_lfp_inverse, 'two')
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
        #ex_lfp_inverse = np.array(ex_lfp_inverse)
        #in_lfp_inverse = np.array(in_lfp_inverse)
        #lfp_inverse = np.array(lfp_inverse)
        #print(np.shape(time), np.shape(ex_lfp_inverse), np.shape(in_lfp_inverse), np.shape(lfp_inverse))
        saveAdress = date + '/fft_filtered'
        if (os.path.isdir(saveAdress)):
            pass
        else:
            os.makedirs(saveAdress)
        with open('{}/lfp_{}.csv'.format(saveAdress,j), 'w') as file:
            writer = csv.writer(file)
            for i in range(len(lfp_inverse)):
                if (i == 0):
                    writer.writerow(('time','ex_lfp','in_lfp', 'LFP'))
                else:
                    writer.writerow((time[i],ex_lfp_inverse[i],in_lfp_inverse[i],lfp_inverse[i]))

def amplitude_acf(date, fileList, ex_tauSyn):

    colorPallete = [u'#86232F',u'#50151C',u'#7C7C7C',u'#7F222E',u'#7C7C7C']
    plt.figure(figsize=(20,10))
    sns.set_style("dark")
    firstValueCorr = np.zeros(len(fileList))
    firstValueCorr_rev = np.zeros(len(fileList))
    secondValueCorr = np.zeros(len(fileList))
    secondValueCorr_rev = np.zeros(len(fileList))
    xlim = np.linspace((fileList[0] - ex_tauSyn), (fileList[-1] - ex_tauSyn), len(fileList))
    counter = 0
    threshold = 0.8
    for j in fileList:
        data = pd.read_csv('{}/lfp_{}.csv'.format(date,j))
        ex_lfp = np.array(data['ex_lfp'])
        time = np.array(data['time'])
        ex_lfp = lc.smooth(ex_lfp,5)
        amplitude_data = lc.amps_detection(ex_lfp)
        autocorrolation = acf(amplitude_data,fft=True)
        shuffling1 = lc.shuff_acf(amplitude_data)
        shuffling2 = lc.shuff_acf(amplitude_data)

        # Extracting First Correlation Term
        firstValueCorr[counter] = autocorrolation[0]
        secondValueCorr[counter] = autocorrolation[1]
        counter += 1

        # Ploting Part
        plt.plot(autocorrolation[:20],'.-',label='APC {} '.format(round(j - 0.5,2)),
        alpha=(1 if (autocorrolation[1] >= threshold) else 0.1),color=np.random.choice(colorPallete))
        plt.fill_between(range(0,20),y1=shuffling1[1:21],alpha=0.05,color=u'#86232F')
        plt.fill_between(range(0,20),y1=shuffling2[1:21],alpha=0.1,color=u'#86232F')
        plt.text(0,autocorrolation[1],'{}'.format(round(autocorrolation[0],3)),
        alpha=(1 if (autocorrolation[1] >= threshold) else 0))
        #plt.ylim(-0.2,1)
        plt.title('Amplitude-auto Correlation')
        plt.xlabel('Steps')
        plt.ylabel('Correlation')
        plt.legend(loc='best')
        plt.grid(alpha=1,color='w',linestyle='--')
        if (j == fileList[-1]):
            ax = inset_axes(plt.gca(),width='45%',height='30%',loc='upper center')
            ax.grid(alpha=1,color='w',linestyle='--')
            #ax.set_ylim(0.2,0.7)
            ax.plot(xlim,secondValueCorr,'.-',color=u'#86232F',label='1st')
            #ax.plot(xlim,secondValueCorr,'.-',color=u'#7C7C7C',label='2nd')
            ax.legend(loc=2)


    corrsAddress = date + '/correlations'
    if (os.path.isdir(corrsAddress)):
        pass
    else:
        os.makedirs(corrsAddress)
    plt.savefig('{}/amplitude_acf.pdf'.format(corrsAddress))
    plt.close()

def periods_acf(date, fileList, ex_tauSyn):
    firstValueCorr = np.zeros(len(fileList))
    firstValueCorr_rev = np.zeros(len(fileList))
    secondValueCorr = np.zeros(len(fileList))
    secondValueCorr_rev = np.zeros(len(fileList))
    xlim = np.linspace((fileList[0] - ex_tauSyn), (fileList[-1] - ex_tauSyn), len(fileList))
    plt.figure(figsize=(25,12))
    for j in fileList:
        data = pd.read_csv('{}/lfp_ex_{}.csv'.format(date,j/10))
        ex_data = np.array(data['ex_lfp'])
        in_data = np.array(data['in_lfp'])
        time = np.array(data['time'])
        ex_diffs = lc.time_diffrences(ex_data, time)
        in_diffs = lc.time_diffrences(in_data, time)
        ex_periods_correlation = acf(ex_diffs,fft=True)
        in_periods_correlation = acf(in_diffs,fft=True)
        np.random.shuffle(ex_diffs)
        np.random.shuffle(in_diffs)
        ex_shuffs = acf(ex_diffs,fft=True)
        in_shuffs = acf(in_diffs,fft=True)
        plt.subplot(1,2,1)
        plt.plot(ex_periods_correlation,'.-',label='ex_periods acf {}'.format(round(j/10 - 2.5,2)),
        alpha = (1 if ex_periods_correlation[1] >= 0.47 else 0.2))
        plt.text(0,ex_periods_correlation[1],'{}'.format(round(ex_periods_correlation[1],3)),
        alpha = (1 if ex_periods_correlation[1] >= 0.47 else 0.2))
        plt.fill_between(range(0,len(ex_shuffs[1:])),y1=ex_shuffs[1:],alpha=0.4)
        plt.title('periods correlation')
        plt.xlabel('steps')
        plt.ylabel('correlation')
        plt.legend(loc='best')
        plt.subplot(1,2,2)
        plt.plot(in_periods_correlation,'.-',label='in_periods acf {}'.format(round(j/10 - 2.5,2)),
        alpha = (1 if in_periods_correlation[1] >= 0.48 else 0.2))
        plt.text(0,in_periods_correlation[1],'{}'.format(round(in_periods_correlation[1],3)),
        alpha = (1 if in_periods_correlation[1] >= 0.48 else 0.2))
        plt.fill_between(range(0,len(in_shuffs[1:])),y1=in_shuffs[1:],alpha=0.4)
        plt.title('periods correlation')
        plt.xlabel('steps')
        plt.ylabel('correlation')
        plt.legend(loc='best')
    corrsAddress = date + '/correlations'
    if (os.path.isdir(corrsAddress)):
        pass
    else:
        os.makedirs(corrsAddress)
    plt.savefig('{}/periods_acf.png'.format(corrsAddress))
    plt.close()

date = '2020/2/3/12/'
filtered_data = date + '/fft_filtered'
fileList = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5 ,4.0]
parameters = pd.read_csv('{}/NetworkParameters_{}.csv'.format(date,fileList[0]))
ex_tauSyn = parameters['ex_tauSyn'][0]

data_csv_filtered(date, fileList)
crossCorrelation(filtered_data, fileList, ex_tauSyn)
smoothing(filtered_data, fileList)
lfpPloting(filtered_data, fileList)
amplitude_acf(filtered_data, fileList, ex_tauSyn)
periods_acf(filtered_data, fileList, ex_tauSyn)
