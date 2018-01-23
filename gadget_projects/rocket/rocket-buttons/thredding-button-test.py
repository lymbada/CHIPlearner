from time import sleep
import thread
from random import randint
import CHIP_IO.GPIO as GPIO

up = "CSID0" #speed goes up
down = "CSID1" #speed goes down
stop = "CSID2"	#stop the loop
flasher = "CSID7" #'indicator' led to show userfeed-back

GPIO.setup(up, GPIO.IN)
GPIO.setup(down, GPIO.IN)
GPIO.setup(stop, GPIO.IN)
GPIO.setup(flasher, GPIO.OUT)

def flash_indicator(flash_count):
	for x in range(flash_count):
		GPIO.output(flasher, True)
		sleep(0.05)
		GPIO.output(flasher, False)
		sleep(0.1)

def up_down_buttons(current_speed): #because only 1 can be used at any time, this does both buttons
	for x in range(500):
		if GPIO.input(up):
			current_speed+=10
			flash_indicator(1)
			sleep(0.2)
			print "up button"
		elif GPIO.input(down):
			current_speed-=10
			flash_indicator(1)
			sleep(0.2)
			print "down button"
		sleep(0.05)
	#return current_speed

def on_off_button():
	stop_count = 0
	for x in range(100):
		if GPIO.input(stop):
			stop_count += 1 
			thread.start_new_thread(flash_indicator, (stop_count,))
			print stop_count
		else:
			stop_count = 0
		if stop_count == 3:
			print "Times 3, stopping"
			break
		sleep(0.3)


def loop1(y,thredX):
    for x in range(y):
    	rand = randint(1,30)
    	sleep(rand/2)
        print "LOOP1:" + str(x) + " Using thread:" + str(thredX) + " Randomnumer:" + str(rand)


def loop2(y,thread_count):
	print "starting loop 2"
	for x in range(thread_count):
		thread.start_new_thread(loop1, (y, x))


# test creating a thread that create more threads, with radom sleep intervals
thread.start_new_thread(loop2, (4, 4))


thread.start_new_thread(up_down_buttons, (3,))
thread.start_new_thread(on_off_button, ())


