####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
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

# System imports
import math

# Blender imports
from mathutils import Vector

# Internal imports
import vmv
import vmv.consts


####################################################################################################
# @BoundingBox
####################################################################################################
class BoundingBox:
    """Bounding box
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self, 
                 p_min=vmv.consts.Math.ORIGIN,
                 p_max=vmv.consts.Math.ORIGIN,
                 center=vmv.consts.Math.ORIGIN,
                 bounds=vmv.consts.Math.ORIGIN):
        """Constructor
        """

        # Construct the bounding box from @p_min and @p_max
        if p_min != vmv.consts.Math.ORIGIN and max != vmv.consts.Math.ORIGIN:
            self.p_min = p_min
            self.p_max = p_max
            self.bounds = p_max - p_min
            self.center = p_min + (self.bounds / 2.0)

        # Construct the bounding box from @bounds and @center
        else:
            self.bounds = bounds
            self.center = center
            self.p_min = center - (self.bounds / 2.0)
            self.p_max = center + (self.bounds / 2.0)

    ################################################################################################
    # @extend_bbox
    ################################################################################################
    def extend_bbox(self,
                    delta=1.0):
        """Extends the bounding box few microns uniformly in all the directions.

        :param delta:
            The value that will be used to extend the bounding box.
        """

        self.p_min -= Vector((delta, delta, delta))
        self.p_max += Vector((delta, delta, delta))
        self.bounds = self.p_max - self.p_min

    ################################################################################################
    # @compute_diagonal
    ################################################################################################
    def compute_diagonal(self):
        """Computes the diagonal of the bounding box.

        :return:
            The diagonal of the bounding box.
        """

        # Compute the diagonal of the bounding box
        return math.sqrt(self.bounds[0] * self.bounds[0] +
                         self.bounds[1] * self.bounds[1] +
                         self.bounds[2] * self.bounds[2])

    ################################################################################################
    # @print_details
    ################################################################################################
    def print_details(self,
                      name='BBox'):
        """Prints the bounding box data.
        """  
        vmv.logger.log("Shape BBox: %s" % name)
        vmv.logger.log("pMin: " + str(self.p_min))
        vmv.logger.log("pMax: " + str(self.p_max))
        vmv.logger.log("Bounds: " + str(self.bounds))
        vmv.logger.log("Center: " + str(self.center))
