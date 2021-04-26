import time
from time import sleep
import RPi.GPIO as GPIO


login_btn 		= 37
logout_btn 		= 36
arrival_btn 	= 31
departure_btn 	= 29
		
def init():
	GPIO.setmode(GPIO.BOARD)
	GPIO.setup(login_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(logout_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(arrival_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	GPIO.setup(departure_btn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
	
	GPIO.add_event_detect(login_btn, GPIO.RISING,  bouncetime=500)
	GPIO.add_event_detect(logout_btn, GPIO.RISING, bouncetime=500)
	GPIO.add_event_detect(arrival_btn, GPIO.RISING, bouncetime=500)
	GPIO.add_event_detect(departure_btn, GPIO.RISING, bouncetime=500)

def clean_up():
	GPIO.cleanup()
	
def read(login_funcy, logout_funcy, arrival_funcy, departure_funcy, name):
	if GPIO.event_detected(login_btn):
		login_funcy(name)
		#if GPIO.input(login_btn) == 1:
		#	login_funcy(name)
		
	if GPIO.event_detected(logout_btn):
		logout_funcy(name)
		#if GPIO.input(logout_btn) == 1:
		#	logout_funcy(name)
		
	if GPIO.event_detected(arrival_btn):
		#arrival_funcy(name)
		if GPIO.input(arrival_btn) == 1:
			arrival_funcy(name)
		
	if GPIO.event_detected(departure_btn):
		#departure_funcy(name)
		if GPIO.input(departure_btn) == 1:
			departure_funcy(name)

def read_kboard():
	
	if GPIO.event_detected(login_btn) and GPIO.event_detected(logout_btn):
		print('Pressed 1')
		
	if GPIO.event_detected(logout_btn):
		print('Pressed 2')
        
	if GPIO.event_detected(arrival_btn):
		print('Pressed 3')

	if GPIO.event_detected(departure_btn):
		print('Pressed 4')


init()
while True:
    sleep(0.1)
    read_kboard()