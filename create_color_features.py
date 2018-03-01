import cv2
import argparse
import utils
import numpy as np
import glob

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='icons',
	help="Path to the dir that contains the images to be indexed")
ap.add_argument("-o", "--output", default='features_output',
	help="Path to the dir to write feature output to")
ap.add_argument("-c", "--colorSpace", default='bgr',
	help="color space to use for generating historgram features (bgr, hsv, or lab)")
args = vars(ap.parse_args())

#gather image paths and sort
image_paths = glob.glob('{}/*'.format(args['dataset']))
image_paths.sort()

#open output file to write to
output = open('{}/color_hists.csv'.format(args["output"]), "w")

#init color histogram descriptor
desc = utils.colorutils.color_histogram([6, 6, 6], color_space = args['colorSpace'])

color_data = []
# loop over the input dataset of images
for image_path in image_paths:
	# load image i and describe
	image = cv2.imread(image_path)
	features = desc.describe(image)

	#write image path and feature values as row in csv
	features = [str(x) for x in features]
	output.write('{},{}\n'.format(image_path, ','.join(features)))

#clean up
output.close()
