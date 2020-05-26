import cv2
import imutils


class color_histogram:
    """
    class to produce color histogram features given an input image
    """
    def __init__(self, bins, color_space='bgr'):
        # store the number of bins for the histogram
        self.bins = bins
        # check if valid color space provided; store if valid
        if color_space not in ['bgr', 'lab', 'hsv']:
            raise ValueError("color_space must be in ['bgr', 'lab', 'hsv']")
        else:
            self.color_space = color_space

    def describe(self, image, mask=None):
        # convert the image to the L*a*b* color space, compute a histogram,
        # and normalize it
        if self.color_space == 'lab':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
            hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                                [0, 256, 0, 256, 0, 256])
        elif self.color_space == 'hsv':
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                                [0, 180, 0, 256, 0, 256])
        else:
            hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
                                [0, 256, 0, 256, 0, 256])

        # handle if we are calculating the histogram for OpenCV 2.4
        if imutils.is_cv2():
            hist = cv2.normalize(hist).flatten()

        # otherwise, we are creating the histogram for OpenCV 3+
        else:
            hist = cv2.normalize(hist, hist).flatten()

        # return the histogram
        return hist
