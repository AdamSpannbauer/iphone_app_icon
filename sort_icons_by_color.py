# this functionality is now in the function `utils.create_sorted_color_montage()`
# leaving script for blog

# SCRIPT WILL FORCE ALL IMAGES TO BE THE SAME SIZE IN OUTPUT
# SCRIPT WILL FORCE ALL IMAGES TO BE THE SAME SIZE IN OUTPUT
# SCRIPT WILL FORCE ALL IMAGES TO BE THE SAME SIZE IN OUTPUT

# ----------------------------------------------------
import argparse

import cv2
import imutils
import imutils.paths as paths

import utils

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="Path to the dir that contains the images to be sorted")
ap.add_argument("-o", "--output", default='sorted_images.jpg',
                help="Path to the dir to write feature output to")
ap.add_argument("-k", "--clusters", type=int, default=3,
                help="# of clusters to use when finding image dominant color")
ap.add_argument("-s", "--sizeHeight", type=int, default=300,
                help="output height of sorted output image in pixels")
args = vars(ap.parse_args())

# grab the image paths from the dataset directory
image_paths = list(paths.list_images(args["input"]))

# init dominant color store
colors = []
# iterate over ims
for i, path in enumerate(image_paths):
    if i > 0 and i % 50 == 0:
        print('processing image {} of {}'.format(i, len(image_paths)))
    # read in image
    image = cv2.imread(path)
    # convert to hsv colorspace
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # get dominant color
    color = utils.get_dominant_color(hsv_image, k=args["clusters"],
                                     image_processing_size=(25, 25))
    # store color
    colors.append(color)

# sort colors by hue (return list of image inds sorted)
sorted_inds = sorted(range(len(colors)), key=lambda i: colors[i], reverse=True)

# use last image's shape as default shape for all images
image_shape = (image.shape[0], image.shape[1])

# init montage
montage = utils.results_montage(
    image_size=image_shape,
    images_per_main_axis=10,
    num_results=len(image_paths),
    by_row=False
)

# iter over sorted image inds
for ind in sorted_inds:
    # read in image
    image = cv2.imread(image_paths[ind])
    # ensure all images are same size
    image = cv2.resize(image, image_shape, interpolation=cv2.INTER_AREA)
    # add image i to montage
    montage.add_result(image)

# resize output collage
out = imutils.resize(montage.montage, height=args["sizeHeight"])

# show image to screen
cv2.imshow('Sorted Images', out)
cv2.waitKey(0)
# save output
cv2.imwrite(args["output"], out)
