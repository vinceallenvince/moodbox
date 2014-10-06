import RPi.GPIO as GPIO
import time

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
    new_a = GPIO.input(old_channel_a)
    new_b = GPIO.input(old_channel_b)
    if new_a != old_channel_a or new_b != old_channel_b :
        if old_channel_a == 0 and new_a == 1 :
            result = (old_channel_b * 2 - 1)
        elif old_channel_b == 0 and new_b == 1 :
            result = -(old_channel_a * 2 - 1)
    old_channel_a, old_channel_b = new_a, new_b
    time.sleep(0.001)
    return result

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

x = 0
y = 0

while True:
    change_channel = get_channel_turn()
    if change_channel != 0 :
      x = x + change_channel
      print(x)
    change_volume = get_volume_turn()
    if change_volume != 0 :
      y = y + change_volume
      print(y)