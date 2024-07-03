import sys

from PyQt6.QtWidgets import QApplication
from Cansat.gui.ui.wait_cansat_window import WaitCansatWindow

app = QApplication(sys.argv)
window = WaitCansatWindow()
window.show()
sys.exit(app.exec())