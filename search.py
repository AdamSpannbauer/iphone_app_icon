from __future__ import print_function
import argparse
import imutils
import utils
import h5py
import numpy as np
import cv2

def chi2_distance(histA, histB, eps=1e-10):
	"""
	function to compute chi square dist between 2 arrays
	"""
	# compute the chi-squared distance
	d = 0.5 * np.sum(((histA - histB) ** 2) / (histA + histB + eps))

	# return the chi-squared distance
	return d

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", default='icons/free-apps_dune_.jpg', 
	help="Path to the query image")
ap.add_argument("-f", "--featuresPath", default='features_output',
	help="path to the directory housing image features")
ap.add_argument("-n", "--numResults", default=5, type=int,
	help="path to the directory housing image features")
ap.add_argument("-c", "--useColorFeatures", default=1, type=int,
	help="use color features in clustering? (0 if no)")
ap.add_argument("-b", "--useBovwFeatures", default=1, type=int,
	help="use bag of words features in clustering? (0 if no)")
args = vars(ap.parse_args())

#check if user specified to use no features
#raise error if no features specified
if args['useColorFeatures'] == 0 and args['useBovwFeatures'] == 0:
	raise ValueError('--useColorFeatures (-c) or --useBovwFeatures (-b) must be non-zero')

#read in image paths from features hdf5
featuresDB = h5py.File('{}/features.hdf5'.format(args["featuresPath"]))
image_paths = featuresDB['image_ids'][:]

#read in color features if specified to be used
if args['useColorFeatures'] != 0:
	#read csv color features to array	
	color_data = np.genfromtxt('{}/color_hists.csv'.format(args["featuresPath"]), 
		delimiter=',')
	#drop first column (first col is image file path)
	color_data = np.delete(color_data, 0, axis=1)
	
	data = color_data

#read in bovw features if specified to be used
if args['useBovwFeatures'] != 0:
	#read in hdf5 of bovw keypoint features
	bovwDB = h5py.File('{}/bovw.hdf5'.format(args["featuresPath"]))
	bovw_data = bovwDB['bovw'][:]
	
	#hstack with color features if both feature sets being used
	if args['useColorFeatures'] != 0:
		data = np.hstack((color_data, bovw_data))
	else:
		data = bovw_data

#extract query's features from feature data
query_features = data[np.where(image_paths == args['query'])]

#init results dict to store each images chi dist from query
results = {}

# loop over the rows in features
for i, row in enumerate(data):
	#calc dist between image i and query image
	d = chi2_distance(row, query_features)

	# store dist in results dict with image path as key
	results[image_paths[i]] = d

#sort results small to large and take top N
results = sorted([(v, k) for (k, v) in results.items()])[:args["numResults"]]

#init montage to display results
montage = utils.results_montage(
		image_size = (100, 100), 
		images_per_main_axis = 5, 
		num_results = args['numResults'],
		by_row = True)

# loop over the results to add image to montage
for (i, (score, path)) in enumerate(results):
	#read image
	result = cv2.imread(path)
	#add image to montage with dist label
	montage.add_result(result, text="dist: {:.2f}".format(score))

# display query image and results
cv2.imshow("Query", cv2.imread(args['query']))
cv2.imshow("Ordered Results", montage.montage)
cv2.waitKey(0)
