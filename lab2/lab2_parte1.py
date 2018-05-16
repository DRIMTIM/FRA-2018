#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/butia')
from pybot import pybot_client, usb4butia
from enum import Enum
import time

FRONT_DISTANCE_SENSOR = 2
RIGHT_MOTOR = 1
LEFT_MOTOR = 0
SENSE = 0
POWER = 500
POWER_MIN = 100

BLACK_COLOR_LEFT = 42000
BLACK_COLOR_RIGHT = 36000

butia = usb4butia.USB4Butia()
modules = butia.getModulesList()
sensor_name = " "
sensor_callback_dict = {}
sensor_port_number_dict = {}
sensor_present = []
casa_actual = 0
casa_objetivo = 1
medida_anterior_hay_casa = False


class State(Enum):
    ENTREGAR_PEDIDO = 1
    VOLVER_PIZZERIA = 2
    FINALIZADO = 3


if modules == ['-1']:
    print('Problema de comunicación con la placa USB4Butiá, revise los permisos udev: ' +
          'https://www.fing.edu.uy/inco/proyectos/butia/mediawiki/index.php/Preguntas_frecuentes')
else:
    print('Se detectaron los siguientes servicios disponibles: ', modules)


def doblar_izquierda(sense, power):
    # cambiar el sentido cuando el estado es volver
    # print('Se ha doblado a la izquierda')
    # Avanzo motor izquierdo en sentido contrario al derecho
    # Avanzo con el motor derecho
   # butia.set2MotorSpeed(1, power, 0, power)
    butia.set2MotorSpeed(0, POWER_MIN, 0, power)


def doblar_derecha(sense, power):
    # cambiar el sentido cuando el estado es volver
    # print('Se ha doblado a la derecha')
    # Avanzo motor izquierdo en sentido contrario al derecho
    # Avanzo con el motor derecho
    #butia.set2MotorSpeed(0, power, 1, power)
    butia.set2MotorSpeed(0, power, 0, POWER_MIN)


def avanzar(sense, power):
    # cambiar el sentido cuando el estado es volver
    butia.set2MotorSpeed(sense, power, sense, power)


def detener():
    print('Se detuvo')
    butia.set2MotorSpeed(0, 0, 0, 0)


def hay_obstaculo_adelante():
    return False


def hay_casa():
    # al volver siempre retorno false
    # print('La distancia es: {}'.format(sensor_distance_right(4)))
    return sensor_distance_right(4) < 50000


def es_negro_sensor_izq():
    return sensor_grey_left(6) > BLACK_COLOR_LEFT


def es_negro_sensor_der():
    return sensor_grey_right(5) > BLACK_COLOR_RIGHT


def llego_a_pizzeria():
    return False


def finalizo_tiempo():
    return False


robot_state = State.ENTREGAR_PEDIDO

for iter in modules:
    if iter.startswith('grey:6'):
        sensor_grey_left = butia.getGray

    if iter.startswith('grey:5'):
        sensor_grey_right = butia.getGray

    if iter.startswith('distanc:3'):
        sensor_distance_front = butia.getDistance

    if iter.startswith('distanc:4'):
        sensor_distance_right = butia.getDistance

    if iter.startswith('button:'):
        sensor_button = butia.getButton


while True:
    hay_casa_aux = hay_casa()
    if finalizo_tiempo():
        detener()
        print('Se finalizo el tiempo de la ronda')
        exit
    elif hay_obstaculo_adelante():
        detener()
    elif hay_casa_aux and not medida_anterior_hay_casa:
        casa_actual += 1
        if casa_objetivo >= casa_actual:
            casa_objetivo += 1
            print('PIZZA ENTREGADA')
            # robot_state = State.VOLVER_PIZZERIA
            detener()
    else:
        if not es_negro_sensor_der() and not es_negro_sensor_izq():
            avanzar(SENSE, POWER)
        elif not es_negro_sensor_der() and not es_negro_sensor_izq():
            avanzar(SENSE, POWER)
        elif es_negro_sensor_izq():
            doblar_izquierda(SENSE, POWER)
        else:
            doblar_derecha(SENSE, POWER)

    medida_anterior_hay_casa = hay_casa_aux

    # print('Valor distancia: {}'.format(sensor_distance_right(4)))
