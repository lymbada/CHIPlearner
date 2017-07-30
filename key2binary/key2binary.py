#!/usr/bin/env python2.7
# Run: sudo python key2binary.py
# Description: Simple little script for use with the C.H.I.P Pro Dev board. When run, 
#    each ASCII input character is taken from the STDIN and the LEDs display the Binary ASCII code for that key
#    To exit, use the 'C' (capitol c) character, this will also clear the LEDs
# Version: 1.0

import tty, sys, termios
import CHIP_IO.GPIO as GPIO

def SetupLEDs():
    for i in range(0,7):
        led = "CSID" + str(i)
        GPIO.setup(led, GPIO.OUT)
        GPIO.output(led, GPIO.LOW) # set all to low for now


class ReadChar():
    def __enter__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(sys.stdin.fileno())
        return sys.stdin.read(1)
    def __exit__(self, type, value, traceback):
        termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)

def getKey():
    while True:
        with ReadChar() as rc:
            char = rc

            # print our each character as a binary
            for index, bit in enumerate(reversed(bin(ord(char))[2:])):
                led = "CSID" + str(index)
                if bit == str(1): 
                    GPIO.output("CSID" + str(index), GPIO.HIGH)
                else:
                    GPIO.output("CSID" + str(index), GPIO.LOW)


        if ord(char) <= 32:
            print("You entered character with ordinal {}."\
                        .format(ord(char)))
        else:
            print("You entered character '{}'."\
                        .format(char))
        if char in "^C^D":
            #exit and turn off all digital GPIO ports
            for i in range(0,7):
                led = "CSID" + str(i)
                GPIO.output(led, GPIO.LOW) # set all to low for now
            #TODO: allow for full release of GPIO digital ports
            sys.exit()

if __name__ == "__main__":
    SetupLEDs()
    getKey()
