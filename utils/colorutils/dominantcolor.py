from collections import Counter
import cv2
from sklearn.cluster import KMeans


def get_dominant_color(image, k=4, image_processing_size=None):
    """
    takes an image as input and returns the dominant color in the image as a list

    dominant color is found by performing k means on the pixel colors and returning the centroid
	of the largest cluster

	processing time is sped up by working with a smaller image; this can be done with the
	image_processing_size param which takes a tuple of image dims as input

	>>> get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
	[56.2423442, 34.0834233, 70.1234123]
	"""
    # resize image if new dims provided
    if image_processing_size is not None:
        image = cv2.resize(image, image_processing_size, interpolation=cv2.INTER_AREA)

    # reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # cluster the pixels and assign labels
    clt = KMeans(n_clusters=k)
    labels = clt.fit_predict(image)

    # count labels to find most popular
    label_counts = Counter(labels)

    # subset out most popular centroid
    dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

    return list(dominant_color)
