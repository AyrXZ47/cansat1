# -----------------------------------------------------------------------------
# Copyright (c) 2020 Nicolas P. Rougier. All rights reserved.
# Distributed under the (new) BSD License.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions, and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions, and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Modified by Ndahai Arenas in 2024.
#
# This file is part of a project that is licensed under the GPLv3.
# You should have received a copy of the GNU General Public License along with this software.
# If not, see <https://www.gnu.org/licenses/>.
# -----------------------------------------------------------------------------



import numpy as np
from PyQt6.QtWidgets import QWidget, QVBoxLayout
from mpl3d import glm
from mpl3d.mesh import Mesh
from mpl3d.camera import Camera
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import meshio

# TODO Mover valores a clase de constantes
class Viewport3D(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout(self)

        self.canvas = Canvas3D(self)
        self.layout.addWidget(self.canvas)
        self.plot()

    def plot(self):
        camera = Camera("ortho", scale=2)

        mesh = meshio.read("lowsoda.obj")
        vertices = mesh.points
        faces = mesh.cells[0].data
        vertices = glm.fit_unit_cube(vertices)
        mesh = Mesh(self.canvas.axis, camera.transform, vertices, faces, cmap=plt.get_cmap("magma"), edgecolors=(0,0,0,0.25))

        camera.connect(self.canvas.axis, mesh.update)
        self.canvas.draw()



class Canvas3D(FigureCanvas):
    def __init__(self, parent=None):
        mpl_figure = Figure(figsize=(4,4))

        self.axis = mpl_figure.add_axes([0,0,1,1], xlim=[-1, +1], ylim=[-1,+1], aspect=1)
        self.axis.axis("off")

        super().__init__(mpl_figure)
        self.setParent(parent)


# --- main --------------------------------------------------------------------
# if __name__ == "__main__":
#     import matplotlib.pyplot as plt
#
#     fig = plt.figure(figsize=(4,4))
#     ax = fig.add_axes([0,0,1,1], xlim=[-1,+1], ylim=[-1,+1], aspect=1)
#     ax.axis("off")
#
#     camera = Camera("ortho", scale=2)
#     mesh = meshio.read("../../resources/lowsoda.obj")
#     vertices = mesh.points
#     faces = mesh.cells[0].data
#     vertices = glm.fit_unit_cube(vertices)
#     mesh = Mesh(ax, camera.transform, vertices, faces,
#                 cmap=plt.get_cmap("magma"),  edgecolors=(0,0,0,0.25))
#     camera.connect(ax, mesh.update)
#     plt.show()
