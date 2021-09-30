####################################################################################################
# Copyright (c) 2019 - 2021, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of VessMorphoVis <https://github.com/BlueBrain/VessMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################


####################################################################################################
# Sample
####################################################################################################
class Sample:
    """Vasculature morphology sample.

    NOTE: The section is composed of a set of segments, and each segment is composed of two samples.
    Each sample has a point in the Cartesian coordinates and a radius that reflects the cross
    sectional area of the morphology at a certain point.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 point,
                 radius,
                 index=None,
                 parent_index=None):
        """Constructor

       :param point:
            Sample position in the cartesian space, Vector((x, y, z)).
        :param radius:
            Sample radius.
        @param index:
            Sample unique index.
        @param parent_index:
            The index of the parent sample, if exists. Used for tracking and connectivity.
        """

        # Sample cartesian point
        self.point = point

        # Sample radius
        self.radius = radius

        # Sample unique index
        self.index = index

        # Sample's parent index
        self.parent_index = parent_index
