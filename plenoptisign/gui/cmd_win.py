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

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

from sys import exit
from plenoptisign import PX, PY, BTN_W

# make object for plot window
class CmdWin(tk.Frame):

    def __init__(self, parent):

        # inheritance
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # run button
        run_btn = tk.Button(self, text="Run", width=int(BTN_W/2), command=self.parent.run)
        run_btn.grid(row=0, column=0, padx=PX, pady=PY)

        # micro image button
        mie_btn = tk.Button(master=self, text='Estimate M', width=BTN_W, command=self.parent.mie)
        mie_btn.grid(row=0, column=1, padx=PX, pady=PY)

        # save button
        sav_btn = tk.Button(self, text="Save config", width=BTN_W, command=self.parent.save_cfg)
        sav_btn.grid(row=0, column=2, padx=PX, pady=PY)

        # quit button
        qit_btn = tk.Button(master=self, text='Quit', width=int(BTN_W/2), command=exit)
        qit_btn.grid(row=0, column=3, padx=PX, pady=PY)