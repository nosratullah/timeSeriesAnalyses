import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft

def sinCreator(time):
    timeRange = np.arange(0,time)
    randA = np.random.randint(1,10)
    randF = np.random.randint(10,100)
    sin = np.sin(randF*timeRange) * randA
    return sin, randF, randA

def dotProduct(a,b):
    dot = 0
    if (len(a) == len(b)):
        for i in range(len(a)):
            dot += a[i] * b[i]
    elif (len(a) > len(b)):
        for i in range(len(b)):
            dot += a[i] * b[i]
    elif (len(b) > len(a)):
        for i in range(len(a)):
            dot += a[i] * b[i]

    return dot

def dot_array(a,b):
    
    if (len(a) == len(b)):
        dot_array = np.zeros(len(a))
        for i in range(len(a)):
            dot_array[i] = a[i] * b[i]
    elif (len(a) > len(b)):
        dot_array = np.zeros(len(a))
        for i in range(len(b)):
            dot_array[i] = a[i] * b[i]
    elif (len(b) > len(a)):
        dot_array = np.zeros(len(b))
        for i in range(len(a)):
            dot_array[i] = a[i] * b[i]

    return dot_array

def automatFFT(signal):
    N = len(signal)
    # sample spacing
    T = 1.0/800.0
    signal_fft = fft(signal)
    time_domain = np.linspace(0.0, 1.0/(2*T), N//2)
    signal_fft = 2.0/N * np.abs(signal_fft[0:N//2])
    return signal_fft,time_domain

def furiertransform(signal):
    timesteps = np.arange(0,len(signal))
    Frequency = np.arange(0,50,1)
    #kernel = sin = np.sin(randF*timeRange) * randA
    furiertransform = np.zeros(len(Frequency))
    for i in Frequency:
        kernel = np.sin(i*timesteps)
        furiertransform[i] = np.mean(dotProduct(signal,kernel))
    return furiertransform

def DFT(x):
    """
    Compute the discrete Fourier Transform of the 1D array x
    :param x: (array)
    """

    N = x.size
    n = np.arange(N)
    k = n.reshape((N, 1))
    e = np.exp(-2j * np.pi * k * n / N)
    return np.dot(e, x), n

def manualFFT(signal, time):
    N = signal.size
    # sampling rate
    T = time[1] - time[0]
    time_domain = np.linspace(0, 1 / (2*T), N//2)
    fft = np.fft.fft(signal)
    fft = 1.0/N * np.abs(fft[0:N//2])
    return fft#, time_domain

def fft_filter(fft_signal, mode='blackman'):
    length = len(fft_signal)
    if (mode == 'blackman'):
        kernel = scipy.signal.blackman(length/20)
    filterSamelength = np.zeros(length)
    filterSamelength[0:len(kernel)] = kernel
    fft_filter = dot_array(fft_signal,filterSamelength)
    return fft_filter

signal = np.zeros(600)
sin1, f1, a1 = sinCreator(len(signal))
sin2, f2, a2 = sinCreator(len(signal))
sin3, f3, a3 = sinCreator(len(signal))
sin4, f4, a4 = sinCreator(len(signal))
noise = np.random.normal(0,1,len(signal))
signal = sin1 + sin2 + sin3 + sin4 + noise

furier = manualFFT(signal, t)
#signal_fft, time_domain = automatFFT(signal)

plt.figure(figsize=(15,8))
plt.subplot(2,1,1)
plt.plot(signal, alpha=0.9, label='Signal')
plt.plot(sin1, alpha=0.6, label='Frequency {} - Amplitude {}'.format(f1,a1))
plt.plot(sin2, alpha=0.6, label='Frequency {} - Amplitude {}'.format(f2,a2))
plt.plot(sin3, alpha=0.6, label='Frequency {} - Amplitude {}'.format(f3,a3))
plt.plot(sin4, alpha=0.6, label='Frequency {} - Amplitude {}'.format(f4,a4))
plt.legend(loc='upper right')
plt.subplot(2,1,2)
plt.plot(furier,label='furiertransform')
#plt.plot(time_domain, signal_fft)
plt.plot();
