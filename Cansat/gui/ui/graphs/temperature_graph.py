import pyqtgraph as qtgraph
import numpy
from PyQt6.QtCore import QTimer, Qt

# TODO Necesita refactor, solo es para probar :p
class TemperatureGraph(qtgraph.PlotWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        pen_color = (255, 0, 0)
        pen_width = 3
        self.temp_plot = self.plot(pen=qtgraph.mkPen(color=pen_color, width=pen_width, antialias=True, style=Qt.PenStyle.DashLine))
        self.temp_data = numpy.linspace(0, 0, 30)
        self.ptr = 0
        self.setBackground('w')
        self.setMouseEnabled(x=False, y=False)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(500)


    def update_data(self):
        new_data = numpy.random.normal(size=30)
        self.temp_data = numpy.roll(self.temp_data, -1)
        self.temp_data[-1] = new_data[-1]
        self.temp_plot.setData(self.temp_data)



    # def init_graph(self):
    #     x = numpy.linspace(0, 100, 50)
    #     self.plo