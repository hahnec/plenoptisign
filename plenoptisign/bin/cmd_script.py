#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2017 Christopher Hahne <inbox@christopherhahne.de>

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

import sys, getopt, os.path
sys.path.append(os.path.abspath('../..'))
from plenoptisign import SpcLfGeo, __version__

def usage():

    print("\nSPC estimator " + __version__ + " by Christopher Hahne")
    print("Usage: geo_spc <options>\n")
    print("Options:")
    print("-r, --refo               Refocusing results only flag")
    print("-t, --tria               Triangulation results only flag")
    print("-p, --plot               Plot paraxial rays flag")
    print("-h, --help               Print this help message.")
    print("")


def parse_options(argv):

    # default settings
    refo_opt = True
    tria_opt = True
    plot_opt = False

    try:
        opts, args = getopt.getopt(argv, ":hrtp", ["help", "refo", "tria", "plot"])

    except getopt.GetoptError:
        usage()
        sys.exit(2)

    if opts:
        for opt, arg in opts:
            if opt in ("-h", "--help"):
                usage()
                sys.exit()
            if opt in ("-r", "--refo"):
                refo_opt = True
                tria_opt = False
            if opt in ("-t", "--tria"):
                refo_opt = False
                tria_opt = True
            if opt in ("-p", "--plot"):
                plot_opt = True

    return refo_opt, tria_opt, plot_opt

def cmd_read():

    py3 = sys.version_info[0] > 2  # boolean for Python version > 2
    vals = [.009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'inf', 2.6846, 1.0, 13, -6, 1]   # default values
    abbs = ['pp', 'fs', 'hh', 'pm', 'dA', 'fU', 'HH', 'df', 'f_num', 'a', 'M', 'i', 'dx']
    expr = ['pixel pitch [mm]', 'micro lens focal length [mm]', 'micro lens principal plane distance [mm]',
            'micro lens pitch [mm]', 'exit pupil distance [mm]', 'main lens focal length [mm]',
            'main lens principal distance [mm]', 'main lens focus distance [mm]', 'F#', 'refocus parameter',
            'micro image resolution [px]', 'virtual camera gap', 'disparity [px]']
    data = dict(zip(abbs, vals))
    name_dict = dict(zip(abbs, expr))

    # read input from command line and put into dict
    for key in abbs:
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
    refo_opt, tria_opt, plot_opt = parse_options(sys.argv[1:])

    # read input from command line only if cgi field storage empty
    data = cmd_read()

    # construct object
    object = SpcLfGeo(data)

    # compute light field geometry
    ret_refo = object.refo() if refo_opt else False
    ret_tria = object.tria() if tria_opt else False
    if not (ret_refo or ret_tria):
        raise AssertionError('Calculation failed.')

    # convert distances to string while adding metric unit under consideration of infinity
    dec_place = 4  # number of decimals
    str_dist = str(round(object.d, dec_place)) + ' mm' if not "inf" in str(object.d) else "infinity"
    str_d_p = str(round(object.d_p, dec_place)) + ' mm' if not "inf" in str(object.d_p) else "infinity"
    str_d_m = str(round(object.d_m, dec_place)) + ' mm' if not "inf" in str(object.d_m) else "infinity"
    str_dof = str(round(object.dof, dec_place)) + ' mm' if not "inf" in str(object.dof) else "infinity"
    str_base = str(round(object.B, dec_place)) + ' mm' if not "inf" in str(object.B) else "infinity"
    str_phi = str(round(object.phi, dec_place)) + ' deg'
    str_tria = str(round(object.Z, dec_place)) + ' mm' if not "inf" in str(object.Z) else "infinity"
    console_msg = object.console_msg

    # output
    if ret_refo:
        print("\nrefoc. distance d: %s" % str_dist)
        print("depth of field DoF: %s" % str_dof)
        print("narrow DoF border: %s" % str_d_m)
        print("far DoF border: %s\n" % str_d_p)
    if ret_tria:
        print("\nbaseline B: %s" % str_base)
        print("tilt angle: %s" % str_phi)
        print("tria. distance Z: %s\n" % str_tria)
    if console_msg:
        print("\nConsole output: \n")
        for msg in console_msg:
            print("%s \n" % msg)
    if plot_opt:
        object.plt_refo(plane_th=.5, ray_th=.5)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(e)