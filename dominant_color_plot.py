import random

import numpy as np
import cv2

from plotly.offline import plot
import plotly.graph_objs as go

from utils.colorutils import get_dominant_color


# reproducible
random.seed(1337)

# apps to plot
apps_of_interest = {'Facebook': 'free-apps_facebook.jpg',
                    'WhatsApp': 'free-apps_whatsapp_messenger.jpg',
                    'Waze': 'free-apps_waze_navigation_live_traffic.jpg',
                    'Soundcloud': 'free-apps_soundcloud_music_audio.jpg'}


# function to gen random walk for fake app data
def gen_random_walk(start=100, n_steps=50, num_range=(-100, 100),
                    new_step_chance=0.5):
    """
    inputs:
        start - start value for walk
        n_steps - number of steps to take from starting point
        num_range - range of values to sample for steps
        new_step_chance - probability of taking step different
                          from last step (ie if 0 then all steps will be
                          same value)
    output: list of values in walk
    """
    # init start point for walk
    walk = [start]
    # gen a default step
    step_val = random.randrange(num_range[0], num_range[1])
    for i in range(n_steps):
        # chance to take a new step or take last step again
        if random.random() > (1 - new_step_chance):
            # update step value
            step_val = random.randrange(num_range[0], num_range[1])
        # add step to last position
        new_pos = walk[i - 1] + step_val
        # append new position to walk history
        walk.append(new_pos)

    return walk


# init plotly trace storage
plot_traces = []
# xaxis data
plot_x = range(1, 101)
plot_images = []
# iterate over app
for name, path in apps_of_interest.items():
    # gen data
    app_data = gen_random_walk(
        start=random.randrange(1000, 2000),
        n_steps=len(plot_x) - 1,
        new_step_chance=0.3)
    # read in image
    bgr_image = cv2.imread('icons/{}'.format(path))
    # convert to HSV; this is a better representation of how we see color
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
    # get dominant color in app icon
    hsv = get_dominant_color(hsv_image, k=5)
    # make into array for color conversion with cv2
    hsv_im = np.array(hsv, dtype='uint8').reshape(1, 1, 3)

    # convert color to rgb for plotly
    rgb = cv2.cvtColor(hsv_im, cv2.COLOR_HSV2RGB).reshape(3).tolist()
    # make string for plotly
    rgb = [str(c) for c in rgb]
    # create plotly trace of line
    trace = go.Scatter(
        x=list(plot_x),
        y=app_data,
        mode='lines',
        name=name,
        line={
            'color': ('rgb({})'.format(', '.join(rgb))),
            'width': 3
        }
    )
    # base url to include images in plotly plot
    image_url = 'https://raw.githubusercontent.com/AdamSpannbauer/iphone_app_icon/master/icons/{}'
    # create plotly image dict
    plot_image = dict(
        source=image_url.format(path),
        xref='x',
        yref='y',
        x=plot_x[-1],
        y=app_data[-1],
        xanchor='left',
        yanchor='middle',
        sizex=5.5,
        sizey=250,
        sizing='stretch',
        layer='above'
    )
    # append trace to plot data
    plot_traces.append(trace)
    plot_images.append(plot_image)

# drop legend, add images to plot,
# remove tick marks, increase x axis range to not cut off images
layout = go.Layout(
    showlegend=False,
    images=plot_images,
    xaxis=dict(
        showticklabels=False,
        ticks='',
        range=[min(plot_x), max(plot_x) + 10]
    ),
    yaxis=dict(
        showticklabels=False,
        ticks=''
    )
)

# create plot figure
fig = go.Figure(data=plot_traces, layout=layout)

# produce plot output
plot(fig, config={'displayModeBar': False},
     filename='readme/app_plot.html')
