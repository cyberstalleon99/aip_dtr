import face_recognition
import imutils
from imutils.video import VideoStream
from imutils.video import FPS
import pickle
import time
import cv2
import sys

from dtr import test
from dtr.dtr_app import aip
from dtr.dtr_app.models import Entry
from helpers import excel


# print(sys.path)
# test.start()
# excel.write('Test', )

# aip.extract_dtr()
Entry.export_to_excel()