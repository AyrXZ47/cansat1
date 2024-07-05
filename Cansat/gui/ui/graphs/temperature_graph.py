import pyqtgraph as qtgraph
import numpy
from PyQt6.QtCore import QTimer, Qt
from Cansat.gui.utils.constants import *

class TemperatureGraph(qtgraph.PlotWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        pen_color = (TEMP_COLOR)
        pen_width = GRAPH_PENWIDTH
        self.temp_plot = self.plot(pen=qtgraph.mkPen(color=pen_color, width=pen_width, antialias=GRAPH_ANTIALIAS, style=GRAPH_PENSTYLE))
        self.temp_data = numpy.linspace(0, 0, GRAPH_HISTORYSIZE)
        self.ptr = 0
        self.setBackground(GRAPH_BACKGROUND)
        self.setMouseEnabled(x=GRAPH_ENABLEMOUSE, y=GRAPH_ENABLEMOUSE)
        # self.timer = QTimer(self)
        # self.timer.timeout.connect(self.update_data)
        # self.timer.start(GRAPH_UPDINTERVAL)


    # TODO Actualizar método para recibir datos de la estacion terrena
    def update_data(self, new_data):
        self.temp_data = numpy.roll(self.temp_data, -1)
        self.temp_data[-1] = new_data
        self.temp_plot.setData(self.temp_data)


