####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
from vmv.analysis import items


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
    return  segments_lengths


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


####################################################################################################
# @compute_total_morphology_length
####################################################################################################
def compute_total_morphology_length(sections_list):
    """Computes the total length of the morphology

    :param sections_list:
        A list of all the sections that compose the morphology.
    :return:
        The total length of the morphology.
    """

    # Morphology total length
    morphology_total_length = 0.0

    # Do it section by section
    for section in sections_list:

        # Compute section length
        section_length = compute_section_length(section=section)

        # Append the result to the total length
        morphology_total_length += section_length

    # Return the total length
    return morphology_total_length


####################################################################################################
# @compute_total_number_samples
####################################################################################################
def compute_total_number_samples(points_list):
    """Computes the total number of samples along the skeleton.

    :param points_list:
        A list of all the points (or samples) as read from the file.
    :return:
        The total number of samples in the morphology
    """

    # Simply return the length of the list
    return len(points_list)


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
# @analyze_samples_radii
####################################################################################################
def analyze_samples_radii(samples_list):
    """Analyse the distribution of the samples of the whole morphology

    :param samples_list:
        A list of all the samples of the morphology
    :return:
        Minimum, maximum and average samples radii.
    """

    # Compile a list of all the radii
    radii_list = list()
    for sample in samples_list:
        radii_list.append(sample[3])

    # Compute the minimum
    minimum_sample_radius = min(radii_list)

    # Compute the maximum
    maximum_sample_radius = max(radii_list)

    # Compute the average
    average_sample_radius = sum(radii_list) / (1.0 * len(radii_list))

    # Return the results
    return minimum_sample_radius, maximum_sample_radius, average_sample_radius


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
# @compute_number_of_loops
####################################################################################################
def compute_number_of_loops(sections_list):
    """Computes the number of loops in the morphology.

    :param sections_list:
        A give list of all the sections in the morphology.
    :return:
        Number of loops in the morphology.
    """

    # Number of loops in the morphology
    number_loops = 0

    # Iterate over all the sections and if you find any section with two parent, this as a loop
    for section in sections_list:

        if len(section.parents) > 1:
            number_loops += 1

    # Return the result
    return number_loops


####################################################################################################
# @compute_number_of_components
####################################################################################################
def compute_number_of_components(sections_list):
    """Computes the number of components of the morphology.

    :param sections_list:
        A give list of all the sections in the morphology.
    :return:
        The number of components in the morphology.
    """

    # Number of components
    number_components_in_morphology = 0

    # Iterate over all the sections and if you find any section with zero parents, increment
    for section in sections_list:

        if len(section.parents) == 0:
            number_components_in_morphology += 1

    # Return the result
    return number_components_in_morphology

####################################################################################################
# @analyze_morphology
####################################################################################################
def analyze_morphology():

    # Construct an object to store all the data
    analysis_items = items.AnalysisItems()

    # update the input to get an output
    pass
