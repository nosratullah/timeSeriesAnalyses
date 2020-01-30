import numpy as np
import matplotlib.pyplot as plt

def sinCreator(time):
    timeRange = np.arange(0,time,0.01)
    randA = np.random.randint(1,10)
    randF = np.random.randint(10,40)
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

def furiertransform(signal):
    timesteps = np.arange(0,len(signal),0.01)
    Frequency = np.arange(0,50,1)
    #kernel = sin = np.sin(randF*timeRange) * randA
    furiertransform = np.zeros(len(Frequency))
    for i in Frequency:
        kernel = np.sin(i*timesteps)
        furiertransform[i] = np.mean(dotProduct(signal,kernel))
    return furiertransform

signal = np.zeros(100)
sin1, f1, a1 = sinCreator(len(signal))
sin2, f2, a2 = sinCreator(len(signal))
sin3, f3, a3 = sinCreator(len(signal))
sin4, f4, a4 = sinCreator(len(signal))

signal = sin1 + sin2 + sin3 + sin4
furier = furiertransform(signal)

plt.figure(figsize=(15,8))
plt.subplot(2,1,1)
plt.plot(signal, alpha=0.9, label='Signal')
plt.plot(sin1, alpha=0.6, label='Frequency {} - Amplitude {}'.format(f1,a1))
plt.plot(sin2, alpha=0.6, label='Frequency {} - Amplitude {}'.format(f2,a2))
plt.plot(sin3, alpha=0.6, label='Frequency {} - Amplitude {}'.format(f3,a3))
plt.plot(sin4, alpha=0.6, label='Frequency {} - Amplitude {}'.format(f4,a4))
plt.legend(loc='upper right')
plt.xlim(0,1000);
plt.subplot(2,1,2)
plt.plot(furier,label='furiertransform')
plt.show()
