####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import random, copy

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.geometry
import vmv.mesh
import vmv.scene
import vmv.skeleton


####################################################################################################
# @DisconnectedSegmentsBuilder
####################################################################################################
class DisconnectedSegmentsBuilder:
    """Morphology reconstruction with disconnected segments, where each segment is drawn as an
    independent object and can have a different color.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology.
        :parm options
            System options.
        """

        # Morphology
        self.morphology = morphology

        # All the options of the project
        self.options = options

        # All the reconstructed objects of the morphology, for example, tubes, spheres, etc... .
        self.morphology_objects = []

    ################################################################################################
    # @get_segments_poly_lines_data
    ################################################################################################
    def get_segments_poly_lines_data(self):
        """Gets a list of the data of all the poly-lines that correspond to the segments in the
        morphology.

        NOTE: Each entry in the the poly-lines list has the following format:
            * poly_lines_data[0]: a list of all the samples (points and their radii)
            * poly_lines_data[0]: the material index

        :return:
            A list of all the poly-lines that correspond to the sections in the entire morphology.
        """

        # A list of all the poly-lines
        poly_lines_data = list()

        # Get the poly-line data of each section
        for i, section in enumerate(self.morphology.sections_list):

            # Add the poly-line to the aggregate list
            poly_lines_data.extend(vmv.skeleton.ops.get_segments_poly_lines(section=section))

        # Return the poly-lines list
        return poly_lines_data

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self):
        """Draws the morphology skeleton using fast reconstruction and drawing method.
        """

        vmv.logger.header('Building skeleton: DisconnectedSegmentsBuilder')

        # Clear the scene
        vmv.logger.detail('Clearing scene')
        vmv.scene.ops.clear_scene()

        # Clear the materials
        vmv.scene.ops.clear_scene_materials()

        # Create a static bevel object that you can use to scale the samples
        bevel_object = vmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Construct sections poly-lines
        vmv.logger.detail('Constructing poly-lines')
        poly_lines_data = self.get_segments_poly_lines_data()

        # Pre-process the radii
        vmv.logger.detail('Adjusting radii')
        vmv.skeleton.update_poly_lines_radii(poly_lines=poly_lines_data, options=self.options)

        # Construct the final object and add it to the morphology
        vmv.logger.detail('Drawing object')
        self.morphology_objects.append(
            vmv.geometry.create_poly_lines_object_from_poly_lines_data(
                poly_lines_data, color=self.options.morphology.color,
                material=self.options.morphology.material, name=self.morphology.name,
                bevel_object=bevel_object))

        # Hide the bevel object


