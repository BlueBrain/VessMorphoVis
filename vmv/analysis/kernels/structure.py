####################################################################################################
# Copyright (c) 2022, EPFL / Blue Brain Project
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
import vmv.utilities


####################################################################################################
# @compute_structure_analysis_items
####################################################################################################
def compute_structure_analysis_items(morphology):

    # Initially, an empty collector
    items = vmv.analysis.StructureAnalysisItems()

    items.number_unique_samples = morphology.number_samples
    items.number_sections = len(morphology.sections_list)

    items.minimum_number_samples_per_section = 1e10
    items.maximum_number_samples_per_section = -1e10

    aggregate_number_samples_per_section = 0

    for section in morphology.sections_list:

        number_samples_in_section = len(section.samples)

        aggregate_number_samples_per_section += number_samples_in_section

        if number_samples_in_section == 2:
            items.number_sections_with_one_segment += 1

        if number_samples_in_section > items.maximum_number_samples_per_section:
            items.maximum_number_samples_per_section = number_samples_in_section

        if number_samples_in_section < items.minimum_number_samples_per_section:
            items.minimum_number_samples_per_section = number_samples_in_section

        items.number_samples += number_samples_in_section
        items.number_segments += number_samples_in_section - 1

        if vmv.analysis.is_short_section(section):
            items.number_short_sections += 1

    items.mean_number_samples_per_section = \
        int(aggregate_number_samples_per_section / len(morphology.sections_list))

    return items
