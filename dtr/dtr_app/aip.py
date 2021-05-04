import os
from datetime import datetime
import RPi.GPIO as GPIO
import requests
from requests.auth import HTTPBasicAuth
import sys

from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import sqlite3

import settings
# Need this to import the helpers package
parentdir = settings.PARENT_DIR
sys.path.insert(0, parentdir)

from helpers.rfid import rfid_reader
from helpers import pushbuttons, dates
from helpers.network import connect, api_request
from helpers.print import pretty_message, BColors

from dtr.dtr_app.models import Entry, FleetEntry

# ****************************************************************
# CONSTANTS
# ****************************************************************
LOCATION = settings.LOCATION
# Set log timeout to 5 minutes
LOG_TIMEOUT = settings.LOG_TIMEOUT

# ****************************************************************
# GLOBAL variables
# ****************************************************************
#Determine faces from encodings.pickle file model created from train_model.py
encodingsP = settings.PICKLE_FILE_PATH
#use this xml file
cascade = settings.XML_FILE_PATH

current_date = datetime.now()
current_date_str = datetime.strftime(current_date, '%Y-%m-%d')

def try_again():
	pretty_message('Haan ko sika makita. Pakiulit man.', BColors.INFO)

def do_login(new_name):
	pretty_message(f"Logging IN {BColors.OKCYAN}{new_name}{BColors.ENDC}.....", BColors.INFO)
	new_in_entry = Entry(name=new_name, location=LOCATION, date_in=current_date)
	new_in_entry.save()
	# print(current_date_str)
	pretty_message(f"Logged {BColors.OKCYAN}{new_name}{BColors.ENDC} successfully at {BColors.OKCYAN}{current_date}{BColors.ENDC}", BColors.OKGREEN)
	
def do_logout(new_name):
	pretty_message(f"Logging OUT {BColors.OKCYAN}{new_name}{BColors.ENDC}.....", BColors.INFO)
	new_out_entry = Entry(name=new_name, location=LOCATION, date_out=current_date)
	new_out_entry.save()
	pretty_message(f"Logged {BColors.OKCYAN}{new_name}{BColors.ENDC} successfully at {BColors.OKCYAN}{current_date_str}{BColors.ENDC}", BColors.OKGREEN)
	
def send_request(unit, trans_type):
	
	pretty_message('Please wait...', BColors.INFO)
	if connect():
		data_out = {
			"body_num": unit,
			"transaction_type": trans_type
		}
		
		try:
			api_url = 'https://eakdev.pythonanywhere.com/api/fleet/travel/update/'
			response = api_request(api_url, data_out)
		except:
			print("")
			pretty_message("WARNING", BColors.FAIL)
			pretty_message("Under Maintenance samet ti system Apo. Inrecord ko ladta locally ti transaction mu.", BColors.INFO)
			pretty_message("Pakiconfirm iti I.T. tau. Salamat Apo.", BColors.INFO)
		else:
			print_response(response)
	else:
		print("")
		pretty_message("WARNING", BColors.FAIL)
		pretty_message("Awan internet mu Apo. Inrecord ko ladta locally dytuy transaction mu.", BColors.FAIL)
		pretty_message("Pakiinform iti Dispatch or Site Checkers ta isu da agupdate. Salamat Apo.", BColors.INFO)

def print_response(response):
	print("")
	pretty_message(response.json()['msg']['trans_status'][1], response.json()['msg']['trans_status'][0])
	try:
		dttm_logged = response.json()['msg']['dttm_logged']
		curr_status = response.json()['msg']['curr_status']
	except:
		pass
	else:
		#qqpretty_message(f"Transaction: {response.json()['msg']['trans_status']}", BColors.OKGREEN)
		pretty_message(f"DTTM Logged: {dttm_logged}", BColors.INFO)
		pretty_message(f"Status: {curr_status}", BColors.INFO)
		
	pretty_message(f"Message: {response.json()['msg']['message']}", response.json()['msg']['trans_status'][0])

