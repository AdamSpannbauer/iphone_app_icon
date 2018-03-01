from __future__ import print_function
from features.descriptors import DetectAndDescribe
from features.indexer import FeatureIndexer, BOVWIndexer
from features.ir import Vocabulary, BagOfVisualWords
from imutils.feature import FeatureDetector_create, DescriptorExtractor_create
from imutils import paths
import pickle
import h5py
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", default='icons',
	help="Path to the dir that contains the images to be indexed")
ap.add_argument("-o", "--output", default='features_output',
	help="Path to the dir to write feature output to")
ap.add_argument("-a", "--approx-images", type=int, default=300,
	help="Approximate # of images in the dataset")
ap.add_argument("-k", "--clusters", type=int, default=200,
	help="# of clusters to generate")
ap.add_argument("-p", "--percentage", type=float, default=0.5,
	help="Percentage of total features to use when clustering")
ap.add_argument("-b", "--max-buffer-size", type=int, default=50000,
	help="Maximum buffer size for # of features to be stored in memory")
args = vars(ap.parse_args())

##################
# CREATE KEYPOINT FEATURES
##################
print('\n\n STARTING FEATURE EXTRACTION \n\n')

# initialize the keypoint detector, local invariant descriptor, and the descriptor
# pipeline
detector = FeatureDetector_create('GFTT')
descriptor = DescriptorExtractor_create('RootSIFT')
dad = DetectAndDescribe(detector, descriptor)

# initialize the feature indexer, then grab the image paths and sort
fi = FeatureIndexer(
	'{}/features.hdf5'.format(args["output"]),
	estNumImages=args["approx_images"],
	maxBufferSize=args["max_buffer_size"], 
	verbose=True)
imagePaths = list(paths.list_images(args["dataset"]))
imagePaths.sort()

# loop over the images in the dataset
for (i, imagePath) in enumerate(imagePaths):
	# check to see if progress should be displayed
	if i > 0 and i % 50 == 0:
		fi._debug("processed {} images".format(i), msgType="[PROGRESS]")

	# load the image and prepare it from description
	image = cv2.imread(imagePath)
	image = imutils.resize(image, width=min(320, image.shape[1]))
	image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

	# describe the image
	(kps, descs) = dad.describe(image)

	# if either the keypoints or descriptors are None, then ignore the image
	if kps is None or descs is None:
		continue

	# index the features
	fi.add(imagePath, kps, descs)

# finish the indexing process
fi.finish()
#---------------------------------------------

##################
# CREATE VOCAB
##################
print('\n\n STARTING VOCAB CREATION \n\n')

# create the visual words vocabulary
voc = Vocabulary('{}/features.hdf5'.format(args["output"]))
vocab = voc.fit(args["clusters"], args["percentage"])

# dump the clusters to file
print("[INFO] storing cluster centers...")
f = open('{}/vocab.cpickle'.format(args["output"]), "wb")
f.write(pickle.dumps(vocab))
f.close()
#---------------------------------------------

##################
# CREATE BOVW FEATURES
##################
print('\n\n STARTING BOVW CREATION \n\n')

bovw = BagOfVisualWords(vocab)

# open the features database and initialize the bag-of-visual-words indexer
featuresDB = h5py.File('{}/features.hdf5'.format(args["output"]), mode="r")
bi = BOVWIndexer(bovw.codebook.shape[0], '{}/bovw.hdf5'.format(args["output"]),
	estNumImages=featuresDB["image_ids"].shape[0],
	maxBufferSize=args["max_buffer_size"])

# loop over the image IDs and index
for (i, (imageID, offset)) in enumerate(zip(featuresDB["image_ids"], featuresDB["index"])):
	# check to see if progress should be displayed
	if i > 0 and i % 50 == 0:
		bi._debug("processed {} images".format(i), msgType="[PROGRESS]")

	# extract the feature vectors for the current image using the starting and
	# ending offsets (while ignoring the keypoints) and then quantize the
	# features to construct the bag-of-visual-words histogram
	features = featuresDB["features"][offset[0]:offset[1]][:, 2:]
	hist = bovw.describe(features)

	# normalize the histogram such that it sums to one then add the
	# bag-of-visual-words to the index
	hist /= hist.sum()
	bi.add(hist)

# close the features database and finish the indexing process
featuresDB.close()
bi.finish()


