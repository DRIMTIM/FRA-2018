#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, MINA/INCO/UDELAR
#
# lego NXT data acquisition program v.0.4
# to use fill the sensor_port_number_dict dictionary with the port number of the sensor,
# if the sensor is not connected use 0 as port number
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/nxt_plugin/')

import nxt.locator
from nxt.sensor import *
import time

SAMPLES = 400

def number2NXTPort(port_number):
    if port_number == 1:
        return PORT_1
    if port_number == 2:
        return PORT_2
    if port_number == 3:
        return PORT_3
    if port_number == 4:
        return PORT_4

def storeExperiment(sensor_name, samples, samples_timestamps):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = sensor_name + "-" + timestr + ".log"
    file = open(filename,"w")
    for iter in xrange(len(samples)):
        file.write(samples_timestamps[iter] + " " + str(samples[iter]) + "\n")
    file.close()
    print "se guardó el experimento: ", filename

def get_samples(get_value):
    samples = []
    timestamps = []
    start_millisec = time.time()*1000.0
    for sample_number in xrange(SAMPLES):
        val = get_value()
        val_time = str(time.time()*1000.0 - start_millisec)
        if val == -1:
            error = True
        else:
            samples.append(val)
            timestamps.append(val_time)
            error = False
    if error:
        print 'Fallo de comunicación con el sensor, revise conexión del cable que lo conecta el brick, si el problema persiste cambielo'
    return error, samples, timestamps

#The behaviour of the light sensor changes depending on the state of the led (on: is a grayscale sensor, off: is a ambient light sensor)
def getGrayValue():
    gray_port = sensor_port_number_dict['gray']
    gray = Light(brick, number2NXTPort(gray_port))
    gray.set_illuminated(True)
    value = gray.get_lightness()
    gray.set_illuminated(False)
    return value

def getLightValue():
    light_port = sensor_port_number_dict['light']
    light = Light(brick, number2NXTPort(light_port))
    light.set_illuminated(False)
    return light.get_lightness()

print 'Detectando brick, si tarda demasiado, vuelva a enchufarlo...'
brick = None
while brick is None:
    try:
        brick = nxt.locator.find_one_brick()
    except:
        brick = None

#Fill this dictionary with the port where each sensor is connected, use 0 if the sensor is not connected; example:
# sensor_port_number_dict = {'button': 1, 'distance': 0, 'light': 0, 'gray': 0, 'color': 0}
# corresponds with the button sensor connected to the port number one and the rest disconnected.
sensor_port_number_dict = {'button': 0, 'distance': 0, 'light': 0, 'gray': 0, 'color': 0}
sensor_callback_dict = {}
sensor_present = []
light_port = int(sensor_port_number_dict['light'])
gray_port = int(sensor_port_number_dict['gray'])
button_port = int(sensor_port_number_dict['button'])
distance_port = int(sensor_port_number_dict['distance'])
color_port = int(sensor_port_number_dict['color'])

if light_port != 0:
    sensor_callback_dict['light'] = getLightValue
    sensor_present.append('light')

if gray_port != 0:
    sensor_callback_dict['gray'] = getGrayValue
    sensor_present.append('gray')

if distance_port != 0:
    distance = Ultrasonic(brick, number2NXTPort(distance_port))
    sensor_callback_dict['distance'] = distance.get_sample
    sensor_present.append('distance')

if button_port != 0:
    button = Touch(brick, number2NXTPort(button_port))
    sensor_callback_dict['button'] = button.get_sample
    sensor_present.append('button')

if color_port != 0:
    color = Color20(brick, number2NXTPort(color_port))
    sensor_callback_dict['color'] = color.get_sample
    sensor_present.append('color')

for sensor_name in sensor_present:
    port_number = int(sensor_port_number_dict[sensor_name])
    print "sensor: " + sensor_name + " " + "conectado al puerto: ", port_number
    error, samples, timestamps = get_samples(sensor_callback_dict[sensor_name])

    if not error:
        storeExperiment(sensor_name, samples, timestamps)

#TODO free resources
