import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from libraries import manualFFT
date = 'data'

data = pd.read_csv('data/lfp.csv')
ex_lfp = np.array(data['ex_lfp'][100:])
in_lfp = np.array(data['in_lfp'][100:])
times = np.array(data['time'][100:])
#ex_lfp = lc.smooth(ex_lfp,5)
#in_lfp = lc.smooth(in_lfp,5)
# The Furiertransform Part
ex_fft, time_domain = manualFFT(ex_lfp)
in_fft, time_domain = manualFFT(in_lfp)
ex_fft = ex_fft[:int(len(ex_fft)/2)]
in_fft = in_fft[:int(len(in_fft)/2)]
time_domain = time_domain[:int(len(time_domain)/2)]

# The Plotting Part
fig = make_subplots(rows=2, cols=2, shared_xaxes=True,
                    subplot_titles=("excitatory lfp", "excitatory fft", "inhibitory lfp", "inhibitory fft"))
fig.add_trace(go.Scatter(x=times, y=ex_lfp,
                    mode='lines',
                    name='excitatory lfp'),
             row=1, col=1)
fig.add_trace(go.Scatter(x=time_domain, y=ex_fft,
                    mode='lines',
                    name='excitatory fft'),
             row=1, col=2)
fig.add_trace(go.Scatter(x=times, y=in_lfp,
                    mode='lines',
                    name='inhibitory lfp'),
             row=2, col=1)
fig.add_trace(go.Scatter(x=time_domain, y=in_fft,
                    mode='lines',
                    name='inhibitory fft'),
             row=2, col=2)

fig.update_yaxes(title_text="Voltage (mV)", row=1, col=1)
fig.update_yaxes(title_text="Intensity", row=1, col=2)
fig.update_yaxes(title_text="Voltage (mV)", row=2, col=1)
fig.update_yaxes(title_text="Intensity", row=2, col=2)

fig.show()
