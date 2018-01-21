        print "LED turned off & Threads should be stopped"
# This I hope to form a quick basis for my simple Python projects to us a geneic API
# We have yet to see what use it will actually be

# docker run --net host --name py --rm -it --device /dev/mem --cap-add SYS_RAWIO -v /sys:/sys $IMAGE python

# This nice little script works with the rocket-server to determin the course of actions that the user-based buttons do
# CSID0 button:up 
# CSID1 button:down
# CSID2 button:power
# CSID8 led:indicator


from time import sleep
import thread
from random import randint
import CHIP_IO.GPIO as GPIO
import json
import sys
import signal

# assign the buttons as CSID values
up = "CSID0" #speed goes up
down = "CSID1" #speed goes down
stop = "CSID2"	#stop the loop
flasher = "CSID7" #'indicator' led to show userfeed-back
threads=[]


# set the direction for GPIO 
GPIO.setup(up, GPIO.IN)
GPIO.setup(down, GPIO.IN)
GPIO.setup(stop, GPIO.IN)
GPIO.setup(flasher, GPIO.OUT)


# Class test string==> c = button(["CSID1","CSID2"])
class button:
	button={}
	pressTime=0
	keepRunning=True #Used by the sub-threads to know when to stop running
	def __init__ (self,GPIObuttonArray,minPressTime):
		for buttonCSID in GPIObuttonArray:
			self.button.update({buttonCSID:False})
			print "Added new button" + buttonCSID
			self.pressTime = minPressTime
	def printButtonList():
		print json.dumps(self.button)

def sigterm_handler(signal, frame):
	try:
		count = 0
		while (thread._count() > 0 and count < 8):
			buttonObject.keepRunning = False
			sleep(0.9)
			count += 1
		GPIO.output(flasher, False)
		GPIO.cleanup()
		print "LED turned off & Threads should be stopped"
		sys.exit(0)
	except Exception as e:
		print "There was an error turning off: " + str(e)
		sys.exit(2)


def buttonPress(buttonObject,buttonID):
    while buttonObject.keepRunning:
    	if GPIO.input(buttonID):
    		buttonObject.button[buttonID] = True
    		sleep(buttonObject.pressTime)
    		#print buttonObject.button
    	else:
    		buttonObject.button[buttonID] = False
    	sleep(0.1) # let another thread take over for a moment

def flashLED(flashCount):
	for x in range(flashCount):
		GPIO.output(flasher, True)
		sleep(0.05)
		GPIO.output(flasher, False)
		sleep(0.1)

def mainControl(buttonObject):
	while buttonObject.keepRunning:
		if buttonObject.button[up]:
			print "Speeding up"
			threads.append(thread.start_new_thread(flashLED, (1,)))
			buttonObject.button[up] = False
		elif buttonObject.button[down]:
			print "Slowing down"
			threads.append(thread.start_new_thread(flashLED, (2,)))
			buttonObject.button[down] = False
		elif buttonObject.button[stop]:
			print "Stopping"
			threads.append(thread.start_new_thread(flashLED, (3,)))
			buttonObject.button[stop] = False
		sleep(0.01)


signal.signal(signal.SIGTERM, sigterm_handler)
if __name__ == "__main__":
	buttonObject = button([up,down,stop],0.5)
	if thread._count() == 0:
		threads.append(thread.start_new_thread(mainControl, (buttonObject,)))
		threads.append(thread.start_new_thread(buttonPress, (buttonObject,up)))
		threads.append(thread.start_new_thread(buttonPress, (buttonObject,down)))
		threads.append(thread.start_new_thread(buttonPress, (buttonObject,stop)))
	else:
		print "ERROR: there seems to be some threads already running"




