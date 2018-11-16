__version__ = '0.3'

class SpcLfGeo(object):
    def __init__(self, data=[]):
        # input variables from data dictionary (set default values to prevent errors)
        self._pp = float(data["pp"]) if "pp" in data else .009        # pixel pitch
        self._fs = float(data["fs"]) if "fs" in data else 2.75        # focal length of micro lens
        self._hh = float(data["hh"]) if "hh" in data else .396        # principal plane separation of micro lens
        self._pm = float(data["pm"]) if "pm" in data else .125        # micro lens pitch
        self._dA = float(data["dA"]) if "dA" in data else 111.0324    # exit pupil distance
        self._fU = float(data["fU"]) if "fU" in data else 193.2935    # focal length of objective lens
        self._HH = float(data["HH"]) if "HH" in data else -65.5563    # principal plane spacing in objective lens
        self._df = float(data["df"]) if "df" in data else float('inf')# object distance
        self._D = self._fU/float(data["f_num"]) if "f_num" in data else self._fU/2.6846  # entrance pupil diameter of main lens
        self._a = float(data["a"]) if "a" in data else 1.0            # iterative refocusing parameter
        self._M = float(data["M"]) if "M" in data else 13             # 1-D micro image diameter
        self._G = float(data["G"]) if "G" in data else -6             # viewpoint gap
        self._dx = float(data["dx"]) if "dx" in data else 1           # disparity value
        
    # load methods and variables
    from .refo import refo
    from .tria import tria
    from .plt_refo import plt_refo
    from .plt_tria import plt_tria