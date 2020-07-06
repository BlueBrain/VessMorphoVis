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
# @ColorMaps
####################################################################################################
class ColorCoding:
    """ColorCoding enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Segment
    ################################################################################################
    class Segment:
        """Segments color coding 
        """

        # Use a single color for all the segments in the morphology 
        SINGLE_COLOR = 'SINGLE_SEGMENT_COLOR'

        # Use alternating colors for all the segments in the morphology 
        ALTERNATING_COLORS = 'ALTERNATING_SEGMENTS_COLORS'

        # Color code the segment according to its radius 
        BY_RADIUS = 'SEGMENT_COLOR_CODING_BY_RADIUS'

        # Color code the segment according to its length
        BY_LENGTH = 'SEGMENT_COLOR_CODING_BY_LENGTH'

        # Color code the segment according to its area 
        BY_AREA = 'SEGMENT_COLOR_CODING_BY_AREA'

        # Color code the segment according to its volume 
        BY_VOLUME = 'SEGMENT_COLOR_CODING_BY_VOLUME'

        ################################################################################################
        # Segments color-coding items to be added to the interface list
        ################################################################################################
        SEGMENTS_COLOR_CODING_ITEMS =[
            
            # Single color for all the segments in the morphology 
            (SINGLE_COLOR,
             'Single Color',
             'Use a single color for all the segments in the entire morphology'),

            # Alternating colors  
            (ALTERNATING_COLORS,
             'Alternating Colors',
             'Use alternating segments colors to visualze certain patterns in the morphology'),

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
            (BY_AREA,
             'Segment Area',
             'Color-code the morphology based on the area of the segment with respect to ' 
             'the distribution of the segments areas along the entire morphology'),

            # Volume
            (BY_VOLUME,
             'Segment Volume',
             'Color-code the morphology based on the volume of the segment with respect to ' 
             'the distribution of the segments volumes along the entire morphology')
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
            
            # Single color 
            if argument == 'single':
                return ColorCoding.Segment.SINGLE_COLOR

            # Alternating colors 
            if argument == 'alternating':
                return ColorCoding.Segment.ALTERNATING_COLORS

            # By radius 
            elif argument == 'radius':
                return ColorCoding.Segment.BY_RADIUS

            # By length
            elif argument == 'length':
                return ColorCoding.Segment.BY_LENGTH

            # By area
            elif argument == 'area':
                return ColorCoding.Segment.BY_AREA

            # By volume
            elif argument == 'volume':
                return ColorCoding.Segment.BY_VOLUME

            # By default use by radius
            else:
                return ColorCoding.Segment.SINGLE_COLOR

    ################################################################################################
    # @Section
    ################################################################################################
    class Section:
        """Sections color coding 
        """

        # Use a single color for all the sections in the morphology 
        SINGLE_COLOR = 'SINGLE_SECTION_COLOR'

        # Use alternating colors for all the sections in the morphology 
        ALTERNATING_COLORS = 'ALTERNATING_SECTIONS_COLORS'

        # Color code the section according to its average radius 
        BY_AVERAGE_RADIUS = 'SECTION_COLOR_CODING_BY_AVERAGE_RADIUS'

        # Color code the section according to its length
        BY_LENGTH = 'SECTION_COLOR_CODING_BY_LENGTH'

        # Color code the section according to its area 
        BY_AREA = 'SECTION_COLOR_CODING_BY_AREA'

        # Color code the section according to its volume 
        BY_VOLUME = 'SECTION_COLOR_CODING_BY_VOLUME'

        # Color code the section according to the number of samples it contain 
        BY_NUMBER_SAMPLES = 'SECTION_COLOR_CODING_BY_NUMBER_SAMPLES'

        # Short Sections 
        SHORT_SECTIONS = 'SHORT_SECTION_COLOR_CODING'

        ################################################################################################
        # Sections color-coding items to be added to the interface list
        ################################################################################################
        SECTIONS_COLOR_CODING_ITEMS =[
            
            # Single color for all the sections in the morphology 
            (SINGLE_COLOR,
             'Single Color',
             'Use a single color for all the sections in the entire morphology'),

            # Alternating colors for every two sections in the morphology 
            (ALTERNATING_COLORS,
             'Alternating Colors',
             'Use alternating sections colors to visualze certain patterns in the morphology'),

            # Radius 
            (BY_AVERAGE_RADIUS,
             'Average Section Radius',
             'Color-code the morphology based on the average radius of the section with respect to ' 
             'the radii distribution along the entire morphology'),
            
            # Length
            (BY_LENGTH,
             'Section Length',
             'Color-code the morphology based on the length of the section with respect to ' 
             'the sections length distribution along the entire morphology'),

            # Area
            (BY_AREA,
             'Section Area',
             'Color-code the morphology based on the area of the section with respect to ' 
             'the distribution of the sections areas along the entire morphology'),

            # Volume
            (BY_VOLUME,
             'Section Volume',
             'Color-code the morphology based on the volume of the section with respect to ' 
             'the distribution of the sections volumes along the entire morphology'),

            # Number of samples 
            (BY_VOLUME,
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
            
            # Single color 
            if argument == 'single':
                return ColorCoding.Section.SINGLE_COLOR

            # Alternating colors 
            if argument == 'alternating':
                return ColorCoding.Section.ALTERNATING_COLORS
            
            # By radius 
            elif argument == 'radius':
                return ColorCoding.Section.BY_AVERAGE_RADIUS

            # By length
            elif argument == 'length':
                return ColorCoding.Section.BY_LENGTH

            # By area
            elif argument == 'area':
                return ColorCoding.Section.BY_AREA

            # By volume
            elif argument == 'volume':
                return ColorCoding.Section.BY_VOLUME

            # By number of samples along the section
            elif argument == 'number-samples':
                return ColorCoding.Section.BY_NUMBER_SAMPLES

            # Color the short sections 
            elif argument == 'short sections':
                return ColorCoding.Section.SHORT_SECTIONS

            # By default use by length
            else:
                return ColorCoding.Section.SINGLE_COLOR



