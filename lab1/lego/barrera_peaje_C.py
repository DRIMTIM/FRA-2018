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

def levantar_barrera():
    motor_barrera.turn(500, 90)


def bajar_barrera():
    # chequear sentido!
    motor_barrera.turn(-500, 90)


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
DISTANCIA_MIN = 1000
DISTANCIA_REF = 2500
TIEMPO_ESPERA = 2
ESPERA_MIN = 0.1
motor_barrera = Motor(brick, PORT_B)
sensor_dist_vehiculo = Ultrasonic(brick, PORT_1)
sensor_dist_ref = Ultrasonic(brick, PORT_2)

while 1:
    distancia_vehiculo = sensor_dist_vehiculo.get_sample()

    if distancia_vehiculo < DISTANCIA_MIN:
        esperar(TIEMPO_ESPERA)
        levantar_barrera()

        distancia_ref = sensor_dist_ref.get_sample()
        while distancia_ref >= DISTANCIA_REF:
            distancia_ref = sensor_dist_ref.get_sample()

        while distancia_ref < DISTANCIA_REF:
            distancia_ref = sensor_dist_ref.get_sample()

        bajar_barrera()
