import glob
import argparse

import numpy as np

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
    return (image)


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='icons',
                help="Path to the dir that contains the images to be indexed")
ap.add_argument("-o", "--output", default='features_output/imagenet_features.csv',
                help="path to write imagenet features to as a csv")
args = vars(ap.parse_args())

# load image net weights but dont include classification layer
model = ResNet50(weights='imagenet', include_top=False, pooling='avg')

# read in image paths in dataset
image_paths = glob.glob('{}/*'.format(args['dataset']))
image_paths.sort()

# count number of images to process for prints
n_paths = len(image_paths)

# open file to write output to
out_file = open(args["output"], 'w')

# iterate over paths in dataset
for i, image_path in enumerate(image_paths):
    if i > 0 and i % 10 == 0:
        print('extracting features from image {} of {}'.format(i, n_paths))
    # preprocess image
    image = image_preprocessor(image_path)
    # extract features
    features = model.predict(image)
    # write image path and feature values as row in csv
    feat_str = [str(x) for x in features[0]]
    out_file.write('{},{}\n'.format(image_path, ','.join(feat_str)))

# close output file
out_file.close()
