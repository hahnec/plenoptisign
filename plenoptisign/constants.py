# -*- coding: utf-8 -*-

class PlenoptisignError(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

# default values
VALS = [(24.048, 36.072), .009, 2.75, .396, .125, 111.0324, 193.2935, -65.5563, 4000, 22., 1.0, 13.9523, -6, 4.0]
# notation characters
ABBS = ['sd', 'pp', 'fs', 'hh', 'pm', 'dA', 'fU', 'HH', 'df', 'f_num', 'a', 'M', 'G', 'dx']
EXPR = ['Sensor Dimensions (Y,X)', 'Pixel Pitch', 'Micro Lens Focal Length', 'Micro Lens Principal Plane Spacing',
        'Micro Lens Pitch', 'Exit Pupil Distance', 'Main Lens Focal Length',
        'Main Lens Principal Plane Spacing', 'Main Lens Focusing Distance', 'F-number',
        'Shift Parameter', 'Micro Image Resolution', 'Virtual Camera Gap', 'Disparity']
RSLT = ['Refocusing Distance', 'Far DoF Border', 'Narrow DoF Border', 'Depth of Field',
        'Baseline', 'Tilt Angle', 'Triangulation Distance']

# notation plots with subscript support
ESYM = ['Sen', 'p_p', 'f_s', 'H_{1s}H_{2s}', 'p_m', "d_{A'}", 'f_U', 'H_{1U}H_{2U}', 'd_f', 'F#', 'a', 'M', 'G', 'Δx']
RSYM = ["d_a", "d_{a+}", "d_{a-}", "DoF", "B_G", "Φ_G", "Z_{(G, ∆x)}"]

# units
UNTS = ['mm', 'mm', 'mm', 'mm', 'mm', 'mm', 'mm', 'mm', 'mm', 'a.u.', 'px', 'px', 'px', 'px',
        '', 'mm', 'mm', 'mm', 'mm', 'mm', 'deg', 'mm']

# GUI dimensions
SW = 10          # spinbox width
PF = 15         # frame margin width
PX = 10         # horizontal margin width
PY = 10         # horizontal margin width
BTN_W = 12      # button width
MSG_W = 100     # message width
DEC_P = 4       # fractional digits

# plot dimensions
FIG_SIZE = (8, 5)