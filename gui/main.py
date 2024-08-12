# Copyright (C) 2024  Ndahai Arenas
#
# Tuzo CanSat Monitor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Tuzo CanSat Monitor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Tuzo CanSat Monitor. If not, see <http://www.gnu.org/licenses/>.
import os

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from ui.connection_window import ConnectionWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ConnectionWindow()
    window.show()
    sys.exit(app.exec())

# EMPAQUETAR MAC Y LINUX
# Sin consola
# pyinstaller --onefile --windowed --icon=resources/icon.icns --add-data "resources/cone.obj:resources" --add-data "resources/lowsoda.obj:resources" main.py
# Con consola
# pyinstaller --onefile --icon=resources/icon.icns --add-data "resources/cone.obj:resources" --add-data "resources/lowsoda.obj:resources" main.py

# Empaquetar Windows
# Sin consola
# pyinstaller --onefile --windowed --icon=resources/icono.ico --add-data "resources/cone.obj:resources" --add-data "resources/lowsoda.obj:resources" --name cansat-monitor main.py

# Con consola
# pyinstaller --onefile --icon=resources/icono.ico --add-data "resources/cone.obj:resources" --add-data "resources/lowsoda.obj:resources" --name cansat-monitor main.py