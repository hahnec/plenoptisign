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
from os.path import join, dirname, abspath, isdir
from os import makedirs, getcwd
from errno import EEXIST

# local python files
from plenoptisign import ABBS, VALS

class Config(object):

    def __init__(self):

        self.params = {}
        self.dir_path = join(abspath('.'), 'cfg')

        try:
            self.read_json()
            if not self.params.keys():
                raise Exception('Config file could not be loaded. Default values will be used instead.')
        except:
            self.default_values()

        return None

    def read_json(self, fp=None):

        if not fp:
            fp = join(self.dir_path, 'cfg.json')#join(getcwd(), 'cfg', 'cfg.json')

        with open(fp, 'r') as f:
            self.params.update(json.load(f))

        return True

    def write_json(self, fp=None):

        if not fp:
            fp = join(self.dir_path, 'cfg.json')#join(getcwd(), 'cfg', 'cfg.json')
        try:
            print(self.dir_path)
            self.mkdir_p(self.dir_path)
            with open(fp, 'w') as f:
                json.dump(self.params, f, sort_keys=True, indent=4)
        except PermissionError as e:
            print(e)
            print('\n\nGrant permission to write to the config file '+fp)

        return True

    def default_values(self):

        self.params = dict(zip(ABBS, VALS))

        return True

    @staticmethod
    def mkdir_p(path):
        try:
            makedirs(path)
        except OSError as exc:  # Python >2.5
            if exc.errno == EEXIST and isdir(path):
                pass
            else:
                raise

        return True