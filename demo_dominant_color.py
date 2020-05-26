import argparse
import cv2
import numpy as np
from utils.colorutils import get_dominant_color

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagePath", required=True,
                help="Path to image to find dominant color of")
ap.add_argument("-k", "--clusters", default=3, type=int,
                help="Number of clusters to use in kmeans when finding dominant color")
args = vars(ap.parse_args())

# read in image of interest
bgr_image = cv2.imread(args['imagePath'])
# convert to HSV; this is a better representation of how we see color
hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

# extract dominant color
# (aka the centroid of the most popular k means cluster)
dom_color = get_dominant_color(hsv_image, k=args['clusters'])

# create a square showing dominant color of equal size to input image
dom_color_hsv = np.full(bgr_image.shape, dom_color, dtype='uint8')
# convert to bgr color space for display
dom_color_bgr = cv2.cvtColor(dom_color_hsv, cv2.COLOR_HSV2BGR)

# concat input image and dom color square side by side for display
output_image = np.hstack((bgr_image, dom_color_bgr))

# show results to screen
cv2.imshow('Image Dominant Color', output_image)
cv2.waitKey(0)
