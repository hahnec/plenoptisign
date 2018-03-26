import unittest
from ddt import ddt, data, unpack
import plenoptisign

@ddt
class TestSPC(unittest.TestCase):

    def setUp(self):
        pass

    @data(
        ([.009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'inf', 2.6846, 1, 13, -6, 1], [962.7459, 1110.0123, 838.1359, 271.8764]),
        )
    @unpack
    def test_refo(self, vals, data_exp):
        # zip to dict
        abbs = ['pp', 'fs', 'hh', 'pm', 'dA', 'fU', 'HH', 'df', 'f_num', 'a', 'M', 'i', 'dx']
        data_in = dict(zip(abbs, vals))
        # object instance
        object = plenoptisign.SpcLfGeo(data_in)
        # refocusing estimation
        object.refo()
        # data readout
        dec_place = 4
        data_out = [round(float(object.d), dec_place), round(float(object.d_p), dec_place), round(float(object.d_m), dec_place),
                    round(float(object.dof), dec_place)]
        # assertion
        self.assertEqual(data_out, data_exp)
    
    @data(
        ([.009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'Inf', 2.6846, 0, 13, -6, 1], [3.7956, 0.0, 5869.2898]),
        ([.009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'Inf', 2.6846, 0, 13, 1, 0], [-0.6326, 0.0, float('-inf')]),
        )
    @unpack
    def test_tria(self, vals, data_exp):
        # zip to dict
        abbs = ['pp', 'fs', 'hh', 'pm', 'dA', 'fU', 'HH', 'df', 'f_num', 'a', 'M', 'i', 'dx']
        data_in = dict(zip(abbs, vals))
        # object instance
        object = plenoptisign.SpcLfGeo(data_in)
        # triangulation estimation
        object.tria()
        # data readout
        dec_place = 4
        data_out = [round(float(object.B), dec_place), round(float(object.phi), dec_place), round(float(object.Z), dec_place)]
        # assertion
        self.assertEqual(data_out, data_exp)


if __name__ == '__main__':
    unittest.main()