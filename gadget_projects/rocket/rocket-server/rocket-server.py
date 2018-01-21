# This I hope to form a quick basis for my simple Python projects to us a geneic API
# We have yet to see what use it will actually be

# docker run --net host --name py --rm -it --device /dev/mem --cap-add SYS_RAWIO -v /sys:/sys rocket-server_bde2fe73-fcf0-458e-b3d8-013e2a0a6fe0-img python

from flask import Flask, url_for
from flask import request
from flask import json
from flask import jsonify
from flask import Response
import sys
import signal
import CHIP_IO.GPIO as GPIO
import CHIP_IO.PWM as PWM
from time import sleep
from functools import wraps
import logging


# Set up the PWM / GPIO settings with the CHIP Pro
PWM.start("PWM0", 100)
leds = "CSID6"
GPIO.setup(leds, GPIO.OUT)
# Set up the Flask API
app = Flask(__name__)
route_url = '/api/v1/'
rocket_base_url = (route_url + 'rocket')

class GPIO_controll:
    def __init__(self,ledpin):
        self.speed = 0
        self.ledID = ledpin
        self.ledState = False
    def get_speed(self):
        return self.speed
    def set_speed(self, new_speed):
        if new_speed > 100:
            new_speed = 100
        elif new_speed > 0 and new_speed < 30 and self.speed == 0:
            new_speed = 30
        elif new_speed < 30:
            new_speed = 0
        self.speed = new_speed
        print "speed set to" + str(100-self.speed)
        PWM.set_duty_cycle("PWM0", (100-self.speed))
    def led_on(self):
        GPIO.output(self.ledID, True)
        self.ledState = True
    def led_off(self):
        GPIO.output(self.ledID, False)
        self.ledState = False
    def get_ledstate(self):
        return self.ledState
    def get_ledid(self):
        return self.ledID

all_vars = GPIO_controll(leds)

def speed_change(speed_change_amount):
        all_vars.set_speed((all_vars.get_speed() + speed_change_amount))

def sigterm_handler(signal, frame):
    # save the state here or do whatever you want
    try:
        try:
            PWM.set_duty_cycle("PWM0", (100))
            print "PWM turned off"
        except Exception as e:
            print "There was an error turning off: " + str(e)
        GPIO.output(leds, False)
        GPIO.cleanup() 
        print "LED turned off"
        sys.exit(0)
    except Exception as e:
        print "There was an error turning off: " + str(e)
        sys.exit(2)

signal.signal(signal.SIGTERM, sigterm_handler)

def setspeed(speed):
    if speed < 30:
        speed = 0
    if speed > 100:
        app.logger.warning('warning: tried to set speed grater than 100%')
        speed = 100
    elif speed > 80 and speed <= 100:
        if speed < 70:
            all_vars.set_speed((70))
            sleep(2) # let it speed up a little before going full pelt
    #PWM.set_duty_cycle("PWM0", (100 - speed)) ## the 100-speed is for when the inverse happens TODO make this a global setting
    all_vars.set_speed((speed))
    return speed

def setled(ledon):
    if ledon:
        all_vars.led_on()
    else:
        all_vars.led_off()


@app.route('/echo', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_echo():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"


@app.route(rocket_base_url + "/data", methods = ['POST'])
def api_rocket_data_post():
    if request.headers['Content-Type'] == 'application/json':
        try:
            return_string = ""
            if 'ledon' in request.json:
                setled(request.json['ledon'])
                return_string += "LEDon set as:" + str(request.json['ledon']) 
            if 'speed' in request.json:
                return_string += ", The speed was set to: " + str(setspeed(request.json['speed']))
            return return_string
        except:
            return "JSON was rejected by server: " + json.dumps(request.json)
        if 'ledon' in request.json:
            return_string += "The LEDs on were set as: "
        if 'speed' in request.json:
            return_string += ", The speed was set to: " + str(setspeed(request.json['speed']))
        return return_string

@app.route(rocket_base_url + "/fullspeed", methods = ['GET'])
def api_rocket_fullspeed_get():
    setspeed(100)
    return 'speed has been set to full'

@app.route(rocket_base_url + "/speeddown", methods = ['GET'])
def api_rocket_speeddown_get():
    if 'value' in request.args:
        print type(request.args['value'])
        #speed_change(-(request.args['value']))
        #return 'speed was increased by '+ str(request.args['value'])
    else:
        speed_change(-10)
        return 'speed was decreased by 10'

@app.route(rocket_base_url + "/speedup", methods = ['GET'])
def api_rocket_speedup_get():
    if 'value' in request.args:
        speed_change(request.args['value'])
        return 'speed was increased by ' + str(request.args['value'])
    else:
        speed_change(10)
        return 'speed was increased by 10'

@app.route(rocket_base_url + "/stop", methods = ['GET'])
def api_rocket_stop_get():
    setspeed(0)
    return 'rotary has been stopped'

@app.route(rocket_base_url + "/getspeed", methods = ['GET'])
def api_rocket_getspeed_get():
    return str(all_vars.get_speed())

@app.route(rocket_base_url + "/ledon", methods = ['GET'])
def api_rocket_ledon_get():
    all_vars.led_on()
    return 'rotary has been stopped'

@app.route(rocket_base_url + "/ledoff", methods = ['GET'])
def api_rocket_ledoff_get():
    all_vars.led_off()
    return 'rotary has been stopped'

@app.route(rocket_base_url + "/ledstate", methods = ['GET'])
def api_rocket_ledstate_get():
    return str(all_vars.get_ledstate())

@app.route(rocket_base_url, methods = ['GET'])
def api_rocket_get():
    return '<h1>Rocket API</h1><p>Yep, you found your way to an un-document API</p>'



@app.route(route_url, methods = ['POST','GET'])
def api_root():
    return 'Welcome\n You seem to have found my basic API for dealing with some projects'
# Finally, run the app
print "Starting the simple API server"
if __name__ == '__main__':
    # set initial default on & speed
    all_vars.led_on()
    all_vars.set_speed(50)
    app.run(host='0.0.0.0')
    print "\nExiting API server"


