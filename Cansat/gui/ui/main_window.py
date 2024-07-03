from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit
from Cansat.gui.utils.constants import *
from Cansat.gui.ui.graphs.temperature_graph import TemperatureGraph

# Clase que define el layout, elementos y propiedades de la ventana principal

class MainWindow(QWidget):
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

        # Definir layout
        layout = QGridLayout()
        self.setLayout(layout)

        layout.setRowStretch(0,1)
        layout.setRowStretch(1,5)
        layout.setRowStretch(2,5)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)



        # Aqui irá el widget para el modelo 3D
        layout.addWidget(QLabel('Modelo 3D'), 1, 0, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        # Aqui se agregarán las graficas con los datos
        # layout.addWidget(QLabel('Grafica 1:'), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        temp_graph = TemperatureGraph()

        layout.addWidget(temp_graph, 1, 2)
        layout.addWidget(QLabel('Grafica 2:'), 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel('Grafica 3:'), 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(QLabel('Grafica 4:'), 2, 3, alignment=Qt.AlignmentFlag.AlignCenter)

        # Boton de configuracion (no sé donde ponerlo y que se vea bien)
        layout.addWidget(QLabel('config:'), 0, 3, alignment=Qt.AlignmentFlag.AlignRight)


        self.setVisible(True)


