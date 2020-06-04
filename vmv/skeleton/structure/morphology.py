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

# Blender imports
from mathutils import Vector

# Internal imports
import vmv.bbox
import vmv.consts


####################################################################################################
# Morphology
####################################################################################################
class Morphology:
    """A structure that contains all the data of the morphology.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology_name='VESSEL',
                 morphology_file_path=None,
                 points_list=None,
                 radii_list=None,
                 structures_list=None,
                 connectivity_list=None,
                 sections_list=None,
                 roots=None):
        """Constructor

        :param morphology_file_path:
            Morphology file path as loaded from disk.
        :param points_list:
            A list of all the points or samples.
        :param radii_list:
            A list of all the radii in the morphology.
        :param structures_list:
            A list of all the sections.
        :param connectivity_list:
            A list that accounts for the connectivity information in the morphology.
        :param sections_list:
            A list of all the constructed sections in the morphology.
        :param roots:
            A list of all the roots. This is ONE if the morphology is entirely connected.
        """
        # Morphology name
        self.name = morphology_name

        # Morphology file path
        self.morphology_file_path = morphology_file_path

        # A list of all the points (or samples) in the morphology file
        self.points_list = points_list

        # A list of the radii of all the samples in the morphology file
        self.radii_list = radii_list

        # A list of all the structures in the morphology file
        self.structures_list = structures_list

        # A list of the connectivity data in the morphology file
        self.connectivity_list = connectivity_list

        # A list of all the sections that were extracted from the loaded data
        self.sections_list = sections_list

        # A list of all the root nodes
        self.roots = roots

        # Morphology bounding box
        self.bounding_box = None

        self.radii_list = None

        # Compute the bounding box of the morphology
        self.compute_bounding_box()

    ################################################################################################
    # @get_center
    ################################################################################################
    def get_center(self):
        """Returns the origin of the morphology.

        :return:
            Returns the center of the morphology to load it at the center.
        """
        return self.bounding_box.center

    ################################################################################################
    # @compute_bounding_box
    ################################################################################################
    def compute_bounding_box(self):

        # Initialize the min and max points
        p_min = Vector((vmv.consts.Math.INFINITY,
                        vmv.consts.Math.INFINITY,
                        vmv.consts.Math.INFINITY))
        p_max = Vector((-1 * vmv.consts.Math.INFINITY,
                        -1 * vmv.consts.Math.INFINITY,
                        -1 * vmv.consts.Math.INFINITY))

        for point in self.points_list:

            # Points
            x = point[0]
            y = point[1]
            z = point[2]

            if x < p_min[0]:
                p_min[0] = x
            if y < p_min[1]:
                p_min[1] = y
            if z < p_min[2]:
                p_min[2] = z

            if x > p_max[0]:
                p_max[0] = x
            if y > p_max[1]:
                p_max[1] = y
            if z > p_max[2]:
                p_max[2] = z

        # Build bounding box object
        self.bounding_box = vmv.bbox.BoundingBox(p_min, p_max)

    ################################################################################################
    # @reset_traversal_states
    ################################################################################################
    def reset_traversal_states(self):
        """Resets the traversal state of every section in the morphology tree after the construct
        of the tree.
        """

        # The sections list must not be empty
        if self.sections_list is not None:

            # For every section
            for section in self.sections_list:

                # Reset the traversal list
                section.traversed = False
