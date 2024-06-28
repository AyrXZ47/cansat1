from pathlib import Path

VERSION = "v0.0.1"

def check_home():
    cansat_folder = Path.home() / ".cansat"
    cansat_folder.mkdir(exist_ok=True)
    return cansat_folder


WINDOW_TITLE = "Visualizador de CanSat " + VERSION
DEFAULT_BAUDRATE = 9600
NULL_COMMUNICATION = 'No se ha abierto la comunicación'
HOME_FOLDER = check_home()


#TEXTOS DE VENTANA DE CONEXIÓN
CONNWINDOW_TEXT = "Establecer conexión con estación terrena"
CONNWINDOW_PORT = "Puerto serie"
CONNWINDOW_SPEED = "Velocidad de transmisión"
CONNWINDOW_BEGIN = "Iniciar"

TRANSM_SPEED = ["300", "600", "1200", "2400", "4800", "9600", "14400", "28800", "38400", "57600", "115200"]



# CONSTANTES DE CONFIGURACIÓN
CONFIG_NAME = "DEFAULT"
CONFIG_FILE = 'cansat_monitor.ini'
FIELD_UNITS = "units"
FIELD_PORT  = "port"
FIELD_LANGUAGE = "language"




STATUS_CODE = {
    1: "Estación terrena lista para recibir datos del CANSAT.",
    2: "Esperando la señal del CANSAT...",
    -1: "Error al iniciar la tarjeta SD",
    -2: "Error al abrir el archivo DATA.csv"
}


