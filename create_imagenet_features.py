import glob
import numpy as np
import argparse
import keras
from keras.preprocessing import image as image_utils
from keras.applications.imagenet_utils import preprocess_input
from keras.layers import Flatten
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

# define image preprocessor for use with imagenet model
def image_preprocessor(image_path):
	image = image_utils.load_img(image_path, target_size=(224, 224))
	image = image_utils.img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image = preprocess_input(image)
	return(image)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='icons',
	help="Path to the dir that contains the images to be indexed")
ap.add_argument("-o", "--output", default='features_output',
	help="Path to the dir to write feature output to")
args = vars(ap.parse_args())

#load image net weights but dont include classification layer
model = keras.applications.resnet50.ResNet50(weights='imagenet', include_top=False)

#read in image paths in dataset
image_paths = glob.glob('{}/*'.format(args['dataset']))
image_paths.sort()

full_features = np.array([], dtype=np.int64).reshape(0, 2048)

for i, image_path in enumerate(image_paths):
	print('extracting features from image {} of {}'.format(i, len(image_paths)))
	#
	#preprocess image
	image = image_preprocessor(image_path)
	#extract features
	features = model.predict(image)
	#flatten features
	features = np.ravel(features)
	#
	full_features = np.vstack((full_features, features))

#DOES NOT PRODUCE GOOD RESULTS
# print('performing TSNE')
# dim_reduce = PCA(n_components=args['nFeatures'], random_state=42)
# dim_reduce = TSNE(n_components=args['nFeatures'], method='exact', random_state=42)
# reduced_features = dim_reduce.fit_transform(full_features)

print('writing output')
with open('{}/imagenet.csv'.format(args["output"]), "w") as f:
	for i, row in enumerate(full_features.tolist()):
		#write image path and feature values as row in csv
		row_str = [str(x) for x in row]
		f.write('{},{}\n'.format(image_paths[i], ','.join(row_str)))
