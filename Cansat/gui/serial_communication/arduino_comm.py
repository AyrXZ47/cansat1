# Copyright (C) 2024  Ndahai Arenas
#
# Dragon's CanSat Monitor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Dragon's CanSat Monitor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Dragon's CanSat Monitor. If not, see <http://www.gnu.org/licenses/>.
import random
import time

import serial
import serial.tools.list_ports
from PyQt6.QtCore import QObject, pyqtSignal, QTimer

from utils.constants import DEFAULT_BAUDRATE, NULL_COMMUNICATION, DECODE_MODE, CONNWINDOW_DEBUG


# Objeto que manejará la comunicación entre
# el arduino y la interfaz

class ArduinoComm(QObject):

    serial_received = pyqtSignal(str)
    serial_error = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.port = None
        self.arduino = None
        self.baudrate = DEFAULT_BAUDRATE
        self.arduino_found = False
        self.debug = False

    # Listar puertos disponibles en el equipo (varía dependiendo del OS)
    @staticmethod
    def list_available_ports():
        ports = serial.tools.list_ports.comports()
        return ports  # list

    # Listar dispositivos disponibles (Para que lo entienda el programa)
    @staticmethod
    def list_available_devices():
        ports = ArduinoComm.list_available_ports()
        device_list = []

        for x in range(len(ports)):
            device_list.append(ports[x].device.split()[0])

        return device_list

    # Validar si se ha iniciado comunicación
    def validate_communication(self):
        if (self.arduino is None or self.port is None):
            return False
        else:
            return True

    # Seleccionar el puerto (a partir de la lista de puertos)
    def select_port(self, port):
        self.port = port  # string

    # Seleccionar velocidad (a partir de la lista)
    def select_baudrate(self, baudrate):
        self.baudrate = baudrate

    # Iniciar comunicación
    def begin_communication(self):
        if self.port == CONNWINDOW_DEBUG:
            print("DEBUG")
            self.debug = True
        else:
            self.arduino = serial.Serial(self.port, self.baudrate)


    # Cerrar comunicación
    def close_communication(self):
        if (self.arduino is None):
            return -1
        else:
            self.arduino.close()

    # Recibir datos
    def readln_serial(self):
        if self.debug == True:
            while True:
                self.serial_received.emit(self.generate_debug_data())
                time.sleep(0.5)

        if not self.validate_communication():
            raise Exception(NULL_COMMUNICATION)

        while True:
            try:
                serial_msg = self.arduino.readline()
                serial_msg = serial_msg.decode(DECODE_MODE).rstrip()
                self.serial_received.emit(serial_msg)
            except Exception as e:
                self.serial_error.emit()

    def generate_debug_data(self):
        random_numbers = [random.randint(-20, 99) for _ in range(6)]
        data_string = ",".join(map(str, random_numbers))
        print (data_string)
        return data_string





