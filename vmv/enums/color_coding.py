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
# @ColorCoding
####################################################################################################
class ColorCoding:
    """ColorCoding enumerators
    """

    # Use a single color for all the components in the morphology 
    SINGLE_COLOR = 'SINGLE_COLOR'

    # Use alternating colors for the different components in the morphology 
    ALTERNATING_COLORS = 'ALTERNATING_COLORS'

    # Color code the components according to their average radius 
    BY_RADIUS = 'COLOR_CODING_BY_RADIUS'

    # Color code the components according to their length
    BY_LENGTH = 'COLOR_CODING_BY_LENGTH'

    # Color code the components according to their area 
    BY_AREA = 'COLOR_CODING_BY_AREA'

    # Color code the components according to their volume 
    BY_VOLUME = 'COLOR_CODING_BY_VOLUME'

    # Color code the section according to the number of samples it contain 
    BY_NUMBER_SAMPLES = 'COLOR_CODING_BY_NUMBER_SAMPLES'

    # Short Sections 
    SHORT_SECTIONS = 'SHORT_SECTION_COLOR_CODING'

    ################################################################################################
    # Segments color-coding items to be added to the interface list
    ################################################################################################
    SEGMENTS_COLOR_CODING_ITEMS = [
        
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
        (BY_RADIUS,
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
        
        # Single color 
        if argument == 'single':
            return ColorCoding.SINGLE_COLOR

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
            return ColorCoding.BY_AREA

        # By volume
        elif argument == 'volume':
            return ColorCoding.BY_VOLUME

        # By number of samples along the section
        elif argument == 'number-samples':
            return ColorCoding.BY_NUMBER_SAMPLES

        # Color the short sections 
        elif argument == 'short sections':
            return ColorCoding.SHORT_SECTIONS

        # By default use by length
        else:
            return ColorCoding.SINGLE_COLOR
            
    
        



