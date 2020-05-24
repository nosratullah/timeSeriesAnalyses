import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.stats import stats

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

def convolution(signal,kernel):
    if (kernel == 'triangle'):
        kernel = [0,1,2,3,4,5,4,3,2,1,0]
    if (kernel == 'line'):
        kernel = np.linspace(0,5,len(signal)/100)
    if (kernel == 'exp'):
        kernel = np.exp(np.linspace(0,10,len(signal)/100))
    convolution = np.zeros(len(signal))
    sameSizeKernel = np.zeros(len(signal))
    for i in range(len(convolution)):
        if ((len(kernel)+i) <= len(convolution)):
            sameSizeKernel[i:len(kernel)+i] = kernel
            convolution[i+int(len(kernel)/2)] = dotProduct(signal,sameSizeKernel)/np.sum(kernel)
        else:
            kernel = kernel[:len(kernel)-1]
            sameSizeKernel[i:len(kernel)+i] = kernel
            convolution[i+int(len(kernel)/2)] = dotProduct(signal,sameSizeKernel)/np.sum(kernel)
    return convolution


t = np.linspace(0,100, 1000)
#triangle = signal.sawtooth(2 * np.pi * 5 * t, 0.5)
signal = np.sin(2*t)
conv_ = convolution(signal,kernel='exp')

mu = 0
variance = 1
sigma = np.sqrt(variance)
#gussian = stats.norm.pdf(x, mu, sigma)

plt.figure(figsize=(15,8))
#plt.subplot()
plt.plot(signal, label='signal')
plt.plot(conv_, label='convolution')
plt.xlim(0,len(signal)/10)
plt.legend(loc=1)
#plt.savefig('convolution.pdf')
