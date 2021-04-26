from mfrc522 import SimpleMFRC522
import time 
from helpers.print import BColors

class MyReader(SimpleMFRC522):
	
	reader_timeout = 30
	
	def read(self):
		id, text = self.read_no_block()
		while not id and self.reader_timeout:
			mins, secs = divmod(self.reader_timeout, 60) 
			#timer = 'Timer: ' + '{:02d}:{:02d}'.format(mins, secs) 
			timer = f'{BColors.FAIL}Timer: {BColors.ENDC}' + '{:02d}'.format(secs) 
			print(timer, end="\r") 
			time.sleep(1) 
			self.reader_timeout -= 1
			
			id, text = self.read_no_block()
		
		self.reader_timeout = 30	
		if id:
			return id, text
		else:
			return None, None
  
rfid_reader = MyReader()
