import serial
import serial.tools.list_ports
from utils.constants import DEFAULT_BAUDRATE, NULL_COMMUNICATION


# Objeto que manejará la comunicación entre
# el arduino y la interfaz

class ArduinoComm:
    def __init__(self):
        super().__init__()
        self.port = None
        self.arduino = None
        self.baudrate = DEFAULT_BAUDRATE

    # Listar puertos disponibles en el equipo (varía dependiendo del OS)
    @staticmethod
    def list_available_ports():
        ports = serial.tools.list_ports.comports()
        return ports  # list

    # Seleccionar el puerto (a partir de la lista de puertos)
    def select_port(self, port):
        self.port = port  # string

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
    def msg_test(self):
        if (self.validate_communication() == False):
            raise Exception(NULL_COMMUNICATION)
            return -1

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
