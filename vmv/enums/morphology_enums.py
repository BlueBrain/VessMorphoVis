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
# @Morphology
####################################################################################################
class Morphology:
    """Morphology enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Visualization
    ################################################################################################
    class Visualization:
        """The kind of visualization, whether structure or dynamics
        """

        # Visualize static structural aspects
        STRUCTURE = 'MORPHOLOGY_VISUALIZATION_STRUCTURE'
        STRUCTURE_UI_ITEM = (
            STRUCTURE,
            'Static Structure',
            'Visualize static data, showing only the structure of the vasculature without any '
            'variations with respect to time')

        # Visualize radius dynamics using structural variations with respect to time
        RADII_STRUCTURAL_DYNAMICS = 'MORPHOLOGY_VISUALIZATION_RADII_STRUCTURAL_DYNAMICS'
        RADII_STRUCTURAL_DYNAMICS_UI_ITEM = (
            RADII_STRUCTURAL_DYNAMICS,
            'Radii Dynamics',
            'Visualize structural dynamics with respect to time showing the variations in radii '
            'along the structure of the morphology with respect to time, without any color-mapping.'
            'This approach uses the Section-based builder only, showing the morphology skeleton as '
            'a set of sections')

        # Visualize radius dynamics using a color-map
        RADII_COLORMAP = 'MORPHOLOGY_VISUALIZATION_RADII_COLORMAP'
        RADII_COLORMAP_DYNAMICS_UI_ITEM = (
            RADII_COLORMAP,
            'Radii (Color Map)',
            'Visualize the variations of the radii along the morphology with respect to time '
            'using a color-map. This approach uses the Segment-based builder only, showing the '
            'morphology as a set of segments')

        # Visualize blood flow dynamics
        FLOW_COLORMAP = 'MORPHOLOGY_VISUALIZATION_FLOW_COLORMAP'
        FLOW_COLORMAP_DYNAMICS_UI_ITEM = (
            FLOW_COLORMAP,
            'Blood Flow (Color Map)',
            'Visualize the variations of the blood flow along the morphology with respect to time '
            'using a color-map. This approach uses the Segment-based builder only, showing the '
            'morphology as a set of segments')

        # Visualize blood pressure dynamics
        PRESSURE_COLORMAP = 'MORPHOLOGY_VISUALIZATION_PRESSURE_COLORMAP'
        PRESSURE_COLORMAP_DYNAMICS_UI_ITEM = (
            PRESSURE_COLORMAP,
            'Blood Pressure (Color Map)',
            'Visualize the variations of the blood pressure along the morphology with respect to '
            'time using a color-map. This approach uses the Segment-based builder only, showing '
            'the morphology as a set of segments')

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

            # Structure
            if argument == 'structure':
                return Morphology.Visualization.STRUCTURE

            # Radii structural variations
            elif argument == 'radii-structural':
                return Morphology.Visualization.RADII_STRUCTURAL_DYNAMICS

            # Radii (with color map)
            elif argument == 'radii':
                return Morphology.Visualization.RADII_COLORMAP

            # Blood flow (with color map)
            elif argument == 'flow':
                return Morphology.Visualization.FLOW_COLORMAP

            # Blood pressure (with color map)
            elif argument == 'pressure':
                return Morphology.Visualization.PRESSURE_COLORMAP

            # By default, visualize structure
            else:
                return Morphology.Visualization.STRUCTURE

    ################################################################################################
    # @Skeleton
    ################################################################################################
    class Style:
        """The style of the morphology skeleton
        """

        # Use the original morphology skeleton
        ORIGINAL = 'MORPHOLOGY_STYLE_ORIGINAL'

        # Create a zigzagged morphology skeleton
        ZIGZAG = 'MORPHOLOGY_STYLE_ZIGZAG'

        # Simplified style, only use the first and last sample of the morphology
        SIMPLIFIED = 'MORPHOLOGY_SKELETON_STYLE_SIMPLIFIED'

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

            # Original
            if argument == 'original':
                return Morphology.Style.ORIGINAL

            # Zigzag
            elif argument == 'zigzag':
                return Morphology.Style.ZIGZAG

            # Simplified
            elif argument == 'simplified':
                return Morphology.Style.SIMPLIFIED

            # By default use the original skeleton
            else:
                return Morphology.Style.ORIGINAL

    ################################################################################################
    # @Builder
    ################################################################################################
    class Builder:
        """The reconstruction method used to build the morphology.
        """

        # Use the Sections builder
        SECTIONS = 'SECTIONS_BUILDER'
        SECTIONS_UI_ITEM = (
            SECTIONS,
            'Sections',
            'Build the morphology as a set of sections, where each section is an independent '
            'object')

        # Use the Segments builder
        SEGMENTS = 'RECONSTRUCTION_METHOD_SEGMENTS_BUILDER'
        SEGMENTS_UI_ITEM = (
            SEGMENTS,
            'Segments',
            'Reconstruct the morphology as a set of segments, where each segment is an '
            'independent object (this approach is time consuming!)')

        # Use the Samples Builder Drawing samples only as spheres
        SAMPLES = 'SAMPLES_BUILDER'
        SAMPLES_UI_ITEM = (
            SAMPLES,
            'Samples',
            'Reconstruct the morphology as a set of samples')

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

            # Segments
            if argument == 'segments':
                return Morphology.Builder.SEGMENTS

            # Sections
            elif argument == 'sections':
                return Morphology.Builder.SECTIONS

            # Samples
            elif argument == 'samples':
                return Morphology.Builder.SAMPLES

            # Default
            else:
                return Morphology.Builder.SECTIONS

    ################################################################################################
    # @Radii
    ################################################################################################
    class Radii:
        """Radii of the samples along the vessels
        """

        # Set the radii of the vessels as specified in the morphology file
        AS_SPECIFIED = 'VESSELS_RADII_AS_SPECIFIED'

        # Set the radii of the vessels to a fixed value
        FIXED = 'VESSELS_RADII_FIXED'

        # Scale the radii of the vessels using a constant factor
        SCALED = 'VESSELS_RADII_SCALED'

        # Minimum threshold
        MINIMUM = 'VESSELS_RADII_MINIMUM_THRESHOLD'

        # Radii items that will appear in the user interface
        RADII_UI_ITEMS = [
            (AS_SPECIFIED,
             'As Specified in Morphology',
             'Use the cross-sectional radii as reported in the morphology file'),

            (FIXED,
             'At a Fixed Radii',
             'Set all the tubes to a fixed radius for enhanced visualization'),

            (SCALED,
             'With Scale Factor',
             'Scale all the tubes using a specified scale factor')
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

            # As specified in the morphology file
            if argument == 'default':
                return Morphology.Radii.AS_SPECIFIED

            # Scaled
            elif argument == 'scaled':
                return Morphology.Radii.SCALED

            # Fixed
            elif argument == 'fixed':
                return Morphology.Radii.FIXED

            # Minimum threshold
            elif argument == 'minimum':
                return Morphology.Radii.MINIMUM

            # By default, as specified in the morphology file
            else:
                return Morphology.Radii.AS_SPECIFIED

