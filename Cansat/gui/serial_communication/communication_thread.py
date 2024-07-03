# Clase que define el hilo donde se llevaraá a cabo la comunicacioón (TODO se moverá mas adelante)
from PyQt6.QtCore import QThread, pyqtSignal

from Cansat.gui.serial_communication.arduino_comm import ArduinoComm


class CommunicationThread(QThread):
    finished = pyqtSignal()

    # Recibiraá el puerto y la velocidad
    def __init__(self, port, speed):
        super().__init__()
        self.port = port
        self.speed = speed

    # Al ejecutar el hilo se establece la comunicación
    def run(self):
        comm = ArduinoComm()
        comm.select_port(self.port)
        comm.select_baudrate(self.speed)
        comm.begin_communication()

        self.finished.emit()