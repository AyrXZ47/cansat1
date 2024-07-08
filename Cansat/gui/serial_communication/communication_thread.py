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

# Clase que define el hilo donde se llevaraá a cabo la comunicacioón (TODO se moverá mas adelante)
from PyQt6.QtCore import QThread, pyqtSignal

from serial_communication.arduino_comm import ArduinoComm


class CommunicationThread(QThread):
    data_received = pyqtSignal(str)
    data_error = pyqtSignal()
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
        comm.serial_received.connect(self.data_received)
        comm.serial_error.connect(self.data_error)
        comm.begin_communication()
        comm.readln_serial()
        self.finished.emit()