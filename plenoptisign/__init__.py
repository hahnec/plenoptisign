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
EXPR = ['Pixel Pitch [mm]', 'Micro Lens Focal Length [mm]', 'Micro Lens Principal Plane Distance [mm]',
        'Micro Lens Pitch [mm]', 'Exit Pupil Distance [mm]', 'Main Lens Focal Length [mm]',
        'Main Lens Principal Plane Distance [mm]', 'Main Lens Focus Distance [mm]', 'F-number', 'Shift Parameter [px]',
        'Micro Image Resolution [px]', 'Virtual Camera Gap', 'Disparity [px]']
RSLT = ['Refoc. Distance', 'Depth of Field', 'Narrow DoF Border', 'Far DoF Border', 'Baseline', 'Tilt Angle', 'tria. distance']
RSYM = ["$$d_a$$", "$$DoF$$", "$$d_{a-}$$", "$$d_{a+}$$", "$$B$$", "$$\Phi$$", "$$Z$$"]
ESYM = ['$p_p$', '$f_s$', '$H_..$', '$p_m$', "$d_{A'}$", '$f_U$', '$H_{1U}H_{2U}$', '$d_f$', '$F#$', '$a$', '$M$', '$G$', '$\delta x$']
UNTS = [' mm', ' mm', ' mm', ' mm', ' mm', ' deg', ' mm']

# GUI dimensions
SW = 8  # spinbox width
PF = 10 # frame margin width
PX = 10 # horizontal margin width
PY = 10 # horizontal margin width
BTN_W = 12
MSG_W = 180
DEC_P = 4

class PlenoptisignError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)