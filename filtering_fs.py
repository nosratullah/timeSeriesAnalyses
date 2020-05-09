import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from scipy.fftpack import fft,ifft
#fig = go.Figure()
def gaussian(x, mu, sig):
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig,2.)))

domain = np.linspace(0, 100, 1000)
sinwave = np.sin(domain*10) + np.random.normal(0, 1, domain.size)
#plt.plot(domain,sinwave)
N = sinwave.size
T = 0.1
time_domain =np.linspace(0, 1/ (2*T), int(N/2)-1)
fft = fft(sinwave)
fft = fft[1:N//2].real
fft = 1/N * np.abs(fft)
plt.plot(time_domain,fft)
