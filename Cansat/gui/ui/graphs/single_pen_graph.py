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

class SinglePenGraph(qtgraph.PlotWidget):

    def __init__(self, graph_color,parent=None, title=""):
        super().__init__(parent)
        pen_color = (graph_color)
        pen_width = GRAPH_PENWIDTH
        self.temp_plot = self.plot(pen=qtgraph.mkPen(color=pen_color, width=pen_width, antialias=GRAPH_ANTIALIAS, style=GRAPH_PENSTYLE))
        self.temp_data = numpy.linspace(0, 0, GRAPH_HISTORYSIZE)
        self.ptr = 0
        self.setBackground(GRAPH_BACKGROUND)
        self.setMouseEnabled(x=GRAPH_ENABLEMOUSE, y=GRAPH_ENABLEMOUSE)
        self.setTitle(title, color=ACCENT_COLOR, size=GRAPH_TITLESIZE)


    def update_data(self, new_data):
        self.temp_data = numpy.roll(self.temp_data, -1)
        self.temp_data[-1] = new_data
        self.temp_plot.setData(self.temp_data)


