import sys

# Running all the tests to make sure the pico is connected to internet and at_sign
shouldRun = str(input('Run? (y/n): ')).lower()
if shouldRun != 'y':
    sys.exit(1)
del sys

from lib.at_client.io_util import read_settings

ssid, password, atSign = read_settings()
del read_settings

print('Connecting to WiFi %s...' % ssid)
from lib.wifi import init_wlan

init_wlan(ssid, password)
del ssid, password, init_wlan
# Connection to the atsign
from lib.at_client.at_client import AtClient

atClient = AtClient(atSign)
del AtClient
atClient.pkam_authenticate(verbose=True)

import machine
from machine import Pin
import time

appAtsign = "@coffee52"
key = 'distance'
# Define the pins for Ultrasonic sensor
trigger_pin = 4
echo_pin = 5

# Define the pins for the speaker
speaker = PWM(Pin(19))

# Define the pins for led
led_r = Pin(16, Pin.OUT)
led_g = Pin(17, Pin.OUT)
led_b = Pin(18, Pin.OUT)

# Define the frequency for the LED
led_r.freq(2000)
led_g.freq(2000)
led_b.freq(2000)

trigger = Pin(trigger_pin, Pin.OUT)
echo = Pin(echo_pin, Pin.IN)
led = machine.Pin("LED", machine.Pin.OUT)


def distance():
    while True:
        trigger.high()
        time.sleep_us(11)
        trigger.low()
        while (echo.value() == 0):
            pass  # wait for echo
        lastreadtime = time.ticks_us()  # record the time when signal went HIGH
        while (echo.value() == 1):
            pass  # wait for echo to finish
        echotime = time.ticks_us() - lastreadtime

        # if echotime is more than 37000, than there is no obstacle around us.
        if echotime > 37000:
            print("No obstacle detected")
            # Lets display a Blue color for no obstacle detected
            led(0, 0, 255)

        # if the echotime is less than 588 microseconds, then it means the object is close
        # 588 ms is 10cm of the distance that I considered close.
        if echotime < 588:
            print("Careful!! Obstacle is close!")
            led.toggle()
            time.sleep(0.5)
            led.toggle()
            # Display red color if close
            # led(255, 0, 0)
            speaker()

            # if the object is on the appropriate distance we divide the time traveled from one
            # sensor that sends an impulse to another one that receives it by the speed of sound
            # in order to get an actual distance
        else:
            distance = (echotime * 0.034) / 2
            print("Obstace distance= {}cm".format(distance))
            # Display green color for good
            # led(0, 255, 0)
        time.sleep(1)


# This is the function to create a flashing RGB LED any color we want.

def led(r, g, b):
    while True:
        # range of random numbers
        # R = random.randint(0, 65535)
        # G = random.randint(0, 65535)
        # B = random.randint(0, 65535)

        print(R, G, B)
        Led_R.duty_u16(R)
        Led_G.duty_u16(G)
        Led_B.duty_u16(B)
        utime.sleep_ms(100)


def speaker():
    while True:
        distance = CheckDistance()
        print(distance)
        speaker.duty_u16(3000)
        speaker.freq(1700)
        utime.sleep(0.05)
        speaker.duty_u16(0)
        utime.sleep(CheckDistance() / 1000)
