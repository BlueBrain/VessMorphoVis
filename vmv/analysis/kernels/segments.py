####################################################################################################
# Copyright (c) 2019 - 2022, EPFL / Blue Brain Project
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
import pandas
import math


####################################################################################################
# @compute_segments_lengths
####################################################################################################
def compute_segments_lengths(section):
    """Computes the distribution of the lengths of the segments of a given section..

    :param section:
        A given section.
    :return:
        An array that contains the distribution of the lengths of all the segments
    """

    # A list of all the segments lengths
    segments_lengths = list()

    # Do it sample by sample
    for i in range(len(section.samples) - 1):

        # Get every two points along the section that make a segment
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point

        # Compute segment length
        segment_length = (p0 - p1).length

        # Append to the total length of the section
        segments_lengths.append(segment_length)

    # Return the array
    return segments_lengths


####################################################################################################
# @compute_segment_surface_area
####################################################################################################
def compute_segment_surface_area(sample_0,
                                 sample_1):

    p0 = sample_0.point
    p1 = sample_0.point
    r0 = sample_1.radius
    r1 = sample_1.radius

    # Compute the segment lateral area
    segment_length = (p0 - p1).length
    r_sum = r0 + r1
    r_diff = r0 - r1
    segment_lateral_area = math.pi * r_sum * math.sqrt((r_diff * r_diff) + segment_length)

    # Compute the segment surface area
    return segment_lateral_area + math.pi * ((r0 * r0) + (r1 * r1))


####################################################################################################
# @compute_segments_surface_areas
####################################################################################################
def compute_segments_surface_areas(section):
    """Computes a list of the surface areas of all the segments in the section.

    :param section:
        A given section to compute the surface area of its segments.
    :return
        A list to collect the resulting data.
    """

    segments_surface_areas = list()

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return segments_surface_areas

    # Integrate the surface area between each two successive samples
    for i in range(len(section.samples) - 1):

        # Compute the segment surface area and append it list
        segments_surface_areas.append(compute_segment_surface_area(
            section.samples[i], section.samples[i + 1]))

    # Return the segments surface area
    return segments_surface_areas


####################################################################################################
# @compute_segment_volume
####################################################################################################
def compute_segment_volume(sample_0,
                           sample_1):
    # Retrieve the data of the samples along each segment on the section
    p0 = sample_0.point
    p1 = sample_1.point
    r0 = sample_0.radius
    r1 = sample_1.radius

    # Compute the segment volume
    return (1.0 / 3.0) * math.pi * (p0 - p1).length * (r0 * r0 + r0 * r1 + r1 * r1)


####################################################################################################
# @compute_segments_volumes
####################################################################################################
def compute_segments_volumes(section):
    """Computes the volume of a section from its segments.

    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its volume.
    :return :
        A list to collect the resulting data.
    """

    segments_volumes = list()

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return segments_volumes

    # Integrate the volume between each two successive samples
    for i in range(len(section.samples) - 1):

        # Append to the list
        segments_volumes.append(compute_segment_volume(
            sample_0=section.samples[i], sample_1=section.samples[i + 1]))

    # Return the data
    return segments_volumes


####################################################################################################
# @compute_sample_radius_distribution_along_axes
####################################################################################################
def compute_segment_length_distribution_along_axes(morphology_object):
    """Computes a dataframe of the XYZ coordinates w.r.t to the lengths of the segments.

    :param morphology_object:
        A give morphology object.
    :return:
        Data frame containing the ['Length' 'X' 'Y' 'Z'] elements.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        for i in range(len(i_section.samples) - 1):
            sample_0 = i_section.samples[i]
            sample_1 = i_section.samples[i + 1]
            length = (sample_1.point - sample_0.point).length
            position = (sample_1.point + sample_0.point) * 0.5
            data.append([length, position[0], position[1], position[2]])

    # Construct the data frame and return it
    return pandas.DataFrame(data, columns=['Length', 'X', 'Y', 'Z'])


####################################################################################################
# @compute_segment_surface_area_distribution_along_axes
####################################################################################################
def compute_segment_surface_area_distribution_along_axes(morphology_object):
    """Computes a dataframe of the XYZ coordinates w.r.t to the surface areas of the segments.

    :param morphology_object:
        A give morphology object.
    :return:
        Data frame containing the ['Area' 'X' 'Y' 'Z'] elements.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        for i in range(len(i_section.samples) - 1):
            sample_0 = i_section.samples[i]
            sample_1 = i_section.samples[i + 1]
            position = (sample_1.point + sample_0.point) * 0.5
            data.append([compute_segment_surface_area(sample_0=sample_0, sample_1=sample_1),
                         position[0], position[1], position[2]])

    # Construct the data frame and return it
    return pandas.DataFrame(data, columns=['Area', 'X', 'Y', 'Z'])


