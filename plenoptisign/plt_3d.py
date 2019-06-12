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

# external libs
import numpy as np
from matplotlib.transforms import Bbox

# local python files
from . import constants as c


class Mixin:

    def plt_3d_init(self, fig, plt3d, elev=10, azim=135):
        ''' This method initializes parameters for plots in 3-D space that only need to be set once.

        :param fig: instance of matplotlib's Figure
        :param plt3d: instance of matplotlib's Axes3D
        :param elev: elevation angle for perspective in 3-D plot
        :param azim: azimuth angle for perspective in 3-D plot
        :type plt3d: :class:`~matplotlib:mpl_toolkits.mplot3d.axes3d.Axes3D`
        :type elev: float
        :type azim: float

        :return: **True**
        :rtype: bool

        '''

        # variable initialization
        w = fig.get_figwidth()
        h = fig.get_figheight()
        aspect_ratio = h/w
        g = (1-aspect_ratio)/2

        # set figure size and bounding box
        fig.set_size_inches((h, h), forward=True)
        bbox = fig.bbox.get_points()
        bbox[1, 0] = w*100

        # self.fig.bbox = Bbox(bbox)
        # self.ax = self.fig.gca()

        # position axes
        enlarge_coeff = 1.15
        pos = np.asarray([[g, 0], [1-g, 1.0]])
        pos = (pos-pos.max()/2.)*enlarge_coeff+.5
        plt3d.set_position(pos=Bbox(pos))

        # perspective view init
        plt3d.view_init(elev, azim)

        return True

    def plt_3d(self, plt3d, amin, dep_type=False, ray_th=.75):
        ''' This method draws depth planes in 3-D space based on provided depth method (e.g. :func:`refo()`).

        :param plt3d: instance of matplotlib's Axes3D
        :param amin: minimum depth plane
        :param sen_dims: sensor dimensions
        :param dep_type: specified depth type, e.g. 'refo' or 'tria'
        :type plt3d: :class:`~matplotlib:mpl_toolkits.mplot3d.axes3d.Axes3D`
        :type amin: float
        :type sen_dims: tuple
        :type dep_type: bool

        :return: **plt3d**

        '''

        x, y, z = ([] for _ in range(3))
        iter_range = [amin, amin+3]
        planes = np.arange(iter_range[0], iter_range[1], 1)[::-1]
        sen_dims = np.asarray(self.sd)

        try:
            for el in planes:
                # compute distances depending on depth types
                if dep_type:
                    self.dx = el
                    self.tria()
                    z.append(float(self.Z))
                else:
                    self.a = el
                    self.refo()
                    z.append(float(self.d))

                # compute field of view
                yy, xx = sen_dims/self.bU*z[-1]
                x.append(xx)
                y.append(yy)

        except TypeError as e:
            raise c.PlenoptisignError(e)

        # determine maximum plot distance
        z_max = max(z) if max(z) != float('inf') else self.non_inf_max(z)
        max_dist = z_max*1.1

        # plot title (padding for vertical positioning)
        plt3d.set_title('3-D ' + ('refo', 'tria')[dep_type] + ' plot', pad=-20)

        # plot axis matter
        plt3d.set_xlabel('$z$ [mm]')
        plt3d.set_ylabel('$x$ [mm]')
        plt3d.set_zlabel('$y$ [mm]')

        # plot camera axis and sensor
        plt3d.scatter(0, 0, 0, s=20, color='k')
        plt3d.plot([0, max_dist], [0, 0], [0, 0], 'k--')
        yy, xx = np.meshgrid((-sen_dims[0]/2, sen_dims[0]/2), (-sen_dims[1]/2, sen_dims[1]/2))
        plt3d.plot_surface(-self.bU*np.ones(xx.shape), xx, yy, color='k', alpha=.8)

        # plot the depth planes
        for i in range(len(z)):
            if z[i] != float('inf'):
                yy, xx = np.meshgrid((-y[i]/2, y[i]/2), (-x[i]/2, x[i]/2))
                zz = z[i]*np.ones(xx.shape)
                plt3d.plot_surface(zz, xx, yy, color='r', alpha=.3)     # depth plane
                plt3d.scatter([z[i]], [0], [0], s=20, color='c')        # plane-axis intersection

                # plot marker
                num_str = str(round(planes[i], 1))
                label_str = "$Z_{("+str(self.G)+', '+num_str+")}$" if dep_type else "$d_{"+num_str+"}$"
                plt3d.text(z[i], -x[i]/1.8, y[i]/1.8, s=label_str, fontsize=16, family='sans-serif')

        # plot field of view lines
        x_hw = self.non_inf_max(x)/2
        y_hw = self.non_inf_max(y)/2
        plt3d.plot([-self.bU, z_max], [-sen_dims[1]/2, +x_hw], [-sen_dims[0]/2, +y_hw], 'k-.', alpha=.8, linewidth=ray_th)
        plt3d.plot([-self.bU, z_max], [-sen_dims[1]/2, +x_hw], [+sen_dims[0]/2, -y_hw], 'k-.', alpha=.8, linewidth=ray_th)
        plt3d.plot([-self.bU, z_max], [+sen_dims[1]/2, -x_hw], [-sen_dims[0]/2, +y_hw], 'k-.', alpha=.8, linewidth=ray_th)
        plt3d.plot([-self.bU, z_max], [+sen_dims[1]/2, -x_hw], [+sen_dims[0]/2, -y_hw], 'k-.', alpha=.8, linewidth=ray_th)

        self.axis_equal_3D(plt3d)

        return plt3d

    @staticmethod
    def non_inf_max(input):
        ''' This function computes the maximum value from an input list without consideration of infinity.

        :param input: list of real numbers
        :param max_val: maximum value excluding infinity
        :type input: list
        :type max_val: float

        :returns: **max_val**

        '''

        try:
            max_val = max([x for x in input if x != float('inf')])
        except:
            max_val = input if isinstance(input, (int, float)) else float('nan')

        return max_val

    @staticmethod
    def axis_equal_3D(ax):
        extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'yz'])
        sz = extents[:, 1]-extents[:, 0]
        centers = np.mean(extents, axis=1)
        maxsize = max(abs(sz))
        r = maxsize/2
        for ctr, dim in zip(centers, 'yz'):
            getattr(ax, 'set_{}lim'.format(dim))(ctr-r, ctr+r)

        return True