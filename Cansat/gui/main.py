from PyQt6.QtWidgets import QApplication

from ui.main_window import MainWindow
from serial_communication.arduino_comm import ArduinoComm

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())



