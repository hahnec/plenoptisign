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

__version__ = '1.0.0'

VALS = [.009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'inf', 16., 1.0, 13., -6, 1]  # default values
ABBS = ['pp', 'fs', 'hh', 'pm', 'dA', 'fU', 'HH', 'df', 'f_num', 'a', 'M', 'G', 'dx']
EXPR = ['pixel pitch [mm]', 'micro lens focal length [mm]', 'micro lens principal plane distance [mm]',
        'micro lens pitch [mm]', 'exit pupil distance [mm]', 'main lens focal length [mm]',
        'main lens principal plane distance [mm]', 'main lens focus distance [mm]', 'F-number', 'shift parameter [px]',
        'micro image resolution [px]', 'virtual camera gap', 'disparity [px]']
RSLT = ['refoc. distance d', 'depth of field DoF', 'narrow DoF border', 'far DoF border', 'baseline B', 'tilt angle Phi', 'tria. distance Z']
UNTS = [' mm', ' mm', ' mm', ' mm', ' mm', ' deg', ' mm']

# GUI dimensions
SW = 8  # spinbox width
PF = 10 # frame margin width
PX = 10 # horizontal margin width
PY = 10 # horizontal margin width
BTN_W = 12
MSG_W = 140
DEC_P = 4

class PlenoptisignError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)