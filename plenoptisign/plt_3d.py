#!/usr/bin/env python

__author__ = "Christopher Hahne"
__email__ = "inbox@christopherhahne.de"
__license__ = """
Copyright (c) 2018 Christopher Hahne <inbox@christopherhahne.de>

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

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

class Mixin:

    def plt_3d(self, iter_range=[0, 5], sen_dims=np.array([24.048, 36.072]), type='tria'):

        x, y, z = ([] for _ in range(3))

        try:
            for el in range(*iter_range):

                # compute distances
                if type == 'refo':
                    self._a = el
                    self.refo()
                    z.append(float(self.d))
                if type == 'tria':
                    self._dx = el
                    self.tria()
                    z.append(float(self.Z))

                # compute field of view
                yy, xx = sen_dims/self._bU*z[-1]
                x.append(xx)
                y.append(yy)

        except TypeError as e:
            raise e

        # determine maximum plot distance
        z_max= max(z) if max(z) != float('inf') else self.non_inf_max(z)
        max_dist = z_max + z_max/10

        # start plottingy
        plt3d = Axes3D(plt.figure(figsize=(9, 5)))
        plt3d.view_init(elev=30, azim=-120)
        plt3d.set_xlabel('z [mm]')
        plt3d.set_ylabel('x [mm]')
        plt3d.set_zlabel('y [mm]')
        plt.title('3-D ' + type + ' plot')

        # plot camera axis and sensor
        plt3d.scatter(0, 0, 0, s=20, color='k')
        plt3d.plot([0, max_dist], [0, 0], [0, 0], 'k--')
        yy, xx = np.meshgrid((-sen_dims[0]/2, sen_dims[0]/2), (-sen_dims[1]/2, sen_dims[1]/2))
        plt3d.plot_surface(-self._bU*np.ones(xx.shape), xx, yy, color='k', alpha=.8)

        # plot the depth planes
        for i in range(len(z)):
            if z[i] != float('inf'):
                yy, xx = np.meshgrid((-y[i]/2, y[i]/2), (-x[i]/2, x[i]/2))
                zz = z[i]*np.ones(xx.shape)
                plt3d.plot_surface(zz, xx, yy, color='r', alpha=.5) # depth plane
                plt3d.scatter([z[i]], [0], [0], s=20, color='r') # plane-axis intersection

                # plot marker
                num_str = str(range(*iter_range)[i])
                label_str = "$d_"+num_str+"$" if type == 'refo' else "$Z_{("+str(self._G)+', '+num_str+")}$"
                plt3d.text(z[i], x[i]/2, y[i]/2, s=label_str, fontsize=18, family='sans-serif')

        # plot field of view lines
        x_hw = self.non_inf_max(x)/2
        y_hw = self.non_inf_max(y)/2
        plt3d.plot([-self._bU, z_max], [-sen_dims[1]/2, x_hw], [-sen_dims[0]/2, y_hw], 'r-.', alpha=.8, linewidth=.5)
        plt3d.plot([-self._bU, z_max], [-sen_dims[1]/2, x_hw], [sen_dims[0]/2, -y_hw], 'r-.', alpha=.8, linewidth=.5)
        plt3d.plot([-self._bU, z_max], [sen_dims[1]/2, -x_hw], [-sen_dims[0]/2, y_hw], 'r-.', alpha=.8, linewidth=.5)
        plt3d.plot([-self._bU, z_max], [sen_dims[1]/2, -x_hw], [sen_dims[0]/2, -y_hw], 'r-.', alpha=.8, linewidth=.5)

        plt.show()

    @staticmethod
    def non_inf_max(input):

        try:
            max_val = max([x for x in input if x != float('inf')])
        except TypeError:
            max_val = input if isinstance(input, (int, float)) else float('nan')

        return max_val