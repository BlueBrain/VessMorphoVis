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
        self.morphology_objects = list()

        # UI Context 
        self.context = None

    ################################################################################################
    # @get_poly_line_data_colored_with_single_color
    ################################################################################################
    def get_poly_line_data_colored_with_single_color(self):

        # The poly-lines data list 
        poly_lines_data = list() 

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_with_single_color(
                    section=section))

        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_line_data_colored_with_single_color
    ################################################################################################
    def get_poly_line_data_colored_with_alternating_colors(self):

        # The poly-lines data list 
        poly_lines_data = list() 
        
        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_with_alternating_colors(
                    section=section))

        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_line_data_based_on_radius
    ################################################################################################
    def get_poly_line_data_based_on_radius(self):
        """Gets a poly-lines data list based on radius.

        :return: 
            A poly-lines data list based on the radius of the segments in the morphology. 
        """
        
        # The poly-lines data list 
        poly_lines_data = list() 

        # Get minimum and maximum radii of the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_samples_radii(self.morphology)

        # Update the interface with the minimum and maximum values for the colormapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_based_on_radius(
                    section=section, minimum=minimum, maximum=maximum, 
                    color_map_resolution=self.options.morphology.color_map_resolution))

        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_line_data_based_on_radius
    ################################################################################################
    def get_poly_line_data_based_on_length(self):
        """Gets a poly-lines data list based on length.

        :return: 
            A poly-lines data list based on the length of the segments in the morphology. 
        """
        
        # The poly-lines data list 
        poly_lines_data = list() 

        # Get minimum and maximum radii of the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_segments_length(self.morphology)
        
        # Update the interface with the minimum and maximum values for the colormapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_based_on_length(
                    section=section, minimum=minimum, maximum=maximum,
                    color_map_resolution=self.options.morphology.color_map_resolution))

        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_line_data_based_on_surface_area
    ################################################################################################
    def get_poly_line_data_based_on_surface_area(self):
        """Gets a poly-lines data list based on surface area.

        :return: 
            A poly-lines data list based on the surface area of the segments in the morphology. 
        """
        
        # The poly-lines data list 
        poly_lines_data = list() 

        # Get minimum and maximum radii of the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_segments_surface_area(
            self.morphology)
        
        # Update the interface with the minimum and maximum values for the colormapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_based_on_surface_area(
                    section=section, minimum=minimum, maximum=maximum,
                    color_map_resolution=self.options.morphology.color_map_resolution))

        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_line_data_based_on_volume
    ################################################################################################
    def get_poly_line_data_based_on_volume(self):
        """Gets a poly-lines data list based on surface area.

        :return: 
            A poly-lines data list based on the surface area of the segments in the morphology. 
        """
        
        # The poly-lines data list 
        poly_lines_data = list() 

        # Get minimum and maximum radii of the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_segments_volume(
            self.morphology)
        
        # Update the interface with the minimum and maximum values for the colormapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_based_on_volume(
                    section=section, minimum=minimum, maximum=maximum,
                    color_map_resolution=self.options.morphology.color_map_resolution))

        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_segments_poly_lines_data
    ################################################################################################
    def get_segments_poly_lines_data(self):

        # Get the data based on the color-coding scheme  
        if self.options.morphology.color_coding == vmv.enums.ColorCoding.SINGLE_COLOR:
            return self.get_poly_line_data_colored_with_single_color()   
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.ALTERNATING_COLORS:
            return self.get_poly_line_data_colored_with_alternating_colors()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_RADIUS:
            return self.get_poly_line_data_based_on_radius() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_LENGTH:
            return self.get_poly_line_data_based_on_length() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_AREA:
            return self.get_poly_line_data_based_on_surface_area()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_VOLUME:
            return self.get_poly_line_data_based_on_volume() 
        else:
            return self.get_poly_line_data_colored_with_single_color() 

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
        if self.options.morphology.color_coding == vmv.enums.ColorCoding.SINGLE_COLOR:
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
        """Draws the morphology skeleton using fast reconstruction and drawing method.
        """

        vmv.logger.header('Building skeleton: DisconnectedSegmentsBuilder')

        # Get the context 
        self.context = context 

        # Clear the scene
        vmv.logger.info('Clearing scene')
        vmv.scene.ops.clear_scene()

        # Clear the materials
        vmv.logger.info('Creating assets')
        vmv.scene.ops.clear_scene_materials()

        # Create assets and color-maps 
        vmv.logger.info('Creating assets')
        color_map = self.create_color_map()

        # Create a static bevel object that you can use to scale the samples
        bevel_object = vmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Construct sections poly-lines
        vmv.logger.info('Constructing poly-lines')
        poly_lines_data = self.get_segments_poly_lines_data()
            
        # Pre-process the radii
        vmv.logger.info('Adjusting radii')
        vmv.skeleton.update_poly_lines_radii(poly_lines=poly_lines_data, options=self.options)

        # Construct the final object and add it to the morphology
        vmv.logger.info('Drawing poly-lines')
        self.morphology_objects.append(
            vmv.geometry.create_poly_lines_object_from_poly_lines_data(
                poly_lines_data, material=self.options.morphology.material, color_map=color_map, 
                name=self.morphology.name, bevel_object=bevel_object))