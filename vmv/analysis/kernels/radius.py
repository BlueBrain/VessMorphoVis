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
import numpy
import pandas

# Internal imports
import vmv.analysis
import vmv.utilities
from vmv.consts import Keys


####################################################################################################
# @perform_per_sample_radius_analysis
####################################################################################################
def perform_per_sample_radius_analysis(sections):

    # Data collecting list
    data = list()

    # Section-by-section
    for section in sections:

        # For every sample in each section
        for sample in section.samples:
            data.append([sample.radius, sample.point[0], sample.point[1], sample.point[2]])

    # Return the result
    return pandas.DataFrame(data, columns=[Keys.SAMPLE_RADIUS, Keys.X, Keys.Y, Keys.Z])



def perform_per_section_radius_analysis(sections):


    pass


####################################################################################################
# @compute_radius_analysis_items
####################################################################################################
def compute_radius_analysis_items(sections):

    # Initially, an empty collector
    items = vmv.analysis.RadiusAnalysisItems()

    # Perform the per-sample radius analysis
    per_sample_df = perform_per_sample_radius_analysis(sections=sections)

    # Reference to the data list
    samples_radius_list = per_sample_df[Keys.SAMPLE_RADIUS]

    # Update the items
    items.minimum_sample_radius = min(samples_radius_list)
    items.minimum_non_zero_sample_radius = vmv.utilities.get_non_zero_minimum_value(
        samples_radius_list)
    items.maximum_sample_radius = numpy.nanmax(numpy.array(samples_radius_list))
    items.mean_sample_radius = vmv.utilities.mean(input_list=samples_radius_list)

    items.global_sample_radius_ratio = \
        items.minimum_non_zero_sample_radius / items.maximum_sample_radius
    items.global_sample_radius_ratio_factor = 1. / items.global_sample_radius_ratio
    items.number_samples_with_zero_radius = vmv.utilities.compute_zero_elements_count(
        input_list=samples_radius_list)

    # Return the results
    return items



