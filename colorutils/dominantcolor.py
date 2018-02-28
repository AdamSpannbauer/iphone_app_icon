from sklearn.cluster import KMeans
from collections import Counter
import cv2

def get_dominant_color(image, k=4):
	#reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))

	#cluster the pixels and assign labels
	clt = KMeans(n_clusters = k)
	labels = clt.fit_predict(image)

	#count labels to find most popular
	label_counts = Counter(labels)

	#subset out most popular centroid
	dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

	return list(dominant_color)
