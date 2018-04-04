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
DISTANCIA_MIN = 10
TIEMPO_ESPERA = 2
motor_barrera = Motor(brick, PORT_A)
sensor_dist_vehiculo = Ultrasonic(brick, PORT_1)
4
print 'Paso'

while 1:
    distancia_vehiculo = sensor_dist_vehiculo.get_sample()

    if distancia_vehiculo < DISTANCIA_MIN:
        esperar(TIEMPO_ESPERA)
        levantar_barrera()

        distancia_vehiculo = distancia_vehiculo.get_sample()
        print distancia_vehiculo + ' antes while'
        while distancia_vehiculo <= DISTANCIA_MIN:
            distancia_vehiculo = distancia_vehiculo.get_sample()

        print distancia_vehiculo + ' despues del while'
        bajar_barrera()
