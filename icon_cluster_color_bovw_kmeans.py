import h5py
import cv2
import argparse
import utils
import numpy as np
from sklearn.cluster import KMeans, AgglomerativeClustering

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--useColorFeatures", default=1, type=int,
	help="use color features in clustering? (0 if no)")
ap.add_argument("-b", "--useBovwFeatures", default=1, type=int,
	help="use bag of words features in clustering? (0 if no)")
ap.add_argument("-f", "--features_db", default='features_output/features.hdf5',
	help="path to the input dataset directory")
ap.add_argument("-v", "--bovw_db", default='features_output/bovw.hdf5',
	help="path to the input dataset directory")
ap.add_argument("-o", "--output", default='cluster_results',
	help="path to the output directory")
ap.add_argument("-k", "--clusters", type=int, default=10,
	help="# of clusters to generate")
ap.add_argument("-s", "--colorSpace", default='bgr',
	help="color space to use for generating historgram features (bgr, hsv, or lab)")
args = vars(ap.parse_args())

featuresDB = h5py.File(args["features_db"])
image_paths = featuresDB['image_ids'][:]


if args['useColorFeatures'] != 0:
	# initialize the image descriptor along with the image matrix
	desc = utils.colorutils.color_histogram([8, 8, 8], color_space = args['colorSpace'])

	color_data = []
	# loop over the input dataset of images
	for image_path in image_paths:
		# load the image, describe the image, then update the list of data
		image = cv2.imread(image_path)
		hist = desc.describe(image)
		color_data.append(hist)

	data = color_data

if args['useBovwFeatures'] != 0:
	bovwDB = h5py.File(args["bovw_db"])
	bovw_data = bovwDB['bovw'][:]
	
	if args['useColorFeatures'] != 0:
		data = np.hstack((color_data, bovw_data))
	else:
		data = bovw_data

# cluster the color histograms
clt = KMeans(n_clusters=args['clusters'], random_state=9)
labels = clt.fit_predict(data)

# loop over the unique labels
for label in np.unique(labels):
	# grab all image paths that are assigned to the current label
	label_paths = image_paths[np.where(labels == label)]

	sorted_montage = utils.create_sorted_color_montage(
		label_paths, 
		tile_size = (100,100),  
		images_per_main_axis = 4, 
		by_row = False, 
		color_processing_size = (25,25),
		verbose=False
		)

	cv2.imwrite('{}/cluster_{}.jpg'.format(args['output'], label), sorted_montage)
	# cv2.imshow('cluster {}'.format(label), sorted_montage)
	# wait for a keypress and then close all open windows
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

