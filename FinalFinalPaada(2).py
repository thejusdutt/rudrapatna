import time
import RPi.GPIO as GPIO
import pygame
#GPIO.cleanup()

'''
cases:
1. none of the sensors are activated , directly button is pressed:
   a. reset button : ignore
   b. small pooje button: call button_sound_play() and play unless reset is clicked, 
      if reset clicked, back to main, start over
      if it plays completely , back to main , star over
   c. big pooje button : same logic as small
2. one of the sensors are activated: call sound_play() and play for respective paada unless any button clicked:
    if reset clicked -> back to main, 
    if small_pooje clicked: call button_sound_play() and play unless reset clicked, 
      if reset clicked -> back to main start over ,
      else if plays completely , back to sound_play() and hence back to main, and start over
    if big pooje clicked: same logic
    if track completely played, back to main , start over

    check if any cases missing 
'''
GPIO.setmode(GPIO.BOARD)

#pin numbers (physical pins)
os1=13#saraswati(sa)
os2=16#purandara(ri)
os3=18#vadiraja(ga)
os4=22#kanakadasa(ma)
os5=32#tyagaraja(pa)
os6=36#deekshitar(da)
os7=38#syamashastry(ni)
bs1=40#push button1 reset 
bs2=7#smallpooje
bs3=11#ganapooje
# add fade in and fade out
pygame.mixer.init(channels=2,buffer=2048)

# paths to repective tracks to be played
url1="/home/pi/Downloads/sa.mp3"
url2="/home/pi/Downloads/ri.mp3"
url3="/home/pi/Downloads/ga.mp3"
url4="/home/pi/Downloads/ma.mp3"
url5="/home/pi/Downloads/pa.mp3"
url6="/home/pi/Downloads/da.mp3"
url7="/home/pi/Downloads/ni.mp3"
url_small_pooje="/home/pi/Downloads/Small Pooje.mp3"
url_big_pooje="/home/pi/Downloads/Gana Pooje"

GPIO.setup(bs1, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #push button1 reset 
GPIO.setup(bs2, GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #push button2 smallPooje
GPIO.setup(bs3, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)  #push button3 big Pooje
GPIO.setup(os1, GPIO.IN)#setup for obstacle sensor1
GPIO.setup(os2, GPIO.IN)#
GPIO.setup(os3, GPIO.IN)#
GPIO.setup(os4, GPIO.IN)#
GPIO.setup(os5, GPIO.IN)#
GPIO.setup(os6, GPIO.IN)#
GPIO.setup(os7, GPIO.IN)#


#play if any obstacle sensor is activated :
''' case1: continues playing till the end then returns to main
   case2: plays till reset is pressed,returns back to main 
   case3: small pooje button pressed, stops music plays small pooje 
   case4: big pooje pressed-  stops music plays big pooje
'''
def sound_play(url):
   startTime1=time.time()
   diff=0
   pygame.mixer.music.load(url)
   pygame.mixer.music.play()
   #initially take input from buttons
   button_state1 = GPIO.input(bs1)
   button_state2 = GPIO.input(bs2)
   button_state3 = GPIO.input(bs3)
   #as longs as music is playing and none of the buttons are clicked do while loop
   while pygame.mixer.music.get_busy()==True  and button_state1==False and button_state2==False and button_state3==False: # add an and condition for resetPressed=Flase and smallPoojePressed=False and OtherPoojePressed=False
      button_state1 = GPIO.input(bs1)
      button_state2 = GPIO.input(bs2)
      button_state3 = GPIO.input(bs3)
     #on taking input from nutton, if any pressed check for the same
      if(button_state1==True or button_state2==True or button_state3==True):
         if(button_state1==True):
            pygame.mixer.music.stop()  #stop the music , return from function : so will go back to main
            #initial_call()
            print("music stop reset")
            return
            #  break
           #initial_call()
         elif(button_state2==True):
            pygame.mixer.music.stop()  #stop the music and play small pooje track
            button_sound_play(url_small_pooje)
            return# once small pooje returns back to this function, return back to main
            #initial_call()
         elif(button_state3==True):
            pygame.mixer.music.stop()  #stop the music and play big pooje track
            button_sound_play(url_big_pooje)
            return# once small pooje returns back to this function, return back to main
            #initial_call()
   pygame.mixer.music.stop() #if none of buttons are clicked and the track for paada is over , stop music and return back to main
  
''' Check if small pooje or big pooje pressed
   case1 : plays entire pooje track with no interrupt
   case2 : reset butoon is pressed so goes back to main(or previous function call, so in case this function is directly call in the beginning 
            goes back to main otherwise , if function was called from soundplay() goes back to soundplay which later returns to main immediately)
'''
def button_sound_play(url):
   pygame.mixer.music.load(url)
   pygame.mixer.music.play()   
   button_state1 = GPIO.input(bs1)
   #as longs as music is playing and reset buttons is not clicked do while loop
   while pygame.mixer.music.get_busy()==True and button_state1==False: 
      button_state1 = GPIO.input(bs1)
      if(button_state1==True):   #in case reset has been clicked, stop the music and return to previous function , which finally returns to main
         pygame.mixer.music.stop()
         return
   pygame.mixer.music.stop()  #in case the entire pooje track has played , close it and go back to main

try:
   while True:
      print("while")
      obstacle_state1 = GPIO.input(os1)  #accept input from each sensor and button
      obstacle_state2 = GPIO.input(os2)
      obstacle_state3 = GPIO.input(os3)
      obstacle_state4 = GPIO.input(os4)
      obstacle_state5 = GPIO.input(os5)
      obstacle_state6 = GPIO.input(os6)
      obstacle_state7 = GPIO.input(os7)
      button_state1 = GPIO.input(bs1)
      button_state2 = GPIO.input(bs2)
      button_state3 = GPIO.input(bs3)
      if(button_state2==True):
         print("button2if")     #check for just small pooje button being clickedd
         button_sound_play(url_small_pooje)
      elif(button_state3==True):   #check for just big pooje
         print("button3if") 
         button_sound_play(url_big_pooje)
      #if both dont satisfy check for sensors.if any of the sensors are activated(ie become false ) and none of the buttons are pressed iE all are true
      elif((obstacle_state1 == False  or obstacle_state3 == False or obstacle_state2 == False  or obstacle_state4 == False  or obstacle_state5 == False  or obstacle_state6 == False  or obstacle_state7 == False) and (button_state1==False and button_state2==False and button_state3==False)):
         print('0')
         if(obstacle_state1 == False): #if 1st sensor play music for 1, same for the others
            print("ob1")
            sound_play(url1)
         elif(obstacle_state2 == False):
            print("ob2")
            sound_play(url2)
         elif(obstacle_state3 == False):
            print("ob3")
            sound_play(url3)
         elif(obstacle_state4 == False):
            print("ob4")
            sound_play(url4)
         elif(obstacle_state5 == False):
            print("ob5")
            sound_play(url5)
         elif(obstacle_state6 == False):
            print("ob6")
            sound_play(url6)
         elif(obstacle_state7 == False):
            print("ob7")
            sound_play(url7)   
      else:
         print "1"
      time.sleep(0.2)
      
except:
   print "Agalla"
