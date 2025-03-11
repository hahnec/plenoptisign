#!/usr/bin/env python3

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
# required for GUI usage from CLI
import matplotlib
matplotlib.use("TkAgg")

from sys import exit, version_info, argv
from getopt import getopt, GetoptError
from matplotlib.pyplot import figure, show
from mpl_toolkits.mplot3d import Axes3D

from plenoptisign import __version__
from plenoptisign.mainclass import MainClass
from plenoptisign.constants import VALS, ABBS, EXPR, DEC_P, FIG_SIZE, PlenoptisignError
from plenoptisign.gui import PlenoptisignApp


def usage():

    print("\nplenoptisign v" + __version__ + " is a light field geometry estimator.")
    print("For information please send an email to inbox [ät] christopherhahne.de")

    print("Usage: plenoptisign <options>\n")
    print("Options:")
    print("-g, --gui                open graphical user interface")
    print("-p, --plot               plot paraxial rays")
    print("-r, --refo               refocusing results only")
    print("-t, --tria               triangulation results only")
    print("-h, --help               print this help message.")
    print("")


def parse_options(argv):

    # default settings
    refo_opt = True
    tria_opt = True
    plot_opt = False
    opts = None

    try:
        opts, args = getopt(argv, ":hrtpg", ["help", "refo", "tria", "plot", "gui"])

    except GetoptError:
        usage()
        exit(2)

    if opts:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                exit()
            if opt in ("-r", "--refo"):
                refo_opt = True
                tria_opt = False
            if opt in ("-t", "--tria"):
                refo_opt = False
                tria_opt = True
            if opt in ("-p", "--plot"):
                plot_opt = True
            if opt in ("-g", "--gui"):
                MainWindow = PlenoptisignApp(None)
                MainWindow.mainloop()
                refo_opt = False
                tria_opt = False
                exit()

    return refo_opt, tria_opt, plot_opt


def cmd_read():

    py3 = version_info[0] > 2  # boolean for Python version > 2
    data = dict(zip(ABBS, VALS))
    name_dict = dict(zip(ABBS, EXPR))

    # read input from command line and put into dict
    for key in ABBS:
        if py3:
            val_input = input(str(name_dict[key]) + ": ")
        else:
            val_input = raw_input(str(name_dict[key]) + ": ")

        # check for number and use default values if not a number
        try:
            data[key] = float(val_input)
        except ValueError:
            print(str(data[key]) + ' (default)')

    return data


def main():

    # parse options
    refo_opt, tria_opt, plot_opt = parse_options(argv[1:])

    # print info
    print('\nPlenoptiSign v'+__version__+'\r')

    # construct object
    obj = MainClass()

    # read input from command line only if cgi field storage empty
    obj.data = cmd_read()

    # compute light field geometry
    ret_refo = obj.refo() if refo_opt else False
    ret_tria = obj.tria() if tria_opt else False
    if not (ret_refo or ret_tria):
        raise AssertionError('Calculation failed.')

    # convert distances to string while adding metric unit under consideration of infinity
    str_dist = str(round(obj.d, DEC_P)) + ' mm' if not "inf" in str(obj.d) else "infinity"
    str_d_p = str(round(obj.d_p, DEC_P)) + ' mm' if not "inf" in str(obj.d_p) else "infinity"
    str_d_m = str(round(obj.d_m, DEC_P)) + ' mm' if not "inf" in str(obj.d_m) else "infinity"
    str_dof = str(round(obj.dof, DEC_P)) + ' mm' if not "inf" in str(obj.dof) else "infinity"
    str_base = str(round(obj.B, DEC_P)) + ' mm' if not "inf" in str(obj.B) else "infinity"
    str_phi = str(round(obj.phi, DEC_P)) + ' deg'
    str_tria = str(round(obj.Z, DEC_P)) + ' mm' if not "inf" in str(obj.Z) else "infinity"
    console_msg = obj.console_msg

    # output
    if ret_refo:
        print("\nrefoc. distance d: %s" % str_dist)
        print("depth of field DoF: %s" % str_dof)
        print("narrow DoF border: %s" % str_d_m)
        print("far DoF border: %s\n" % str_d_p)
    if ret_tria:
        print("\nbaseline B: %s" % str_base)
        print("tilt angle Phi: %s" % str_phi)
        print("tria. distance Z: %s\n" % str_tria)
    if console_msg:
        print("\nConsole output: \n")
        for msg in console_msg:
            print("%s \n" % msg)
    if plot_opt:
        if ret_refo:
            fig = figure(figsize=FIG_SIZE)
            ax = fig.gca()
            obj.plt_refo(ax, plane_th=.5)
            show(block=True)
            fig = figure(figsize=(FIG_SIZE[0]-2, FIG_SIZE[0]-2))
            ax = Axes3D(fig)
            obj.plt_3d_init(fig, ax)
            obj.plt_3d(ax, amin=obj.a, dep_type=False)
            show(block=True)
        if ret_tria:
            fig = figure(figsize=FIG_SIZE)
            ax = fig.gca()
            obj.plt_tria(ax, plane_th=.5)
            show(block=True)
            fig = figure(figsize=(FIG_SIZE[0]-2, FIG_SIZE[0]-2))
            ax = Axes3D(fig)
            obj.plt_3d_init(fig, ax)
            obj.plt_3d(ax, amin=obj.dx, dep_type=True)
            show(block=True)


if __name__ == "__main__":
    try:
        exit(main())
    except Exception as e:
        PlenoptisignError(e)
