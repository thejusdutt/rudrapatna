#!/usr/bin/env python
import os
import time 
import random
import pygame
import RPi.GPIO as GPIO

pygame.mixer.init(channels=2,buffer=2048)
pygame.mixer.music.load("/home/pi/Downloads/C.mp3")
url="/home/pi/Downloads/C.mp3"

def door_sound_play(url):
	pygame.mixer.music.load(url)
	pygame.mixer.music.play()
	time.sleep(5) 
	pygame.mixer.music.fadeout(1000)
	
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7,GPIO.IN) #first door outer
GPIO.setup(12,GPIO.IN)#second door inner

GPIO.setup(16,GPIO.IN) #first door outer
GPIO.setup(18,GPIO.IN)#second door inner

GPIO.add_event_detect(7, GPIO.RISING,bouncetime=500)
GPIO.add_event_detect(12, GPIO.RISING,bouncetime=500)
GPIO.add_event_detect(16, GPIO.RISING,bouncetime=500)
GPIO.add_event_detect(18, GPIO.RISING,bouncetime=500)


while True:
			
	if GPIO.event_detected(7):
		
		print "outertouched1"
		#startTime1 = time.time() 
		#print(startTime1)
		
		t_end1 = time.time() + 2
		
		while time.time()<t_end1:
			print("waiting")
			if GPIO.event_detected(12):
				print "innertouched111111111111111111"
				door_sound_play(url)

			
	elif GPIO.event_detected(12):
		print("########")
		time.sleep(0.5)		
	
			
	#######################
	
	if GPIO.event_detected(16):
		
		print "outertouched2"
		#startTime1 = time.time() 
		#print(startTime1)
		
		t_end2 = time.time() + 2
		
		while time.time()<t_end2:
			print("waiting")
			if GPIO.event_detected(18):
				print "innertouched222222222222222222"
				door_sound_play(url)

			
	elif GPIO.event_detected(18):
		print("########")
		time.sleep(0.5)		
	
	
