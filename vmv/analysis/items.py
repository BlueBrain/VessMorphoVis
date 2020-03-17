####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
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


####################################################################################################
# @AnalysisItems
####################################################################################################
class AnalysisItems:
    """A structure for all the analysis items. This list will be used to make analysis once and
    store the results to drop the results to text files.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Total number of samples or points in the morphology
        self.total_number_samples = 0

        # Number of duplicated samples
        self.number_duplicated_samples = 0

        # Number of samples with the zero radii
        self.number_samples_with_zero_radius = 0

        # Minimum sample radius
        self.minimum_sample_radius = 0.0

        # Maximum sample radius
        self.maximum_sample_radius = 0.0

        # Average sample radius
        self.average_sample_radius = 0.0

        # Total length of the morphology
        self.total_morphology_length = 0.0

        # Total number of segments
        self.total_number_segment = 0

        # Total number of sections
        self.total_number_sections = 0

        # Number of sections with two samples
        self.number_sections_with_two_samples = 0

        # Number of short sections
        self.number_short_sections = 0

        # Minimum segment length
        self.minimum_segment_length = 0.0

        # Maximum segment length
        self.maximum_segment_length = 0.0

        # Average segment length
        self.average_segment_length = 0.0

        # Minimum section length
        self.minimum_section_length = 0.0

        # Maximum section length
        self.maximum_section_length = 0.0

        # Average section length
        self.average_section_length = 0.0

        # Number of loops
        self.number_loops = 0

        # Number of components in the morphology
        self.number_components = 0

        # Morphology bounding box
        self.bounding_box = None

