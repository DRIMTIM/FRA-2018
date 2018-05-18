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
POWER = 1000
POWER_MIN = 600

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


def avanzar(sense, power):
    # cambiar el sentido cuando el estado es volver
    butia.set2MotorSpeed(sense, power, sense, power)


def atras(power):
    # cambiar el sentido cuando el estado es volver
    butia.set2MotorSpeed(1, power, 1, power)
    time.sleep(0.5)


def detener():
    print('Se detuvo')
    butia.set2MotorSpeed(0, 0, 0, 0)


def hay_obstaculo_adelante():
    global val_front
    val_posta = sensor_distance_front(6)
    val_front = val_front + 0.8 * (val_posta - val_front)
    return val_front < 35000  # ver bien este valor


def hay_casa():
    global val
    # al volver siempre retorno false
    # print('La distancia es: {}'.format(sensor_distance_right(4)))
    val_posta = sensor_distance_right(3)
    val = val + 0.8 * (val_posta - val)
    return val < 40000


def es_negro_sensor_izq():
    global val_grey_izq
    val_posta = sensor_grey_left(2)
    val_grey_izq = val_grey_izq + 0.5 * (val_posta - val_grey_izq)
    return val_grey_izq > BLACK_COLOR_LEFT


def es_negro_sensor_der():
    global val_grey_der
    val_posta = sensor_grey_right(4)
    # teniamos val_grey_izq en la formula de aca abajo
    val_grey_der = val_grey_der + 0.5 * (val_posta - val_grey_der)
    return val_grey_der > BLACK_COLOR_RIGHT


def llego_a_pizzeria():
    if sensor_button(5) == 1:
        return True
    else:
        return False


def finalizo_tiempo():
    return False


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
    time.sleep(0.4)
    while True:
        if estado == 1 and es_negro_sensor_izq():
            estado = 2
        elif estado == 2 and es_negro_sensor_der():
            print('salgo')
            break
        else:
            if estado == 0:
                estado = 1
            girar_izq_eje(POWER)


# revisar, testear
def doblar_esquivando():
    power_izq = 800  # ver estos valores
    power_der = 600  # ver estos valores
    butia.set2MotorSpeed(0, power_der, 0, power_izq)
    es_negro = False
    disminuir = 1
    direccion = 0
    while not es_negro:
        if power_der < 0:
            direccion = 1
            power_der = -1 * power_der
        if power_der > 1000:
            power_der = 1000
        es_negro = es_negro_sensor_der()  # or es_negro_sensor_izq
        butia.set2MotorSpeed(0, power_izq, direccion, power_der - disminuir)
        disminuir -= 1  # ver este valor


# revisar, testear
def esquivar_obstaculo():
    girar_izq_eje(POWER)
    time.sleep(0.5)
    doblar_esquivando()


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

while True:
    hay_casa_aux = hay_casa()
    if finalizo_tiempo():
        detener()
        print('Se finalizo el tiempo de la ronda')
        break
    elif hay_obstaculo_adelante():
        detener()
        esquivar_obstaculo()
    elif robot_state == State.VOLVER_PIZZERIA and llego_a_pizzeria():
        print('LLEGO A PIZZERIA')
        robot_state = State.ENTREGAR_PEDIDO
        atras(POWER)
        cambiar_direccion()
        offset = 0
        casa_actual = 0
        if casa_objetivo > 3:
            detener()
            print('SE ENTREGARON TODOS LOS PEDIDOS')

    elif robot_state == State.ENTREGAR_PEDIDO and hay_casa_aux and not medida_anterior_hay_casa:
        casa_actual += 1
        offset = 0
        if casa_objetivo == casa_actual:
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
            offset -= 1.3
            doblar_izquierda(SENSE, POWER)
        else:
            if doblando_izq != 2:
                offset = 0
            doblando_izq = 2
            offset -= 1.3
            doblar_derecha(SENSE, POWER)

    medida_anterior_hay_casa = hay_casa_aux

#    print('Valor boton: {}'.format(sensor_button(5)))

