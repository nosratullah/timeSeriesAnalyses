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
ex_fft, time_domain = lc.manualFFT(ex_lfp,time)
in_fft, time_domain = lc.manualFFT(in_lfp,time)
# The Plotting Part

fig = make_subplots(rows=2, cols=2, shared_xaxes=True)
fig.add_trace(go.Scatter(x=times, y=ex_lfp,
                    mode='lines',
                    name='excitatory lfp'),
             row=1, col=1)
fig.add_trace(go.Scatter(x=time_domain, y=ex_fft,
                    mode='lines',
                    name='excitatory lfp'),
             row=2, col=1)
fig.add_trace(go.Scatter(x=times, y=in_lfp,
                    mode='lines',
                    name='inhibitory lfp'),
             row=1, col=2)
fig.add_trace(go.Scatter(x=time_domain, y=in_fft,
                    mode='lines',
                    name='inhibitory lfp'),
             row=2, col=2)

#fig.add_trace(go.Scatter(x=random_x, y=random_y2,
#                   mode='markers', name='markers'))

#fig.show()
