#! /usr/bin/python

# import the necessary packages
import os
import shutil

from imutils import paths
import face_recognition
#import argparse
import pickle
import cv2

from helpers.print import pretty_message, BColors
import settings

def train_model_partial():
	_main(train_all=False)

def train_model_all():
	_main()

def read_pickle_file():
	data = pickle.loads(open(settings.PICKLE_FILE_PATH, 'rb').read())

	# data is a dictionary
	return data

def _move_folders():
	pretty_message("Moving folders...", BColors.INFO)
	for emp_dir in os.scandir(settings.DATASET_UNTRAINED_PATH):
		if emp_dir.is_dir():
			shutil.move(emp_dir.path, settings.DATASET_PATH)

def _do_train_all(data):
	f = open(settings.PICKLE_FILE_PATH, "wb")
	f.write(pickle.dumps(data))
	f.close()

def _do_train_partial(data):

	curr_data = pickle.loads(open(settings.PICKLE_FILE_PATH, 'rb').read())

	for key, values in data.items():
		for value in values:
			curr_data[key].append(value)

	f = open(settings.PICKLE_FILE_PATH, "wb")
	f.write(pickle.dumps(curr_data))
	f.close()

def _main(train_all=True):

	if train_all:
		# Set Dataset path to the trained models Directory
		imagePaths = list(paths.list_images(settings.DATASET_PATH))
	else:
		# Set the Dataset path to the untrained models  directory
		imagePaths = list(paths.list_images(settings.DATASET_UNTRAINED_PATH))

		if not imagePaths:
			pretty_message("No new images...", BColors.FAIL)
			return

	pretty_message("Start processing faces...", BColors.INFO)
	pretty_message("Please wait until finished...", BColors.FAIL)
	# initialize the list of known encodings and known names
	knownEncodings = []
	knownNames = []

	# loop over the image paths
	for (i, imagePath) in enumerate(imagePaths):
		# extract the person name from the image path
		pretty_message("Processing image {}/{}".format(i + 1, len(imagePaths)), BColors.INFO)
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

	if train_all:
		_do_train_all(data)
	else:
		_do_train_partial(data)

	_move_folders()

	

if __name__ == "__main__":
	train_model_all()