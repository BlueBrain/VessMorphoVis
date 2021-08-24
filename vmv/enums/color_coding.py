####################################################################################################
# Copyright (c) 2019 - 2021, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
# @ColorCoding
####################################################################################################
class ColorCoding:
    """ColorCoding enumerators
    """

    # Color the morphology by components
    DEFAULT = 'DEFAULT_COLOR_CODING'

    # Use alternating colors for every other component in the morphology
    ALTERNATING_COLORS = 'ALTERNATING_COLORS_COLOR_CODING'

    # Color code the components according to their average radius
    BY_RADIUS = 'COLOR_CODING_BY_RADIUS_COLOR_CODING'

    # Color code the components according to their length
    BY_LENGTH = 'COLOR_CODING_BY_LENGTH_COLOR_CODING'

    # Color code the components according to their surface area
    BY_SURFACE_AREA = 'COLOR_CODING_BY_AREA_COLOR_CODING'

    # Color code the components according to their volume
    BY_VOLUME = 'COLOR_CODING_BY_VOLUME_COLOR_CODING'

    # Color code the section according to the number of samples it contains
    BY_NUMBER_SAMPLES = 'COLOR_CODING_BY_NUMBER_SAMPLES_COLOR_CODING'

    # Label the short sections
    SHORT_SECTIONS = 'SHORT_SECTION_COLOR_CODING'

    ################################################################################################
    # Segments color-coding items to be added to the interface list
    ################################################################################################
    SEGMENTS_COLOR_CODING_ITEMS = [

        # Default coloring scheme
        (DEFAULT,
         'Default',
         'A single color will be applied to the entire morphology'),

        # Alternating colors for every two segments in the morphology
        (ALTERNATING_COLORS,
         'Alternating Colors',
         'Use alternating segments colors to visualize certain patterns in the morphology'),

        # Radius
        (BY_RADIUS,
         'Segment Radius',
         'Color-code the morphology based on the radius of the segment with respect to '
         'the radii distribution along the entire morphology'),

        # Length
        (BY_LENGTH,
         'Segment Length',
         'Color-code the morphology based on the length of the segment with respect to '
         'the segments length distribution along the entire morphology'),

        # Area
        (BY_SURFACE_AREA,
         'Segment Area',
         'Color-code the morphology based on the area of the segment with respect to '
         'the distribution of the segments areas along the entire morphology'),

        # Volume
        (BY_VOLUME,
         'Segment Volume',
         'Color-code the morphology based on the volume of the segment with respect to '
         'the distribution of the segments volumes along the entire morphology')
    ]

    ################################################################################################
    # Color coding options per section
    ################################################################################################
    SECTIONS_COLOR_CODING_ITEMS = [

        # Default coloring scheme
        (DEFAULT,
         'Default',
         'A single color will be applied to the entire morphology'),

        # Alternating colors for every two sections in the morphology
        (ALTERNATING_COLORS,
         'Alternating Colors',
         'Use alternating sections colors to visualize certain patterns in the morphology'),

        # Length
        (BY_LENGTH,
         'Section Length',
         'Color-code the morphology based on the length of the section with respect to '
         'the sections length distribution along the entire morphology'),

        # Area
        (BY_SURFACE_AREA,
         'Section Surface Area',
         'Color-code the morphology based on the area of the section with respect to '
         'the distribution of the sections surface areas along the entire morphology'),

        # Volume
        (BY_VOLUME,
         'Section Volume',
         'Color-code the morphology based on the volume of the section with respect to '
         'the distribution of the sections volumes along the entire morphology'),

        # Number of samples
        (BY_NUMBER_SAMPLES,
         'Number of Samples',
         'Color-code the morphology based on the number of samples along the section')
    ]

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ############################################################################################
    # @get_enum
    ############################################################################################
    @staticmethod
    def get_enum(argument):

        # Default scheme
        if argument == 'default':
            return ColorCoding.DEFAULT

        # Alternating colors
        if argument == 'alternating':
            return ColorCoding.ALTERNATING_COLORS

        # By radius
        elif argument == 'radius':
            return ColorCoding.BY_RADIUS

        # By length
        elif argument == 'length':
            return ColorCoding.BY_LENGTH

        # By area
        elif argument == 'area':
            return ColorCoding.BY_SURFACE_AREA

        # By volume
        elif argument == 'volume':
            return ColorCoding.BY_VOLUME

        # By number of samples along the section
        elif argument == 'number-samples':
            return ColorCoding.BY_NUMBER_SAMPLES

        # By default use the default scheme
        else:
            return ColorCoding.DEFAULT
