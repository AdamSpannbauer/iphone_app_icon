#TODO: add sorting by color within color montage
import cv2
import glob
import utils
import argparse
import colorutils
import numpy as np
from sklearn.cluster import KMeans

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='icons',
	help="path to the input dataset directory")
ap.add_argument("-k", "--clusters", type=int, default=5,
	help="# of clusters to generate")
ap.add_argument("-c", "--colorSpace", default='bgr',
	help="color space to use (bgr, hsv, or lab); defaults to bgr")
args = vars(ap.parse_args())

# initialize the image descriptor along with the image matrix
desc = colorutils.color_histogram([8, 8, 8], color_space = args['colorSpace'])
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

	montage = utils.results_montage(image.shape, 7, label_paths.shape[0])

	# loop over the image paths that belong to the current label
	for (i, path) in enumerate(label_paths):
		# load the image and add to montage
		image = cv2.imread(path)
		montage.add_result(image)

	cv2.imshow('cluster {}'.format(label), montage.montage)
	# wait for a keypress and then close all open windows
	cv2.waitKey(0)
