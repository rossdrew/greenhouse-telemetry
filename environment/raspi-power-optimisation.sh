#!/bin/bash

#-25mA
/usr/bin/tvservice -o

#-5mA per LED
echo 0 | sudo tee /sys/class/leds/led0/brightness
echo 0 | sudo tee /sys/class/leds/led1/brightness

