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
import copy
import math 

import vmv.geometry
import vmv.skeleton
import vmv.utilities


####################################################################################################
# @get_color_coded_segments_poly_lines_with_single_color
####################################################################################################
def get_color_coded_segments_poly_lines_with_single_color(section):
    """Gets a list of polylines for the segments in the section with a single color.

    :param section:
        Morphology section.
    :return:
        A list of polylines corresponding to the segments.
    """

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
# @get_color_coded_segments_poly_lines_with_alternating_colors
####################################################################################################
def get_color_coded_segments_poly_lines_with_alternating_colors(section):
    """Gets a list of polylines for the segments in the section with alternating colors.

    :param section:
        Morphology section.
    :return:
        A list of polylines corresponding to the segments.
    """

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
        section, minimum, maximum, color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):

    """Gets a list of all the segments composing the section color-coded based 
    on their radii in the morphology.

    :param section:     
        A given section to extract its segments from.
    :param minimum:
        The radius of the smallest sample in the morphology.
    :param maximum:
        The radius of the largest sample in the morphology.
    :param color_map_resolution:
        The resolution of the colormap.
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
# @get_color_coded_segments_poly_lines_based_on_length
####################################################################################################
def get_color_coded_segments_poly_lines_based_on_length(
        section, minimum, maximum, color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):
    """Gets a list of all the segments composing the section color-coded based 
    on their length in the morphology.

    :param section:     
        A given section to extract its segments from.
    :param minimum:
        The length of the shortest segment in the morphology. 
    :param maximum:
        The length of the longest segment in the morphology.
    :param color_map_resolution:
        The resolution of the colormap.
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
# @get_color_coded_segments_poly_lines_based_on_surface_area
####################################################################################################
def get_color_coded_segments_poly_lines_based_on_surface_area(
        section, minimum, maximum, color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):
    """Gets a list of all the segments composing the section color-coded based 
    on their surface area in the morphology.

    :param section:     
        A given section to extract its segments from.
    :param minimum:
        The area of the smallest segment in the morphology.
    :param maximum:
        The area of the biggest segment in the morphology.
    :param color_map_resolution:
        The resolution of the colormap.
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
def get_color_coded_segments_poly_lines_based_on_volume(
        section, minimum, maximum, color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):
    """Gets a list of all the segments composing the section color-coded based on their volume
    in the morphology.

    :param section:
        A given section to extract its segments from.
    :param minimum:
        The volume of the smallest segment in the morphology.
    :param maximum:
        The volume of the biggest segment in the morphology.
    :param color_map_resolution:
        The resolution of the colormap.
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
def get_color_coded_segments_poly_lines_based_on_index(
        morphology, section, minimum, maximum,
        color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):
    """Gets a list of all the segments composing the section color-coded based on their index
        in the morphology.

    :param morphology:
        A reference to the morphology being visualized.
    :param section:
        A given section to extract its segments from.
    :param minimum:
        The minimum segment index in the morphology.
    :param maximum:
        The maximum segment index in the morphology.
    :param color_map_resolution:
        The resolution of the colormap.
    :return:
        A list of segments represented by color-coded poly-lines.
    """

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


####################################################################################################
# @get_color_coded_segments_poly_lines_based_on_alignment
####################################################################################################
def get_color_coded_segments_poly_lines_based_on_alignment(section):
    """Gets a list of polylines of all the segments in the section color-coded based on their XYZ
    alignment.

    :param section:
        A given section.
    :return:
        A list of polylines.
    """

    def get_index(value):
        if 0 <= value < 0.25:
            return 0
        elif 0.25 <= value < 0.50:
            return 1
        elif 0.50 <= value < 0.75:
            return 2
        elif 0.50 <= value < 0.75:
            return 3
        else:
            return 4

    # A list of all the poly-lines that correspond to each segment in the morphology
    poly_lines = list()

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

        # Computes the direction of the vector and get tha absolute values of the angles
        direction = (point_2 - point_1).normalized()
        alpha = math.fabs(direction[0])
        beta = math.fabs(direction[1])
        gamma = math.fabs(direction[2])

        x_index = get_index(alpha)
        y_index = get_index(beta)
        z_index = get_index(gamma)

        color_index = z_index + 5 * (y_index + 5 * x_index)

        # Add the poly-line to the aggregate list
        poly_lines.append(vmv.skeleton.PolyLine(samples, color_index))

    # Return the list of polylines
    return poly_lines

