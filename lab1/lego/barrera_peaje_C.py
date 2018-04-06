#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/nxt_plugin/')

import nxt.locator
from nxt.sensor import *
from nxt.motor import *
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

def levantar_barrera():
    motor_barrera.turn(-64, 90)


def bajar_barrera():
    # chequear sentido!
    motor_barrera.turn(64, 90)


def esperar(segundos):
    time.sleep(segundos)


print 'Detectando brick, si tarda demasiado, vuelva a enchufarlo...'
brick = None
while brick is None:
    try:
        brick = nxt.locator.find_one_brick()
    except:
        brick = None

# ver que poner como distancia en la cual se empiezan a contar los 2s
DISTANCIA_MIN = 20
TIEMPO_ESPERA = 2
motor_barrera = Motor(brick, PORT_A)
sensor_dist_vehiculo = Ultrasonic(brick, PORT_1)

while 1:
    distancia_vehiculo = sensor_dist_vehiculo.get_sample()
    print str(distancia_vehiculo)

    if distancia_vehiculo < DISTANCIA_MIN:
        esperar(TIEMPO_ESPERA)
        levantar_barrera()

        distancia_vehiculo = sensor_dist_vehiculo.get_sample()
        while distancia_vehiculo <= DISTANCIA_MIN:
            distancia_vehiculo = sensor_dist_vehiculo.get_sample()

        print str(distancia_vehiculo) + ' despues del while'
        esperar(TIEMPO_ESPERA)
        bajar_barrera()
