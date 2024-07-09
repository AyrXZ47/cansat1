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
VERSION = "v0.6.4"
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
WAITING_STARTING2 = "pablo"



# TEXTOS DE VENTANA DE ESPERA
WAITWINDOW_TITLE = "Espere..."
WAITWINDOW_LABEL = "Esperando estación terrena..."
WAITWINDOW_CANCEL = "Cancelar"

# VALORES POR DEFECTO DE GRAFICAS
GRAPH_BACKGROUND = 'k'
GRAPH_UPDINTERVAL = 500
GRAPH_ENABLEMOUSE = False
GRAPH_PENWIDTH = 2
GRAPH_HISTORYSIZE = 30
GRAPH_ANTIALIAS = True
GRAPH_PENSTYLE = Qt.PenStyle.SolidLine

# VALORES ESPECIFICOS PARA CADA GRAFICA
TEMP_COLOR = [255, 0, 0]  # rojo
ACCL_COLOR1 = [153, 0, 153]
ACCL_COLOR2 = [153, 153, 0]
ACCL_COLOR3 = [204, 102, 0]
ALTI_COLOR = [0, 0, 255]
PRES_COLOR = [0, 255, 0]


# VALORES DE VISOR 3D
MESH_NAME = "lowsoda.obj"
MESH_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', MESH_NAME)
MESH_COLORMAP = "viridis"
MESH_BACKGROUND = 'gray'
CAMERA_MODE = "ortho"
CAMERA_SCALE = 1


# CONSTANTES DE CONFIGURACION
CONFIG_NAME = "DEFAULT"
CONFIG_FILE = 'cansat_monitor.ini'
FIELD_UNITS = "units"
FIELD_PORT = "port"
FIELD_LANGUAGE = "language"

# CODIGOS DE ESTADO
STATUS_CODE = {
    1: "Estación terrena lista para recibir datos del CANSAT.",
    2: "Esperando la señal del CANSAT...",
    -1: "Error al iniciar la tarjeta SD",
    -2: "Error al abrir el archivo DATA.csv"
}

# FUNCIONES
def check_home():
    cansat_folder = Path.home() / ".cansat"
    cansat_folder.mkdir(exist_ok=True)
    return cansat_folder

# INICIALIZAR CARPETA
HOME_FOLDER = check_home()

