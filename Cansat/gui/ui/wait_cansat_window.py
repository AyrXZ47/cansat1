from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QProgressBar, QVBoxLayout

from Cansat.gui.utils.constants import WINDOW_TITLE, WAITWINDOW_LABEL, WAITWINDOW_CANCEL


class WaitCansatWindow(QWidget):
    def __init__(self, connection_window):
        super().__init__()
        self.initUI()
        #TODO self.comm_thread = comm_thread
        self.connection_window = connection_window


    def center(self):
        rectangle = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()

        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

    def cancel(self):
        self.connection_window.center()
        self.connection_window.show()
        self.close()

    def initUI(self):
        # Definir propiedades de la ventana.
        self.setWindowTitle(WINDOW_TITLE)
        self.setBaseSize(800, 400)
        self.setGeometry(100, 100, 800, 400)
        self.center()

        # Definir elementos de la ventana
        label = QLabel(WAITWINDOW_LABEL)
        self.cancel_button =  QPushButton(WAITWINDOW_CANCEL)
        font = QFont()
        font.setPointSize(20)
        label.setFont(font)

        # Crear QLabel para la imagen
        image_label = QLabel()
        pixmap = QPixmap("../resources/antenna.radiowaves.left.and.right.png")
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # Definir layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        layout.setContentsMargins(15,15,15,15)

        # Añadir elementos
        layout.addWidget(image_label)
        layout.addWidget(label)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.cancel_button, alignment=Qt.AlignmentFlag.AlignCenter)

        #Añadir eventos
        self.cancel_button.clicked.connect(self.cancel)




