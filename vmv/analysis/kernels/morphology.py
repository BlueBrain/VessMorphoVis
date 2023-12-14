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

# Internal imports
import vmv.analysis
import vmv.skeleton


####################################################################################################
# @compute_total_morphology_length
####################################################################################################
def compute_total_morphology_length(sections_list):
    """Computes the total length of the morphology.

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
        section_length = vmv.analysis.compute_section_length(section=section)

        # Append the result to the total length
        morphology_total_length += section_length

    # Return the total length
    return morphology_total_length


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
def compute_number_of_components(morphology):
    """Computes the number of components of the morphology.

    :param morphology:
        The vascular morphology.
    :return:
        The number of components in the morphology.
    """

    return vmv.skeleton.get_number_components_in_graph(morphology=morphology)
