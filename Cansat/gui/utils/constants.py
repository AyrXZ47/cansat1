from pathlib import Path

def check_home():
    cansat_folder = Path.home() / ".cansat"
    cansat_folder.mkdir(exist_ok=True)
    return cansat_folder


WINDOW_TITLE = "Visualizador de CanSat"
DEFAULT_BAUDRATE = 9600
NULL_COMMUNICATION = 'No se ha abierto la comunicación'
HOME_FOLDER = check_home()


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


