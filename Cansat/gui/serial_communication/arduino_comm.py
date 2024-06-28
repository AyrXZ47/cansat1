import time

import serial
import serial.tools.list_ports
from Cansat.gui.utils.constants import DEFAULT_BAUDRATE, NULL_COMMUNICATION


# Objeto que manejará la comunicación entre
# el arduino y la interfaz

class ArduinoComm:
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
        print("pablo")
        # try:
        #     self.arduino = serial.Serial(self.port, self.baudrate, timeout=1)
        #     time.sleep(2)  # Esperar a que el puerto serie se inicialice
        #     if self.handshake_with_arduino():
        #         self.arduino_found = True
        #         print(f"Arduino found on port {self.port}")
        #     else:
        #         print(f"No Arduino on port {self.port}")
        #         self.close_communication()
        # except serial.SerialException as e:
        #     print(f"Error: {e}")

    # Cerrar comunicación
    def close_communication(self):
        if (self.arduino is None):
            return -1
        else:
            self.arduino.close()

    # Test de recibir datos
    def msg_test(self):
        if (self.validate_communication() == False):
            raise Exception(NULL_COMMUNICATION)

        while (1):
            serial_msg = self.arduino.readline()
            serial_msg = serial_msg.decode('utf-8')
            serial_msg.upper()
            print(serial_msg)

    # Validar si se ha iniciado comunicación
    def validate_communication(self):
        if (self.arduino is None or self.port is None):
            return False
        else:
            return True


