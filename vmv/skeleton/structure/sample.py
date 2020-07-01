####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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
    """Morphological skeleton sample.

    The section is composed of a set of segments, and each segment is composed of two samples.
    Each sample has a point in the cartesian coordinates and a radius that reflect the
    cross-sectional area of the morphology at a certain point.
    Note that the samples
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 point,
                 radius,
                 index=-1,
                 parent_index=-1):
        """Constructor

        :param point:
            Sample position in the cartesian space, Vector((x, y, z)).
        :param radius:
            Sample radius.
        """

        # Sample cartesian point
        self.point = point

        # Sample radius
        self.radius = radius

        self.index=index

        self.parent_index = parent_index
