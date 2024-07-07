from pathlib import Path
from PyQt6.QtCore import QTimer, Qt

# Version
VERSION = "v0.3.1"

# CONSTANTES
WINDOW_TITLE = "Visualizador de CanSat " + VERSION
DEFAULT_BAUDRATE = 9600
NULL_COMMUNICATION = 'No se ha abierto la comunicación'

# TEXTOS DE VENTANA DE CONEXION
CONNWINDOW_TEXT = "Establecer conexión con estación terrena"
CONNWINDOW_PORT = "Puerto serie"
CONNWINDOW_SPEED = "Velocidad de transmisión"
CONNWINDOW_BEGIN = "Iniciar"
TRANSM_SPEED = [
    "300", "600", "1200", "2400", "4800", "9600",
    "14400", "28800", "38400", "57600", "115200"
]

# TEXTOS DE VENTANA DE ESPERA
WAITWINDOW_LABEL = "Esperando señal del CanSat"
WAITWINDOW_CANCEL = "Cancelar"

# VALORES POR DEFECTO DE GRAFICAS
GRAPH_BACKGROUND = 'w'
GRAPH_UPDINTERVAL = 500
GRAPH_ENABLEMOUSE = False
GRAPH_PENWIDTH = 3
GRAPH_HISTORYSIZE = 100
GRAPH_ANTIALIAS = False
GRAPH_PENSTYLE = Qt.PenStyle.DotLine

# VALORES ESPECIFICOS PARA CADA GRAFICA
TEMP_COLOR = [255, 0, 0]  # rojo
# ACELERACION
# ALTITUD
# PRESION

# VALORES DE VISOR 3D
MESH_PATH = "lowsoda.obj"
MESH_COLORMAP = "magma"
CAMERA_MODE = "ortho"
CAMERA_SCALE = 2

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