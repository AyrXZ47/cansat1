from PyQt6.QtWidgets import QApplication
from Cansat.gui.ui.main_window import MainWindow
from Cansat.gui.ui.connection_window import ConnectionWindow

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ConnectionWindow()
    window.show()
    sys.exit(app.exec())