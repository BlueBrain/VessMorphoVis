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
import math
import pandas

# Internal imports
import vmv.utilities
from vmv.consts import Keys


####################################################################################################
# @SectionStatsResult
####################################################################################################
class SectionStatsResult:
    """

    """
    def __init__(self, total=0.0, minimum_value=0.0, mean_value=0.0, maximum_value=0.0, ratio=0.0):
        self.total = total
        self.min = minimum_value
        self.mean = mean_value
        self.max = maximum_value
        self.ratio = ratio


####################################################################################################
# @compute_section_length
####################################################################################################
def compute_section_length(section):
    """Computes the total length of the section.

    :param section:
        A given section.
    :return:
        The length of the section
    """

    # Section total length
    section_length = 0.0

    # Do it sample by sample
    for i in range(len(section.samples) - 1):

        # Get every two points along the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point

        # Compute segment length
        segment_length = (p0 - p1).length

        # Append to the total length of the section
        section_length += segment_length

    # Return the section length
    return section_length


def compute_section_center_point(section):

    # If the section has a single sample
    if len(section.samples) == 1:
        return section.samples[0].point

    # If the section has two samples
    if len(section.samples) == 2:
        return (section.samples[0].point + section.samples[1].point) * 0.5

    # Note: If the section has more than two samples, the logic becomes more complex
    # Compute the section half-length
    section_half_length = compute_section_length(section=section) * 0.5

    # Keeps track on the section length
    current_length = 0
    for i in range(len(section.samples) - 1):

        # Get every two points along the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point

        # If the current length is less than half the path length
        if current_length < section_half_length:

            # Compute segment length and update the current length
            current_length += (p0 - p1).length

        # If the current length becomes larger than half the path length
        if current_length >= section_half_length:

            # Compute the difference
            difference = current_length - section_half_length

            # Compute the direction
            direction = (p1 - p0).normalized()

            # Return the computed point
            return p1 - (difference * direction)


####################################################################################################
# @compute_section_average_radius
####################################################################################################
def compute_section_average_radius(section):

    average_radius = 0
    for i_sample in section.samples:
        average_radius += i_sample.radius
    return average_radius / len(section.samples)


####################################################################################################
# @is_short_sections
####################################################################################################
def is_short_section(section):
    """Analyze the short sections, which have their length shorter than the sum of their
    initial and final diameters.

    :param section:
        A given section to get analyzed.
    """

    # Only applies if the section has more than two samples
    if len(section.samples) > 1:

        # Compute the sum of the diameters of the first and last samples
        diameters_sum = (section.samples[0].radius + section.samples[-1].radius) * 2

        # Compute section length
        section_length = compute_section_length(section=section)

        # If the sum is smaller than the section length, then report it as an issue
        if section_length < diameters_sum:
            return True

        # Not a short section
        return False

    # Default
    return False


####################################################################################################
# @compute_number_of_short_sections
####################################################################################################
def compute_number_of_short_sections(sections_list):
    """Computes the number of short sections in the morphology

    :param sections_list:
        A list of all the sections that compose the morphology.
    :return:
        The number of short sections in the morphology.
    """

    # Number of short sections in the morphology
    number_short_sections = 0

    # Do it section by section
    for section in sections_list:

        # Check
        if is_short_section(section):
            number_short_sections += 1

    # Return the total number of short sections
    return number_short_sections


####################################################################################################
# @compute_number_of_sections_with_two_samples
####################################################################################################
def compute_number_of_sections_with_two_samples(sections_list):
    """Computes the number of sections with two samples only.

    :param sections_list:
        A given list of all the sections in the morphology
    :return:
    """

    # Number of sections with two samples only
    number_section_with_two_samples = 0

    # Do it section by section
    for section in sections_list:

        # If the section has only two samples, increment
        if len(section.samples) == 2:
            number_section_with_two_samples += 1

    # Return the result
    return number_section_with_two_samples


####################################################################################################
# @compute_total_number_sections
####################################################################################################
def compute_total_number_sections(sections_list):
    """Computes the total number of sections along the skeleton.

    :param sections_list:
        A list of all the sections as parsed from the file.
    :return:
        The total number of sections in the morphology
    """

    # Simply return the length of the list
    return len(sections_list)


####################################################################################################
# @compute_section_surface_area
####################################################################################################
def compute_section_surface_area(section):
    """Computes the surface area of a section from its segments.
    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its surface area.
    :return:
        Section total surface area in square microns.
    """

    # Section surface area
    section_surface_area = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_surface_area

    # Integrate the surface area between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment lateral area
        segment_length = (p0 - p1).length
        r_sum = r0 + r1
        r_diff = r0 - r1
        segment_lateral_area = math.pi * r_sum * math.sqrt((r_diff * r_diff) + segment_length)

        # Compute the segment surface area and append it to the total section surface area
        section_surface_area += segment_lateral_area + math.pi * ((r0 * r0) + (r1 * r1))

    # Return the section surface area
    return section_surface_area


