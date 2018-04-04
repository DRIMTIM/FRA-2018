#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/nxt_plugin/')

import nxt.locator
from nxt.sensor import *
import time

COLOR_VERDE = 3
COLOR_AZUL = 2
COLOR_ROJO = 5

def number2NXTPort(port_number):
    if port_number == 1:
        return PORT_1
    if port_number == 2:
        return PORT_2
    if port_number == 3:
        return PORT_3
    if port_number == 4:
        return PORT_4


print 'Detectando brick, si tarda demasiado, vuelva a enchufarlo...'
brick = None
while brick is None:
    try:
        brick = nxt.locator.find_one_brick()
    except:
        brick = None


sensor_port_number_dict = {'button': 1, 'distance': 0, 'light': 0, 'gray': 0, 'color': 0}
color_port = 3

color_sensor = Color20(brick, number2NXTPort(color_port))
color_value = color_sensor.get_sample()
print color_value

if color_value == COLOR_AZUL:
    print 'El color es Azul'
if color_value == COLOR_ROJO:
    print 'El color es Rojo'
else:
    print 'Color no reconocido'

while 1:
    estado = color_sensor.get_sample()
    if estado <> color_value:
        if estado == COLOR_AZUL:
            print 'El color es Azul'
        if estado == COLOR_ROJO:
            print 'El color es Rojo'
        else:
            print 'Color no reconocido'
        color_value = estado