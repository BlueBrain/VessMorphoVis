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


####################################################################################################
# Meshing
####################################################################################################
class Prefix:
    """Prefix constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Vessel radius
    VESSEL_RADIUS = 'vessel-radius'

    # Zero-radius samples
    ZERO_RADIUS_SAMPLES = 'zero-radius-samples'

    # Section mean radius
    SECTION_MEAN_RADIUS = 'section-mean-radius'

    # Section radius ratio
    SECTION_RADIUS_RATIO = 'section-radius-ratio'


    SECTION_LENGTH = 'section-length'
    SEGMENT_MEAN_LENGTH = 'segment-mean-length'
    SEGMENT_LENGTH_RATIO = 'segment-length-ratio'

    NUMBER_SAMPLES_PER_SECTION = 'number-samples-per-section'
    NUMBER_SEGMENTS_PER_SECTION = 'number-segments-per-section'

    SECTIONS_WITH_SINGLE_SEGMENTS = 'sections-with-single-segments'

    SHORT_SECTIONS = 'short-sections'

    SECTION_VOLUME = 'section-volume'
    SEGMENT_MEAN_VOLUME = 'segment-mean-volume'

    SEGMENT_VOLUME_RATIO = 'segment-volume-ratio'



    STRUCTURE = 'structure'
    RADIUS = 'radius'
    LENGTH = 'length'
    SURFACE_AREA = 'surface_area'
    VOLUME = 'volume'
