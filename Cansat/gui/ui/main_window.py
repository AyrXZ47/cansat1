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

import math

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QStatusBar, QMainWindow

from Cansat.gui.ui.graphs.three_pen_graph import ThreePenGraph
from Cansat.gui.utils.constants import *
from Cansat.gui.ui.graphs.single_pen_graph import SinglePenGraph
from Cansat.gui.ui.model3d.viewport_3d import Viewport3D

# Clase que define el layout, elementos y propiedades de la ventana principal

class MainWindow(QMainWindow):
    def __init__(self, comm_thread):
        super().__init__()
        self.comm_thread = comm_thread
        self.comm_thread.data_received.connect(self.handle_received_data)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
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
        print("si")
        self.setWindowTitle(WINDOW_TITLE)
        self.setBaseSize(800, 400)
        self.setGeometry(100, 100, 800, 400)
        self.center()


        # Definir layout
        layout = QGridLayout()
        self.central_widget.setLayout(layout)

        layout.setRowStretch(0,1)
        layout.setRowStretch(1,5)
        layout.setRowStretch(2,5)

        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)



        # Aqui irá el widget para el modelo 3D
        # layout.addWidget(QLabel('Modelo 3D'), 1, 0, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.viewport3D = Viewport3D()
        layout.addWidget(self.viewport3D, 1, 0, 2, 2)

        # Aqui se agregarán las graficas con los datos
        # layout.addWidget(QLabel('Grafica 1:'), 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)

        self.temp_graph = SinglePenGraph(TEMP_COLOR)
        self.acel_graph = ThreePenGraph(ACCL_COLOR1, ACCL_COLOR2, ACCL_COLOR3)
        self.alti_graph = SinglePenGraph(ALTI_COLOR)
        self.pres_graph = SinglePenGraph(PRES_COLOR)

        self.temp_graph.setMinimumWidth(300)
        self.acel_graph.setMinimumWidth(300)
        self.alti_graph.setMinimumWidth(300)
        self.pres_graph.setMinimumWidth(300)


        layout.addWidget(self.temp_graph, 1, 2)
        layout.addWidget(self.acel_graph, 1, 3)
        layout.addWidget(self.alti_graph, 2, 2)
        layout.addWidget(self.pres_graph, 2, 3)

        # Boton de configuracion (no sé donde ponerlo y que se vea bien)
        self.config_label = QLabel('config:')
        layout.addWidget(self.config_label, 0, 3, alignment=Qt.AlignmentFlag.AlignRight)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.setVisible(True)


    # Handlers
    def handle_received_data(self, data):
        print(data)
        self.statusbar.showMessage(data)

        raw_data = data.split(",")

        if(len(raw_data) == 6):
            altitude = raw_data[0]
            pressure = raw_data[1]
            accelX = int(raw_data[2])
            accelY = int(raw_data[3])
            accelZ = int(raw_data[4])
            temp = raw_data[5]

            print(f"x {accelX}")
            print(f"y {accelY}")
            print(f"z {accelZ}")


            roll = math.atan2(accelY, accelZ)
            pitch = math.atan2(-accelX, math.sqrt(accelY * accelY + accelZ * accelZ))


            print(f"roll: {math.degrees(roll)}");
            print(f"pitch: {math.degrees(pitch)}");



            self.temp_graph.update_data(temp)
            self.acel_graph.update_data(accelX, accelY, accelZ)
            self.alti_graph.update_data(altitude)
            self.pres_graph.update_data(pressure)
            print(roll)
            print(pitch)
            self.viewport3D.rotate(math.degrees(pitch), 0, math.degrees(roll))









