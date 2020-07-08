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


####################################################################################################
# @DisconnectedSectionsBuilder
####################################################################################################
class DisconnectedSectionsBuilder:
    """The builder reconstructs a an object composed of a series of disconnected sections, where 
    each section is drawn as an independent object.
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

        # All the reconstructed objects of the morphology, for example, tubes, spheres, etc...
        self.morphology_objects = list()

        # Context for the UI to display certain messages 
        self.context=None

    ################################################################################################
    # @get_poly_lines_data_colored_with_single_color
    ################################################################################################
    def get_poly_lines_data_colored_with_single_color(self):

        # Get the poly-line data of each section
        poly_lines_data = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_with_single_color(section=section) 
                for section in self.morphology.sections_list] 
        
        # Return the list 
        return poly_lines_data 


    ################################################################################################
    # @get_poly_lines_data_colored_with_alternating_colors
    ################################################################################################
    def get_poly_lines_data_colored_with_alternating_colors(self):

        # Get the poly-line data of each section
        poly_lines_data = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_with_alternating_colors(
                section=section)
                    for section in self.morphology.sections_list] 
        
        # Return the list 
        return poly_lines_data 

    ################################################################################################
    # @get_poly_lines_data_colored_based_on_radius
    ################################################################################################
    def get_poly_lines_data_colored_based_on_radius(self):
        """Gets a list of poly-lines that are color-coded based on the average radii of the 
        sections.

        :return: 
            A list of poly-lines that are color-coded based on the average radii of the 
            sections.
        """

        # Get minimum and maximum (average-radii) of the sections in the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_sections_average_radii(
            self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        poly_lines_data = [vmv.skeleton.ops.get_color_coded_section_poly_line_based_on_radius(
                    section=section, minimum=minimum, maximum=maximum, 
                    color_map_resolution=self.options.morphology.color_map_resolution) \
                        for section in self.morphology.sections_list] 
        
        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_lines_data_colored_based_on_length
    ################################################################################################
    def get_poly_lines_data_colored_based_on_length(self):
        """Gets a list of poly-line that are color-coded based on the lengths of the sections.

        :return: 
            A list of poly-line that are color-coded based on the lengths of the sections.
        """

        # Get minimum and maximum lengths of the sections in the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_sections_lengths(
            self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        poly_lines_data = [vmv.skeleton.ops.get_color_coded_section_poly_line_based_on_length(
            section=section, minimum=minimum, maximum=maximum, 
            color_map_resolution=self.options.morphology.color_map_resolution) 
                for section in self.morphology.sections_list] 
        
        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_lines_data_colored_based_on_surface_area
    ################################################################################################
    def get_poly_lines_data_colored_based_on_surface_area(self):
        """Gets a list of poly-line that are color-coded based on the areas of the sections.

        :return: 
            A list of poly-line that are color-coded based on the areas of the sections.
        """

        # Get minimum and maximum surface areas of the sections in the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_sections_surface_areas(
            self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        poly_lines_data = [vmv.skeleton.ops.get_color_coded_section_poly_line_based_on_surface_area(
            section=section, minimum=minimum, maximum=maximum, 
            color_map_resolution=self.options.morphology.color_map_resolution) 
                for section in self.morphology.sections_list] 
        
        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_lines_data_colored_based_on_volume
    ################################################################################################
    def get_poly_lines_data_colored_based_on_volume(self):
        """Gets a list of poly-line that are color-coded based on the volumes of the sections.

        :return: 
            A list of poly-line that are color-coded based on the volumes of the sections.
        """

        # Get minimum and maximum volumes of the sections in the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_sections_volumes(self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        poly_lines_data = [vmv.skeleton.ops.get_color_coded_section_poly_line_based_on_volume(
            section=section, minimum=minimum, maximum=maximum,
            color_map_resolution=self.options.morphology.color_map_resolution) 
                for section in self.morphology.sections_list] 
        
        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_lines_data_colored_based_on_number_samples_in_section
    ################################################################################################
    def get_poly_lines_data_colored_based_on_number_samples_in_section(self):
        """Gets a list of poly-line that are color-coded based on the number of samples in the 
        sections.

        :return: 
            A list of poly-line that are color-coded based on the number of samples in the sections.
        """

        # Get minimum and maximum volumes of the sections in the morphology
        minimum, maximum = vmv.skeleton.get_minumum_and_maximum_sections_number_samples(
            self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.MinimumValue = str(minimum)
            self.context.scene.MaximumValue = str(maximum)

        # Get the poly-line data of each section
        poly_lines_data = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_based_on_number_samples(
                section=section, minimum=minimum, maximum=maximum,
                color_map_resolution=self.options.morphology.color_map_resolution) 
                    for section in self.morphology.sections_list] 
        
        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_sections_poly_lines_data
    ################################################################################################
    def get_sections_poly_lines_data(self):

        # A list of all the poly-lines
        poly_lines_data = list()
        
        # Get the data based on the color-coding scheme  
        if self.options.morphology.color_coding == vmv.enums.ColorCoding.SINGLE_COLOR:
            return self.get_poly_lines_data_colored_with_single_color()   
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.ALTERNATING_COLORS:
            return self.get_poly_lines_data_colored_with_alternating_colors()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_RADIUS:
            return self.get_poly_lines_data_colored_based_on_radius() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_LENGTH:
            return self.get_poly_lines_data_colored_based_on_length() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_AREA:
            return self.get_poly_lines_data_colored_based_on_surface_area()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_VOLUME:
            return self.get_poly_lines_data_colored_based_on_volume() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_NUMBER_SAMPLES:
            return self.get_poly_lines_data_colored_based_on_number_samples_in_section() 
        else:
            return self.get_poly_lines_data_colored_with_single_color()   

        return poly_lines_data 
    
    
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
    def build_skeleton(self, context=None):
        """Draws the morphology skeleton using fast reconstruction and drawing method.
        """

        vmv.logger.header('Building skeleton: DisconnectedSectionsBuilder')

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
        color_map = self.create_color_map()

        # Create a static bevel object that you can use to scale the samples
        bevel_object = vmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Construct sections poly-lines
        vmv.logger.info('Constructing poly-lines')
        poly_lines_data = self.get_sections_poly_lines_data()

        # Pre-process the radii
        vmv.logger.info('Adjusting radii')
        vmv.skeleton.update_poly_lines_radii(poly_lines=poly_lines_data, options=self.options)

        # Adaptively resampling the reconstructed sections
        if self.options.morphology.adaptive_resampling:
            vmv.logger.info('Re-sampling poly-lines')
            vmv.skeleton.resample_poly_lines_adaptively(poly_lines=poly_lines_data)

        # Construct the final object and add it to the morphology
        vmv.logger.info('Drawing object')
        return vmv.geometry.create_poly_lines_object_from_poly_lines_data(
            poly_lines_data, material=self.options.morphology.material, color_map=color_map,
            name=self.morphology.name, bevel_object=bevel_object)
