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

# Internal imports
import vmv.geometry
import vmv.mesh
import vmv.scene
import vmv.skeleton
from .base import MorphologyBuilder


####################################################################################################
# @SectionsBuilder
####################################################################################################
class SectionsBuilder(MorphologyBuilder):
    """The builder reconstructs a an object composed of a series of disconnected sections, where 
    each section is drawn as an independent object.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given vascular morphology to reconstruct its skeleton as a series of disconnected
            sections.
        :param options:
            System options.
        """

        # Base
        MorphologyBuilder.__init__(self, morphology=morphology, options=options)

    ################################################################################################
    # @get_poly_lines_data_colored_with_single_color
    ################################################################################################
    def get_poly_lines_data_colored_with_single_color(self):
        """Gets a list of polylines (or polyline data in Blender format) for a morphology
        color-coded with a single color only.

        :return:
            A list of polylines.
        """

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
        """Gets a list of polylines (or polyline data in Blender format) for a morphology
        color-coded with alternating colors.

        :return:
            A list of polylines.
        """

        # Get the poly-line data of each section
        poly_lines_data = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_with_alternating_colors(
                section=section)
            for section in self.morphology.sections_list]
        
        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_lines_data_colored_for_short_sections
    ################################################################################################
    def get_poly_lines_data_colored_for_short_sections(self):
        """Gets a list of polylines (or polyline data in Blender format) for a morphology
        color-coded with alternating colors to reveal the short sections in the morphology.

        :return:
            A list of polylines.
        """

        # Get the poly-line data of each section
        poly_lines_data = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_for_short_sections(
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
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_sections_average_radii(
            self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

        # Get the poly-line data of each section
        poly_lines_data = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_based_on_radius(
                section=section, minimum=minimum, maximum=maximum,
                color_map_resolution=self.options.morphology.color_map_resolution)
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
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_sections_lengths(
            self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

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
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_sections_surface_areas(
            self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

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
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_sections_volumes(self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

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
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_sections_number_samples(
            self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping  
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

        # Get the poly-line data of each section
        poly_lines_data = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_based_on_number_samples(
                section=section, minimum=minimum, maximum=maximum,
                color_map_resolution=self.options.morphology.color_map_resolution)
            for section in self.morphology.sections_list]
        
        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_lines_data_colored_based_on_section_index
    ################################################################################################
    def get_poly_lines_data_colored_based_on_section_index(self):
        """Gets a list of poly-line that are color-coded based on the section index, where the
        sections will start from zero and to the last section index.

        :return:
            A list of poly-line that are color-coded based on the section index.
        """

        # Get minimum and maximum volumes of the sections in the morphology
        minimum = 0
        maximum = len(self.morphology.sections_list)

        # Update the interface with the minimum and maximum values for the color-mapping
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

        # Get the poly-line data of each section
        poly_lines_data = [
            vmv.skeleton.ops.get_color_coded_sections_poly_lines_based_on_section_index(
                section=section, minimum=minimum, maximum=maximum,
                color_map_resolution=self.options.morphology.color_map_resolution)
            for section in self.morphology.sections_list]

        # Return the list
        return poly_lines_data

    ################################################################################################
    # @get_sections_poly_lines_data
    ################################################################################################
    def get_sections_poly_lines_data(self):
        """Gets a list of all the polylines that account for the sections in the morphology.
        """

        # Get the data based on the color-coding scheme  
        if self.options.morphology.color_coding == vmv.enums.ColorCoding.DEFAULT:
            return self.get_poly_lines_data_colored_with_single_color()   
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.ALTERNATING_COLORS:
            return self.get_poly_lines_data_colored_with_alternating_colors()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.SHORT_SECTIONS:
            return self.get_poly_lines_data_colored_for_short_sections()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_RADIUS:
            return self.get_poly_lines_data_colored_based_on_radius() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_LENGTH:
            return self.get_poly_lines_data_colored_based_on_length() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_SURFACE_AREA:
            return self.get_poly_lines_data_colored_based_on_surface_area()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_VOLUME:
            return self.get_poly_lines_data_colored_based_on_volume() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_NUMBER_SAMPLES:
            return self.get_poly_lines_data_colored_based_on_number_samples_in_section()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_SECTION_INDEX:
            return self.get_poly_lines_data_colored_based_on_section_index()
        else:
            return self.get_poly_lines_data_colored_with_single_color()

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self,
                       context=None,
                       dynamic_colormap=False):
        """Draws the morphology skeleton using fast reconstruction and drawing method.

        :param context:
            Blender context.
        :param dynamic_colormap:
            A dynamic colormap.
        :return:
            A reference to the reconstructed morphology skeleton.
        """

        vmv.logger.header('Building Skeleton: SectionsBuilder')

        # Call the base function
        super(SectionsBuilder, self).build_skeleton(
            context=context, dynamic_colormap=dynamic_colormap)

        # Create a static bevel object that you can use to scale the samples
        bevel_object = vmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')
        vmv.scene.hide_object(scene_object=bevel_object)

        # Construct sections poly-lines
        vmv.logger.info('Constructing Poly-lines')
        poly_lines_data = self.get_sections_poly_lines_data()

        # Pre-process the radii
        vmv.logger.info('Adjusting Radii')
        vmv.skeleton.update_poly_lines_radii(poly_lines=poly_lines_data, options=self.options)

        # Adaptively resampling the reconstructed sections
        if self.options.morphology.adaptive_resampling:
            vmv.logger.info('Re-sampling poly-lines')
            vmv.skeleton.resample_poly_lines_adaptively(poly_lines=poly_lines_data)

        # Construct the final object and add it to the morphology
        vmv.logger.info('Drawing Object')
        self.morphology_skeleton = vmv.geometry.create_poly_lines_object_from_poly_lines_data(
            poly_lines_data, material=self.options.morphology.material, color_map=self.color_map,
            name=self.morphology_name, bevel_object=bevel_object)
        return self.morphology_skeleton

    ################################################################################################
    # @adjust_point_radius_at_time_step
    ################################################################################################
    def adjust_point_radius_at_time_step(self,
                                         polyline,
                                         point_index,
                                         section_index,
                                         time_step):
        """Adjusts the radius of a point along a morphological section at a given time step.

        :param polyline:
            Spline polyline.
        :param point_index:
            The unique index of the point.
        :param section_index:
            Morphological section index.

        :param time_step:
            The time step.
        """

        # Get the index of the radius from the samples list
        radius_index = self.morphology.sections_list[section_index].samples[point_index].index

        # Get a reference to the radii
        radius_list = self.morphology.radius_simulation_data[radius_index - 1]

        # Update the point radius along the spline
        polyline.points[point_index].radius = radius_list[time_step]

        # Set the keyframe to the time step
        polyline.points[point_index].keyframe_insert('radius', frame=time_step)

    ################################################################################################
    # @update_section_radii_at_step
    ################################################################################################
    def update_section_radii_at_step(self,
                                     section_index,
                                     time_step):
        """Updates the radii of a given section at a time.

        :param section_index:
            The index of the section.
        :param time_step:
            The time step.
        """

        if len(self.morphology.sections_list[section_index].samples) > 0:

            # Get a reference to the polyline
            polyline = self.morphology_skeleton.data.splines[section_index]

            [self.adjust_point_radius_at_time_step(polyline, i_point, section_index, time_step)
             for i_point in range(len(polyline.points))]

    ################################################################################################
    # @load_radius_simulation_data_at_step
    ################################################################################################
    def load_radius_simulation_data_at_step(self,
                                            time_step,
                                            context=None):
        """Loads the radius simulation data at a specific time step.

        :param time_step:
            The time step.
        :param context:
            Blender context.
        """

        # Update the context
        self.context = context

        # Do it per section
        [self.update_section_radii_at_step(i_section, time_step)
         for i_section in range(len(self.morphology.sections_list))]

    ################################################################################################
    # @load_radius_simulation_data
    ################################################################################################
    def load_radius_simulation_data(self):
        """Loads the radius simulation data for all the time steps.
        """

        # Add simulation data
        [self.load_radius_simulation_data_at_step(time_step=time_step)
         for time_step in range(0, len(self.morphology.radius_simulation_data[0]))]
