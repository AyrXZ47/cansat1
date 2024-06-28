from configparser import ConfigParser
from Cansat.gui.utils.constants import HOME_FOLDER, CONFIG_FILE, CONFIG_NAME, FIELD_UNITS, FIELD_PORT, FIELD_LANGUAGE


config = ConfigParser()

# Configuración por defecto del programa
config[CONFIG_NAME] = {
    FIELD_UNITS: "metric",
    FIELD_PORT: "None",
    FIELD_LANGUAGE: "es"
}

language = ["es", "en"]
units = ["metric", "us_imperial"]




# FIXME REVISAR, VALIDAR CONFIGURACIÓN, SI ES INVALIDA, REESCRIBIR USANDO CONFIGURACION POR DEFECTO

def make_config_file():
    with open(HOME_FOLDER / CONFIG_FILE, "w") as f:
        config.write(f)

def validate_config(user_config):
    if(user_config[CONFIG_NAME][FIELD_UNITS] not in units):
        return False

    if(user_config[CONFIG_NAME][FIELD_LANGUAGE] not in language):
        return False

    return True



def load_config_file():
    try:
        config_data = ConfigParser()
        config_data.read(HOME_FOLDER / CONFIG_FILE)
        if not validate_config(config_data):
            make_config_file()
            config_data.read(HOME_FOLDER / CONFIG_FILE)
    except:
        make_config_file()
        config_data.read(HOME_FOLDER / CONFIG_FILE)

    return config_data


