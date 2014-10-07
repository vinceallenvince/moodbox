import RPi.GPIO as GPIO
import time
from urllib2 import Request, urlopen, URLError

GPIO.setmode(GPIO.BCM)

ready = False

###################

LED = 25
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, True)

###################

input_channel_A = 12
input_channel_B = 16

GPIO.setup(input_channel_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_channel_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

old_channel_a = True
old_channel_b = True

init_channel_val = 3

def get_channel_turn():
    # return -1, 0, or +1
    global old_channel_a, old_channel_b
    result = 0
    new_a = GPIO.input(input_channel_A)
    new_b = GPIO.input(input_channel_B)
    if new_a != old_channel_a or new_b != old_channel_b :
        if old_channel_a == 0 and new_a == 1 :
            result = (old_channel_b * 2 - 1)
        elif old_channel_b == 0 and new_b == 1 :
            result = -(old_channel_a * 2 - 1)
    old_channel_a, old_channel_b = new_a, new_b
    time.sleep(0.001)
    return result

x = 0

###################

input_volume_A = 18
input_volume_B = 23

GPIO.setup(input_volume_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_volume_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

old_volume_a = True
old_volume_b = True

init_volume_val = 32768

def get_volume_turn():
    # return -1, 0, or +1
    global old_volume_a, old_volume_b
    result = 0
    new_a = GPIO.input(input_volume_A)
    new_b = GPIO.input(input_volume_B)
    if new_a != old_volume_a or new_b != old_volume_b :
        if old_volume_a == 0 and new_a == 1 :
            result = (old_volume_b * 2 - 1)
        elif old_volume_b == 0 and new_b == 1 :
            result = -(old_volume_a * 2 - 1)
    old_volume_a, old_volume_b = new_a, new_b
    time.sleep(0.001)
    return result

y = 0

def set_channel(x):
    x = x + init_channel_val
    if x > 0 and x < 6:
        urllib2.urlopen("http://127.0.0.1:15004/action?action=preset-" + `x`).read()

def set_volume(x):
    vol = scale(x, (0.0, +20.0), (0.0, +65535.0)) + init_volume_val
    print(vol)
    if vol > 0 and vol < 65535 :
        urllib2.urlopen("http://127.0.0.1:15004/action?action=volume&level=" + `vol`).read()

def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def check_ready():
    # response = urllib2.urlopen("http://127.0.0.1:15004/status-data")
    # check if refspeaker webserver is running; if so, ready = True
    # need to handle error here when server is not running
    # ready = True
    #

    global ready, urllib2, URLError
    if ready == False :
        req = urllib2.Request("http://127.0.0.1:15004/status-data")
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server couldn\'t fulfill the request.'
                print 'Error code: ', e.code
        else:
            # everything is fine
            ready = True

def start():
    while True:
        if ready == True :
            change_channel = get_channel_turn()
            if change_channel != 0 :
                x = x + change_channel
                print(x)
                if x % 5 == 0 :
                    set_channel(x / 5)

            change_volume = get_volume_turn()
            if change_volume != 0 :
              y = y + change_volume
              print(y)
              set_volume(y)
        else:
            check_ready()

start()
