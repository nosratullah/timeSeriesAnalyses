import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

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

def convolution(signal,magnitude=3):
    kernel = np.linspace(0,magnitude,10)
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


t = np.linspace(0, 1, 100)
#triangle = signal.sawtooth(2 * np.pi * 5 * t, 0.5)
triangle = np.zeros(len(t))
triangle[10:20] = 10
conv_ = convolution(triangle,3)

plt.figure(figsize=(15,8))
plt.plot(triangle, label='signal')
plt.plot(conv_, label='convolution')
plt.legend(loc=1)
