from utils.colorutils import get_dominant_color
from plotly.offline import plot, iplot, init_notebook_mode
import plotly.graph_objs as go
import random
import cv2
import numpy as np

random.seed(1337)

#apps to plot
apps_of_interest = {'Facebook': 'free-apps_facebook.jpg',
					'WhatsApp': 'free-apps_whatsapp_messenger.jpg',
					'Waze': 'free-apps_waze_navigation_live_traffic.jpg',
					'Soundcloud': 'free-apps_soundcloud_music_audio.jpg'}

#function to gen random stats
def gen_random_walk(start=100, n_steps=50, num_range=(-100,100), new_step_chance=0.5):
	walk = [start]
	step_val = random.randrange(num_range[0], num_range[1])
	for i in range(n_steps):
		#chance to take a new step or take last step again
		if random.random() > (1-new_step_chance):
			step_val = random.randrange(num_range[0], num_range[1])
		new_pos = walk[i-1] + step_val

		walk.append(new_pos)
	return walk

#init plotly trace storage
plot_traces = []
#xaxis data
plot_x = range(1,101)
plot_images = []
#iterate over app
for name, path in apps_of_interest.items():
	#gen data
	app_data = gen_random_walk(
		start=random.randrange(1000,2000), 
		n_steps = len(plot_x)-1,
		new_step_chance=0.3)
	#read in image
	bgr_image = cv2.imread('icons/{}'.format(path))
	#convert to HSV; this is a better representation of how we see color
	hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
	#get dominant color in app icon
	hsv = get_dominant_color(hsv_image, k=5)
	#make into array for color conversion with cv2
	hsv_im = np.array(hsv, dtype='uint8').reshape(1,1,3)
	
	#convert color to rgb for plotly
	rgb = cv2.cvtColor(hsv_im, cv2.COLOR_HSV2RGB).reshape(3).tolist()
	#make string for plotly
	rgb = [str(c) for c in rgb]
	#create plotly trace of line
	trace = go.Scatter(
		x = plot_x,
		y = app_data,
		mode = 'lines',
		name = name,
		line = {
		'color': ('rgb({})'.format(', '.join(rgb))),
		'width': 3
		}
		)
	image_url = 'https://raw.githubusercontent.com/AdamSpannbauer/iphone_app_icon/master/icons/{}'
	plot_image = dict(
		source = image_url.format(path),
		xref = 'x',
		yref = 'y',
		x = plot_x[-1],
		y = app_data[-1],
		xanchor='left',
		yanchor = 'middle',
		sizex = 5,
		sizey = 250,
		sizing='stretch',
		layer='above'
		)
	#append trace to plot data
	plot_traces.append(trace)
	plot_images.append(plot_image)

#set plot formating/titles
layout = go.Layout(
		images = plot_images,
		title = "App Trends in Fake Statistic",
		xaxis = dict(
			showticklabels = False,
			ticks = '',
			title = 'Time (probably)',
			range = [min(plot_x), max(plot_x) + 10]
			)
		)

#create plot figure
fig = go.Figure(data=plot_traces, layout=layout)

#produce plot output
plot(fig, config={'displayModeBar': False})




