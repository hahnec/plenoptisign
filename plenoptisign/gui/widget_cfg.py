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
    from tkinter.font import Font
except ImportError:
    import Tkinter as tk

# local python files
from plenoptisign.constants import ABBS, EXPR, RSLT, UNTS, SW, PX, PY, MSG_W, DEC_P, RSYM, ESYM

# 'from', 'to' and 'increment' exponents for 'pp, fs, hh, pm, dA, fU, HH, df, f_num, a, M, G, dx, sen' in that order
SPIN_SET = ((2,-1), (1,-3), (2,-2), (2,-3), (3,-3), (3,-2), (3,-2), (3,-2), (5,2), (3,-1), (2,-1), (2,-1), (2,-1), (2,-1))

# make object for config widget
class CfgWidget(tk.Frame):

    def __init__(self, parent):

        # inheritance
        tk.Frame.__init__(self, parent)
        self.parent = parent

        # declare multiple tk string variables
        tk_params = dict(zip(ABBS, (tk.StringVar() for _ in range(len(ABBS)))))

        # transfer config parameters to tk strings
        for key in ABBS:
            tk_params[key].set(str(self.parent.cfg.params[key]))

        # place scientific notations (used throughout the author's publications)
        for i, exp in enumerate(ESYM+[' ']+RSYM):
            text = tk.Text(self, width=8, height=2, borderwidth=0, background=self.cget('background'), font=('', 10))
            text.tag_configure('ver_align', offset=-4)
            text.tag_configure('sub', offset=-8, font=('', 8))
            if exp.__contains__('_'):
                tags = exp.split('_')
                tags = list(filter(None, sum([tag.split('{') for tag in tags], [])))
                tags = list(filter(None, sum([tag.split('}') for tag in tags], [])))

                if len(tags) == 2:
                    text.insert(tk.INSERT, tags[0], 'ver_align', tags[1], 'sub')
                elif len(tags) == 4:
                    text.insert(tk.INSERT, tags[0], 'ver_align', tags[1], 'sub', tags[2], 'ver_align', tags[3], 'sub')
                text.configure(state=tk.DISABLED)
            else:
                text.insert(tk.INSERT, exp, 'ver_align')
            text.grid(row=i+1, column=0, sticky='S')

        # place entry labels
        for i, exp in enumerate(EXPR):
            label = tk.Label(self, text=exp)
            label.grid(row=i+1, column=1, sticky='W')

        # place entries and keep them as instance variables
        self.entries = []
        for i, (s, key) in enumerate(zip(SPIN_SET, ABBS)):
            if key == 'df':
                # special treatment for focus distance 'df' to cover infinity values
                entry = tk.Entry(self, textvariable=tk_params[key], width=SW)
            elif key == 'f_num':
                # special treatment for f-number 'f_num' to trigger micro image resolution estimation
                entry = tk.Spinbox(self, from_=-10**s[0], to=10**s[0], increment=10**s[1],
                                   textvariable=tk_params[key], width=SW, command=self.update_M)
            elif key == 'M':
                # special treatment for micro image size 'M' to trigger f-number estimation
                entry = tk.Spinbox(self, from_=-10**s[0], to=10**s[0], increment=10**s[1],
                                   textvariable=tk_params[key], width=SW, command=self.update_fnum)
            elif key == 'sd':
                var = TwoStringVars(values=self.parent.cfg.params[key])
                entry = DoubleSpinbox(self, from_=10**s[1], to=10**s[0], increment=10**s[1],
                                      textvariable=var, width=SW, command=self.parent.run)
                entry.xview_moveto(0.0)  # display text from most right
            else:
                entry = tk.Spinbox(self, from_=-10**s[0], to=10**s[0], increment=10**s[1],
                                   textvariable=tk_params[key], width=SW, command=self.parent.run)

            entry.grid(row=i+1, column=2, sticky='W', padx=PX)
            self.entries.append(entry)

        # margin separating inputs from outputs
        margin = tk.Label(self, height=0, pady=-25)
        margin.grid(row=i+2, column=2)

        # place output labels
        for j, res in enumerate(RSLT):
            label = tk.Label(self, text=res)
            label.grid(row=i+3+j, column=1, sticky='W')

        # place outputs
        self.grid_columnconfigure(index=2, minsize=MSG_W)
        self.msgs = []
        for j in range(len(RSLT)):
            msg = tk.Message(self, text='', width=MSG_W)
            msg.grid(row=i+3+j, column=2, sticky='E')
            self.msgs.append(msg)

        # place units
        for j, unit in enumerate(UNTS):
            label = tk.Label(self, text=unit)
            label.grid(row=j+1, column=3, sticky='W')

    def update_M(self):

        # compute micro image size
        self.parent.obj.compute_mic_img_size()

        # pass estimated micro image size to entry in GUI
        tk_var = tk.StringVar()
        tk_var.set(str(round(self.parent.obj.M, DEC_P)))
        self.entries[11].config(textvariable=tk_var)

        # update results in GUI
        self.parent.run()

        return True

    def update_fnum(self):

        # compute micro image size
        self.parent.obj.compute_pupil_size()

        # pass estimated micro image size to entry in GUI
        tk_var = tk.StringVar()
        tk_var.set(str(round(self.parent.obj.fU/self.parent.obj.D, DEC_P)))
        self.entries[9].config(textvariable=tk_var)

        # update results in GUI
        self.parent.run()

        return True

    def refresh(self):

        # convert results to string with respective metric unit under consideration of infinity
        strings = []
        for res in self.parent.obj.get_results():
            strings.append('%.4f' %round(res, DEC_P) if not "inf" in str(res) else "infinity")

        # update results
        for j, res_str in enumerate(strings):
            self.msgs[j].config(text=res_str)

