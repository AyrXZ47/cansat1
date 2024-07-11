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
    QMessageBox, QPushButton, QVBoxLayout

from ui.graphs.three_pen_graph import ThreePenGraph
from utils.constants import *
from ui.graphs.single_pen_graph import SinglePenGraph
from ui.model3d.viewport_3d import Viewport3D

# Clase que define el layout, elementos y propiedades de la ventana principal

class MainWindow(QMainWindow):
    def __init__(self, comm_thread, connwindow):
        super().__init__()
        self.conn_window = connwindow
        self.comm_thread = comm_thread
        self.comm_thread.data_received.connect(self.handle_received_data)
        self.comm_thread.data_error.connect(self.handle_communication_error)
        self.show_graphs = False
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
        self.setGeometry(100, 100, 800, 400)
        self.center()

        # Definir layout
        self.layout = QGridLayout()
        self.central_widget.setLayout(self.layout)

        # Ajustar stretch de filas y columnas para que se estiren igualmente.
        for i in range(3):
            self.layout.setRowStretch(i, 1)
        for i in range(4):
            self.layout.setColumnStretch(i, 1)

        # Definir estilos
        font = QFont()
        font.setPointSize(36)

        # Definir elementos
        self.viewport3D = Viewport3D()
        self.temp_graph = SinglePenGraph(TEMP_COLOR, title="Temperatura")
        self.acel_graph = ThreePenGraph(ACCL_COLOR1, ACCL_COLOR2, ACCL_COLOR3, title = "Aceleración")
        self.alti_graph = SinglePenGraph(ALTI_COLOR, title="Altitud")
        self.pres_graph = SinglePenGraph(PRES_COLOR, title="Presión")
        self.temp_label = QLabel(TEMP_PLACEHOLDER)
        self.acelX_label = QLabel(ACEL_PLACEHOLDER)
        self.acelY_label = QLabel(ACEL_PLACEHOLDER)
        self.acelZ_label = QLabel(ACEL_PLACEHOLDER)
        self.alti_label = QLabel(ALTI_PLACEHOLDER)
        self.pres_label = QLabel(PRES_PLACEHOLDER)
        self.back_button = QPushButton("< Volver")
        self.statusbar = QStatusBar()
        self.graph_checkbox = QCheckBox(MAINWINDOW_GRAPH_CHECKBOX)


            # Widget de aceleracion
        self.accel_widget = QWidget()
        accel_layout = QVBoxLayout()
        self.accel_widget.setLayout(accel_layout)

        accel_layout.addWidget(self.acelX_label)
        accel_layout.addWidget(self.acelY_label)
        accel_layout.addWidget(self.acelZ_label)


        # Definir propiedades de widgets
        self.viewport3D.setMinimumSize(300, 300)
        self.temp_graph.setMinimumWidth(300)
        self.acel_graph.setMinimumWidth(300)
        self.alti_graph.setMinimumWidth(300)
        self.pres_graph.setMinimumWidth(300)

        # Aplicar estilos
        self.temp_label.setFont(font)
        self.acelX_label.setFont(font)
        self.acelY_label.setFont(font)
        self.acelZ_label.setFont(font)
        self.alti_label.setFont(font)
        self.pres_label.setFont(font)

        # Agregar a layout
        self.layout.addWidget(self.viewport3D, 1, 0, 2, 2)
        self.layout.addWidget(self.temp_graph, 1, 2)
        self.layout.addWidget(self.acel_graph, 1, 3)
        self.layout.addWidget(self.alti_graph, 2, 2)
        self.layout.addWidget(self.pres_graph, 2, 3)
        self.layout.addWidget(self.temp_label, 1, 2)
        self.layout.addWidget(self.alti_label, 2, 2)
        self.layout.addWidget(self.pres_label, 2, 3)
        self.layout.addWidget(self.accel_widget, 1, 3)
        self.layout.addWidget(self.back_button, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.setStatusBar(self.statusbar)
        self.statusbar.addPermanentWidget(self.graph_checkbox)




        # Conectar con eventos
        self.back_button.clicked.connect(self.reopen_connection_window)
        self.graph_checkbox.stateChanged.connect(self.toggle_graphs)


        self.toggle_graphs()
        self.setVisible(True)
        self.apply_style()


    # Eventos
    def apply_style(self):
        self.setStyleSheet("""
                    QWidget {
                        background-color: #0e0e0e;
                        color: #00ff00;
                    }

                    QPushButton {
                        background-color: #333333;
                        border: 2px solid #00ff00;
                        color: #00ff00;
                        padding: 10px;
                        font-size: 16px;
                    }

                    QPushButton:hover {
                        background-color: #00ff00;
                        color: #333333;
                    }

                    QLabel {
                        color: #00ff00;
                        font-size: 18px;
                    }

                    SinglePenGraph, ThreePenGraph {
                        background-color: #1e1e1e;
                        border: 1px solid #00ff00;
                    }

                    Viewport3D {
                        border: 1px solid #00ff00;
                        padding: 10px; 
                    }

                    QCheckBox {
                        font-size: 16px;
                        padding: 5px;
                    }

                    QStatusBar {
                        background-color: #0e0e0e;
                        color: #00ff00;
                        font-size: 16px;
                        border-top: 1px solid #00ff00;
                    }

                    QLineEdit {
                        background-color: #1e1e1e;
                        border: 2px solid #00ff00;
                        color: #00ff00;
                        padding: 5px;
                        font-size: 16px;
                    }

                    QLabel {
                        font-size: 36px;
                    }

                    Viewport3D {
                        border: 2px solid #00ff00;
                    }
                    """)


    def reopen_connection_window(self):
        self.conn_window.center()
        self.conn_window.show()
        self.setVisible(False)
        self.conn_window.on_thread_finished()
        self.close()

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
    def handle_communication_error(self, data:str):
        self.conn_window.center()
        self.conn_window.show()
        self.setVisible(False)
        self.comm_thread.terminate()
        QMessageBox.critical(self, ERRORMSG_TITLE, data.capitalize())
        self.conn_window.enable_window()
        self.conn_window.show()
        self.close()


    def handle_received_data(self, data):
        print(data)
        self.statusbar.showMessage(data)

        if (data.startswith("e")):
            self.handle_communication_error(data)
            return 0

        raw_data = data.split(DATA_SEPARATOR)

        if(len(raw_data) == 6):
            altitude = int(raw_data[0])
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









