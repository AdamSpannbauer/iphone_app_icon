import re
import requests
from bs4 import BeautifulSoup
from urllib import urlretrieve

#set up urls of interest
base_url = 'https://www.apple.com'
chart_base_url = base_url + '/itunes/charts/'
#top 100 chart url exts
charts = ['top-grossing-apps','paid-apps','free-apps']

#iterate over chart names
for chart in charts:
	print('gathering icons for {}'.format(chart))
	#build url of interest
	url = chart_base_url + chart

	#scrape html
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html5lib")

	#find all img tags (these are the app icons in the charts top 100)
	imgs = soup.find_all('img')
	#create dictionary of img titles : src
	img_dict = {img.get('alt'): img.get('src') for img in imgs}

	#iterate over img dict
	counter = 0
	for title, src in img_dict.items():
		counter += 1
		print('\tdownloading {} icon {} of {}'.format(chart, counter, len(img_dict)))
		#remove non alpha numeric chars for file name
		clean_title = re.sub('[^0-9a-zA-Z]+', '_', title.lower())
		#create img resource url
		full_img_src = base_url + src
		#download app icon
		urlretrieve(full_img_src, 'icons/{}_{}.jpg'.format(chart, clean_title))
