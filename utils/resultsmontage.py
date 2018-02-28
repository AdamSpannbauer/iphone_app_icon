# import the necessary packages
import numpy as np
import cv2

class results_montage:
	def __init__(self, image_size, images_per_row, num_results):
		# store the target image size and the number of images per row
		self.imageW = image_size[0]
		self.imageH = image_size[1]
		self.images_per_row = images_per_row

		# allocate memory for the output image
		num_cols = -(-num_results // images_per_row) #ceiling division
		self.montage = np.zeros((num_cols * self.imageW, images_per_row * self.imageH, 3), dtype="uint8")

		# initialize the counter for the current image along with the row and column
		# number
		self.counter = 0
		self.row = 0
		self.col = 0

	def add_result(self, image, text=None, highlight=False):
		# check to see if the number of images per row has been met, and if so, reset
		# the column counter and increment the row
		if self.counter != 0 and self.counter % self.images_per_row == 0:
			self.col = 0
			self.row += 1

		# resize the image to the fixed width and height and set it in the montage
		image = cv2.resize(image, (self.imageH, self.imageW))
		(startY, endY) = (self.row * self.imageW, (self.row + 1) * self.imageW)
		(startX, endX) = (self.col * self.imageH, (self.col + 1) * self.imageH)
		self.montage[startY:endY, startX:endX] = image

		# if the text is not None, draw it
		if text is not None:
			cv2.putText(self.montage, text, (startX + 10, startY + 30), cv2.FONT_HERSHEY_SIMPLEX,
				1.0, (0, 255, 255), 3)

		# check to see if the result should be highlighted
		if highlight:
			cv2.rectangle(self.montage, (startX + 3, startY + 3), (endX - 3, endY - 3), (0, 255, 0), 4)

		# increment the column counter and image counter
		self.col += 1
		self.counter += 1