def arrival(new_name):
	if not new_name == 'Unknown':
		try:
			print("***************************************************")
			pretty_message("Vehicle Arrival or Borrow a Vehicle", BColors.OKCYAN, False)
			print("Please put the RFID of the unit you want to use.")
			print("***************************************************")
			id, unit = rfid_reader.read()
			if id != None:
				#print(id)
				pretty_message(f"Unit: {unit}", BColors.INFO)
				#save to database
				new_arrival_entry = FleetEntry(name=new_name, unit=unit, date_in=current_date_str)
				new_arrival_entry.save()
				#pretty_message('Unit Logged IN successfully, drive safe!', BColors.OKGREEN)
				pretty_message("User: %s" %(new_name), BColors.INFO)
				print("***************************************************")
				send_request(unit, "In")
				print("***************************************************")
			else:
				pretty_message('Nagururay ak ngem awan met naiscan ko. Kasin mu na lang.', BColors.FAIL)
				
			print("")
		finally:
			time.sleep(2)
	else:
		try_again()
		
def departure(new_name):
	if not new_name == 'Unknown':
		try:
			print("***************************************************")
			pretty_message("Vehicle Departure", BColors.OKCYAN, False)
			print("Please put the RFID of the unit you want to use.")
			print("***************************************************")
			id, unit = rfid_reader.read()
			if id != None:
				#print(id)
				pretty_message(f"Unit: {unit}", BColors.INFO)
				#save to database
				new_departure_entry = FleetEntry(name=new_name, unit=unit, date_out=current_date_str)
				new_departure_entry.save()
				#pretty_message('Unit Logged OUT successfully, drive safe!', BColors.OKGREEN)
				pretty_message("User: %s" %(new_name), BColors.INFO)
				print("***************************************************")
				send_request(unit, "Out")
				print("***************************************************")
				
			else:
				pretty_message('Nagururay ak ngem awan met naiscan ko. Kasin mu na lang.', BColors.FAIL)
				
			print("")
		finally:
			time.sleep(2)
	else:
		try_again()
	print("")
		
def log_in(new_name):
	if not new_name == 'Unknown':
		# Check if user is already logged in
		last_user_time_in = Entry.last_user_entry(new_name)
		if last_user_time_in == None:
			do_login(new_name)
		else:
			time_diff = (current_date - last_user_time_in).total_seconds() / 60.0
			if time_diff < LOG_TIMEOUT:
				pretty_message(F'Ustun. Nakalogin kan apo {BColors.OKCYAN}{new_name}{BColors.ENDC}', BColors.FAIL)
			else:
				do_login(new_name)
	else:
		try_again()
	print("")

def log_out(new_name):	
	if not new_name == 'Unknown':

		# Get if  there is a last time in within the day
		if Entry.last_user_entry(name=new_name) == None:
			pretty_message('Haan ka naglogin tadtay apo. Haan mu lipatan nu next wen?', BColors.FAIL)
		
		# Get if  there is a last time out within the day
		last_user_time_out = Entry.last_user_entry(name=new_name, time_in=False)
		if last_user_time_out == None:
			do_logout(new_name)
			
		else:
			time_diff = (current_date - last_user_time_out).total_seconds() / 60.0 
			if time_diff < LOG_TIMEOUT:
				pretty_message(F'Ustun. Nakalogout kan apo {BColors.OKCYAN}{new_name}{BColors.ENDC}', BColors.FAIL)
			else:
				do_logout(new_name)
	else:
		try_again()
	print("")

def show_menu():
	print("*******************************************************")
	print('Program started at: %s' % (datetime.now()))
	pretty_message("Welcome to the AIP Kiosk!", BColors.OKGREEN, False)
	print("*******************************************************")
	pretty_message("Number Choices: 1-4", BColors.OKCYAN, False)
	pretty_message(" - (1): To login", BColors.OKGREEN, False)
	pretty_message(" - (2): To logout", BColors.FAIL, False)
	pretty_message(" - (3): Vehicle Arrival or Borrow a Vehicle", BColors.FAIL, False)
	pretty_message(" - (4): Vehicle Departure", BColors.FAIL, False)
	pretty_message(" - (Q): To Exit", BColors.HEADER, False)
	print("*******************************************************")

