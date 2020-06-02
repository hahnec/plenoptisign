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

import unittest
from ddt import ddt, data, unpack
from plenoptisign.mainclass import MainClass
from plenoptisign.constants import ABBS, DEC_P

@ddt
class PlenoptiSignTester(unittest.TestCase):

    @data(
        ([(0, 0), .009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'inf', 2.6846, 1, 13, -6, 1],
         [962.7459, 1110.0123, 838.1359, 271.8764]),
        )
    @unpack
    def test_refo(self, vals, data_exp):
        # zip to dict
        data_in = dict(zip(ABBS, vals))
        # object instance
        object = MainClass(data_in)
        # refocusing estimation
        object.refo()
        # data readout
        data_out = [round(float(object.d), DEC_P), round(float(object.d_p), DEC_P), round(float(object.d_m), DEC_P),
                    round(float(object.dof), DEC_P)]
        # assertion
        self.assertEqual(data_out, data_exp)
    
    @data(
        ([(0, 0), .009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'Inf', 2.6846, 0, 13, -6, 1],
         [3.7956, 0.0, 5869.2898]),
        ([(0,0), .009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'Inf', 2.6846, 0, 13, 1, 0],
         [-0.6326, 0.0, float('inf')]),
        )
    @unpack
    def test_tria(self, vals, data_exp):
        # zip to dict
        data_in = dict(zip(ABBS, vals))
        # object instance
        object = MainClass(data_in)
        # triangulation estimation
        object.tria()
        # data readout
        data_out = [round(float(object.B), DEC_P), round(float(object.phi), DEC_P), round(float(object.Z), DEC_P)]
        # assertion
        self.assertEqual(data_out, data_exp)


if __name__ == '__main__':
    unittest.main()
