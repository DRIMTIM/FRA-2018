#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/butia')
from pybot import pybot_client, usb4butia
import time

RIGHT_MOTOR = 1
LEFT_MOTOR = 0
SENSE = 1
POWER = 300

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
    # Detengo motor izquierdo
    butia.setMotorSpeed(LEFT_MOTOR, 0, 0)
    # Avanzo con el motor derecho
    butia.setMotorSpeed(RIGHT_MOTOR, sense, power)


def doblar_derecha(sense, power):
    # Detengo motor derecho
    butia.setMotorSpeed(RIGHT_MOTOR, 0, 0)
    # Avanzo con el motor izquierdo
    butia.setMotorSpeed(LEFT_MOTOR, sense, power)


def avanzar(sense, power):
    butia.set2MotorSpeed(sense, power, sense, power)


i = 0
while i < CICLOS:
    avanzar(SENSE, POWER)
    # dejo avanzar 2 segundos
    time.sleep(2)
    # doblo
    doblar_izquierda(SENSE, POWER)
    # dejo doblar 0.5 segundos
    time.sleep(0.5)
    # aumento un ciclo
    i += 1

butia.close()