def init():
	pushbuttons.init()

def start_dtr():
	settings.ACTIVE_APP = os.path.splitext(os.path.basename(__file__))[0]
	_main()

def _main():
	name = 'Unknown'
	curr_name = ''

	init()
	show_menu()
	# load the known faces and embeddings along with OpenCV's Haar
	# cascade for face detection
	pretty_message("loading encodings + face detector...", BColors.INFO)
	data = pickle.loads(open(encodingsP, "rb").read())
	detector = cv2.CascadeClassifier(cascade)

	# initialize the video stream and allow the camera sensor to warm up
	pretty_message("starting video stream...", BColors.INFO)
	vs = VideoStream(src=0).start()
	# vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)
	# start the FPS counter
	fps = FPS().start()

	# loop over frames from the video file stream
	while True:
		# grab the frame from the threaded video stream and resize it
		# to 500px (to speedup processing)
		frame = vs.read()
		frame = imutils.resize(frame, width=500)
		
		# convert the input frame from (1) BGR to grayscale (for face
		# detection) and (2) from BGR to RGB (for face recognition)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

		# detect faces in the grayscale frame
		rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
			minNeighbors=5, minSize=(30, 30),
			flags=cv2.CASCADE_SCALE_IMAGE)

		# OpenCV returns bounding box coordinates in (x, y, w, h) order
		# but we need them in (top, right, bottom, left) order, so we
		# need to do a bit of reordering
		boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

		# compute the facial embeddings for each face bounding box
		encodings = face_recognition.face_encodings(rgb, boxes)
		names = []

		# loop over the facial embeddings
		for encoding in encodings:
			# attempt to match each face in the input image to our known
			# encodings
			matches = face_recognition.compare_faces(data["encodings"],
				encoding, tolerance=0.36)
			name = "Unknown"

			# check to see if we have found a match
			if True in matches:
				# find the indexes of all matched faces then initialize a
				# dictionary to count the total number of times each face
				# was matched
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				# loop over the matched indexes and maintain a count for
				# each recognized face face
				for i in matchedIdxs:
					name = data["names"][i]
					counts[name] = counts.get(name, 0) + 1

				# determine the recognized face with the largest number
				# of votes (note: in the event of an unlikely tie Python
				# will select first entry in the dictionary)
				name = max(counts, key=counts.get)
								
			# update the list of names
			names.append(name)

		# loop over the recognized faces
		for ((top, right, bottom, left), name) in zip(boxes, names):
			# draw the predicted face name on the image - color is in BGR
			cv2.rectangle(frame, (left, top), (right, bottom),
				(0, 255, 0), 2)
			y = top - 15 if top - 15 > 15 else top + 15
			cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
				.8, (0, 255, 0), 2)

		
		# display the image to our screen
		cv2.imshow("Facial Recognition is Running", frame)
		# cv2.moveWindow("Facial Recognition is Running", 40, 30)
		key = cv2.waitKey(1) & 0xFF

		# if key%256 != 255:
		# 	return (key, name)
		
		#if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break
		elif key%256 == 49:
			# 1 pressed
			log_in(name)
			# print_disabled_kbrd()
		elif key%256 == 50:
			# 2 pressed
			log_out(name)
			# print_disabled_kbrd()
		elif key%256 == 51:
			# 3 pressed
			arrival(name)
			# print_disabled_kbrd()
		elif key%256 == 52:
			# 4 pressed
			departure(name)
			#print_disabled_kbrd()
		else:
			# print(name)
			curr_name = name
			
		pushbuttons.read(log_in, log_out, arrival, departure, curr_name)
		# pushbuttons.read_kboard()
		# update the FPS counter
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	pretty_message("Thank you!", BColors.INFO)
	pretty_message("approx. FPS: {:.2f}".format(fps.fps()) ,BColors.INFO)

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()
	GPIO.cleanup()		

	# return (key, name)											

if __name__ == "__main__":
	start_dtr()