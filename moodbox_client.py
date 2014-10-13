import RPi.GPIO as GPIO
import time
from urllib2 import Request, urlopen, URLError
import json
from subprocess import call

GPIO.setmode(GPIO.BCM)

ready = False
base_client_uri = "http://127.0.0.1:15004"
base_server_uri = "http://162.243.120.32:8888"
title_uri = False
current_channel = False
status_check_count = 0
status_check_max = 200
fetching_new_tracks = False
playing = False

###################

LED = 23
LED_count = 0
LED_state = 1
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, True)

def led_on():
    GPIO.output(LED, True)

def led_off():
    GPIO.output(LED, False)

###################

input_channel_A = 12
input_channel_B = 16

GPIO.setup(input_channel_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_channel_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

old_channel_a = True
old_channel_b = True

init_channel_val = 3

button_shutdown = 5
GPIO.setup(button_shutdown, GPIO.IN, pull_up_down=GPIO.PUD_UP)

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

input_volume_A = 13
input_volume_B = 21

GPIO.setup(input_volume_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_volume_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

old_volume_a = True
old_volume_b = True

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

y = 15 #initial volume

def play():
    global playing
    playing = True
    req = Request(base_client_uri + "/action?action=play")
    urlopen(req)

def pause():
    global playing
    playing = False
    req = Request(base_client_uri + "/action?action=pause")
    urlopen(req)

def set_channel(x):
    global current_channel
    x = x + init_channel_val
    if x > 0 and x < 6:
        current_channel = x;
        req = Request(base_client_uri + "/action?action=preset-" + `x`)
        urlopen(req)

def set_volume(y):
    if y >= -10 or y <= 10:
    	vol = scale(y, (-15.0, +15.0), (+0.0, +100.0))
        call("amixer set PCM " + `vol` + "%", shell=True)
        if vol < 50 and playing == True:
            pause()
        elif vol >= 50 and playing == False:
            play()

def set_max_connect_volume():
    req = Request(base_client_uri + "/action?action=volume&level=65535")
    urlopen(req)

def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

def check_status():

    global title_uri, fetching_new_tracks, x

    req = Request(base_client_uri + "/status-data")
    response = urlopen(req)
    data = response.read()
    json_data = json.loads(data)

    if json_data.get("playing") == "0":
        if fetching_new_tracks == False :
            print "Fetching new tracks!"
            fetching_new_tracks = True
            push_playlist(current_channel)
    else:
        if title_uri == False: # this is the first track
            title_uri = json_data["title_uri"]
        elif title_uri != json_data["title_uri"] : # playing a new track; remove the old
            shift_playlist(title_uri, current_channel)
            title_uri = json_data["title_uri"]
    #TODO: if we're getting new tracks, we don't need to remove the last track

def shift_playlist(title_uri, current_channel):
    print "Removing track " + title_uri.encode("ascii") + " from moodbox-ch" + str(current_channel) + "."
    req = Request(base_server_uri + "/shiftplaylist?uri=" + title_uri.encode("ascii") + "&num=" + str(current_channel))
    response = urlopen(req)

def push_playlist(current_channel):
    req = Request(base_server_uri + "/pushplaylist?num=" + str(current_channel))
    response = urlopen(req)
    set_channel(x / 3)
    play()
    fetching_new_tracks == False

def shutdown_pi():
    call(["/home/pi/shutdown.sh"])

def check_ready():
    global ready, LED_count, LED_state, Request, URLError
    if ready == False :
        req = Request(base_client_uri + "/status-data")
        try:
            response = urlopen(req)
        except URLError as e:
            if hasattr(e, "reason"):
                LED_count += 1
                if LED_count > 40:
                    LED_state *= -1
                    LED_count = 0
                if LED_state == 1:
                    led_on()
                else:
                    led_off()
                #print 'We failed to reach a server.'
                #print 'Reason: ', e.reason
            elif hasattr(e, "code"):
                #print 'The server couldn\'t fulfill the request.'
                #print 'Error code: ', e.code
                pass
        else:
            # everything is fine
            ready = True
            led_on()
            set_max_connect_volume() # max the Spotify connect volume
            set_volume(y)
            set_channel(0) # range is -2 -> 2
            play()

while True:
    if ready == True :
        change_channel = get_channel_turn()
        if change_channel != 0 :
            x = x + change_channel
            if x % 3 == 0 :
                set_channel(x / 3)

        change_volume = get_volume_turn()
        if change_volume != 0 :
          y = y + change_volume
          set_volume(y)

        # check status on an interval
        status_check_count += 1
        if status_check_count > status_check_max :
            status_check_count = 0
            check_status()

        shutdown_state = GPIO.input(button_shutdown)
        if shutdown_state == False:
            print('shutdown button Pressed')
            shutdown_pi()
            time.sleep(0.2)

    else:
        check_ready()


