from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton
from Cansat.gui.utils.constants import *
from Cansat.gui.serial_communication.arduino_comm import ArduinoComm

# Clase que define el layout, elementos y propiedades de la ventana de conexión

class ConnectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Función para centrar la ventana
    def center(self):
        rectangle = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()

        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

    # Función para construir la ventana (agrega elementos, define layout, etc.)
    def initUI(self):
        # Definir propiedades de la ventana.
        self.setWindowTitle(WINDOW_TITLE)
        self.setBaseSize(800, 400)
        self.setGeometry(100, 100, 800, 400)
        self.center()



        # Definir elementos
        title = QLabel(CONNWINDOW_TEXT)
        serial_text = QLabel(CONNWINDOW_PORT)
        speed_text = QLabel(CONNWINDOW_SPEED)
        begin_button = QPushButton(CONNWINDOW_BEGIN)

        font = QFont()
        font.setPointSize(20)
        title.setFont(font)


        # Obtener los puertos y añadirlos a la lista
        port_combobox = QComboBox()
        ports = ArduinoComm.list_available_devices()

        for x in range (len(ports)):
            port_combobox.addItem(ports[x])

        # Obtener las velocidades posibles del puerto serie
        rate_combobox = QComboBox()
        baudrates = TRANSM_SPEED

        for x in range (len(baudrates)):
            rate_combobox.addItem(baudrates[x])


        # Definir layout
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(15,15,15,15)


        layout.addWidget(title, 0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(serial_text, 1, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(port_combobox, 2, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(speed_text, 3, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(rate_combobox, 4, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(begin_button, 5, 0, Qt.AlignmentFlag.AlignCenter)

