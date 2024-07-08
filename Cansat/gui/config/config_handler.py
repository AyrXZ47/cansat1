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

from configparser import ConfigParser
from Cansat.gui.utils.constants import HOME_FOLDER, CONFIG_FILE, CONFIG_NAME, FIELD_UNITS, FIELD_PORT, FIELD_LANGUAGE

# TODO Esto debe ser una clase

config = ConfigParser()

# Configuración por defecto del programa
config[CONFIG_NAME] = {
    FIELD_UNITS: "metric",
    FIELD_PORT: "None"
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


