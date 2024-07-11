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

from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton, \
    QProgressDialog, QMessageBox, QHBoxLayout
from serial_communication.communication_thread import CommunicationThread
from ui.main_window import MainWindow
from utils.constants import *
from serial_communication.arduino_comm import ArduinoComm


# Clase que define el layout, elementos y propiedades de la ventana de conexión
class ConnectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_window = None
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
        if (data.startswith(ERROR_START)):
            self.show_gndstation_error_dialog(data)
            if self.progress_dialog:
                self.progress_dialog.canceled.disconnect(self.on_thread_finished)
                self.progress_dialog.close()
        elif (data.startswith(WAITING_STARTING1)):
            if not self.progress_dialog:
                self.init_progress_dialog()
                self.progress_dialog.show()
        else:
            if self.progress_dialog:
                self.progress_dialog.canceled.disconnect(self.on_thread_finished)
                self.progress_dialog.close()
            self.thread.data_received.disconnect(self.data_event_handler)
            self.thread.data_error.disconnect(self.show_communication_error_dialog)
            self.open_mainwindow()



    ## Eventos ##
    def debug_button_pressed(self):
        selected_port = CONNWINDOW_DEBUG
        selected_speed = int(DEFAULT_BAUDRATE)

        self.thread = CommunicationThread(selected_port, selected_speed)
        self.thread.data_received.connect(self.data_event_handler)
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.data_error.connect(self.show_communication_error_dialog)
        self.thread.start()

        self.open_mainwindow()

    # Al presionar el boton de iniciar
    def begin_button_pressed(self):
        self.init_progress_dialog()
        self.progress_dialog.show()
        self.port_combobox.setEnabled(False)
        self.rate_combobox.setEnabled(False)
        self.begin_button.setEnabled(False)

        selected_port = self.port_combobox.currentText()
        selected_speed = int(self.rate_combobox.currentText())

        self.thread = CommunicationThread(selected_port, selected_speed)
        self.thread.data_received.connect(self.data_event_handler)
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.data_error.connect(self.show_communication_error_dialog)
        self.thread.start()

    # Cuando se finalice la conexión (el hilo) se volveraán a habilitar los selectores
    def on_thread_finished(self):
        print("TERMINADO")
        self.thread.terminate()  # FIXME Finalizar el hilo de comunicación correctamente
        self.enable_window()



    ## Procesos ##

    # Obtener puertos serie disponibles
    def populate_ports_combobox(self):
        ports = ArduinoComm.list_available_devices()
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
        self.main_window = MainWindow(self.thread, self)
        self.main_window.show()
        self.close()

    # Mostrar mensaje de error si hay un error en la estación terrena
    def show_gndstation_error_dialog(self, error_message):
        self.on_thread_finished()
        QMessageBox.critical(self, ERRORMSG_TITLE, error_message.capitalize())

    # Mostrar mensaje de error si hubo un error de comunicacion entre la estacion y el programa.
    def show_communication_error_dialog(self, data:str):
        if self.progress_dialog:
            self.progress_dialog.canceled.disconnect(self.on_thread_finished)
            self.progress_dialog.close()
        QMessageBox.critical(self, ERRORMSG_TITLE, data.capitalize())
        self.on_thread_finished()





