from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QVBoxLayout, QComboBox, QPushButton, \
    QProgressDialog

from Cansat.gui.serial_communication.communication_thread import CommunicationThread
from Cansat.gui.ui.wait_cansat_window import WaitCansatWindow
from Cansat.gui.utils.constants import *
from Cansat.gui.serial_communication.arduino_comm import ArduinoComm


# Clase que define el layout, elementos y propiedades de la ventana de conexión

class ConnectionWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_progress_dialog()
        self.initUI()

    def init_progress_dialog(self):
        self.progress_dialog = QProgressDialog(WAITWINDOW_LABEL, WAITWINDOW_CANCEL, 0, 0, self)
        self.progress_dialog.setWindowTitle("Espere...")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setValue(0)
        self.progress_dialog.canceled.connect(self.on_thread_finished)


    # Función para centrar la ventana
    def center(self):
        rectangle = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()

        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

    # Definir eventos

    def begin_comm(self):
        self.progress_dialog.show()

        self.port_combobox.setEnabled(False)
        self.rate_combobox.setEnabled(False)
        self.begin_button.setEnabled(False)

        selected_port = self.port_combobox.currentText()
        selected_speed = int(self.rate_combobox.currentText())



        # TODO Aun no se si usar una ventana aparte o un dialogo
        # self.wait_window = WaitCansatWindow(self)
        # self.wait_window.show()
        # self.close()


        # TODO Iniciar comunicacion en un nuevo hilo
        self.thread = CommunicationThread(selected_port, selected_speed)
        self.thread.finished.connect(self.on_thread_finished)
        self.thread.start()

    # Cuando se finalice la conexión (el hilo) se volveraán a habilitar los selectores
    def on_thread_finished(self):
        self.thread.terminate() # FIXME Finalizar el hilo de comunicación correctamente
        self.port_combobox.setEnabled(True)
        self.rate_combobox.setEnabled(True)
        self.begin_button.setEnabled(True)




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
        self.begin_button = QPushButton(CONNWINDOW_BEGIN)

        font = QFont()
        font.setPointSize(20)
        title.setFont(font)


        # Obtener los puertos y añadirlos a la lista
        self.port_combobox = QComboBox()
        ports = ArduinoComm.list_available_devices()

        for x in range (len(ports)):
            self.port_combobox.addItem(ports[x])

        # Obtener las velocidades posibles del puerto serie
        self.rate_combobox = QComboBox()
        baudrates = TRANSM_SPEED

        for x in range (len(baudrates)):
            self.rate_combobox.addItem(baudrates[x])


        # Definir layout
        layout = QGridLayout()
        self.setLayout(layout)
        layout.setContentsMargins(15,15,15,15)


        layout.addWidget(title, 0, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(serial_text, 1, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.port_combobox, 2, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(speed_text, 3, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.rate_combobox, 4, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.begin_button, 5, 0, Qt.AlignmentFlag.AlignCenter)

        self.begin_button.clicked.connect(self.begin_comm)






