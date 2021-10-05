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

# System imports
import sys

# Internal imports
import vmv.geometry
import vmv.mesh
import vmv.scene
import vmv.skeleton
import vmv.utilities
from .base import MorphologyBuilder


####################################################################################################
# @SegmentsBuilder
####################################################################################################
class SegmentsBuilder(MorphologyBuilder):
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
            A given vascular morphology.
        :parm options
            System options.
        """

        # Base
        MorphologyBuilder.__init__(self, morphology=morphology, options=options)

    ################################################################################################
    # @get_poly_line_data_colored_with_single_color
    ################################################################################################
    def get_poly_line_data_colored_with_single_color(self):
        """Gets a list of polylines (or polyline data in Blender format) for a morphology
        color-coded with a single color only.

        :return:
            A list of polylines.
        """
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
        """Gets a list of polylines (or polyline data in Blender format) for a morphology
        color-coded with alternating colors.

        :return:
            A list of polylines.
        """
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
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_samples_radii(self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_based_on_radius(
                    section=section, minimum=minimum, maximum=maximum, 
                    color_map_resolution=self.options.morphology.color_map_resolution))

        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_line_data_based_on_length
    ################################################################################################
    def get_poly_line_data_based_on_length(self):
        """Gets a poly-lines data list based on length.

        :return: 
            A poly-lines data list based on the length of the segments in the morphology. 
        """
        
        # The poly-lines data list 
        poly_lines_data = list() 

        # Get minimum and maximum radii of the morphology
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_segments_length(self.morphology)
        
        # Update the interface with the minimum and maximum values for the color-mapping
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

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
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_segments_surface_area(
            self.morphology)
        
        # Update the interface with the minimum and maximum values for the color-mapping
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

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
        """Gets a poly-lines data list based on volume.

        :return: 
            A poly-lines data list based on the volume of the segments in the morphology.
        """
        
        # The poly-lines data list 
        poly_lines_data = list() 

        # Get minimum and maximum radii of the morphology
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_segments_volume(self.morphology)
        
        # Update the interface with the minimum and maximum values for the color-mapping
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_based_on_volume(
                    section=section, minimum=minimum, maximum=maximum,
                    color_map_resolution=self.options.morphology.color_map_resolution))

        # Return the list 
        return poly_lines_data

    ################################################################################################
    # @get_poly_line_data_based_on_segment_index
    ################################################################################################
    def get_poly_line_data_based_on_segment_index(self):
        """Gets a poly-lines data list based on the segment index (or the sample index).

        :return:
            A poly-lines data list based on the index of the segments in the morphology.
        """

        # The poly-lines data list
        poly_lines_data = list()

        # Get minimum and maximum radii of the morphology
        minimum, maximum = vmv.skeleton.get_minimum_and_maximum_segments_index(self.morphology)

        # Update the interface with the minimum and maximum values for the color-mapping
        if self.context is not None:
            self.context.scene.VMV_MinimumValue = str(minimum)
            self.context.scene.VMV_MaximumValue = str(maximum)

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_based_on_index(
                    morphology=self.morphology, section=section, minimum=minimum, maximum=maximum,
                    color_map_resolution=self.options.morphology.color_map_resolution))

        # Return the list
        return poly_lines_data

    ################################################################################################
    # @get_poly_line_data_based_on_segment_alignment
    ################################################################################################
    def get_poly_line_data_based_on_segment_alignment(self):
        """Gets a list of all the polylines based on the alignment of the segments in the morphology.
        """

        # The poly-lines data list
        poly_lines_data = list()

        # Get the poly-line data of each section
        for section in self.morphology.sections_list:
            poly_lines_data.extend(
                vmv.skeleton.ops.get_color_coded_segments_poly_lines_based_on_alignment(
                    section=section))

        # Return the list
        return poly_lines_data

    ################################################################################################
    # @get_segments_poly_lines_data
    ################################################################################################
    def get_segments_poly_lines_data(self):
        """Gets a list of all the polylines that account for the sections in the morphology.
        """

        # Get the data based on the color-coding scheme  
        if self.options.morphology.color_coding == vmv.enums.ColorCoding.DEFAULT:
            return self.get_poly_line_data_colored_with_single_color()   
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.ALTERNATING_COLORS:
            return self.get_poly_line_data_colored_with_alternating_colors()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_RADIUS:
            return self.get_poly_line_data_based_on_radius() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_LENGTH:
            return self.get_poly_line_data_based_on_length() 
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_SURFACE_AREA:
            return self.get_poly_line_data_based_on_surface_area()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_VOLUME:
            return self.get_poly_line_data_based_on_volume()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_SEGMENT_INDEX:
            return self.get_poly_line_data_based_on_segment_index()
        elif self.options.morphology.color_coding == vmv.enums.ColorCoding.BY_SEGMENT_ALIGNMENT:
            return self.get_poly_line_data_based_on_segment_alignment()

        else:
            return self.get_poly_line_data_colored_with_single_color()

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self,
                       context=None,
                       dynamic_colormap=False):
        """Draws the morphology skeleton using a fast reconstruction and drawing method.
        """

        # Header
        vmv.logger.header('Building skeleton: SegmentsBuilder')

        # Call the base function
        super(SegmentsBuilder, self).build_skeleton(
            context=context, dynamic_colormap=dynamic_colormap)

        # Create a static bevel object that you can use to scale the samples
        bevel_object = vmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')
        vmv.scene.hide_object(scene_object=bevel_object)

        # Construct sections poly-lines
        vmv.logger.info('Constructing polylines')
        poly_lines_data = self.get_segments_poly_lines_data()

        # Pre-process the radii
        vmv.logger.info('Adjusting Radii')
        vmv.skeleton.update_poly_lines_radii(poly_lines=poly_lines_data, options=self.options)

        # Construct the final object and add it to the morphology
        vmv.logger.info('Drawing Polylines')
        self.morphology_skeleton = vmv.geometry.create_poly_lines_object_from_poly_lines_data(
            poly_lines_data, material=self.options.morphology.material, color_map=self.color_map,
            name=self.morphology_name, bevel_object=bevel_object)
        return self.morphology_skeleton

    ################################################################################################
    # @update_ui_minimum_and_maximum_values
    ################################################################################################
    def update_ui_minimum_and_maximum_values(self):
        """Updates the minimum and maximum values for the UI.
        """

        # Get the minimum and maximum values
        self.context.scene.VMV_MinimumValue = str(self.minimum_simulation_value)
        self.context.scene.VMV_MaximumValue = str(self.maximum_simulation_value)

    ################################################################################################
    # @identify_radius_simulation_dynamic_range
    ################################################################################################
    def identify_radius_simulation_dynamic_range(self):
        """Identifies the dynamic range of the radius simulation, or variation, data.
        """

        # Scan the entire simulation data to obtain the dynamic range
        for sample_simulation_list in self.morphology.radius_simulation_data:
            for value in sample_simulation_list:
                if value < self.minimum_simulation_value:
                    self.minimum_simulation_value = value
                if value > self.maximum_simulation_value:
                    self.maximum_simulation_value = value

        # Update the values
        self.update_ui_minimum_and_maximum_values()

    ################################################################################################
    # @identify_flow_simulation_dynamic_range
    ################################################################################################
    def identify_flow_simulation_dynamic_range(self):

        # Scan the entire simulation data to obtain the dynamic range
        for sample_simulation_list in self.morphology.flow_simulation_data:
            for value in sample_simulation_list:
                if value < self.minimum_simulation_value:
                    self.minimum_simulation_value = value
                if value > self.maximum_simulation_value:
                    self.maximum_simulation_value = value

        # Update the values
        self.update_ui_minimum_and_maximum_values()

    ################################################################################################
    # @identify_pressure_simulation_dynamic_range
    ################################################################################################
    def identify_pressure_simulation_dynamic_range(self):

        # Scan the entire simulation data to obtain the dynamic range
        for sample_simulation_list in self.morphology.pressure_simulation_data:
            for value in sample_simulation_list:
                if value < self.minimum_simulation_value:
                    self.minimum_simulation_value = value
                if value > self.maximum_simulation_value:
                    self.maximum_simulation_value = value

        # Update the values
        self.update_ui_minimum_and_maximum_values()

    ################################################################################################
    # @load_radius_simulation_data_at_step
    ################################################################################################
    def load_radius_simulation_data_at_step(self,
                                            time_step,
                                            context=None):
        """

        :param time_step:
        :return:
        """

        self.context = context

        segment_index = 0

        # For every section in the morphology
        for section in self.morphology.sections_list:

            # For every segment in the section
            for i_sample in range(len(section.samples) - 1):

                # The index
                radius_index = section.samples[i_sample].index

                # Get a reference to the radii
                radius_list = self.morphology.radius_simulation_data[radius_index - 1]

                # Get the segment polyline
                segment_polyline = self.morphology_skeleton.data.splines[segment_index]

                # Compute the material index
                color_index = vmv.utilities.get_index(
                    value=radius_list[time_step],
                    minimum_value=self.minimum_simulation_value,
                    maximum_value=self.maximum_simulation_value,
                    number_steps=self.options.morphology.color_map_resolution)

                if self.context is not None:
                    if radius_list[time_step] < float(self.context.scene.VMV_MinimumValue):
                        self.context.scene.VMV_MinimumValue = str(radius_list[time_step])

                    if radius_list[time_step] > float(self.context.scene.VMV_MaximumValue):
                        self.context.scene.VMV_MaximumValue = str(radius_list[time_step])

                # Get a reference to the material list of the morphology skeleton
                segment_polyline.material_index = color_index
                segment_polyline.keyframe_insert('material_index', frame=time_step)

                segment_index += 1

    ################################################################################################
    # @load_radius_simulation_data
    ################################################################################################
    def load_radius_simulation_data(self):
        """

        :return:
        """

        self.identify_radius_simulation_dynamic_range()

        # Add simulation data
        for time_step in range(0, len(self.morphology.radius_simulation_data[0])):
            self.load_radius_simulation_data_at_step(time_step=time_step)
