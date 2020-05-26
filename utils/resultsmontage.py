# import the necessary packages
import numpy as np
import cv2


class results_montage:
    """
    class to combine input images into a single image displaying a combined grid
    of the input images
    """

    def __init__(self, image_size, images_per_main_axis, num_results, by_row=True):
        # store the target image size and the number of images per row
        self.imageW = image_size[0]
        self.imageH = image_size[1]
        self.images_per_main_axis = images_per_main_axis
        self.by_row = by_row

        # allocate memory for the output image
        num_main_axis = -(-num_results // images_per_main_axis)  # ceiling division
        if by_row:
            self.montage = np.zeros(
                (num_main_axis * self.imageW, min(images_per_main_axis, num_results) * self.imageH, 3),
                dtype="uint8"
            )
        else:
            self.montage = np.zeros(
                (min(images_per_main_axis, num_results) * self.imageW, num_main_axis * self.imageH, 3),
                dtype="uint8"
            )

        # initialize the counter for the current image along with the row and column
        # number
        self.counter = 0
        self.row = 0
        self.col = 0

    def add_result(self, image, text=None, highlight=False):
        # check to see if the number of images per row/col has been met, and if so, reset
        # the row/col counter and increment the row
        if self.by_row:
            if self.counter != 0 and self.counter % self.images_per_main_axis == 0:
                self.col = 0
                self.row += 1
        else:
            if self.counter != 0 and self.counter % self.images_per_main_axis == 0:
                self.col += 1
                self.row = 0

        # resize the image to the fixed width and height and set it in the montage
        image = cv2.resize(image, (self.imageH, self.imageW))
        (startY, endY) = (self.row * self.imageW, (self.row + 1) * self.imageW)
        (startX, endX) = (self.col * self.imageH, (self.col + 1) * self.imageH)
        self.montage[startY:endY, startX:endX] = image

        # if the text is not None, draw it
        if text is not None:
            cv2.putText(self.montage, text, (startX + 5, startY + 13), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)

        # check to see if the result should be highlighted
        if highlight:
            cv2.rectangle(self.montage, (startX + 3, startY + 3), (endX - 3, endY - 3), (0, 255, 0), 4)

        if self.by_row:
            # increment the column counter
            self.col += 1
        else:
            # increment the row counter
            self.row += 1
        # increment total image counter
        self.counter += 1
