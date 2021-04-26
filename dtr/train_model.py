#! /usr/bin/python

# import the necessary packages
import os

from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2

from helpers.print import pretty_message, BColors
import settings

def train_model():
	_main()

def _main():
	# our images are located in the dataset folder
	pretty_message("start processing faces...", BColors.INFO)
	# imagePaths = list(paths.list_images("/home/pi/aip_mvc/dtr/dtr_app/dataset"))
	imagePaths = list(paths.list_images(settings.DATASET_PATH))

	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		pretty_message("[INFO] processing image {}/{}".format(i + 1, len(imagePaths)), BColors.INFO)
		name = imagePath.split(os.path.sep)[-2]

		# load the input image and convert it from RGB (OpenCV ordering)
		# to dlib ordering (RGB)
		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		# detect the (x, y)-coordinates of the bounding boxes
		# corresponding to each face in the input image
		boxes = face_recognition.face_locations(rgb, model="hog")

		# compute the facial embedding for the face
		encodings = face_recognition.face_encodings(rgb, boxes)

		# loop over the encodings
		for encoding in encodings:
			# add each encoding + name to our set of known names and
			# encodings
			knownEncodings.append(encoding)
			knownNames.append(name)

	# dump the facial encodings + names to disk
	pretty_message("serializing encodings...", BColors.INFO)
	pretty_message("Training done.", BColors.OKGREEN)
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(settings.PICKLE_FILE_PATH, "wb")
	f.write(pickle.dumps(data))
	f.close()

if __name__ == "__main__":
	train_model()