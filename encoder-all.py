import RPi.GPIO as GPIO
import time
import urllib2

GPIO.setmode(GPIO.BCM)

input_channel_A = 12
input_channel_B = 16

GPIO.setup(input_channel_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(input_channel_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

old_channel_a = True
old_channel_b = True

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
    if x <= 5:
        urllib2.urlopen("http://127.0.0.1:15004/action?action=preset-" + `x`).read()

def set_volume(x):
    print(scale(x, (0, 100), (0, 65535)))

def scale(val, src, dst):
    return ((val - src[0]) / (src[1]-src[0])) * (dst[1]-dst[0]) + dst[0]

while True:
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
