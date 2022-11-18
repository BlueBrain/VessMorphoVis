####################################################################################################
# Copyright (c) 2021 - 2022, EPFL / Blue Brain Project
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
# Keys
####################################################################################################
class Keys:
    """Keys constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Axes
    X = 'X'
    Y = 'Y'
    Z = 'Z'
    AXES = [X, Y, Z]

    # Section Index
    SECTION_INDEX = 'Section Index'

    # Section Center
    SECTION_CENTER = 'Section Center '

    # Number of Samples (per Section)
    NUMBER_SAMPLES_PER_SECTION = 'Number Samples per Section'

    # Number of Segments (per Section)
    NUMBER_SEGMENTS_PER_SECTION = 'Number Segments per Section'

    # Radius
    SAMPLE_RADIUS = 'Sample Radius'
    SECTION_MIN_RADIUS = 'Section Min. Radius'
    SECTION_MEAN_RADIUS = 'Section Mean Radius'
    SECTION_MAX_RADIUS = 'Section Max. Radius'
    SECTION_RADIUS_RATIO = 'Section Radius Ratio'

    # Length
    SECTION_LENGTH = 'Section Length'
    SEGMENT_MIN_LENGTH = 'Segment Min. Length'
    SEGMENT_MEAN_LENGTH = 'Segment Mean Length'
    SEGMENT_MAX_LENGTH = 'Segment Max. Length'
    SEGMENT_LENGTH_RATIO = 'Segment Length Ratio'
    SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO = 'Section Thickness to Length Ratio'
    SECTION_SAMPLING_DENSITY = 'Section Sampling Density'

    # Surface Area
    SECTION_SURFACE_AREA = 'Section Surface Area'
    SEGMENT_SURFACE_AREA = 'Segment Surface Area'
    SEGMENT_MIN_SURFACE_AREA = 'Segment Min. Surface Area'
    SEGMENT_MEAN_SURFACE_AREA = 'Segment Mean Surface Area'
    SEGMENT_MAX_SURFACE_AREA = 'Segment Max. Surface Area'
    SEGMENT_SURFACE_AREA_RATIO = 'Segment Surface Area Ratio'

    # Volume
    SECTION_VOLUME = 'Section Volume'
    SEGMENT_VOLUME = 'Segment Volume'
    SEGMENT_MIN_VOLUME = 'Segment Min. Volume'
    SEGMENT_MEAN_VOLUME = 'Segment Mean Volume'
    SEGMENT_MAX_VOLUME = 'Segment Max. Volume'
    SEGMENT_VOLUME_RATIO = 'Segment Volume Ratio'
    



