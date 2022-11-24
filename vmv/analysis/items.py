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

        # Number of samples per section
        self.minimum_number_samples_per_section = 0
        self.maximum_number_samples_per_section = 0
        self.mean_number_samples_per_section = 0
        self.global_ratio_number_samples_per_section = 0

        # Number of samples with the zero radii
        self.number_samples_with_zero_radius = 0

        # Sampling distance
        self.minimum_sampling_distance = 0
        self.maximum_sampling_distance = 0
        self.mean_sampling_distance = 0

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


####################################################################################################
# @StructureAnalysisItems
####################################################################################################
class StructureAnalysisItems:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):

        self.number_unique_samples = 0
        self.number_samples = 0
        self.number_segments = 0
        self.number_sections = 0
        self.number_sections_with_one_segment = 0
        self.number_short_sections = 0
        self.minimum_number_samples_per_section = 0
        self.maximum_number_samples_per_section = 0
        self.mean_number_samples_per_section = 0
        self.mean_sampling_density_x = 0
        self.mean_sampling_density_y = 0
        self.mean_sampling_density_z = 0


####################################################################################################
# @RadiusAnalysisItems
####################################################################################################
class RadiusAnalysisItems:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):

        self.minimum_sample_radius = 0
        self.minimum_non_zero_sample_radius = 0
        self.maximum_sample_radius = 0
        self.mean_sample_radius = 0
        self.global_sample_radius_ratio = 0
        self.global_sample_radius_ratio_factor = 0
        self.number_samples_with_zero_radius = 0
        self.number_sections_with_zero_radius_samples = 0


####################################################################################################
# @LengthAnalysisItems
####################################################################################################
class LengthAnalysisItems:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):

        # Morphology
        self.total_morphology_length = 0

        # Segment
        self.minimum_segment_length = 0
        self.minimum_non_zero_segment_length = 0
        self.maximum_segment_length = 0
        self.mean_segment_length = 0
        self.global_segment_length_ratio = 0
        self.global_segment_length_ratio_factor = 0

        # Section
        self.minimum_section_length = 0
        self.maximum_section_length = 0
        self.mean_section_length = 0
        self.global_section_length_ratio = 0
        self.minimum_segment_length_ratio_per_section = 0
        self.maximum_segment_length_ratio_per_section = 0
        self.mean_segment_length_ratio_per_section = 0

        # Numbers
        self.number_segments_with_zero_length = 0
        self.number_sections_with_zero_length = 0


####################################################################################################
# @SurfaceAreaAnalysisItems
####################################################################################################
class SurfaceAreaAnalysisItems:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):

        # Morphology
        self.total_morphology_surface_area = 0

        # Segment
        self.minimum_segment_surface_area = 0
        self.minimum_non_zero_segment_surface_area = 0
        self.maximum_segment_surface_area = 0
        self.mean_segment_surface_area = 0
        self.global_segment_surface_area_ratio = 0
        self.global_segment_surface_area_ratio_factor = 0

        # Section
        self.minimum_section_surface_area = 0
        self.maximum_section_surface_area = 0
        self.mean_section_surface_area = 0
        self.global_section_surface_area_ratio = 0
        self.minimum_segment_surface_area_ratio_per_section = 0
        self.maximum_segment_surface_area_ratio_per_section = 0
        self.mean_segment_surface_area_ratio_per_section = 0

        # Numbers
        self.number_segments_with_zero_surface_area = 0
        self.number_sections_with_zero_surface_area = 0


####################################################################################################
# @VolumeAnalysisItems
####################################################################################################
class VolumeAnalysisItems:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):

        # Morphology
        self.total_morphology_volume = 0

        # Segment
        self.minimum_segment_volume = 0
        self.minimum_non_zero_segment_volume = 0
        self.maximum_segment_volume = 0
        self.mean_segment_volume = 0
        self.global_segment_volume_ratio = 0
        self.global_segment_volume_ratio_factor = 0

        # Section
        self.minimum_section_volume = 0
        self.maximum_section_volume = 0
        self.mean_section_volume = 0
        self.global_section_volume_ratio = 0
        self.minimum_segment_volume_ratio_per_section = 0
        self.maximum_segment_volume_ratio_per_section = 0
        self.mean_segment_volume_ratio_per_section = 0

        # Numbers
        self.number_segments_with_zero_volume = 0
        self.number_sections_with_zero_volume = 0
