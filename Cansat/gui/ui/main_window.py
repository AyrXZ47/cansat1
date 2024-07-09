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
from PyQt6.QtGui import QColor, QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QLineEdit, QStatusBar, QMainWindow, QHBoxLayout, QCheckBox, \
    QMessageBox

from ui.graphs.three_pen_graph import ThreePenGraph
from utils.constants import *
from ui.graphs.single_pen_graph import SinglePenGraph
from ui.model3d.viewport_3d import Viewport3D

# Clase que define el layout, elementos y propiedades de la ventana principal

class MainWindow(QMainWindow):
    def __init__(self, comm_thread):
        super().__init__()
        self.comm_thread = comm_thread
        self.comm_thread.data_received.connect(self.handle_received_data)
        self.comm_thread.data_error.connect(self.handle_communication_error)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.show_graphs = False
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
        #self.setBaseSize(800, 400)
        self.setGeometry(100, 100, 800, 400)
        self.center()


        # Definir layout
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        self.layout.setRowStretch(0,1)
        self.layout.setRowStretch(1,5)
        self.layout.setRowStretch(2,5)

        self.layout.setColumnStretch(0, 2)
        self.layout.setColumnStretch(1, 1)
        self.layout.setColumnStretch(2, 1)



        # Aqui irá el widget para el modelo 3D
        # layout.addWidget(QLabel('Modelo 3D'), 1, 0, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.viewport3D = Viewport3D()
        self.viewport3D.setMinimumSize(300, 300)
        self.layout.addWidget(self.viewport3D, 1, 0, 2, 2)

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


        self.temp_label = QLabel(TEMP_PLACEHOLDER)
        self.acelX_label = QLabel(ACEL_PLACEHOLDER)
        self.acelY_label = QLabel(ACEL_PLACEHOLDER)
        self.acelZ_label = QLabel(ACEL_PLACEHOLDER)
        self.alti_label = QLabel(ALTI_PLACEHOLDER)
        self.pres_label = QLabel(PRES_PLACEHOLDER)

        font = QFont()
        font.setPointSize(36)
        self.temp_label.setFont(font)
        self.acelX_label.setFont(font)
        self.acelY_label.setFont(font)
        self.acelZ_label.setFont(font)
        self.alti_label.setFont(font)
        self.pres_label.setFont(font)


        #if
        self.layout.addWidget(self.temp_graph, 1, 2)
        self.layout.addWidget(self.acel_graph, 1, 3)
        self.layout.addWidget(self.alti_graph, 2, 2)
        self.layout.addWidget(self.pres_graph, 2, 3)
        #else

        self.accel_widget = QWidget()
        accel_layout = QHBoxLayout()
        self.accel_widget.setLayout(accel_layout)

        self.layout.addWidget(self.temp_label, 1, 2)
        accel_layout.addWidget(self.acelX_label)
        accel_layout.addWidget(self.acelY_label)
        accel_layout.addWidget(self.acelZ_label)
        self.layout.addWidget(self.alti_label, 2, 2)
        self.layout.addWidget(self.pres_label, 2, 3)
        self.layout.addWidget(self.accel_widget, 1, 3)

        # Boton de configuracion (no sé donde ponerlo y que se vea bien)
        self.config_label = QLabel('config:')
        self.layout.addWidget(self.config_label, 0, 3, alignment=Qt.AlignmentFlag.AlignRight)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.graph_checkbox = QCheckBox(MAINWINDOW_GRAPH_CHECKBOX)
        self.graph_checkbox.stateChanged.connect(self.toggle_graphs)
        self.toggle_graphs()
        self.statusbar.addPermanentWidget(self.graph_checkbox)
        self.setVisible(True)

    def toggle_graphs(self):
        if self.graph_checkbox.isChecked():
            # Dibujar graficos y eliminar texto
            self.temp_label.setVisible(False)
            self.accel_widget.setVisible(False)
            self.alti_label.setVisible(False)
            self.pres_label.setVisible(False)

            self.temp_graph.setVisible(True)
            self.acel_graph.setVisible(True)
            self.alti_graph.setVisible(True)
            self.pres_graph.setVisible(True)


        else:
            # Dibujar texto y eliminar graficos
            self.temp_label.setVisible(True)
            self.accel_widget.setVisible(True)
            self.alti_label.setVisible(True)
            self.pres_label.setVisible(True)

            self.temp_graph.setVisible(False)
            self.acel_graph.setVisible(False)
            self.alti_graph.setVisible(False)
            self.pres_graph.setVisible(False)


    # Handlers
    def handle_communication_error(self):
        from ui.connection_window import ConnectionWindow
        conn = ConnectionWindow()
        conn.show()
        QMessageBox.critical(self, ERRORMSG_TITLE, "error")

        self.comm_thread.terminate()


    def reopen_app(self):
        print("pablo")










    def handle_received_data(self, data):
        print(data)
        self.statusbar.showMessage(data)

        raw_data = data.split(DATA_SEPARATOR)

        if(len(raw_data) == 6):
            altitude = raw_data[0]
            pressure = raw_data[1]
            accelX = int(raw_data[2])
            accelY = int(raw_data[3])
            accelZ = int(raw_data[4])
            temp = raw_data[5]
            roll = math.atan2(accelY, accelZ)
            pitch = math.atan2(-accelX, math.sqrt(accelY * accelY + accelZ * accelZ))

            self.temp_graph.update_data(temp)
            self.acel_graph.update_data(accelX, accelY, accelZ)
            self.alti_graph.update_data(altitude)
            self.pres_graph.update_data(pressure)


            self.temp_label.setText(f'{temp} {TEMP_UNIT}')
            self.acelX_label.setText(f'{accelX} {ACEL_UNIT}')
            self.acelY_label.setText(f'{accelY} {ACEL_UNIT}')
            self.acelZ_label.setText(f'{accelZ} {ACEL_UNIT}')
            self.pres_label.setText(f'{pressure} {PRES_UNIT}')
            self.alti_label.setText(f'{altitude} {ALTI_UNIT}')

            self.viewport3D.rotate(math.degrees(pitch), 0, math.degrees(roll))









