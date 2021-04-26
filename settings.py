import os
import sys

# Do not edit this variable
ACTIVE_APP = ''

PARENT_DIR = '/home/pi/aip'

# DTR SETTINGS
DB_PATH = os.path.join(PARENT_DIR, 'dtr/dtr_app/aip_dtr.db')
PICKLE_FILE_PATH = os.path.join(PARENT_DIR, 'dtr/dtr_app/encodings.pickle')
XML_FILE_PATH = os.path.join(PARENT_DIR, 'dtr/dtr_app/haarcascade_frontalface_default.xml')
LOCATION = 'AIP Main'
# Time before user can time in/out in minutes
LOG_TIMEOUT = 5
USE_LOGIN_BTN_TO_CAPTURE = True

# HEADSHOTS SETTINGS
DATASET_PATH = os.path.join(PARENT_DIR, 'dtr/dtr_app/dataset')

# SWITCH: KEYBOARD OR PUSHBUTTONS
USE_KEYBOARD = True
