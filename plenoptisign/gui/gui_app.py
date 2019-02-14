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
    from tkinter.filedialog import askopenfilename
except ImportError:
    import Tkinter as tk
    from tkFileDialog import askopenfilename

from tempfile import mkstemp
import sys
from os.path import normpath

# local python files
from plenoptisign import __version__, ABBS, PF, DEC_P, PlenoptisignError
from plenoptisign.mainclass import MainClass
from plenoptisign.gui.cfg import Config
from plenoptisign.gui.cfg_widget import CfgWidget
from plenoptisign.gui.plt_widget import PltWidget
from plenoptisign.gui.cmd_widget import CmdWidget
from plenoptisign.gui.con_widget import ConWidget
from plenoptisign.gui.abt_widget import AbtWidget

# generate blank icon on windows
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
        if sys.platform == 'win32':
            self.iconbitmap(default=ICON_PATH)

        # initialize parameters
        self.cfg = Config()

        # instantiate plot widget as object
        self.plt_wid = PltWidget(self)
        self.plt_wid.grid(row=0, column=0, rowspan=2, padx=PF, pady=PF)

        # instantiate config widget as object
        self.cfg_wid = CfgWidget(self)
        self.cfg_wid.grid(row=0, column=1, padx=PF, pady=PF, sticky='NSWE')

        # instantiate command widget as object
        self.con_wid = ConWidget(self)
        self.con_wid.grid(row=1, column=1, padx=PF, pady=PF, sticky='NSWE')

        # instantiate command widget as object
        self.cmd_wid = CmdWidget(self)
        self.cmd_wid.grid(row=2, column=1, padx=PF, pady=PF)

        # enable tkinter resizing
        self.resizable(True, False)

        # update results in GUI
        self.run()

    def run(self):

        # fetch parameter data from GUI
        self.data = dict(zip(ABBS, [float(entry.get()) for entry in self.cfg_wid.entries]))

        # construct object
        self.obj = MainClass(self.data)

        # compute light field geometry
        self.obj.refo()
        self.obj.tria()

        # update widgets
        self.cfg_wid.refresh()
        self.plt_wid.refresh()

        self.con_wid.msg_box.config(text=self.obj.console_msg)

        return True

    def mie(self):

        # compute micro image size
        self.obj.compute_mic_img_size()

        # pass estimated micro image size to entry in GUI
        tk_var = tk.StringVar()
        tk_var.set(str(round(self.obj.M, DEC_P)))
        self.cfg_wid.entries[10].config(textvariable=tk_var)

        # update results in GUI
        self.run()

        return True

    def save_cfg(self):
        ''' overwrite config file settings '''

        self.con_wid.msg_box.config(text='Save settings ...')

        # update results in GUI
        self.run()

        # transfer parameters from GUI to config object
        for i, key in enumerate(ABBS):
            self.cfg.params[key] = float(self.cfg_wid.entries[i].get())

        # write parameters from config object to hard drive
        self.cfg.write_json()

        self.con_wid.msg_box.config(text='Config saved')

        return True

    def load_cfg(self):
        ''' load config file settings '''

        # open window to select config file
        cfn_win = tk.Tk()
        cfn_win.withdraw()
        cfn = normpath(askopenfilename(parent=cfn_win, title="Select file", filetypes=[("Config files", "*.json")]))

        if cfn != '.':

            self.con_wid.msg_box.config(text='Load settings ...')

            # read parameters from hard drive to config object
            self.cfg.read_json(fp=cfn)

            # transfer parameters from config object to GUI
            for i, key in enumerate(ABBS):
                tk_var = tk.StringVar()
                tk_var.set(str(self.cfg.params[key]))
                self.cfg_wid.entries[i].config(textvariable=tk_var)

            # update results in GUI
            self.run()

            self.con_wid.msg_box.config(text='Config loaded')

        return True

    def open_abt_win(self):
        ''' open about window '''

        # instantiate about widget as object
        AbtWidget()

        return True

    def quit_app(self):
        ''' quit app '''

        # destroy tkinter object
        self.destroy()
        sys.exit()


if __name__ == "__main__":
    try:
        MainWin = PlenoptisignApp(None)
        MainWin.mainloop()
    except Exception as e:
        PlenoptisignError(e)