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
import os
from pathlib import Path
from PyQt6.QtCore import QTimer, Qt

# Version
VERSION = "v0.7.3-rc"
DEBUG = True



# CONSTANTES
WINDOW_TITLE = "Dragon's CanSat Monitor" + " " + VERSION
DEFAULT_BAUDRATE_INDEX = 5
TRANSM_SPEED = [
    "300", "600", "1200", "2400", "4800", "9600",
    "14400", "28800", "38400", "57600", "115200"
]
NULL_COMMUNICATION = 'No se ha abierto la comunicación'
DECODE_MODE = 'utf-8'
DEFAULT_BAUDRATE = TRANSM_SPEED[DEFAULT_BAUDRATE_INDEX]
FONT = "'Consolas', 'Courier New', monospace'"

# TEXTOS DE VENTANA PRINCIPAL
TEMP_UNIT = " ˚C"
ACEL_UNIT = " m/s"
PRES_UNIT = " hPa"
ALTI_UNIT = " m"
DATA_SEPARATOR = ","
MAINWINDOW_GRAPH_CHECKBOX = "Mostrar gráficos   "
TEMP_PLACEHOLDER = "-- ˚C"
ACEL_PLACEHOLDER = "-- m/s"
PRES_PLACEHOLDER = "-- hPa"
ALTI_PLACEHOLDER = "-- m"


# TEXTOS DE VENTANA DE CONEXION
CONNWINDOW_TEXT = "Establecer conexión con estación terrena"
CONNWINDOW_PORT = "Puerto serie"
CONNWINDOW_SPEED = "Velocidad de transmisión"
CONNWINDOW_BEGIN = "Iniciar"
CONNWINDOW_RELOAD = "Recargar"
ERRORMSG_TITLE = "Error"
ERRORMSG_COMM = "Hubo un error en la comunicación"
CONNWINDOW_DEBUG = "Debug"

# TEXTOS DE HANDLER DEL ARDUINO
ERROR_START = "e"
WAITING_STARTING1 = "Esperando"


# TEXTOS DE VENTANA DE ESPERA
WAITWINDOW_TITLE = "Espere..."
WAITWINDOW_LABEL = "Esperando estación terrena..."
WAITWINDOW_CANCEL = "Cancelar"

# VALORES POR DEFECTO DE GRAFICAS
GRAPH_UPDINTERVAL = 500
GRAPH_ENABLEMOUSE = False
GRAPH_PENWIDTH = 2
GRAPH_HISTORYSIZE = 30
GRAPH_ANTIALIAS = True
GRAPH_PENSTYLE = Qt.PenStyle.SolidLine
GRAPH_TITLESIZE = '10pt'


# VALORES ESPECIFICOS PARA CADA GRAFICA
TEMP_COLOR = [255, 0, 0]  # rojo
ACCL_COLOR1 = [153, 0, 153]
ACCL_COLOR2 = [153, 153, 0]
ACCL_COLOR3 = [204, 102, 0]
ALTI_COLOR = [0, 0, 255]
PRES_COLOR = [0, 255, 0]


TEMP_TITLE = "Temperatura"
ACCL_TITLE = "Aceleración"
ALTI_TITLE = "Altitud"
PRES_TITLE = "Presión"



# VALORES DE VISOR 3D
# This project uses the 3D model "Low Poly Soda Can"
# by sanekcloff, available at https://skfb.ly/owLss
# licensed under CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/).
# Removed texture mappings
MESH_NAME = "lowsoda.obj"
MESH_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', MESH_NAME)
CAMERA_MODE = "ortho"
CAMERA_SCALE = 1

APPLY_CSS_STYLE = True
BACKGROUND_COLOR = "#141824"
TEXT_COLOR = "#00ccff"
ACCENT_COLOR = "#00ccff"
BUTTON_COLOR = "#141824"
MESH_BACKGROUND = BACKGROUND_COLOR
MESH_COLORMAP = "cool"
# https://matplotlib.org/stable/users/explain/colors/colormaps.html
GRAPH_BACKGROUND = BACKGROUND_COLOR
BORDER_THICKNESS = "1px"



# HOJA DE ESTILOS PARA INTERFAZ
STYLE_SHEET = f"""
QWidget {{
                        background-color: {BACKGROUND_COLOR};
                        color: {TEXT_COLOR};
                        font-family: 'Consolas', 'Courier New', monospace;

                    }}

                    QPushButton {{
                        background-color: {BUTTON_COLOR};
                        border: {BORDER_THICKNESS} solid {ACCENT_COLOR};
                        color: {TEXT_COLOR};
                        padding: 10px;
                        font-size: 16px;
                        border-radius: 5px;
                    }}

                    QPushButton:hover {{
                        background-color: {ACCENT_COLOR};
                        color: {BUTTON_COLOR};
                    }}

                    QLabel {{
                        color: {TEXT_COLOR};
                        font-size: 18px;
                    }}

                    SinglePenGraph, ThreePenGraph {{
                        background-color: {BACKGROUND_COLOR};
                        border: {BORDER_THICKNESS} solid {ACCENT_COLOR};
                        border-radius: 5px;
                    }}

                    Viewport3D {{
                        border: {BORDER_THICKNESS} solid {ACCENT_COLOR};
                        padding: 10px; 
                    }}

                    QCheckBox {{
                        font-size: 16px;
                        padding: 5px;
                    }}

                    QStatusBar {{
                        background-color: {BACKGROUND_COLOR};
                        color: {TEXT_COLOR};
                        font-size: 16px;
                    }}

                    QLabel {{
                        font-size: 36px;
                    }}

                    Viewport3D {{
                        border: {BORDER_THICKNESS} solid {ACCENT_COLOR};
                    }}
"""

# FUNCIONES
def check_home():
    cansat_folder = Path.home() / ".cansat"
    cansat_folder.mkdir(exist_ok=True)
    return cansat_folder

# INICIALIZAR CARPETA
HOME_FOLDER = check_home()




