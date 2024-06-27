from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit
from Cansat.gui.utils.constants import *

# Clase que define el layout y propiedades de la ventana principal

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Definir propiedades de la ventana.
        self.setWindowTitle(WINDOW_TITLE)
        self.setBaseSize(800, 400)

        # Definir layout
        layout = QGridLayout()
        self.setLayout(layout)

        # Aqui irá el widget para el modelo 3D
        layout.addWidget(QLabel('Modelo 3D'), 1, 1, 2, 2)

        # Aqui se agregarán las graficas con los datos
        layout.addWidget(QLabel('Grafica 1:'), 1, 2)
        layout.addWidget(QLabel('Grafica 2:'), 1, 3)
        layout.addWidget(QLabel('Grafica 3:'), 2, 2)
        layout.addWidget(QLabel('Grafica 4:'), 2, 3)

        # Boton de configuracion (no sé donde ponerlo y que se vea bien)
        layout.addWidget(QLabel('config:'), 0, 3, alignment=Qt.AlignmentFlag.AlignRight)


        self.setVisible(True)


