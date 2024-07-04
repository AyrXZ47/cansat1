from Cansat.gui.config import config_handler
from Cansat.gui.utils.constants import CONFIG_NAME, FIELD_LANGUAGE, FIELD_PORT, FIELD_UNITS

a = config_handler.load_config_file()
print(a[CONFIG_NAME][FIELD_UNITS])
print(a[CONFIG_NAME][FIELD_PORT])

print("-----")

config_handler.make_config_file()
a = config_handler.load_config_file()
print(a[CONFIG_NAME][FIELD_UNITS])
print(a[CONFIG_NAME][FIELD_PORT])

