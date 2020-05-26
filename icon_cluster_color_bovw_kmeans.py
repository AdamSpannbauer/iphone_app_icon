import argparse

import numpy as np
import cv2
import h5py

from sklearn.cluster import KMeans

import utils


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--featuresPath", default='features_output',
                help="path to the directory housing image features")
ap.add_argument("-c", "--useColorFeatures", default=1, type=int,
                help="use color features in clustering? (0 if no)")
ap.add_argument("-b", "--useBovwFeatures", default=1, type=int,
                help="use bag of words features in clustering? (0 if no)")
ap.add_argument("-o", "--output", default='cluster_results',
                help="path to the output directory")
ap.add_argument("-k", "--clusters", type=int, default=10,
                help="# of clusters to generate")
args = vars(ap.parse_args())

# check if user specified to use no features
# raise error if no features specified
if args['useColorFeatures'] == 0 and args['useBovwFeatures'] == 0:
    raise ValueError('--useColorFeatures (-c) or --useBovwFeatures (-b) must be non-zero')

# read in image paths from features hdf5
featuresDB = h5py.File('{}/features.hdf5'.format(args["featuresPath"]))
image_paths = featuresDB['image_ids'][:]

# read in color features if specified to be used
if args['useColorFeatures'] != 0:
    # read csv color features to array
    color_data = np.genfromtxt('{}/color_hists.csv'.format(args["featuresPath"]),
                               delimiter=',')
    # drop first column (first col is image file path)
    color_data = np.delete(color_data, 0, axis=1)

    data = color_data

# read in bovw features if specified to be used
if args['useBovwFeatures'] != 0:
    # read in hdf5 of bovw keypoint features
    bovwDB = h5py.File('{}/bovw.hdf5'.format(args["featuresPath"]))
    bovw_data = bovwDB['bovw'][:]

    # hstack with color features if both feature sets being used
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

    # create color sorted tiled image displaying cluster members
    sorted_montage = utils.create_sorted_color_montage(
        label_paths,
        tile_size=(100, 100),
        images_per_main_axis=4,
        by_row=False,
        color_processing_size=(25, 25),
        verbose=False
    )

    cv2.imwrite('{}/cluster_{}.jpg'.format(args['output'], label), sorted_montage)
# cv2.imshow('cluster {}'.format(label), sorted_montage)
# wait for a keypress and then close all open windows
# cv2.waitKey(0)
# cv2.destroyAllWindows()
