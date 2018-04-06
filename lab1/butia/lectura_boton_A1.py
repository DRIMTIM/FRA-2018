#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/butia')
from pybot import pybot_client, usb4butia
import time

butia = usb4butia.USB4Butia()
modules = butia.getModulesList()
port_number = 0
get_value_function = butia.getButton

if modules == ['-1']:
    print('Problema de comunicación con la placa USB4Butiá, revise los permisos udev: ' +
          'https://www.fing.edu.uy/inco/proyectos/butia/mediawiki/index.php/Preguntas_frecuentes')
else:
    print 'Se detectaron los siguientes servicios disponibles: ', modules

for iter in modules:
    if iter.startswith('button:'):
        port_number = iter.strip('button:')
        sensor_name = 'ButiaContactSensor'
        value = butia.getButton(port_number)
        print 'Valor inicial del {}: {}'.format(sensor_name, value)

estado = butia.getButton(port_number)
while 1:
    value = get_value_function(port_number)
    if estado <> value:
        print 'Se pulsó el botón el valor es: {}'.format(value)
        estado = value
