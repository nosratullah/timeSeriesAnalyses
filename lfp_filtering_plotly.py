import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from libraries import manualFFT, smooth

date = 'data'

data = pd.read_csv('data/lfp.csv')
ex_lfp = np.array(data['ex_lfp'][100:])
in_lfp = np.array(data['in_lfp'][100:])
times = np.array(data['time'][100:])
lfp_tot = (ex_lfp + in_lfp)/2.0
lfp_filter = smooth(lfp_tot,1)
#in_lfp = lc.smooth(in_lfp,5)
# The Furiertransform Part
#ex_fft, time_domain = manualFFT(ex_lfp)
#in_fft, time_domain = manualFFT(in_lfp)
fft_tot, time_domain = manualFFT(lfp_tot)
fft_filter, time_domain = manualFFT(lfp_filter)
#ex_fft = ex_fft[:int(len(ex_fft)/2)]
#in_fft = in_fft[:int(len(in_fft)/2)]
lfp_filter = lfp_filter[:int(len(lfp_filter)/2)]
fft_filter = fft_filter[:int(len(fft_filter)/2)]

time_domain = time_domain[:int(len(time_domain)/2)]

# The Plotting Part
fig = make_subplots(rows=2, cols=2, shared_xaxes=True,
                    subplot_titles=("excitatory lfp", "excitatory fft", "inhibitory lfp", "inhibitory fft"))
fig.add_trace(go.Scatter(x=times, y=lfp_tot,
                    mode='lines',
                    name='excitatory lfp'),
             row=1, col=1)
fig.add_trace(go.Scatter(x=time_domain, y=fft_tot,
                    mode='lines',
                    name='excitatory fft'),
             row=1, col=2)
fig.add_trace(go.Scatter(x=times, y=lfp_filter,
                    mode='lines',
                    name='inhibitory lfp'),
             row=2, col=1)
fig.add_trace(go.Scatter(x=time_domain, y=fft_filter,
                    mode='lines',
                    name='inhibitory fft'),
             row=2, col=2)

fig.update_yaxes(title_text="Voltage (mV)", row=1, col=1)
fig.update_yaxes(title_text="Intensity", row=1, col=2)
fig.update_yaxes(title_text="Voltage (mV)", row=2, col=1)
fig.update_yaxes(title_text="Intensity", row=2, col=2)

fig.show()

'''
# Create figure
fig = go.Figure()

# Add traces, one for each slider step
for step in np.arange(0, 5, 0.1):
    fig.add_trace(
        go.Scatter(
            visible=False,
            line=dict(color="#00CED1", width=6),
            name="𝜈 = " + str(step),
            x=np.arange(0, 10, 0.01),
            y=np.sin(step * np.arange(0, 10, 0.01))))

# Make 10th trace visible
fig.data[10].visible = True

# Create and add slider
steps = []
for i in range(len(fig.data)):
    step = dict(
        method="update",
        args=[{"visible": [False] * len(fig.data)},
              {"title": "Slider switched to step: " + str(i)}],  # layout attribute
    )
    step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
    steps.append(step)

sliders = [dict(
    active=10,
    currentvalue={"prefix": "Frequency: "},
    pad={"t": 50},
    steps=steps
)]

fig.update_layout(
    sliders=sliders
)

fig.show()
'''
