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

import json
import os
import errno

# local python files
from plenoptisign import ABBS, VALS
from ... import PlenoptisignError

class Config(object):

    def __init__(self):

        self.params = {}
        self.dir_path = os.path.join(os.path.abspath('.'), 'cfg')

        try:
            self.read_json()
            if not self.params.keys():
                raise PlenoptisignError('Config file could not be loaded')
        except:
            self.default_values()

        return None

    def read_json(self, fp=None):

        if not fp:
            fp = os.path.join(self.dir_path, 'cfg.json')

        with open(fp, 'r') as f:
            json_data = json.load(f)#self.params.update(json.load(f))

        # transfer parameters to config object
        for key in json_data:
            self.params[key] = float(json_data[key])

        return True

    def write_json(self, fp=None):

        if not fp:
            fp = os.path.join(self.dir_path, 'cfg.json')
        try:
            # create config folder (if not already present)
            self.mkdir_p(self.dir_path)
            # write config file
            with open(fp, 'w') as f:
                json.dump(self.params, f, sort_keys=True, indent=4)
        except PermissionError:
            raise PlenoptisignError('\n\nGrant permission to write to the config file '+fp)

        return True

    def default_values(self):

        self.params = dict(zip(ABBS, VALS))

        return True

    @staticmethod
    def mkdir_p(path):
        try:
            os.makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == errno.EEXIST and os.path.isdir(path):
                pass
            else:
                raise

        return True