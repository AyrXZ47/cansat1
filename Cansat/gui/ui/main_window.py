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

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QWidget, QGridLayout, QLabel, QStatusBar, QMainWindow, QCheckBox, \
    QMessageBox, QPushButton, QVBoxLayout

from ui.graphs.single_pen_graph import SinglePenGraph
from ui.graphs.three_pen_graph import ThreePenGraph
from ui.model3d.viewport_3d import Viewport3D
from utils.constants import *


# Clase que define el layout, elementos y propiedades de la ventana principal
class MainWindow(QMainWindow):
    def __init__(self, comm_thread, connwindow):
        super().__init__()
        self.conn_window = connwindow # Recibir ventana de conexion
        self.comm_thread = comm_thread # Recibir hilo
        self.comm_thread.data_received.connect(self.handle_received_data) # Conectar senñal de recibido con el handler de esta ventana
        self.comm_thread.data_error.connect(self.handle_communication_error) # Conectar señal de error con el handler de esta ventana
        self.show_graphs = False # Las graficas no se muestran por defecto
        self.central_widget = QWidget() # Establecer widget central
        self.setCentralWidget(self.central_widget)
        self.initUI() # Inicializar UI

    # Función para centrar la ventana
    def center(self):
        rectangle = self.frameGeometry()
        center_point = self.screen().availableGeometry().center()

        rectangle.moveCenter(center_point)
        self.move(rectangle.topLeft())

    # Función para construir la ventana (agrega elementos, define layout, etc.)
    def initUI(self):
        # Definir propiedades de la ventana.
        print("Inicializar ventana principal")
        self.setWindowTitle(WINDOW_TITLE)
        self.setGeometry(100, 100, 950, 400)
        self.center()

        # Definir layout
        self.layout = QGridLayout() #
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
        self.temp_graph = SinglePenGraph(TEMP_COLOR, title=TEMP_TITLE)
        self.acel_graph = ThreePenGraph(ACCL_COLOR1, ACCL_COLOR2, ACCL_COLOR3, title = ACCL_TITLE)
        self.alti_graph = SinglePenGraph(ALTI_COLOR, title=ALTI_TITLE)
        self.pres_graph = SinglePenGraph(PRES_COLOR, title=PRES_TITLE)
        self.temp_label = QLabel(TEMP_PLACEHOLDER)
        self.acelX_label = QLabel(ACEL_PLACEHOLDER)
        self.acelY_label = QLabel(ACEL_PLACEHOLDER)
        self.acelZ_label = QLabel(ACEL_PLACEHOLDER)
        self.alti_label = QLabel(ALTI_PLACEHOLDER)
        self.pres_label = QLabel(PRES_PLACEHOLDER)
        self.back_button = QPushButton(BACK_BTTN)
        self.statusbar = QStatusBar()
        self.graph_checkbox = QCheckBox(MAINWINDOW_GRAPH_CHECKBOX)

        # Widget de temperatura
        self.temp_widget = QWidget()
        temp_layout = QVBoxLayout()
        self.temp_widget.setLayout(temp_layout)
        temp_title = QLabel(TEMP_TITLE)
        temp_layout.addWidget(temp_title)
        temp_layout.addWidget(self.temp_label,  alignment=Qt.AlignmentFlag.AlignCenter)

        # Widget de altitud
        self.alti_widget = QWidget()
        alti_layout = QVBoxLayout()
        self.alti_widget.setLayout(alti_layout)
        alti_title = QLabel(ALTI_TITLE)
        alti_layout.addWidget(alti_title)
        alti_layout.addWidget(self.alti_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Widget de presion
        self.pres_widget = QWidget()
        pres_layout = QVBoxLayout()
        self.pres_widget.setLayout(pres_layout)
        pres_title = QLabel(PRES_TITLE)
        pres_layout.addWidget(pres_title)
        pres_layout.addWidget(self.pres_label, alignment=Qt.AlignmentFlag.AlignCenter)


            # Widget de aceleracion
        self.accel_widget = QWidget()
        accel_layout = QVBoxLayout()
        self.accel_widget.setLayout(accel_layout)
        accel_title = QLabel(ACCL_TITLE)

        accel_layout.addWidget(accel_title, alignment=Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.acelX_label, alignment=Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.acelY_label, alignment=Qt.AlignmentFlag.AlignCenter)
        accel_layout.addWidget(self.acelZ_label, alignment=Qt.AlignmentFlag.AlignCenter)


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
        self.layout.addWidget(self.temp_widget, 1, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.alti_widget, 2, 2, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.pres_widget, 2, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.accel_widget, 1, 3, alignment=Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.back_button, 0, 0, alignment=Qt.AlignmentFlag.AlignLeft)
        self.setStatusBar(self.statusbar)
        self.statusbar.addPermanentWidget(self.graph_checkbox)




        # Conectar con eventos
        self.back_button.clicked.connect(self.reopen_connection_window) # Al volver, reabrir ventana de conexion
        self.graph_checkbox.stateChanged.connect(self.toggle_graphs) # Conectar checkbox con el metodo toggle_graphs


        self.toggle_graphs()

        # Si se desean aplicar los estilos desde constants.py
        if APPLY_CSS_STYLE:
            self.setStyleSheet(STYLE_SHEET)
            self.temp_widget.setStyleSheet(WIDGET_STYLESHEET)
            self.accel_widget.setStyleSheet(WIDGET_STYLESHEET)
            self.alti_widget.setStyleSheet(WIDGET_STYLESHEET)
            self.pres_widget.setStyleSheet(WIDGET_STYLESHEET)
            temp_title.setStyleSheet(TITLE_STYLESHEET)
            alti_title.setStyleSheet(TITLE_STYLESHEET)
            pres_title.setStyleSheet(TITLE_STYLESHEET)
            accel_title.setStyleSheet(TITLE_STYLESHEET)

        self.setVisible(True)

    # Eventos


    def reopen_connection_window(self):
        self.conn_window.center()
        self.conn_window.show()
        self.setVisible(False)
        self.conn_window.on_thread_finished() # Finalizar hilo de comunicacion desde la ventana de conexion
        self.close()

    def toggle_graphs(self):
        if self.graph_checkbox.isChecked():
            # Dibujar graficos y ocultar texto
            self.temp_widget.setVisible(False)
            self.accel_widget.setVisible(False)
            self.alti_widget.setVisible(False)
            self.pres_widget.setVisible(False)

            self.temp_graph.setVisible(True)
            self.acel_graph.setVisible(True)
            self.alti_graph.setVisible(True)
            self.pres_graph.setVisible(True)


        else:
            # Dibujar texto y ocultar graficos
            self.temp_widget.setVisible(True)
            self.accel_widget.setVisible(True)
            self.alti_widget.setVisible(True)
            self.pres_widget.setVisible(True)

            self.temp_graph.setVisible(False)
            self.acel_graph.setVisible(False)
            self.alti_graph.setVisible(False)
            self.pres_graph.setVisible(False)


    # Handlers
    def handle_communication_error(self, data:str):
        self.conn_window.center() # Mostrar la ventana de comunicacion
        self.conn_window.show()
        self.setVisible(False)
        QMessageBox.critical(self, ERRORMSG_TITLE, data.capitalize())
        self.conn_window.enable_window()
        self.conn_window.show()
        self.close()
    # El hilo termina automaticamente al detectar un error de comunicacion, por eso no
    # se finaliza manualmente desde este metodo


    def handle_gndstation_error(self, data:str):
        self.conn_window.center()
        self.conn_window.show() # Mostrar ventana de conexion
        self.setVisible(False)
        self.comm_thread.terminate() # Terminar hilo de comunicacion manualmente (se trata de un error de estacion terrena)
        QMessageBox.critical(self, ERRORMSG_TITLE, data.capitalize())
        self.conn_window.enable_window()
        self.conn_window.show()
        self.close()


    def handle_received_data(self, data):
        print(data)
        self.statusbar.showMessage(data)

        if (data.startswith(ERROR_START)): # Si se reciben datos, pero se trata de un error de la estacion, se manda a llamar el metodo
            self.handle_gndstation_error(data)
            return 0

        raw_data = data.split(DATA_SEPARATOR) # Separar datos

        # Asignar datos a variables en la forma
        # altitud, presion, x, y, z, temp
        # Ademas de calcular el roll y pitch en base a las aceleraciones
        if(len(raw_data) == 6):
            altitude = int(raw_data[0])
            pressure = raw_data[1]
            accelX = int(raw_data[2])
            accelY = int(raw_data[3])
            accelZ = int(raw_data[4])
            temp = raw_data[5]
            roll = math.atan2(accelY, accelZ)
            pitch = math.atan2(-accelX, math.sqrt(accelY * accelY + accelZ * accelZ))

            # Actualizar graficos y labels
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









