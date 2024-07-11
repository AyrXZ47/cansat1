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

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox, QPushButton, \
    QProgressDialog, QMessageBox, QHBoxLayout

from serial_communication.arduino_comm import ArduinoComm
from serial_communication.communication_thread import CommunicationThread
from ui.main_window import MainWindow
from utils.constants import *


# Clase que define el layout, elementos y propiedades de la ventana de conexión
class ConnectionWindow(QWidget):
    # Es el punto de entrada del programa
    def __init__(self):
        super().__init__()
        self.main_window = None # Definir ventana principal como atributo de la clase
        self.progress_dialog = None
        self.initUI()
        print("Init connection window")


    # Función para centrar la ventana
    def center(self):
        rectangle = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()
        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())


    # Inicializar elementos
    def init_progress_dialog(self):
        self.progress_dialog = QProgressDialog(WAITWINDOW_LABEL, WAITWINDOW_CANCEL, 0, 0, self)
        self.progress_dialog.setWindowTitle(WAITWINDOW_TITLE)
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setValue(0)
        self.progress_dialog.canceled.connect(self.on_thread_finished)


    # Función para construir la ventana (agrega elementos, define layout, etc.)
    def initUI(self):
        # Definir propiedades de la ventana.
        self.setWindowTitle(WINDOW_TITLE)
        self.setBaseSize(800, 400)
        self.setGeometry(100, 100, 800, 400)
        self.center()
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(15, 15, 15, 15)

        # Definir estilos
        font = QFont()
        font.setPointSize(20)

        # Definir elementos
        title = QLabel(CONNWINDOW_TEXT)
        serial_text = QLabel(CONNWINDOW_PORT)
        speed_text = QLabel(CONNWINDOW_SPEED)
        self.begin_button = QPushButton(CONNWINDOW_BEGIN)
        self.port_combobox = QComboBox()
        self.reload_button =  QPushButton(CONNWINDOW_RELOAD)
        port_layout = QHBoxLayout()
        port_layout.addWidget(self.port_combobox)
        port_layout.addWidget(self.reload_button)
        port_panel = QWidget()
        port_panel.setLayout(port_layout)
        self.rate_combobox = QComboBox()
        self.debug_button = QPushButton(CONNWINDOW_DEBUG)

        # Aplicar estilos
        title.setFont(font)

        # Poblar elementos
        self.populate_ports_combobox()
        for x in range (len(TRANSM_SPEED)):
            self.rate_combobox.addItem(TRANSM_SPEED[x])

        # Conectar con eventos
        self.reload_button.clicked.connect(self.populate_ports_combobox)
        self.begin_button.clicked.connect(self.begin_button_pressed)
        if DEBUG:
            layout.addWidget(self.debug_button, 6, 0, Qt.AlignmentFlag.AlignLeft)
            self.debug_button.clicked.connect(self.debug_button_pressed)


        # Establecer valores por defecto
        self.rate_combobox.setCurrentIndex(DEFAULT_BAUDRATE_INDEX)

        # Agregar elementos a layout
        layout.addWidget(title, 0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(serial_text, 1, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(port_panel, 2, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(speed_text, 3, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.rate_combobox, 4, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.begin_button, 5, 0, Qt.AlignmentFlag.AlignCenter)

    # Handlers
    def data_event_handler(self, data: str):
        received_data = data.split(",")
        if (data.startswith(ERROR_START)): # Si se recibieron datos pero se trata de un error,
                                            # mostrar el mensaje de error, y desconectar el
                                            # hilo del dialogo de progreso para evitar
                                            # que se congele
            self.show_gndstation_error_dialog(data)
            if self.progress_dialog:
                self.progress_dialog.canceled.disconnect(self.on_thread_finished)
                self.progress_dialog.close()

        # Si llega un mensaje de espera, mostrar el dialogo de progreso y construirlo si aun no lo está
        elif (data.startswith(WAITING_STARTING1)):
            if not self.progress_dialog:
                self.init_progress_dialog()
                self.progress_dialog.show()
        else:
            # Si se recibe otro dato, desconectar el dialogo de progreso de la finalizacion del hilo
            # despues cerrar el dialogo y desconectar los handlers de esta ventana, para abrir
            # la ventana principal.
            if self.progress_dialog:
                self.progress_dialog.canceled.disconnect(self.on_thread_finished)
                self.progress_dialog.close()
            self.thread.data_received.disconnect(self.data_event_handler)
            self.thread.data_error.disconnect(self.show_communication_error_dialog)
            self.open_mainwindow()



    ## Eventos ##
    def debug_button_pressed(self):
        selected_port = CONNWINDOW_DEBUG # Establecer puerto seleccionado como DEBUG
        selected_speed = int(DEFAULT_BAUDRATE) # La velocidad es irrelevante

        self.thread = CommunicationThread(selected_port, selected_speed) # Crear hilo con parametros
        self.thread.data_received.connect(self.data_event_handler)  # Cada vez que se reciba un mensaje proveniente
                                                                    # de la señal de datos recibidos, se manda a llamar
                                                                    # la funcion data_event_handler
        self.thread.finished.connect(self.on_thread_finished)       # Se realizan los procedimientos de finalizacion del hilo al recibir la señal
        self.thread.data_error.connect(self.show_communication_error_dialog)
        self.thread.start() # iniciar el hilo

        self.open_mainwindow() # abrir la ventana principal

    # Al presionar el boton de iniciar
    def begin_button_pressed(self):
        self.init_progress_dialog() # Inicializar dialogo de progreso
        self.progress_dialog.show()
        self.port_combobox.setEnabled(False) # Desactivar elementos de la ventana
        self.rate_combobox.setEnabled(False)
        self.begin_button.setEnabled(False)

        selected_port = self.port_combobox.currentText() # Obtener puerto desde el combobox
        selected_speed = int(self.rate_combobox.currentText()) # Obtener velocidad desde el combobox

        self.thread = CommunicationThread(selected_port, selected_speed) # Crear hilo de comunicacion con parametros
        self.thread.data_received.connect(self.data_event_handler) # Conectar señal de datos recibidos con el handler para los datos
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.data_error.connect(self.show_communication_error_dialog) # Conectar señal de error con el dialogo de error
        self.thread.start() # Iniciar hilo

    # Cuando se finalice la conexión (el hilo) se volveraán a habilitar los selectores
    def on_thread_finished(self):
        print("TERMINADO")
        self.enable_window() # Reactivar ventana
        self.thread.terminate()


    ## Procesos ##

    # Obtener puertos serie disponibles
    def populate_ports_combobox(self):
        ports = ArduinoComm.list_available_devices() # Obtener puertos disponibles en el equipo
        self.port_combobox.clear()

        for x in range(len(ports)):
            self.port_combobox.addItem(ports[x])

    # Activar elementos de la ventana
    def enable_window(self):
        self.port_combobox.setEnabled(True)
        self.rate_combobox.setEnabled(True)
        self.begin_button.setEnabled(True)

    # Abrir ventana principal si se establece conexion exitosa con la estacion terrena
    def open_mainwindow(self):
        self.main_window = MainWindow(self.thread, self) # Pasar el hilo de comunicacion, y la instancia actual de la ventana de conexion para evitar imports cruzados
        self.main_window.show()
        self.close()

    # Mostrar mensaje de error si hay un error en la estación terrena
    def show_gndstation_error_dialog(self, error_message):
        self.on_thread_finished() # Finalizar hilo para evitar errores duplicados
        QMessageBox.critical(self, ERRORMSG_TITLE, error_message.capitalize())

    # Mostrar mensaje de error si hubo un error de comunicacion entre la estacion y el programa.
    def show_communication_error_dialog(self, data:str):
        if self.progress_dialog:
            self.progress_dialog.canceled.disconnect(self.on_thread_finished) # Desconectar de la señal para evitar que se congele
            self.progress_dialog.close()
        QMessageBox.critical(self, ERRORMSG_TITLE, data.capitalize())
        self.on_thread_finished() # Finalizar hilo despues de mostrar el mensaje





