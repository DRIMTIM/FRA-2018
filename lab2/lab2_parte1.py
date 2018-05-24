#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '/usr/share/sugar/activities/TurtleBots.activity/plugins/butia')
from pybot import pybot_client, usb4butia
from enum import Enum
import time
import datetime

FRONT_DISTANCE_SENSOR = 2
RIGHT_MOTOR = 1
LEFT_MOTOR = 0
SENSE = 0
POWER = 500
POWER_MIN = 0
ESQUIVAR = True

BLACK_COLOR_LEFT = 42000 #41000
BLACK_COLOR_RIGHT = 42000 #41000

butia = usb4butia.USB4Butia()
modules = butia.getModulesList()
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
    global offset
    power_aux = POWER_MIN + offset
    direccion = 0
    if power_aux < 0:
        direccion = 1
        power_aux = (-1) * power_aux
    if power_aux > 1000:
        power_aux = 1000

    butia.set2MotorSpeed(direccion, int(power_aux), 0, power)


def doblar_derecha(sense, power):
    global offset
    power_aux = POWER_MIN + offset
    direccion = 0
    if power_aux < 0:
        direccion = 1
        power_aux = (-1)*power_aux
    if power_aux > 1000:
        power_aux = 1000

    butia.set2MotorSpeed(0, power, direccion, int(power_aux))


def girar_izq_eje(power):
    butia.set2MotorSpeed(1, power, 0, power)


def girar_der_eje(power):
    butia.set2MotorSpeed(0, power, 1, power)


def avanzar(sense, power):
    # cambiar el sentido cuando el estado es volver
    butia.set2MotorSpeed(sense, power, sense, power)


def atras(power):
    # cambiar el sentido cuando el estado es volver
    butia.set2MotorSpeed(1, power, 1, power)
    time.sleep(0.1)


def detener():
    butia.set2MotorSpeed(0, 0, 0, 0)


def hay_obstaculo_adelante():
    global ESQUIVAR
    global val_front
    if ESQUIVAR:
        val_posta = sensor_distance_front(6)
        val_front = val_front + 0.8 * (val_posta - val_front)
        return val_front < 30000  # ver bien este valor
    else:
        return False


def hay_casa():
    if robot_state == State.ENTREGAR_PEDIDO:
        global val
        # al volver siempre retorno false
        # print('La distancia es: {}'.format(sensor_distance_right(4)))
        val_posta = sensor_distance_right(3)
        val = val + (0.2 * (val_posta - val))
        return val < 40000  # ajustar
    else:
        return False

def es_negro_sensor_izq():
    global val_grey_izq
    val_posta = sensor_grey_left(2)
    val_grey_izq = val_grey_izq + 0.8 * (val_posta - val_grey_izq)
    return val_grey_izq > BLACK_COLOR_LEFT


def es_negro_sensor_der():
    global val_grey_der
    val_posta = sensor_grey_right(4)
    val_grey_der = val_grey_der + 0.8 * (val_posta - val_grey_der)
    return val_grey_der > BLACK_COLOR_RIGHT


def llego_a_pizzeria():
    if robot_state == State.VOLVER_PIZZERIA:
        if sensor_button(5) == 1:
            return True
        else:
            return False
    else:
        return False


def finalizo_tiempo():
    if datetime.datetime.now() < tiempo_limite:
        return False
    else:
        return True


# revisar alternativa
def cambiar_direccion2():
    girar_izq_eje(POWER)
    time.sleep(0.6)  # puede ser otro valor, hay que ver
    es_negro = False
    while not es_negro:
        es_negro = es_negro_sensor_izq()  # or es_negro_sensor_der


def cambiar_direccion():
    estado = 0
    girar_izq_eje(POWER)
    # Se gira con sleep para que salga de la linea
    time.sleep(0.5)
    while True:
        #if estado == 0 and es_negro_sensor_izq():
        #    estado = 1
        if estado == 0 and es_negro_sensor_der():
            # print('salgo')
            break
        else:
            girar_izq_eje(300)


# revisar, testear
def doblar_esquivando():
    power_izq = 400  # ver estos valores
    power_der = 200  # ver estos valores
    butia.set2MotorSpeed(0, power_izq, 0, power_der)
    es_negro = False
    disminuir = 1
    direccion = 0
    while not es_negro_sensor_izq():
        butia.set2MotorSpeed(0, power_der, 0, power_izq)


