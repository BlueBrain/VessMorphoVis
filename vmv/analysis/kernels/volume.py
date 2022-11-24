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
# @perform_per_segment_volume_analysis
####################################################################################################
def perform_per_segment_volume_analysis(sections):

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

            # Compute volume
            r0 = section.samples[i].radius
            r1 = section.samples[i + 1].radius
            segment_volume = (1. / 3.) * math.pi * (p0 - p1).length * (r0 * r0 + r0 * r1 + r1 * r1)
            data.append([center[0], center[1], center[2], segment_volume])

    # Construct the data frame
    return pandas.DataFrame(data, columns=[Keys.X, Keys.Y, Keys.Z, Keys.SEGMENT_VOLUME])


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
        SectionStatsResult object containing the results.
    """

    # A container for the data that will be computed
    result = vmv.analysis.SectionStatsResult()

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
# @perform_per_section_volume_analysis
####################################################################################################
def perform_per_section_volume_analysis(sections,
                                        sections_centers=None):
    data = list()
    for i_section, section in enumerate(sections):

        # Get the section center, do NOT recalculate if provided
        section_center = vmv.analysis.compute_section_center_point(section) if sections_centers is None else \
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


####################################################################################################
# @compute_volume_analysis_items
####################################################################################################
def compute_volume_analysis_items(sections):

    # Initially, an empty collector
    items = vmv.analysis.VolumeAnalysisItems()

    # Perform the per-segment analysis
    per_segment_df = perform_per_segment_volume_analysis(sections=sections)

    # Reference to the data list
    segments_volume_list = per_segment_df[Keys.SEGMENT_VOLUME]

    # Update the items
    items.minimum_segment_volume = min(segments_volume_list)
    items.minimum_non_zero_segment_volume = vmv.utilities.get_non_zero_minimum_value(
        input_list=segments_volume_list)
    items.maximum_segment_volume = max(segments_volume_list)
    items.mean_segment_volume = vmv.utilities.mean(input_list=segments_volume_list)
    items.global_segment_volume_ratio = \
        items.minimum_non_zero_segment_volume / items.maximum_segment_volume
    items.global_segment_volume_ratio_factor = 1. / items.global_segment_volume_ratio
    items.number_segments_with_zero_volume = vmv.utilities.compute_zero_elements_count(
        input_list=segments_volume_list)

    # Perform the per-section analysis
    per_section_df = perform_per_section_volume_analysis(sections=sections)

    # Reference to the data list
    sections_volume_list = per_section_df[Keys.SECTION_VOLUME]

    # Update the items
    items.minimum_section_volume = min(sections_volume_list)
    items.minimum_non_zero_section_volume = vmv.utilities.get_non_zero_minimum_value(
        input_list=sections_volume_list)
    items.maximum_section_volume = max(sections_volume_list)
    items.mean_section_volume = vmv.utilities.mean(input_list=sections_volume_list)
    items.global_section_volume_ratio = \
        items.minimum_non_zero_section_volume / items.maximum_section_volume
    items.global_section_volume_ratio_factor = 1. / items.global_section_volume_ratio
    items.number_sections_with_zero_volume = vmv.utilities.compute_zero_elements_count(
        input_list=sections_volume_list)

    items.total_morphology_volume = sum(sections_volume_list)

    # Return the results
    return items




