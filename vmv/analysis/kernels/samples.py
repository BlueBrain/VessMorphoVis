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

import vmv


def compute_samples_density(morphology):

    data = list()

    # For every section
    for section in morphology.sections_list:

        # For every sample
        for sample in section.samples:

            # Append the data
            data.append([sample.radius, sample.point[0], sample.point[1], sample.point[2]])

    # Create and return the data frame
    return pandas.DataFrame(data, columns=['Radius', 'X', 'Y', 'Z'])


####################################################################################################
# @compute_total_of_number_samples_from_sections_list
####################################################################################################
def compute_total_of_number_samples_from_sections_list(sections_list):
    """Computes the total number of samples along the skeleton including the duplicate samples
    along the branching points.

    :param sections_list:
        A list of all the sections that are processed after loading the morphology.
    :return:
        The total number of samples in the morphology from the sections including the duplicate
        samples along the branching points.
    """

    # Morphology total number of samples
    morphology_total_number_of_samples = 0

    # Do it section by section
    for section in sections_list:

        # Compute section length
        number_of_samples_in_section = compute_number_of_samples_in_section(section=section)

        # Append the result to the total
        morphology_total_number_of_samples += number_of_samples_in_section

    # Return the total length
    return morphology_total_number_of_samples


####################################################################################################
# @compute_number_of_samples_in_section
####################################################################################################
def compute_number_of_samples_in_section(section):
    """Returns the current number of samples in a given section.

    :param section:
        A given section to compute its number of samples.
    :return:
        The current number of samples in a given section.
    """

    # Returns the number of samples in the sections
    return len(section.samples)


####################################################################################################
# @compute_section_radius_ratio
####################################################################################################
def compute_section_radius_ratio(section):
    """Computes the ratio between the minimum sample radius to the maximum sample radius.

    :param section:
        A given section for analysis.
    :return:
        Radius Ratio = Minimum Sample Radius / Maximum Sample Radius
        If the Maximum Sample Radius is zero, the result is zero.
    :rtype:
    """

    # Initialize
    min_sample_radius = 1e32
    max_sample_radius = -1e32

    # Comparisons
    for sample in section.samples:
        if sample.radius < min_sample_radius:
            min_sample_radius = sample.radius
        if sample.radius > max_sample_radius:
            max_sample_radius = sample.radius

    # If the maximum sample radius is zero, then return 0
    if max_sample_radius < 1e-32:
        return 0
    # Otherwise, return the actual ratio
    else:
        return min_sample_radius / max_sample_radius


####################################################################################################
# @compute_number_of_samples_per_section_distribution
####################################################################################################
def compute_number_of_samples_per_section_distribution(morphology_object):
    """Computes the distribution of the number of samples per section along the morphology.

    :param morphology_object:
        A give morphology object.
    :return:
        A list containing the number of samples in all the sections.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        data.append(len(i_section.samples))
    return data


def compute_number_of_samples_per_section_distribution_(morphology_object):
    """Computes the distribution of the number of samples per section along the morphology.

    :param morphology_object:
        A give morphology object.
    :return:
        A list containing the number of samples in all the sections.
    """

    data = list()
    for i, i_section in enumerate(morphology_object.sections_list):
        data.append([i, len(i_section.samples)])
    return pandas.DataFrame(data, columns=['Section Index', 'Number Samples'])


####################################################################################################
# @compute_sample_radius_distribution
####################################################################################################
def compute_sample_radius_distribution(morphology_object):
    """Computes the distribution of the samples' radii along the morphology.

    :param morphology_object:
        A give morphology object.
    :return:
        List of all the radii.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        for i_sample in i_section.samples:
            data.append(i_sample.radius)
    return data


####################################################################################################
# @compute_sample_radius_distribution_along_axes
####################################################################################################
def compute_sample_radius_distribution_along_axes(morphology_object):
    """Computes a dataframe of the XYZ coordinates including the radii of the samples in the entire
    morphology.

    :param morphology_object:
        A give morphology object.
    :return:
        Data frame containing the ['Radius' 'X' 'Y' 'Z'] elements.
    """

    data = list()
    for i_section in morphology_object.sections_list:
        for i_sample in i_section.samples:
            position = i_sample.point
            data.append([i_sample.radius, position[0], position[1], position[2]])

    # Construct the data frame and return it
    return pandas.DataFrame(data, columns=['Radius', 'X', 'Y', 'Z'])


