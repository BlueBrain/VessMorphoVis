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
# @perform_per_segment_surface_area_analysis
####################################################################################################
def perform_per_segment_surface_area_analysis(sections):

    # Data collecting list
    data = list()

    # Section-by-section
    for section in sections:

        # Segment by segment
        for i in range(len(section.samples) - 1):

            # Retrieve the data of the samples along each segment on the section
            p0 = section.samples[i].point
            p1 = section.samples[i + 1].point
            r0 = section.samples[i].radius
            r1 = section.samples[i + 1].radius

            # Segment center
            center = 0.5 * (p0 + p1)

            # Compute the segment lateral area
            segment_length = (p0 - p1).length
            r_sum = r0 + r1
            r_diff = r0 - r1
            segment_lateral_area = math.pi * r_sum * math.sqrt((r_diff * r_diff) + segment_length)
            segment_surface_area = segment_lateral_area + math.pi * ((r0 * r0) + (r1 * r1))
            data.append([center[0], center[1], center[2], segment_surface_area])

    # Construct the data frame
    return pandas.DataFrame(data, columns=[Keys.X, Keys.Y, Keys.Z, Keys.SEGMENT_SURFACE_AREA])


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
    result = vmv.analysis.SectionStatsResult()

    # If the section has less than two samples, then return
    if len(section.samples) < 2:
        return result

    # Compute the surface area of each segment and add it to the list
    segments_surface_area = list()
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
        segment_surface_area = segment_lateral_area + (math.pi * ((r0 * r0) + (r1 * r1)))
        segments_surface_area.append(segment_surface_area)

    result.total = sum(segments_surface_area)
    result.min = min(segments_surface_area)
    result.mean = result.total / len(section.samples)
    result.max = max(segments_surface_area)
    result.ratio = result.min / result.max if result.max > 0 else 0

    # Return the statistics
    return result


####################################################################################################
# @perform_per_section_surface_area_analysis
####################################################################################################
def perform_per_section_surface_area_analysis(sections,
                                              sections_centers=None):
    data = list()
    for i_section, section in enumerate(sections):

        # Get the section center, do NOT recalculate if provided
        section_center = vmv.analysis.compute_section_center_point(section) \
            if sections_centers is None else sections_centers[i_section]

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
# @compute_surface_area_analysis_items
####################################################################################################
def compute_surface_area_analysis_items(sections):

    # Initially, an empty collector
    items = vmv.analysis.SurfaceAreaAnalysisItems()

    # Perform the per-segment analysis
    per_segment_df = perform_per_segment_surface_area_analysis(sections=sections)

    # Reference to the data list
    segments_surface_area_list = per_segment_df[Keys.SEGMENT_SURFACE_AREA]

    # Update the items
    items.minimum_segment_surface_area = min(segments_surface_area_list)
    items.minimum_non_zero_segment_surface_area = vmv.utilities.get_non_zero_minimum_value(
        input_list=segments_surface_area_list)
    items.maximum_segment_surface_area = max(segments_surface_area_list)
    items.mean_segment_surface_area = vmv.utilities.mean(input_list=segments_surface_area_list)
    items.global_segment_surface_area_ratio = \
        items.minimum_non_zero_segment_surface_area / items.maximum_segment_surface_area
    items.global_segment_surface_area_ratio_factor = 1. / items.global_segment_surface_area_ratio
    items.number_segments_with_zero_surface_area = vmv.utilities.compute_zero_elements_count(
        input_list=segments_surface_area_list)

    # Perform the per-section analysis
    per_section_df = perform_per_section_surface_area_analysis(sections=sections)

    # Reference to the data list
    sections_surface_area_list = per_section_df[Keys.SECTION_SURFACE_AREA]

    # Update the items
    items.minimum_section_surface_area = min(sections_surface_area_list)
    items.minimum_non_zero_section_surface_area = vmv.utilities.get_non_zero_minimum_value(
        input_list=sections_surface_area_list)
    items.maximum_section_surface_area = max(sections_surface_area_list)
    items.mean_section_surface_area = vmv.utilities.mean(input_list=sections_surface_area_list)
    items.global_section_surface_area_ratio = \
        items.minimum_non_zero_section_surface_area / items.maximum_section_surface_area
    items.global_section_surface_area_ratio_factor = 1. / items.global_section_surface_area_ratio
    items.number_sections_with_zero_surface_area = vmv.utilities.compute_zero_elements_count(
        input_list=sections_surface_area_list)

    items.total_morphology_surface_area = sum(sections_surface_area_list)

    # Return the results
    return items
