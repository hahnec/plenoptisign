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
import os

# local python files
from plenoptisign import __version__
from plenoptisign.constants import ABBS, PF
from plenoptisign.mainclass import MainClass
from plenoptisign.gui.cfg import Config
from plenoptisign.gui.widget_men import MenWidget
from plenoptisign.gui.widget_cfg import CfgWidget, TwoStringVars
from plenoptisign.gui.widget_plt import PltWidget
from plenoptisign.gui.widget_cmd import CmdWidget
from plenoptisign.gui.widget_con import ConWidget

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
        self.wm_title("PlenoptiSign-"+__version__)

        # icon handling
        if sys.platform == 'win32':
            self.wm_iconbitmap(default=ICON_PATH)
            cwd = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.getcwd()
            fp = os.path.join(cwd, 'misc', 'circlecompass_1055093.ico')
            fp = fp if os.path.exists(fp) else ICON_PATH
            self.iconbitmap(fp)

        # initialize parameters
        self.cfg = Config()

        # instantiate menu widget
        self.men_wid = MenWidget(self)
        self.men_wid.grid()

        # instantiate plot widget as object
        self.plt_wid = PltWidget(self)
        self.plt_wid.grid(row=0, column=0, padx=PF, pady=PF, sticky='NSWE')

        # instantiate config widget as object
        self.cfg_wid = CfgWidget(self)
        self.cfg_wid.grid(row=0, column=1, rowspan=3, padx=PF, pady=PF, sticky='NSWE')

        # instantiate command widget as object
        self.cmd_wid = CmdWidget(self)
        self.cmd_wid.grid(row=1, column=0, sticky='N')

        # instantiate console widget as object
        self.con_wid = ConWidget(self)
        self.con_wid.grid(row=2, column=0, padx=PF, pady=PF, sticky='NSWE')

        # about button in menu
        self.createcommand('tkAboutDialog', self.men_wid.open_about)

        # enable tkinter resizing
        self.resizable(True, False)

        # construct main class object
        self.obj = MainClass()

        # update results in GUI
        self.run()

    @staticmethod
    def tryfloat(val):
        try:
            return float(val)
        except:
            return val

    def run(self):

        # fetch parameter data from GUI
        self.obj.data = dict(zip(ABBS, [self.tryfloat(entry.get()) for entry in self.cfg_wid.entries]))

        # compute light field geometry
        self.obj.refo()
        self.obj.tria()

        # update widgets
        self.cfg_wid.refresh()
        self.plt_wid.refresh()

        # update console message
        self.con_wid.msg_box.config(text=self.obj.console_msg)

        return True

    @staticmethod
    def typefloat(var):
        if var:
            pass

    def save_cfg(self):
        ''' overwrite config file settings '''

        self.con_wid.msg_box.config(text='Save settings ...')

        # update results in GUI
        self.run()

        # transfer parameters from GUI to config object
        for i, key in enumerate(ABBS):
            self.cfg.params[key] = self.tryfloat(self.cfg_wid.entries[i].get())

        # write parameters from config object to hard drive
        self.cfg.write_json()

        self.con_wid.msg_box.config(text='Config saved')

        return True

    def load_cfg(self):
        ''' load config file settings '''

        # open window to select config file
        cfn_win = tk.Tk()
        cfn_win.withdraw()
        cfn = os.path.normpath(
            askopenfilename(parent=cfn_win, title="Select file", filetypes=[("Config files", "*.json")])
        )

        if cfn != '.':

            self.con_wid.msg_box.config(text='Load settings ...')

            # read parameters from hard drive to config object
            self.cfg.read_json(fp=cfn)

            # transfer parameters from config object to GUI
            for i, key in enumerate(ABBS):

                if isinstance(self.cfg.params[key], (list, tuple)):
                    tk_var = TwoStringVars(values=self.cfg.params[key])
                else:
                    tk_var = tk.StringVar()
                    tk_var.set(str(self.cfg.params[key]))

                self.cfg_wid.entries[i].config(textvariable=tk_var)

            # update results in GUI
            self.run()

            self.con_wid.msg_box.config(text='Config loaded')

        return True

    def quit_app(self):
        ''' quit app '''

        # destroy tkinter object
        self.destroy()
        sys.exit()


if __name__ == "__main__":

    MainWin = PlenoptisignApp(None)
    MainWin.mainloop()
