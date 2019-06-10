#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2019 Christopher Hahne <inbox@christopherhahne.de>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import Axes3D

try:
    import tkinter as tk
    from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
except ImportError:
    import Tkinter as tk
    from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as NavigationToolbar2Tk

from plenoptisign.constants import BTN_W, FIG_SIZE

# make object for plot widget
class PltWidget(tk.Frame):

    def __init__(self, parent):

        # inheritance
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # figure init
        self.fig = Figure(figsize=FIG_SIZE)
        self.ax = self.fig.gca()

        # a tk.DrawingArea
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        toolbar = NavigationToolbar2Tk(self.canvas, self)
        toolbar.update()
        toolbar.pack(side=tk.BOTTOM)
        toolbar.home()

        # toggle refo/tria button
        dep_btn = tk.Button(master=self, text='refo/tria toggle', width=BTN_W, command=self.toggle_dep_type)
        dep_btn.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

        # toggle 2D/3D button
        dim_btn = tk.Button(master=self, text='2D/3D toggle', width=BTN_W, command=self.toggle_dim_type)
        dim_btn.pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

        # default toggle settings
        self.dep_type = False
        self.dim_type = True

    def refresh(self):
        ''' update window '''

        self.ax.clear()
        if self.dim_type:
            if self.dep_type:
                self.ax = self.parent.obj.plt_tria(self.ax)
            else:
                self.ax = self.parent.obj.plt_refo(self.ax)
        else:
            amin = self.parent.obj.dx if self.dep_type else self.parent.obj.a
            self.ax = self.parent.obj.plt_3d(self.ax, amin=amin, dep_type=self.dep_type)
        self.canvas.draw()

    @staticmethod
    def xor(a, b):
        return bool(a) != bool(b)

    def toggle_dep_type(self):
        self.dep_type = self.xor(self.dep_type, 1)
        self.refresh()

    def toggle_dim_type(self):
        self.dim_type = self.xor(self.dim_type, 1)
        self.change_dim_type()
        self.refresh()

    def change_dim_type(self):
        self.fig.delaxes(self.ax)
        if self.dim_type:
            self.fig.set_size_inches(FIG_SIZE, forward=True)
            self.ax = self.fig.gca()
        else:
            self.ax = Axes3D(self.fig)
            self.parent.obj.plt_3d_init(self.fig, self.ax)