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

# System imports
import math
import pandas


# Internal imports
import vmv.analysis
import vmv.utilities
from vmv.consts import Keys


####################################################################################################
# @perform_per_segment_length_analysis
####################################################################################################
def perform_per_segment_length_analysis(sections):

    # Data collecting list
    data = list()

    # Section-by-section
    for section in sections:

        # Segment by segment
        for i in range(len(section.samples) - 1):

            # Segment
            p0 = section.samples[i].point
            p1 = section.samples[i + 1].point

            # Its center
            center = 0.5 * (p0 + p1)

            # Compute segment length
            segment_length = (p0 - p1).length

            # Add it to the list
            data.append([center[0], center[1], center[2], segment_length])

    # Construct the data frame
    return pandas.DataFrame(data, columns=[Keys.X, Keys.Y, Keys.Z, Keys.SEGMENT_LENGTH])


####################################################################################################
# @compute_section_volume_data
####################################################################################################
def compute_section_length_data(section):
    """Computes the length of a section from its segments.

    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its volume.
    :return:
        SectionStatsResult object containing the results.
    """

    # A container for the data that will be computed
    result = vmv.analysis.SectionStatsResult()

    # If the section has less than two samples, then return
    if len(section.samples) < 2:
        return result

    # Compute the length of each segment and add it to the list
    segments_length = list()
    for i in range(len(section.samples) - 1):
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        segment_length = (p0 - p1).length
        segments_length.append(segment_length)

    result.total = sum(segments_length)
    result.min = min(segments_length)
    result.mean = result.total / len(section.samples)
    result.max = max(segments_length)
    result.ratio = result.min / result.max if result.max > 0 else 0

    # Return the statistics
    return result


####################################################################################################
# @perform_per_section_length_analysis
####################################################################################################
def perform_per_section_length_analysis(sections,
                                        sections_centers=None):
    data = list()
    for i_section, section in enumerate(sections):

        # Get the section center, do NOT recalculate if provided
        section_center = vmv.analysis.compute_section_center_point(section) \
            if sections_centers is None else sections_centers[i_section]

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
                     result.ratio])

    # Construct the data frame
    return pandas.DataFrame(data, columns=[Keys.SECTION_INDEX,
                                           Keys.X, Keys.Y, Keys.Z,
                                           Keys.SECTION_LENGTH,
                                           Keys.SEGMENT_MIN_LENGTH,
                                           Keys.SEGMENT_MEAN_LENGTH,
                                           Keys.SEGMENT_MAX_LENGTH,
                                           Keys.SEGMENT_LENGTH_RATIO])


####################################################################################################
# @compute_length_analysis_items
####################################################################################################
def compute_length_analysis_items(sections):

    # Initially, an empty collector
    items = vmv.analysis.LengthAnalysisItems()

    # Perform the per-segment analysis
    per_segment_df = perform_per_segment_length_analysis(sections=sections)

    # Reference to the data list
    segments_length_list = per_segment_df[Keys.SEGMENT_LENGTH]

    # Update the items
    items.minimum_segment_length = min(segments_length_list)
    items.minimum_non_zero_segment_length = vmv.utilities.get_non_zero_minimum_value(
        input_list=segments_length_list)
    items.maximum_segment_length = max(segments_length_list)
    items.mean_segment_length = vmv.utilities.mean(input_list=segments_length_list)
    items.global_segment_length_ratio = \
        items.minimum_non_zero_segment_length / items.maximum_segment_length
    items.global_segment_length_ratio_factor = 1. / items.global_segment_length_ratio
    items.number_segments_with_zero_length = vmv.utilities.compute_zero_elements_count(
        input_list=segments_length_list)

    # Perform the per-section analysis
    per_section_df = perform_per_section_length_analysis(sections=sections)

    # Reference to the data list
    sections_length_list = per_section_df[Keys.SECTION_LENGTH]

    # Update the items
    items.minimum_section_length = min(sections_length_list)
    items.minimum_non_zero_section_length = vmv.utilities.get_non_zero_minimum_value(
        input_list=sections_length_list)
    items.maximum_section_length = max(sections_length_list)
    items.mean_section_length = vmv.utilities.mean(input_list=sections_length_list)
    items.global_section_length_ratio = \
        items.minimum_non_zero_section_length / items.maximum_section_length
    items.global_section_length_ratio_factor = 1. / items.global_section_length_ratio
    items.number_sections_with_zero_length = vmv.utilities.compute_zero_elements_count(
        input_list=sections_length_list)

    items.total_morphology_length = sum(sections_length_list)

    # Return the results
    return items
