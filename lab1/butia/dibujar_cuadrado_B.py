#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/butia')
from pybot import pybot_client, usb4butia
import time

RIGHT_MOTOR = 1
LEFT_MOTOR = 0
SENSE = 1
POWER = 500

CICLOS = 50

butia = usb4butia.USB4Butia()
modules = butia.getModulesList()
port_number = 0

if modules == ['-1']:
    print('Problema de comunicación con la placa USB4Butiá, revise los permisos udev: ' +
          'https://www.fing.edu.uy/inco/proyectos/butia/mediawiki/index.php/Preguntas_frecuentes')
else:
    print('Se detectaron los siguientes servicios disponibles: ', modules)


def doblar_izquierda(sense, power):
    # Avanzo motor izquierdo en sentido contrario al derecho
    # Avanzo con el motor derecho
    butia.set2MotorSpeed(sense, power, 0, power)


def avanzar(sense, power):
    butia.set2MotorSpeed(sense, power, sense, power)


def detener():
    butia.set2MotorSpeed(0, 0, 0, 0)


while 1:
    avanzar(SENSE, POWER)
    # dejo avanzar 2 segundos
    time.sleep(2)
    detener()
    # doblo
    doblar_izquierda(SENSE, POWER)
    # dejo doblar 0.5 segundos
    time.sleep(0.7)
    detener()

butia.close()
