#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, MINA/INCO/UDELAR
#
# USB4Butiá data acquisition program v.0.2
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import sys
sys.path.insert(0,'/usr/share/sugar/activities/TurtleBots.activity/plugins/butia')
from pybot import pybot_client, usb4butia
import time

SAMPLES = 400

def storeExperiment(sensor_name, samples, samples_timestamps, filter_samples, filter_sample2):
    timestr = time.strftime("%Y%m%d-%H%M%S")
    filename = sensor_name + "-" + timestr + ".log.filter"
    file = open(filename,"w")
    for iter in xrange(len(samples)):
        file.write(samples_timestamps[iter] + "  " + str(samples[iter]) + "  " + str(filter_samples[iter]) + "  " + str(filter_sample2[iter]) + "\n")
    file.close()
    print "se guardó el experimento: ", filename

def get_samples(port_number, get_value):
    samples = []
    timestamps = []
    filter_samples = []
    filter_samples2 = []
    start_millisec = time.time()*1000.0
    if port_number > 0:
        for sample_number in xrange(SAMPLES):
            if sample_number == 0:
                val = get_value(port_number)
                val_posta = val
                val2 = val
            else:
                val_posta = get_value(port_number)
                val = val + 0.9 * (val_posta - val)
                val2 = val2 + 0.1 * (val_posta - val2)


            val_time = str(time.time()*1000.0 - start_millisec)
            if val == -1:
                error = True
            else:
                filter_samples2.append(val2)
                filter_samples.append(val)
                samples.append(val_posta)
                timestamps.append(val_time)
                error = False
    else:
        error = True
    if error:
        print 'Fallo de comunicación con el sensor, revise conexión del cable que lo conecta a la placa USB4Butiá, si el problema persiste cambielo'
    return error, samples, timestamps, filter_samples, filter_samples2

butia = usb4butia.USB4Butia()
#butia = pybot_client.robot() #for communication through pybot server
modules = butia.getModulesList()
port_number = 0
get_value_function = butia.getButton #dummy initial value
sensor_name = " "
sensor_callback_dict = {}
sensor_port_number_dict = {}
sensor_present = []

if modules == ['-1']:
    print "Problema de comunicación con la placa USB4Butiá, revise los permisos udev: https://www.fing.edu.uy/inco/proyectos/butia/mediawiki/index.php/Preguntas_frecuentes"
else:
    print "Se detectaron los siguientes servicios disponibles: ", modules

for iter in modules:
    if iter.startswith('grey:'):
        port_number = iter.strip('grey:')
        get_value_function = butia.getGray
        sensor_name = "ButiaGrayScaleSensor"
        sensor_present.append(sensor_name)
        sensor_callback_dict[sensor_name] = get_value_function
        sensor_port_number_dict[sensor_name] = port_number

    if iter.startswith('light:'):
        port_number = iter.strip('light:')
        get_value_function = butia.getLight
        sensor_name = "ButiaLightSensor"
        sensor_present.append(sensor_name)
        sensor_callback_dict[sensor_name] = get_value_function
        sensor_port_number_dict[sensor_name] = port_number

    if iter.startswith('distanc:'):
        port_number = iter.strip('distanc:')
        get_value_function = butia.getDistance
        sensor_name = "ButiaDistanceSensor"
        sensor_present.append(sensor_name)
        sensor_callback_dict[sensor_name] = get_value_function
        sensor_port_number_dict[sensor_name] = port_number

    if iter.startswith('button:'):
        port_number = iter.strip('button:')
        get_value_function = butia.getButton
        sensor_name = "ButiaContactSensor"
        sensor_present.append(sensor_name)
        sensor_callback_dict[sensor_name] = get_value_function
        sensor_port_number_dict[sensor_name] = port_number

#TODO add more sensor callbacks for new modules like voltage, resistence, and generic

for sensor_name in sensor_present:
    port_number = int(sensor_port_number_dict[sensor_name])
    print "encontré el sensor: " + sensor_name + " " + "conectado al puerto: ", port_number
    error, samples, timestamps, filter_samples, filter_samples2 = get_samples(port_number, sensor_callback_dict[sensor_name])

    if not error:
        storeExperiment(sensor_name, samples, timestamps, filter_samples, filter_samples2)

butia.close()



