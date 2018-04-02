#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/nxt_plugin/')

import nxt.locator
from nxt.sensor import *
import time

def number2NXTPort(port_number):
    if port_number == 0:
        return 'No conectado'
    if port_number == 1:
        return PORT_1
    if port_number == 2:
        return PORT_2
    if port_number == 3:
        return PORT_3
    if port_number == 4:
        return PORT_4


def print_sensors_ports(sensors_ports):
    print '\n'
    print ' ** Sensores y sus respectivos puertos LEGO: ** '
    for key in sensors_ports:
        print '- ' + key + ' -> ' + str(number2NXTPort(sensors_ports[key]))


sensors_ports = {'button': 0, 'distance': 0, 'light': 0, 'gray': 0, 'color': 0}

print time.strftime('%d/%m/%Y %H:%M:%S')
print 'Por favor ingrese los puertos en los que conecto los siguientes sensores: '
print '(Coloque el número del puerto en el cual esta conectado el sensor, de lo contrario ingrese 0)'

for sensor in sensors_ports:
    port = ''
    while not type(port) == int:
        try:
            port = int(raw_input('Puerto del sensor -> {}: '.format(sensor)))
            sensors_ports[sensor] = int(port)
        except ValueError:
            print 'Por favor ingrese un número...'

print_sensors_ports(sensors_ports)
