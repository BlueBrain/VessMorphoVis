

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

# System imports
import copy
import math 

import vmv.geometry
import vmv.skeleton
import vmv.utilities


####################################################################################################
# @get_segments_poly_lines
####################################################################################################
def get_color_coded_segments_poly_lines_with_single_color(section):

    # A list of all the poly-lines that correspond to each segment in the morphology
    poly_lines = list()

    # Construct the section from all the samples
    for i in range(len(section.samples) - 1):

        # Segment poly-line
        samples = list()

        # First sample
        point = section.samples[i].point
        radius = section.samples[i].radius
        samples.append([(point[0], point[1], point[2], 1), radius])

        # Second sample
        point = section.samples[i + 1].point
        radius = section.samples[i + 1].radius
        samples.append([(point[0], point[1], point[2], 1), radius])

        # Add the poly-line to the aggregate list
        poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=0))

    return poly_lines


####################################################################################################
# @get_segments_poly_lines
####################################################################################################
def get_color_coded_segments_poly_lines_with_alternating_colors(section):

    # A list of all the poly-lines that correspond to each segment in the morphology
    poly_lines = list()

    # Construct the section from all the samples
    for i in range(len(section.samples) - 1):

        # Segment poly-line
        samples = list()

        # First sample
        point = section.samples[i].point
        radius = section.samples[i].radius
        samples.append([(point[0], point[1], point[2], 1), radius])

        # Second sample
        point = section.samples[i + 1].point
        radius = section.samples[i + 1].radius
        samples.append([(point[0], point[1], point[2], 1), radius])

        # Add the poly-line to the aggregate list
        poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=i % 2))

    return poly_lines


####################################################################################################
# @get_color_coded_segments_poly_lines_based_on_radius
####################################################################################################
def get_color_coded_segments_poly_lines_based_on_radius(
        section, minimum, maximum,
        color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):
    """Gets a list of all the segments composing the section color-coded based 
    on their radii in the morphology.

    :param section:     
        A given section to extract its segments from.
    :param minimum:
        The radius of the smaller sample in the morphology. 
    :param maximum: [description]
        The radius of the larger sample in the morphology.
    :return:
        A list of segments represented by color-coded poly-lines. 
    """

    # A list of all the poly-lines that correspond to each segment in the morphology
    poly_lines = list()

    # Construct the section from all the samples
    for i in range(len(section.samples) - 1):

        # Segment poly-line
        samples = list()

        # Initialize the average radius to zero 
        average_radius = 0

        # First sample
        point = section.samples[i].point
        radius = section.samples[i].radius
        samples.append([(point[0], point[1], point[2], 1), radius])

        # Add the value of the first sample radius
        average_radius += radius

        # Second sample
        point = section.samples[i + 1].point
        radius = section.samples[i + 1].radius
        samples.append([(point[0], point[1], point[2], 1), radius])

        # Add the value of the second sample radius 
        average_radius += radius

        # Get the average radius 
        average_radius *= 0.5

        # Poly-line color index (we use two colors to highlight the segment)
        color_index = vmv.utilities.get_index(value=average_radius,
                                              minimum_value=minimum,
                                              maximum_value=maximum,
                                              number_steps=color_map_resolution)

        # Add the poly-line to the aggregate list
        poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=color_index))

    # Return the list of polylines 
    return poly_lines


####################################################################################################
# @get_color_coded_segments_poly_lines_based_on_radius
####################################################################################################
def get_color_coded_segments_poly_lines_based_on_length(section, 
                                                        minimum, 
                                                        maximum,
    color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):
    """Gets a list of all the segments composing the section color-coded based 
    on their length in the morphology.

    :param section:     
        A given section to extract its segments from.
    :param minimum_length:  
        The length of the shortest segment in the morphology. 
    :param maximum_length: [description]
        The length of the longest segment in the morphology.
    :return:
        A list of segments represented by color-coded poly-lines. 
    """

    # A list of all the poly-lines that correspond to each segment in the morphology
    poly_lines = list()

    # Construct the section from all the samples
    for i in range(len(section.samples) - 1):

        # Segment poly-line
        samples = list()

        # First sample
        point_1 = section.samples[i].point
        radius_1 = section.samples[i].radius
        samples.append([(point_1[0], point_1[1], point_1[2], 1), radius_1])

        # Second sample
        point_2 = section.samples[i + 1].point
        radius_2 = section.samples[i + 1].radius
        samples.append([(point_2[0], point_2[1], point_2[2], 1), radius_2])

        # Segment length 
        segment_length = (point_1 - point_2).length

        # Poly-line color index (we use two colors to highlight the segment)
        color_index = vmv.utilities.get_index(value=segment_length,
                                              minimum_value=minimum,
                                              maximum_value=maximum,
                                              number_steps=color_map_resolution)

        # Add the poly-line to the aggregate list
        poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=color_index))

    # Return the list of polylines 
    return poly_lines