class TwoStringVars(tk.StringVar):

    def __init__(self, master=None, values=('', '')):
        tk.StringVar.__init__(self, master, values)

        self.set(values)

    def get(self):
        one = int(self._one.get())
        two = int(self._two.get())
        return [one, two]

    def set(self, values):
        if len(values) == 2:
            self._one = tk.StringVar(value=str(values[0]))
            self._two = tk.StringVar(value=str(values[1]))
        else:
            raise ValueError('Pass list or tuple of two values only')

    @property
    def one(self):
        return float(self._one.get())

    @property
    def two(self):
        return float(self._two.get())

class DoubleSpinbox(tk.Frame):

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, borderwidth=-3, cursor="arrow")    # remove border and use arrow for hovering

        self._v = kwargs['textvariable'] if 'textvariable' in kwargs else TwoStringVars()
        kwargs['from_'] = kwargs['from_'] if 'from_' in kwargs else 0
        kwargs['to'] = kwargs['to'] if 'to' in kwargs else 10**2
        kwargs['width'] = int(kwargs['width']/2)-2 if 'width' in kwargs else 3

        # remove kwarg keys in widget which are given as tuple
        kwargs.pop('textvariable', None)

        self._spinbox_one = tk.Spinbox(self, textvariable=self._v._one, **kwargs)
        self._spinbox_one.grid(row=0, column=0, sticky='NSW', ipadx=2, padx=0)
        self._spinbox_two = tk.Spinbox(self, textvariable=self._v._two, **kwargs)
        self._spinbox_two.grid(row=0, column=1, sticky='NSE', ipadx=2, padx=2)

    def xview_moveto(self, val):
        ''' display text from most right '''

        self._spinbox_one.xview_moveto(val)
        self._spinbox_two.xview_moveto(val)

    def get(self):
        return self._v.one, self._v.two

    def config(self, **kwargs):

        self._v = kwargs['textvariable'] if 'textvariable' in kwargs else TwoStringVars()

        # remove kwarg keys in widget which are given as tuple
        kwargs.pop('textvariable', None)

        self._spinbox_one.config(textvariable=self._v._one, **kwargs)
        self._spinbox_two.config(textvariable=self._v._two, **kwargs)