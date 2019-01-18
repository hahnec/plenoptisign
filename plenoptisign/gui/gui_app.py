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

from os.path import join, abspath
from tempfile import mkstemp
#from sys import platform

# local python files
from plenoptisign import __version__, ABBS, PF, DEC_P
from plenoptisign.mainclass import MainClass
from plenoptisign.gui.cfg import Config
from plenoptisign.gui.cfg_win import CfgWin
from plenoptisign.gui.plt_win import PltWin
from plenoptisign.gui.cmd_win import CmdWin
from plenoptisign.gui.con_win import ConWin

ICON = (b'\x00\x00\x01\x00\x01\x00\x10\x10\x00\x00\x01\x00\x08\x00h\x05\x00\x00'
        b'\x16\x00\x00\x00(\x00\x00\x00\x10\x00\x00\x00 \x00\x00\x00\x01\x00'
        b'\x08\x00\x00\x00\x00\x00@\x05\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        b'\x00\x01\x00\x00\x00\x01') + b'\x00'*1282 + b'\xff'*64

_, ICON_PATH = mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

# object for application window
class PlenoptisignApp(tk.Tk):

    def __init__(self, parent):

        tk.Tk.__init__(self, parent)
        self.parent = parent

        # window title
        self.wm_title("Plenoptisign-"+__version__)

        # icon handling
        self.iconbitmap(default=ICON_PATH)
        #if platform == 'win32':
            #self.iconbitmap(join(abspath('.'), 'circlecompass_1055093.ico'))

        # initialize parameters
        self.cfg = Config()

        # instantiate plot window widget as object
        self.plt_win = PltWin(self)
        self.plt_win.grid(row=0, column=0, rowspan=2, padx=PF, pady=PF)

        # instantiate config window widget as object
        self.cfg_win = CfgWin(self)
        self.cfg_win.grid(row=0, column=1, padx=PF, pady=PF, sticky='NSWE')

        # instantiate command window widget as object
        self.con_win = ConWin(self)
        self.con_win.grid(row=1, column=1, padx=PF, pady=PF, sticky='NSWE')

        # instantiate command window widget as object
        self.cmd_win = CmdWin(self)
        self.cmd_win.grid(row=2, column=1, padx=PF, pady=PF)

        # enable tkinter resizing
        self.resizable(True, False)

        self.run()

        return None


    def run(self):

        # get parameter data from GUI
        data = dict(zip(ABBS, [float(entry.get()) for entry in self.cfg_win.entries]))

        # construct object
        self.obj = MainClass(data)

        # compute light field geometry
        self.obj.refo()
        self.obj.tria()

        # update widgets
        self.cfg_win.refresh()
        self.plt_win.refresh()

        self.con_win.msg_box.config(text=self.obj.console_msg)

        return True

    def mie(self):

        # compute micro image size
        self.obj.get_mic_img_size()

        # pass estimated micro image size to entry in GUI
        tk_var = tk.StringVar()
        tk_var.set(str(round(self.obj.M, DEC_P)))
        self.cfg_win.entries[10].config(textvariable=tk_var)

        return True

    def save_cfg(self):
        ''' overwrite config settings '''

        self.con_win.msg_box.config(text='Save settings ...')

        # update results (if changes were made)
        self.run()

        # read parameters
        for i, key in enumerate(ABBS):
            self.cfg.params[key] = float(self.cfg_win.entries[i].get())

        # write parameters to hard drive
        self.cfg.write_json()

        self.con_win.msg_box.config(text='Config saved!')

        return True


if __name__ == "__main__":
    try:
        MainWin = PlenoptisignApp(None)
        MainWin.mainloop()
    except Exception as e:
        print(e)
        input()