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

import pyqtgraph as qtgraph
import numpy
from PyQt6.QtCore import QTimer, Qt
from utils.constants import *

class ThreePenGraph(qtgraph.PlotWidget):

    def __init__(self, graph_color1, graph_color2, graph_color3,parent=None):
        super().__init__(parent)
        pen_color = (graph_color1)
        pen_width = GRAPH_PENWIDTH

        self.temp_plotX = self.plot(
            pen=qtgraph.mkPen(color=graph_color1, width=pen_width, antialias=GRAPH_ANTIALIAS, style=GRAPH_PENSTYLE))
        self.temp_plotY = self.plot(
            pen=qtgraph.mkPen(color=graph_color2, width=pen_width, antialias=GRAPH_ANTIALIAS, style=GRAPH_PENSTYLE))
        self.temp_plotZ = self.plot(
            pen=qtgraph.mkPen(color=graph_color3, width=pen_width, antialias=GRAPH_ANTIALIAS, style=GRAPH_PENSTYLE))

        self.temp_dataX = numpy.linspace(0, 0, GRAPH_HISTORYSIZE)
        self.temp_dataY = numpy.linspace(0, 0, GRAPH_HISTORYSIZE)
        self.temp_dataZ = numpy.linspace(0, 0, GRAPH_HISTORYSIZE)

        self.ptr = 0
        self.setBackground(GRAPH_BACKGROUND)
        self.setMouseEnabled(x=GRAPH_ENABLEMOUSE, y=GRAPH_ENABLEMOUSE)

    def update_data(self, new_dataX, new_dataY, new_dataZ):
        self.temp_dataX = numpy.roll(self.temp_dataX, -1)
        self.temp_dataX[-1] = new_dataX
        self.temp_plotX.setData(self.temp_dataX)

        self.temp_dataY = numpy.roll(self.temp_dataY, -1)
        self.temp_dataY[-1] = new_dataY
        self.temp_plotY.setData(self.temp_dataY)

        self.temp_dataZ = numpy.roll(self.temp_dataZ, -1)
        self.temp_dataZ[-1] = new_dataZ
        self.temp_plotZ.setData(self.temp_dataZ)


