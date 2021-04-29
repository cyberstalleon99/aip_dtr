import pickle
import os

import settings

def start():

	data = pickle.loads(open(settings.PICKLE_FILE_PATH, 'rb').read())


	cnt = 0
	for item in data['names']:
		print(item)
		cnt += 1

	# data = []
	# with open(settings.PICKLE_FILE_PATH, 'rb') as fr:
	# 	try:
	# 		while True:
	# 			data.append(pickle.load(fr))
	# 	except EOFError:
	# 		pass
