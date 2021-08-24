####################################################################################################
# Copyright (c) 2018 - 2019, EPFL / Blue Brain Project
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
import sys
import copy

# Blender imports
import bpy

# Internal imports
import vmv
import vmv.geometry
import vmv.mesh
import vmv.scene
import vmv.skeleton
import vmv.utilities


####################################################################################################
# @DisconnectedSectionsBuilder
####################################################################################################
class MorphologyBuilder:
    """Base class, where all the morphology builders will inherit from.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology to reconstruct its skeleton as a series of disconnected sections.
        :param options:
            System options.
        """

        # Clone the original morphology to morphology before the pre=processing
        self.morphology = morphology

        # All the options of the project
        self.options = options

        # Skeleton materials
        self.materials = None

        # The colormap of the morphology
        self.color_map = None

        # A reference to the morphology skeleton after reconstruction
        self.morphology_skeleton = None

        # Context for the UI to display certain messages
        self.context = None

    ################################################################################################
    # @create_skeleton_materials
    ################################################################################################
    def create_skeleton_materials(self):
        """Creates the materials of the skeleton.

        NOTE: The created materials are stored in private variables.
        """

        # Clear all the materials that are already present in the scene
        for material in bpy.data.materials:
            if 'morphology_skeleton' in material.name:
                material.user_clear()
                bpy.data.materials.remove(material)

        # Skeleton materials
        self.materials = vmv.skeleton.ops.create_skeleton_materials(
            name='morphology_skeleton', material_type=self.options.morphology.material,
            color=self.options.morphology.color)

    ################################################################################################
    # @create_color_map
    ################################################################################################
    def create_color_map(self):
        """Creates the color map that will be assigned to the skeleton.

        :return:
            A color-map list.
        :rtype:
            List of Vector((X, Y, Z))
        """

        # Single color
        if self.options.morphology.color_coding == vmv.enums.ColorCoding.DEFAULT:
            return [self.options.morphology.color]

        # Alternating colors
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.ALTERNATING_COLORS:
            return [self.options.morphology.color, self.options.morphology.alternating_color]

        # Otherwise, it is a color-map
        else:
            return vmv.utilities.create_color_map_from_color_list(
                self.options.morphology.color_map_colors,
                number_colors=self.options.morphology.color_map_resolution)

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self,
                       context=None):
        """Draws the morphology skeleton and return a reference to it.
        """

        # Get the context
        self.context = context

        # Clear the scene
        vmv.logger.info('Clearing scene')
        vmv.scene.ops.clear_scene()

        # Clear the materials
        vmv.logger.info('Clearing assets')
        vmv.scene.ops.clear_scene_materials()

        # Create assets and color-maps
        vmv.logger.info('Creating assets')
        self.color_map = self.create_color_map()