####################################################################################################
# @compute_section_volume
####################################################################################################
def compute_section_volume(section):
    """Computes the volume of a section from its segments.
class SectionStatsResult:

    def __init__(self, total=0.0, minimum_value=0.0, mean_value=0.0, maximum_value=0.0, ratio=0.0):
        self.total = total
        self.min = minimum_value
        self.mean = mean_value
        self.max = maximum_value
        self.ratio = ratio
    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its volume.
    :return:
        Section total volume in cube microns.
    """

    # Section volume
    section_volume = 0.0

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:

        # Return 0
        return section_volume

    # Integrate the volume between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment volume and append to the total section volume
        section_volume += (1.0 / 3.0) * math.pi * (p0 - p1).length * (r0 * r0 + r0 * r1 + r1 * r1)

    # Return the section volume
    return section_volume









####################################################################################################
# @compute_sections_length_distributions
####################################################################################################
def compute_sections_length_distributions(morphology_object):
    """Computes the distribution of the lengths of the sections in the morphology.

    :param morphology_object:
        Input morphology.
    :return:
        A list containing the data.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        data.append(vmv.analysis.compute_section_length(i_section))
    return data


####################################################################################################
# @compute_sections_average_radius_distributions
####################################################################################################
def compute_sections_average_radius_distributions(morphology_object):
    """Computes the distribution of the average radius of the sections in the morphology.

    :param morphology_object:
        Input morphology.
    :return:
        A list containing the data.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        data.append(vmv.analysis.compute_section_average_radius(i_section))
    return data


####################################################################################################
# @compute_sections_surface_area_distribution
####################################################################################################
def compute_sections_surface_area_distribution(morphology_object):
    """Computes the distribution of the surface areas of the sections in the morphology.

    :param morphology_object:
        Input morphology.
    :return:
        A list containing the data.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        data.append(vmv.analysis.compute_section_surface_area(i_section))
    return data


####################################################################################################
# @compute_sections_volume_distribution
####################################################################################################
def compute_sections_volume_distribution(morphology_object):
    """Computes the distribution of the volumes of the sections in the morphology.

    :param morphology_object:
        Input morphology.
    :return:
        A list containing the data.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        data.append(vmv.analysis.compute_section_volume(i_section))
    return data


####################################################################################################
# @analyze_sections_length
####################################################################################################
def analyze_sections_length(sections_list):
    """Analyse the distribution of the length of the sections across the morphology.

    :param sections_list:
        A list of all the sections of the morphology.
    :return:
        Minimum, maximum and average lengths of the sections.
    """

    # A list of the lengths of all the sections in the morphology
    sections_lengths = list()

    # Do it section by section
    for section in sections_list:

        # Compute section length
        section_length = compute_section_length(section=section)

        # Append the result to the total length
        sections_lengths.append(section_length)

    # Compute the minimum
    minimum_section_length = min(sections_lengths)

    # Compute the maximum
    maximum_section_length = max(sections_lengths)

    # Compute the average
    average_section_length = sum(sections_lengths) / (1.0 * len(sections_lengths))

    # Return the results
    return minimum_section_length, maximum_section_length, average_section_length



####################################################################################################
# @compute_section_length_data
####################################################################################################
def compute_section_length_data(section):

    # A container for the data that will be computed
    result = SectionStatsResult()

    # If the section has less than two samples, then return
    if len(section.samples) < 2:
        return result

    # Compute the surface area of each segment and add it to the list
    segments_lengths = list()
    for i in range(len(section.samples) - 1):
        # Get every two points along the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point

        # Compute segment length
        segment_length = (p0 - p1).length
        segments_lengths.append(segment_length)

    result.total = sum(segments_lengths)
    result.min = min(segments_lengths)
    result.mean = result.total / len(section.samples)
    result.max = max(segments_lengths)
    result.ratio = result.min / result.max if result.max > 0 else 0

    # Return the statistics
    return result


####################################################################################################
# @compute_section_surface_area_data
####################################################################################################
def compute_section_surface_area_data(section):
    """Computes the surface area of a section from its segments.
    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its surface area.
    :return:
        Section total surface area in square microns.
    """

    # A container for the data that will be computed
    result = SectionStatsResult()

    # If the section has less than two samples, then return
    if len(section.samples) < 2:
        return result

    # Compute the surface area of each segment and add it to the list
    segments_surface_areas = list()
    for i in range(len(section.samples) - 1):
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment lateral area
        segment_length = (p0 - p1).length
        r_sum = r0 + r1
        r_diff = r0 - r1
        segment_lateral_area = math.pi * r_sum * math.sqrt((r_diff * r_diff) + segment_length)
        segment_surface_area = segment_lateral_area + math.pi * ((r0 * r0) + (r1 * r1))
        segments_surface_areas.append(segment_surface_area)

    result.total = sum(segments_surface_areas)
    result.min = min(segments_surface_areas)
    result.mean = result.total / len(section.samples)
    result.max = max(segments_surface_areas)
    result.ratio = result.min / result.max if result.max > 0 else 0

    # Return the statistics
    return result