####################################################################################################
# @compute_segment_volume_distribution_along_axes
####################################################################################################
def compute_segment_volume_distribution_along_axes(morphology_object):
    """Computes a dataframe of the XYZ coordinates w.r.t to the volumes of the segments.

    :param morphology_object:
        A give morphology object.
    :return:
        Data frame containing the ['Volume' 'X' 'Y' 'Z'] elements.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        for i in range(len(i_section.samples) - 1):
            sample_0 = i_section.samples[i]
            sample_1 = i_section.samples[i + 1]
            position = (sample_1.point + sample_0.point) * 0.5
            data.append([compute_segment_volume(sample_0=sample_0, sample_1=sample_1),
                         position[0], position[1], position[2]])

    # Construct the data frame and return it
    return pandas.DataFrame(data, columns=['Volume', 'X', 'Y', 'Z'])


####################################################################################################
# @compute_segments_length_distributions
####################################################################################################
def compute_segments_length_distributions(morphology_object):
    """Computes the distribution of the lengths of the segments in the morphology.

    :param morphology_object:
        Input morphology.
    :return:
        A list containing the data.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        for i in range(len(i_section.samples) - 1):
            length = (i_section.samples[i].point - i_section.samples[i + 1].point).length
            data.append(length)
    return data


####################################################################################################
# @compute_segments_surface_area_distribution
####################################################################################################
def compute_segments_surface_area_distribution(morphology_object):
    """Computes the distribution of the surface areas of the segments in the morphology.

    :param morphology_object:
        Input morphology.
    :return:
        A list containing the data.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        data.extend(compute_segments_surface_areas(section=i_section))
    return data


####################################################################################################
# @compute_segments_volumes_distribution
####################################################################################################
def compute_segments_volume_distribution(morphology_object):
    """Computes the distribution of the volumes of the segments in the morphology.

    :param morphology_object:
        Input morphology.
    :return:
        A list containing the data.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        data.extend(compute_segments_volumes(section=i_section))
    return data


####################################################################################################
# @analyze_segments_length
####################################################################################################
def analyze_segments_length(sections_list):
    """Analyse the distribution of the length of the segments across the morphology.

    :param sections_list:
        A list of all the sections of the morphology.
    :return:
        Minimum, maximum and average lengths of the segments.
    """

    # A list of the lengths of all the segments in the morphology
    segments_lengths = list()

    # Do it section by section
    for section in sections_list:

        # Compute the lengths of the segments of a specific section
        section_segments_length = compute_segments_lengths(section=section)

        # Append the result to the total length
        segments_lengths.extend(section_segments_length)

    # Compute the minimum
    minimum_segment_length = min(segments_lengths)

    # Compute the maximum
    maximum_segment_length = max(segments_lengths)

    # Compute the average
    average_segment_length = sum(segments_lengths) / (1.0 * len(segments_lengths))

    # Return the results
    return minimum_segment_length, maximum_segment_length, average_segment_length


####################################################################################################
# @analyze_segments_alignment_length
####################################################################################################
def analyze_segments_alignment_length(sections_list):

    total_segment_length_x = 0.0
    total_segment_length_y = 0.0
    total_segment_length_z = 0.0

    # Do it per section in the morphology
    for i_section in sections_list:

        # Construct the section from all the samples
        for i_sample in range(len(i_section.samples) - 1):

            # First sample
            point_1 = i_section.samples[i_sample].point
            radius_1 = i_section.samples[i_sample].radius

            # Second sample
            point_2 = i_section.samples[i_sample + 1].point
            radius_2 = i_section.samples[i_sample + 1].radius

            # Computes the direction of the vector and get tha absolute values of the angles
            direction = (point_2 - point_1).normalized()
            alpha = math.fabs(direction[0])
            beta = math.fabs(direction[1])
            gamma = math.fabs(direction[2])

            if alpha > beta and alpha > gamma:
                total_segment_length_x += (point_2 - point_1).length
            elif beta > alpha and beta > gamma:
                total_segment_length_y += (point_2 - point_1).length
            elif gamma > alpha and gamma > beta:
                total_segment_length_z += (point_2 - point_1).length
            else:
                print('Analysis issue %f %f %f' % (alpha, beta, gamma))

    # Return the results
    return total_segment_length_x, total_segment_length_y, total_segment_length_z