# revisar, testear
def esquivar_obstaculo():
    girar_izq_eje(700)
    time.sleep(0.71)

    avanzar(SENSE, POWER)
    time.sleep(0.8)

    girar_der_eje(700)
    time.sleep(0.71)

    avanzar(SENSE, POWER)
    time.sleep(1.5)

    girar_der_eje(700)
    time.sleep(0.71)

    doblar_esquivando()


def hay_obstaculo_al_costado():
    global val
    # al volver siempre retorno false
    # print('La distancia es: {}'.format(sensor_distance_right(4)))
    val_posta = sensor_distance_right(3)
    val = val + 0.5 * (val_posta - val)
    return val < 20000 # ajustar


def esquivar_obstaculo2():
    offset = 0
    while True:
        if hay_obstaculo_adelante():
            offset -= 2
            doblar_izquierda(SENSE, POWER)
            time.sleep(1)
        elif hay_obstaculo_al_costado():
            offset = 0
            avanzar(SENSE, POWER)
            time.sleep(2)
        elif es_negro_sensor_der():
            #llego a la linea, salgo
            detener()
            offset = 0
            break
        else:
             # ajustar este factor
            doblar_derecha(SENSE, POWER)


robot_state = State.ENTREGAR_PEDIDO

for iter in modules:
    if iter.startswith('grey:2'):
        sensor_grey_left = butia.getGray

    if iter.startswith('grey:4'):
        sensor_grey_right = butia.getGray

    if iter.startswith('distanc:6'):
        sensor_distance_front = butia.getDistance

    if iter.startswith('distanc:3'):
        sensor_distance_right = butia.getDistance

    if iter.startswith('button:5'):
        sensor_button = butia.getButton

val = sensor_distance_right(3)
val_front = sensor_distance_front(6)
val_grey_izq = sensor_grey_left(2)
val_grey_der = sensor_grey_right(4)

offset = 0
doblando_izq = 0
contador_obstaculos = 0

tiempo_limite = datetime.datetime.now() + datetime.timedelta(minutes=5)
tiempo_offset = datetime.datetime.now() + datetime.timedelta(seconds=1)

while True:
    hay_casa_aux = hay_casa()
    if datetime.datetime.now() < tiempo_offset:
        hay_casa_aux = medida_anterior_hay_casa
    else:
        if hay_casa_aux:
            tiempo_offset = datetime.datetime.now() + datetime.timedelta(seconds=2)

    if finalizo_tiempo():
        detener()
        print('Se finalizo el tiempo de la ronda')
        break
    elif hay_obstaculo_adelante() and not (robot_state == State.VOLVER_PIZZERIA and contador_obstaculos == 0):
        print('ENCONTRO OBSTACULO')
        if robot_state == State.ENTREGAR_PEDIDO:
            contador_obstaculos += 1
        elif robot_state == State.VOLVER_PIZZERIA:
            contador_obstaculos -= 1

        detener()
        esquivar_obstaculo()
        print('SALIO OBSTACULO')
    elif robot_state == State.VOLVER_PIZZERIA and llego_a_pizzeria():
        print('LLEGO A PIZZERIA')
        atras(POWER)
        cambiar_direccion()
        offset = 0
        casa_actual = 0
        robot_state = State.ENTREGAR_PEDIDO
        if casa_objetivo > 3:
            detener()
            print('SE ENTREGARON TODOS LOS PEDIDOS')
            break

    elif hay_casa_aux and not medida_anterior_hay_casa:
        print('Entro HAY_CASA')
        casa_actual += 1
        if casa_objetivo == casa_actual:
            offset = 0
            casa_objetivo += 1
            print('PIZZA ENTREGADA {}'.format(casa_actual))
            robot_state = State.VOLVER_PIZZERIA
            cambiar_direccion()
    else:
        if not es_negro_sensor_der() and not es_negro_sensor_izq():
            doblando_izq = 0
            offset = 0
            avanzar(SENSE, POWER)
        elif es_negro_sensor_izq():
            if doblando_izq != 1:
                offset = 0
            doblando_izq = 1
            offset -= 1
            doblar_izquierda(SENSE, POWER)
        else:
            if doblando_izq != 2:
                offset = 0
            doblando_izq = 2
            offset -= 1
            doblar_derecha(SENSE, POWER)


    medida_anterior_hay_casa = hay_casa_aux


   # print('Valor boton: {}'.format(sensor_grey_left(4)))

