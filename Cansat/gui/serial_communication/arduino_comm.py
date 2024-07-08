import time

import serial
import serial.tools.list_ports
from PyQt6.QtCore import QObject, pyqtSignal

from Cansat.gui.utils.constants import DEFAULT_BAUDRATE, NULL_COMMUNICATION


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


    # Seleccionar el puerto (a partir de la lista de puertos)
    def select_port(self, port):
        self.port = port  # string

    # Seleccionar velocidad (a partir de la lista)
    def select_baudrate(self, baudrate):
        self.baudrate = baudrate

    def handshake_with_arduino(self, timeout=10):
        start_time = time.time()
        while True:
            if self.arduino.in_waiting > 0:
                line = self.arduino.readline().decode('utf-8').strip()
                if line == "HANDSHAKE":
                    print("Handshake received from Arduino")
                    self.arduino.write(b"CONFIRM\n")
                    print("Handshake confirmed")
                    return True
            # Verificar si el timeout ha sido alcanzado
            if time.time() - start_time > timeout:
                print(f"Timeout reached on port {self.port}")
                return False
            time.sleep(0.1)

    # Iniciar comunicación
    def begin_communication(self):
        self.arduino = serial.Serial(self.port, self.baudrate)

    # Cerrar comunicación
    def close_communication(self):
        if (self.arduino is None):
            return -1
        else:
            self.arduino.close()

    # Test de recibir datos
    def readln_serial(self):
        if not self.validate_communication():
            raise Exception(NULL_COMMUNICATION)

        while True:
            try:
                serial_msg = self.arduino.readline()
                serial_msg = serial_msg.decode('utf-8').rstrip()
                self.serial_received.emit(serial_msg)
            except Exception as e:
                self.serial_error.emit()


    # Validar si se ha iniciado comunicación
    def validate_communication(self):
        if (self.arduino is None or self.port is None):
            return False
        else:
            return True


