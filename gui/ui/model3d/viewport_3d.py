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


import matplotlib.pyplot as plt
import meshio
import numpy as np
from PyQt6.QtWidgets import QVBoxLayout, QFrame
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from mpl3d import glm
from mpl3d.camera import Camera
from mpl3d.mesh import Mesh

from utils.constants import *


def frustum(left, right, bottom, top, znear, zfar):
    M = np.zeros((4, 4), dtype=np.float32)
    M[0, 0] = +2.0 * znear / (right - left)
    M[1, 1] = +2.0 * znear / (top - bottom)
    M[2, 2] = -(zfar + znear) / (zfar - znear)
    M[0, 2] = (right + left) / (right - left)
    M[2, 1] = (top + bottom) / (top - bottom)
    M[2, 3] = -2.0 * znear * zfar / (zfar - znear)
    M[3, 2] = -1.0
    return M


def perspective(fovy, aspect, znear, zfar):
    h = np.tan(0.5 * np.radians(fovy)) * znear
    w = h * aspect
    return frustum(-w, w, -h, h, znear, zfar)


def translate(x, y, z):
    return np.array([[1, 0, 0, x], [0, 1, 0, y],
                     [0, 0, 1, z], [0, 0, 0, 1]], dtype=float)


def xrotate(theta):
    t = np.pi * theta / 180
    c, s = np.cos(t), np.sin(t)
    return np.array([[1, 0, 0, 0], [0, c, -s, 0],
                     [0, s, c, 0], [0, 0, 0, 1]], dtype=float)


def yrotate(theta):
    t = np.pi * theta / 180
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, 0, s, 0], [0, 1, 0, 0],
                     [-s, 0, c, 0], [0, 0, 0, 1]], dtype=float)


def zrotate(theta):
    t = np.pi * theta / 180
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s, 0, 0], [s, c, 0, 0],
                     [0, 0, 1, 0], [0, 0, 0, 1]], dtype=float)

# Widget que se insertara en la ventana
class Viewport3D(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        #self.setFrameShape(QFrame.Shape.Box)
        #self.setFrameShadow(QFrame.Shadow.Plain)


        self.layout = QVBoxLayout(self)

        self.canvas = Canvas3D(self)
        self.layout.addWidget(self.canvas)
        self.plot()


    def plot(self):
        self.camera = Camera(CAMERA_MODE, scale=CAMERA_SCALE)

        self.mesh_data = meshio.read(MESH_PATH)
        self.vertices = self.mesh_data.points
        self.faces = self.mesh_data.cells[0].data
        self.vertices = glm.fit_unit_cube(self.vertices)
        self.mesh = Mesh(self.canvas.axis, self.camera.transform, self.vertices, self.faces,
                         cmap=plt.get_cmap(MESH_COLORMAP), edgecolors=(0, 0, 0, 0.25))

        self.camera.connect(self.canvas.axis, self.mesh.update)
        self.canvas.draw()

    def rotate(self, angle_x, angle_y, angle_z):
        MVP = perspective(25, 1, 1, 100) @ translate(0, 0, -3.5) @ xrotate(angle_x) @ yrotate(angle_y) @ zrotate(
            angle_z)
        self.mesh.update(MVP)
        self.canvas.draw()


# Actua como lienzo para el widget
class Canvas3D(FigureCanvas):
    def __init__(self, parent=None):
        mpl_figure = Figure(figsize=(4, 4))
        mpl_figure.set_facecolor(MESH_BACKGROUND)

        self.axis = mpl_figure.add_axes([0, 0, 1, 1], xlim=[-1, +1], ylim=[-1, +1], aspect=1)
        self.axis.axis("off")

        super().__init__(mpl_figure)
        self.setParent(parent)


