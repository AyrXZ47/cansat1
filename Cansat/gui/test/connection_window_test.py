import sys

from PyQt6.QtWidgets import QApplication
from Cansat.gui.ui.connection_window import ConnectionWindow

app = QApplication(sys.argv)
window = ConnectionWindow()
window.show()
sys.exit(app.exec())