def compute_section_radius_ratio_distribution(morphology_object):
    data = list()
    for i, section in enumerate(morphology_object.sections_list):
        data.append([i, compute_section_radius_ratio(section=section)])
    return pandas.DataFrame(data, columns=['Section Index', 'Radius Ratio'])


def compute_section_radius_distribution(morphology_object):

    data = list()
    for i_section, section in enumerate(morphology_object.sections_list):
        average_sample_radius = 0
        minimum_sample_radius = 1e32
        maximum_sample_radius = -1e32

        for i_sample in section.samples:
            average_sample_radius += i_sample.radius
            if i_sample.radius < minimum_sample_radius:
                minimum_sample_radius = i_sample.radius
            if i_sample.radius > maximum_sample_radius:
                maximum_sample_radius = i_sample.radius

        average_sample_radius /= len(section.samples)

        data.append([section.index, average_sample_radius, minimum_sample_radius, maximum_sample_radius])

    return pandas.DataFrame(data, columns=['Section Index',
                                           'Mean Sample Radius',
                                           'Min. Sample Radius',
                                           'Max. Sample Radius'])


####################################################################################################
# @analyze_samples_with_zero_radii
####################################################################################################
def analyze_samples_with_zero_radii(radii_list, epsilon=1e-3):
    """Count the number of samples that have zero-radii.

    :param radii_list:
        A list of all the radii of the morphology.
    :param epsilon:
        Very small value that is close to zero, it is user defined and by default any sample that
        has a radius less than this value is an error.
    :return:
        The total number of samples with zero-radii.
    """

    # Initially zero
    zero_radii_samples = 0

    # Iterate over all the samples and detect
    for radius in radii_list:

        # If smaller than epsilon
        if radius < epsilon:

            # Increment
            zero_radii_samples += 1

    # Return the final value
    return zero_radii_samples


####################################################################################################
# @correct_samples_with_zero_radii
####################################################################################################
def correct_samples_with_zero_radii(sections_list, epsilon=1e-3):
    """Updating the radii of the samples whose radii are set to zero due to reconstruction artifact.
    NOTE: This operation is performed on a per-section level.

    :param sections_list:
        A list of all the sections in the morphology.
    :param epsilon:
        Smallest value.
    """

    # Per section
    for section in sections_list:

        # Make sure that the section has at least one sample
        if len(section.samples) == 0:
            return

        # Get the mean radius
        mean_radius = 0
        for sample in section.samples:
            mean_radius += sample.radius
        mean_radius = mean_radius / len(section.samples)

        # Check if the sample radius is below the threshold or not
        for sample in section.samples:

            # If yes, update it
            if sample.radius < epsilon:
                sample.radius = mean_radius


####################################################################################################
# @analyze_samples_radii
####################################################################################################
def analyze_samples_radii(sections_list,
                          epsilon=1e-3):
    """Analyse the distribution of the samples of the whole morphology

    :param sections_list:
        A list of all the sections of the morphology
    :param epsilon:
        The minimum acceptable value for sample radius.
    :return:
        Minimum, maximum and average samples radii, and number of zero-radius samples.
    """

    # Get a list of all the radii in the morphology
    radii_list = [sample.radius for section in sections_list for sample in section.samples]

    # Get a list of zero-radii
    zero_radii = [radius for radius in radii_list if radius < epsilon]

    # Compute the minimum
    minimum_sample_radius = min(radii_list)

    # Compute the maximum
    maximum_sample_radius = max(radii_list)

    # Compute the average
    average_sample_radius = sum(radii_list) / (1.0 * len(radii_list))

    # Return the results
    return minimum_sample_radius, maximum_sample_radius, average_sample_radius, len(zero_radii)




