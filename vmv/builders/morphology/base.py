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
from mathutils import Vector

# Internal imports
import vmv
import vmv.geometry
import vmv.mesh
import vmv.consts
import vmv.scene
import vmv.skeleton
import vmv.shading
import vmv.utilities


####################################################################################################
# @SectionsBuilder
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

        # Minimum simulation value
        self.minimum_simulation_value = 1e30

        # Maximum simulation value
        self.maximum_simulation_value = -1 * 1e30

        # The morphology name
        self.morphology_name = '%s%s' % (morphology.name, vmv.consts.Suffix.MORPHOLOGY_SUFFIX)

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
    def create_color_map(self,
                         dynamic_colormap=False):
        """Creates a color map that will be assigned to the skeleton.

        :param dynamic_colormap:
            A dynamic color map is requested.
        :rtype:
            List of Vector((X, Y, Z))
        """

        # Dynamic color map for the simulation
        if dynamic_colormap:
            return vmv.utilities.create_color_map_from_color_list(
                self.options.morphology.color_map_colors,
                number_colors=self.options.morphology.color_map_resolution)
        else:
            # Single color
            if self.options.morphology.color_coding == vmv.enums.ColorCoding.DEFAULT:
                return [self.options.morphology.color]

            # Alternating colors
            elif self.options.morphology.color_coding == vmv.enums.ColorCoding.ALTERNATING_COLORS:
                return [self.options.morphology.color, self.options.morphology.alternating_color]

            elif self.options.morphology.color_coding == vmv.enums.ColorCoding.SHORT_SECTIONS:
                return [self.options.morphology.color, self.options.morphology.alternating_color]

            elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_SEGMENT_ALIGNMENT:
                return vmv.utilities.create_xyz_color_list()

            # Otherwise, it is a color-map
            else:
                return vmv.utilities.create_color_map_from_color_list(
                    self.options.morphology.color_map_colors,
                    number_colors=self.options.morphology.color_map_resolution)

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self,
                       context=None,
                       dynamic_colormap=False):
        """Draws the morphology skeleton and return a reference to it.
        """

        # Get the context
        self.context = context

        # Clear the scene
        vmv.logger.info('Clearing Scene')
        vmv.scene.ops.clear_scene()

        # Clear the materials
        vmv.logger.info('Clearing Assets')
        vmv.scene.ops.clear_scene_materials()

        # Create assets and color-maps, based on what is selected in the morphology panel
        vmv.logger.info('Creating Colormap')
        self.color_map = self.create_color_map(dynamic_colormap=dynamic_colormap)

        # Create the corresponding illumination
        vmv.shading.create_material_specific_illumination(
            material_type=self.options.morphology.material)