####################################################################################################
# @compute_section_volume_data
####################################################################################################
def compute_section_volume_data(section):
    """Computes the volume of a section from its segments.

    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its volume.
    :return:
        Section total volume in cube microns.
    """

    # A container for the data that will be computed
    result = SectionStatsResult()

    # If the section has less than two samples, then return
    if len(section.samples) < 2:
        return result

    # Compute the volume of each segment and add it to the list
    segments_volume = list()
    for i in range(len(section.samples) - 1):
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius
        segment_volume = (1.0 / 3.0) * math.pi * (p0 - p1).length * (r0 * r0 + r0 * r1 + r1 * r1)
        segments_volume.append(segment_volume)

    result.total = sum(segments_volume)
    result.min = min(segments_volume)
    result.mean = result.total / len(section.samples)
    result.max = max(segments_volume)
    result.ratio = result.min / result.max if result.max > 0 else 0

    # Return the statistics
    return result


####################################################################################################
# @perform_length_analysis
####################################################################################################
def perform_length_analysis(sections,
                            sections_centers=None):

    data = list()
    for i_section, section in enumerate(sections):

        # Get the section center, do NOT recalculate if provided
        section_center = compute_section_center_point(section) if sections_centers is None else \
            sections_centers[i_section]

        # Compute the sum of the radii of the first and last samples
        radius_sum = section.samples[0].radius + section.samples[-1].radius

        # Compute the result
        result = compute_section_length_data(section)
        data.append([section.index,
                     section_center[0],
                     section_center[1],
                     section_center[2],
                     result.total,
                     result.min,
                     result.mean,
                     result.max,
                     result.ratio,
                     radius_sum / result.total,
                     len(section.samples) / result.total if result.total > 0 else 0])

    # Construct the data frame
    return pandas.DataFrame(data, columns=[Keys.SECTION_INDEX,
                                           Keys.X, Keys.Y, Keys.Z,
                                           Keys.SECTION_LENGTH,
                                           Keys.SEGMENT_MIN_LENGTH,
                                           Keys.SEGMENT_MEAN_LENGTH,
                                           Keys.SEGMENT_MAX_LENGTH,
                                           Keys.SEGMENT_LENGTH_RATIO,
                                           Keys.SECTION_THICKNESS_TO_LENGTH_RATIO,
                                           Keys.SECTION_SAMPLING_DENSITY])


####################################################################################################
# @perform_surface_area_analysis
####################################################################################################
def perform_surface_area_analysis(sections,
                                  sections_centers=None):

    data = list()
    for i_section, section in enumerate(sections):

        # Get the section center, do NOT recalculate if provided
        section_center = compute_section_center_point(section) if sections_centers is None else \
            sections_centers[i_section]

        # Compute the result
        result = compute_section_surface_area_data(section)
        data.append([section.index,
                     section_center[0],
                     section_center[1],
                     section_center[2],
                     result.total,
                     result.min,
                     result.mean,
                     result.max,
                     result.ratio])

    # Construct the data frame
    return pandas.DataFrame(data, columns=[Keys.SECTION_INDEX,
                                           Keys.X, Keys.Y, Keys.Z,
                                           Keys.SECTION_SURFACE_AREA,
                                           Keys.SEGMENT_MIN_SURFACE_AREA,
                                           Keys.SEGMENT_MEAN_SURFACE_AREA,
                                           Keys.SEGMENT_MAX_SURFACE_AREA,
                                           Keys.SEGMENT_SURFACE_AREA_RATIO])




####################################################################################################
# @perform_volume_analysis
####################################################################################################
def perform_volume_analysis(sections,
                            sections_centers=None):
    data = list()
    for i_section, section in enumerate(sections):

        # Get the section center, do NOT recalculate if provided
        section_center = compute_section_center_point(section) if sections_centers is None else \
            sections_centers[i_section]

        # Compute the result
        result = compute_section_volume_data(section)
        data.append([section.index,
                     section_center[0],
                     section_center[1],
                     section_center[2],
                     result.total,
                     result.min,
                     result.mean,
                     result.max,
                     result.ratio])

    # Construct the data frame
    return pandas.DataFrame(data, columns=[Keys.SECTION_INDEX,
                                           Keys.X, Keys.Y, Keys.Z,
                                           Keys.SECTION_VOLUME,
                                           Keys.SEGMENT_MIN_VOLUME,
                                           Keys.SEGMENT_MEAN_VOLUME,
                                           Keys.SEGMENT_MAX_VOLUME,
                                           Keys.SEGMENT_VOLUME_RATIO])
