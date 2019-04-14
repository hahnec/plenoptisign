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

from plenoptisign.gui.abt_widget import AbtWidget

import os

# make object for plot widget
class MenWidget(tk.Frame):

    def __init__(self, parent):

        # inheritance
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.parent.createcommand('tkAboutDialog', self.open_about_dialog)

        menubar = tk.Menu(self)

        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Update", command=self.parent.run)

        filemenu.add_separator()

        filemenu.add_command(label="Quit", command=self.parent.quit_app)
        menubar.add_cascade(label="File", menu=filemenu)

        helpmenu = tk.Menu(menubar, tearoff=0)
        helpmenu.add_command(label="About...", command=self.open_about_dialog)
        helpmenu.add_command(label="Help...", command=self.open_docs)
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.parent.config(menu=menubar)

    def open_about_dialog(self):
        ''' open about window '''

        # instantiate about widget
        AbtWidget()

        return True

    def open_docs(self):
        ''' open documentation in webbrowser '''

        # relative path for html documentation
        REL_PATH = "docs/build/html/index.html"

        # current working directory
        cwd = os.getcwd()

        # open local html, in this case, the webbrowser docs
        if os.path.exists(os.path.join(cwd, REL_PATH)):
            url = os.path.join(cwd, REL_PATH)
        else:
            url = os.path.join(os.path.dirname(os.path.dirname(cwd)), REL_PATH)

        # open in a new tab, if possible
        import webbrowser
        webbrowser.open("file:///"+url, new=2)