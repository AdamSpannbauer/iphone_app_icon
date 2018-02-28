import cv2
import glob
import argparse
import utils
import utils.colorutils
import numpy as np
from sklearn.cluster import KMeans
import random

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='icons',
	help="path to the input dataset directory")
ap.add_argument("-o", "--output", default='cluster_results',
	help="path to the output directory")
ap.add_argument("-k", "--clusters", type=int, default=5,
	help="# of clusters to generate")
ap.add_argument("-c", "--colorSpace", default='bgr',
	help="color space to use (bgr, hsv, or lab); defaults to bgr")
ap.add_argument("-s", "--randomseed", type=int, default=42,
	help="random seed to set for repro results")
args = vars(ap.parse_args())

random.seed(args['randomseed'])

# initialize the image descriptor along with the image matrix
desc = utils.colorutils.color_histogram([8, 8, 8], color_space = args['colorSpace'])
data = []

# grab the image paths from the dataset directory
image_paths = glob.glob('{}/*.jpg'.format(args['dataset']))
image_paths = np.array(sorted(image_paths))

# loop over the input dataset of images
for image_path in image_paths:
	# load the image, describe the image, then update the list of data
	image = cv2.imread(image_path)
	hist = desc.describe(image)
	data.append(hist)

# cluster the color histograms
clt = KMeans(n_clusters=args['clusters'])
labels = clt.fit_predict(data)

# loop over the unique labels
for label in np.unique(labels):
	# grab all image paths that are assigned to the current label
	label_paths = image_paths[np.where(labels == label)]

	sorted_montage = utils.create_sorted_color_montage(
		label_paths, 
		tile_size = (100,100),  
		images_per_main_axis = 5, 
		by_row = False, 
		color_processing_size = (25,25),
		verbose=False
		)

	cv2.imwrite('{}/cluster_{}.jpg'.format(args['output'], label), sorted_montage)
	cv2.imshow('cluster {}'.format(label), sorted_montage)
	# wait for a keypress and then close all open windows
	cv2.waitKey(0)
	cv2.destroyAllWindows()
