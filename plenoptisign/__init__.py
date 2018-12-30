__version__ = '0.3'

from .mainclass import MainClass

VALS = [.009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 'inf', 2.6846, 1.0, 13, -6, 1]  # default values
ABBS = ['pp', 'fs', 'hh', 'pm', 'dA', 'fU', 'HH', 'df', 'f_num', 'a', 'M', 'G', 'dx']
EXPR = ['pixel pitch [mm]', 'micro lens focal length [mm]', 'micro lens principal plane distance [mm]',
        'micro lens pitch [mm]', 'exit pupil distance [mm]', 'main lens focal length [mm]',
        'main lens principal distance [mm]', 'main lens focus distance [mm]', 'F#', 'refocus parameter',
        'micro image resolution [px]', 'virtual camera gap', 'disparity [px]']