# Copyright (C) 2024  Ndahai Arenas
#
# Tuzo CanSat Monitor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tuzo CanSat Monitor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tuzo CanSat Monitor. If not, see <http://www.gnu.org/licenses/>.

# Clase que define el hilo donde se llevaraá a cabo la comunicacioón (TODO se moverá mas adelante)
from PyQt6.QtCore import QThread, pyqtSignal

from serial_communication.arduino_comm import ArduinoComm

# Clase que maneja el hilo de comunicacion, sirve como punto de entrada
# para la comunicacion serial.
class CommunicationThread(QThread):
    data_received = pyqtSignal(str) # Señal que se emitirá si se reciben datos
    data_error = pyqtSignal(str) # Señal que se emitirá si hubo un error de comunicacion
    finished = pyqtSignal() # Señal que se emitirá al finalizar el hilo

    # Recibiraá el puerto y la velocidad
    def __init__(self, port, speed):
        super().__init__()
        self.port = port
        self.speed = speed

    # Al ejecutar el hilo se establece la comunicación
    def run(self):
        comm = ArduinoComm() #
        comm.select_port(self.port)
        comm.select_baudrate(self.speed)
        # Crear objeto a partir de los parametros recibidos en la creacion del objeto
        comm.serial_received.connect(self.data_received) # Conectar señal de recepcion de ArduinoComm con data_received
        comm.serial_error.connect(self.data_error) # Conectar señal de error de ArduinoComm con data_error
        comm.begin_communication() # Iniciar comunicacion
        comm.readln_serial() # Empezar a leer desde el puerto serie
        self.finished.emit()