####################################################################################################
# @get_color_coded_segments_poly_lines_based_on_radius
####################################################################################################
def get_color_coded_segments_poly_lines_based_on_surface_area(section, 
                                                              minimum, 
                                                              maximum,
    color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):
    """Gets a list of all the segments composing the section color-coded based 
    on their length in the morphology.

    :param section:     
        A given section to extract its segments from.
    :param minimum_length:  
        The length of the shortest segment in the morphology. 
    :param maximum_length: [description]
        The length of the longest segment in the morphology.
    :return:
        A list of segments represented by color-coded poly-lines. 
    """

    # A list of all the poly-lines that correspond to each segment in the morphology
    poly_lines = list()

    # Construct the section from all the samples
    for i in range(len(section.samples) - 1):

        # Segment poly-line
        samples = list()

        # First sample
        point_1 = section.samples[i].point
        radius_1 = section.samples[i].radius
        samples.append([(point_1[0], point_1[1], point_1[2], 1), radius_1])

        # Second sample
        point_2 = section.samples[i + 1].point
        radius_2 = section.samples[i + 1].radius
        samples.append([(point_2[0], point_2[1], point_2[2], 1), radius_2])

        # Surface area 
        segment_surface_area = vmv.skeleton.compute_segment_surface_area(
            section.samples[i], section.samples[i + 1])

        # Poly-line color index (we use two colors to highlight the segment)
        color_index = vmv.utilities.get_index(value=segment_surface_area,
                                              minimum_value=minimum,
                                              maximum_value=maximum,
                                              number_steps=color_map_resolution)

        # Add the poly-line to the aggregate list
        poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=color_index))

    # Return the list of polylines 
    return poly_lines


####################################################################################################
# @get_color_coded_segments_poly_lines_based_on_radius
####################################################################################################
def get_color_coded_segments_poly_lines_based_on_volume(section, 
                                                        minimum, 
                                                        maximum,
    color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):

    # A list of all the poly-lines that correspond to each segment in the morphology
    poly_lines = list()

    # Construct the section from all the samples
    for i in range(len(section.samples) - 1):

        # Segment poly-line
        samples = list()

        # First sample
        point_1 = section.samples[i].point
        radius_1 = section.samples[i].radius
        samples.append([(point_1[0], point_1[1], point_1[2], 1), radius_1])

        # Second sample
        point_2 = section.samples[i + 1].point
        radius_2 = section.samples[i + 1].radius
        samples.append([(point_2[0], point_2[1], point_2[2], 1), radius_2])

        # Volume
        segment_volume = vmv.skeleton.compute_segment_volume(
            section.samples[i], section.samples[i + 1])

        # Poly-line color index (we use two colors to highlight the segment)
        color_index = vmv.utilities.get_index(value=segment_volume,
                                              minimum_value=minimum,
                                              maximum_value=maximum,
                                              number_steps=color_map_resolution)

        # Add the poly-line to the aggregate list
        poly_lines.append(vmv.skeleton.PolyLine(samples, color_index))

    # Return the list of polylines 
    return poly_lines


####################################################################################################
# @get_color_coded_segments_poly_lines_based_on_index
####################################################################################################
def get_color_coded_segments_poly_lines_based_on_index(morphology,
                                                       section,
                                                       minimum,
                                                       maximum,
    color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):

    # A list of all the poly-lines that correspond to each segment in the morphology
    poly_lines = list()

    # Compute the first segment index based on the section index in the morphology
    first_segment_index = 0
    for i_section in range(0, section.index):
        first_segment_index += len(morphology.sections_list[i_section].samples)

    # Construct the section from all the samples
    for i_sample in range(len(section.samples) - 1):

        # Segment poly-line
        samples = list()

        # First sample
        point_1 = section.samples[i_sample].point
        radius_1 = section.samples[i_sample].radius
        samples.append([(point_1[0], point_1[1], point_1[2], 1), radius_1])

        # Second sample
        point_2 = section.samples[i_sample + 1].point
        radius_2 = section.samples[i_sample + 1].radius
        samples.append([(point_2[0], point_2[1], point_2[2], 1), radius_2])

        # Compute the current segment index
        segment_index = first_segment_index + i_sample

        # Poly-line color index (we use two colors to highlight the segment)
        color_index = vmv.utilities.get_index(value=segment_index,
                                              minimum_value=minimum,
                                              maximum_value=maximum,
                                              number_steps=color_map_resolution)

        # Add the poly-line to the aggregate list
        poly_lines.append(vmv.skeleton.PolyLine(samples, color_index))

    # Return the list of polylines
    return poly_lines