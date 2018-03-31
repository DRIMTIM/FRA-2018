#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/nxt_plugin/')

import nxt.locator
from nxt.sensor import *
import time


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


sensor_port_number_dict = {'button': 0, 'distance': 0, 'light': 0, 'gray': 0, 'color': 0}
button_port = int(sensor_port_number_dict['button'])

if button_port != 0:
    button = Touch(brick, number2NXTPort(button_port))
    value = button.get_sample()
    print('Valor inicial del botón: {}'.format(value))

while not value == 1:
    value = button.get_sample()
    if value == 1:
        print('Se pulsó el botón el valor es: {}'.format(value))
    else:
        print('El valor actual del botón es: {}'.format(value))