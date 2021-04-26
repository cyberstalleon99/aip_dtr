import urllib
import requests
from requests.auth import HTTPBasicAuth

API_URL = 'https://eakdev.pythonanywhere.com/api/fleet/travel/update/'
SYSTEM_AUTH = HTTPBasicAuth('CAK', 'clyde_2021it')

def connect():
	try:
		urllib.request.urlopen('https://eakdev.pythonanywhere.com/')
		return True
	except:
		return False

def api_request(api_url, data_out):
	return requests.patch(API_URL, json=data_out, auth=SYSTEM_AUTH)
