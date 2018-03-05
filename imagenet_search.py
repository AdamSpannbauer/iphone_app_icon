import argparse
import cv2
import utils
import imutils
import numpy as np
import pandas as pd

import keras
from keras.applications.resnet50 import ResNet50
from keras.preprocessing import image as image_utils
from keras.applications.imagenet_utils import preprocess_input

# define image preprocessor for use with imagenet model
def image_preprocessor(image_path):
	image = image_utils.load_img(image_path, target_size=(224, 224))
	image = image_utils.img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = preprocess_input(image)
	return(image)

# function to compute chi square dist
def chi2_distance(histA, histB, eps=1e-10):
	d = 0.5 * np.sum(((histA - histB) ** 2) / (histA + histB + eps))
	return d

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-q", "--query", default='icons/paid-apps_papa_s_burgeria_to_go_.jpg', 
	help="Path to the query image")
ap.add_argument("-f", "--featuresPath", default='features_output/imagenet_features.csv',
	help="path to csv containing imagenet features")
ap.add_argument("-n", "--numResults", default=5, type=int,
	help="number of search results to return")
args = vars(ap.parse_args())

#read in csv feature data
feature_df = pd.read_csv(args["featuresPath"], header=None)

#get image paths from first column of df
image_paths = np.array(feature_df.iloc[:,0])

#convert features to array (drop first column of paths)
feat_data = np.array(feature_df.iloc[:,1:])

#check if query image is in our feature db already
if args['query'] in image_paths:
	#extract query's features from feature data
	query_features = feat_data[np.where(image_paths == args['query'])]
else:
	#load image net weights but dont include classification layer
	model = ResNet50(weights='imagenet', include_top=False)
	#preprocess image
	image = image_preprocessor(args['query'])
	#extract features
	features = model.predict(image)
	#flatten features
	query_features = np.ravel(features)

#init results dict to store each images chi dist from query
results = {}

# loop over the rows in features
for i, row in enumerate(feat_data):
	#calc dist between image i and query image
	d = chi2_distance(row, query_features)
	# store dist in results dict with image path as key
	results[image_paths[i]] = d

#sort results best to worst and take top N
results = sorted([(v, k) for (k, v) in results.items()])[:args["numResults"]]

#init montage to display results
montage = utils.results_montage(image_size = (100, 100), 
				images_per_main_axis = 5, 
				num_results = args['numResults'],
				by_row = True)

# loop over the results to add image to montage
for (i, (score, path)) in enumerate(results):
	#read image
	result = cv2.imread(path)
	#resize image to ensure it fits in output montage
	resized = cv2.resize(result, (100, 100), interpolation = cv2.INTER_AREA)
	#add image to montage with dist label
	montage.add_result(resized, text="dist: {:.2f}".format(score))

# display query image and results
query_image = cv2.imread(args['query'])
# resize query image while keeping aspect ratio
query_resized = imutils.resize(query_image, width = min(300, query_image.shape[1]))
cv2.imshow("Query", query_resized)
cv2.imshow("Ordered Results", montage.montage)
cv2.waitKey(0)
