import time
import RPi.GPIO as GPIO

import settings
from helpers import keyboard

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

	if GPIO.event_detected(login_btn):
		if settings.ACTIVE_APP == 'aip':
			keyboard.press('1')
		elif settings.ACTIVE_APP == 'head_shots':
			keyboard.press(keyboard.Key.space)
		
	if GPIO.event_detected(logout_btn):
		keyboard.press('2')
		
	if GPIO.event_detected(arrival_btn):
		keyboard.press('3')
		
	if GPIO.event_detected(departure_btn):
		keyboard.press('4')


	