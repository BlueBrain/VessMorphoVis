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

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Visualization
    ################################################################################################
    class Visualization:
        """The kind of visualization, whether structure or dynamics
        """

        # Visualize structural aspects
        STRUCTURE = 'MORPHOLOGY_VISUALIZATION_STRUCTURE'
        STRUCTURE_UI_ITEM = (STRUCTURE,
                             'Structure',
                             'Visualize static data, showing only the structure of the vasculature')

        # Visualize dynamics, simulation and functional aspects
        DYNAMICS = 'MORPHOLOGY_VISUALIZATION_DYNAMICS'
        DYNAMICS_UI_ITEM = (DYNAMICS,
                            'Dynamics',
                            'Visualize simulation data with respect to time (function dynamics)')

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

            # Dynamics
            elif argument == 'dynamics':
                return Morphology.Visualization.DYNAMICS

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

        # Use the Segments builder
        SEGMENTS = 'RECONSTRUCTION_METHOD_SEGMENTS_BUILDER'

        # Use the Samples Builder Drawing samples only as spheres
        SAMPLES = 'SAMPLES_BUILDER'

        # The list that will appear in the GUI
        METHOD_ITEMS = [
            (SEGMENTS,
             'Segments',
             "Reconstruct the morphology as a set of segments, where each segment is an "
             "independent object (this approach is time consuming!)"),

            (SECTIONS,
             'Sections',
             "Reconstruct the morphology as a set of sections, where each section is an "
             "independent object"),

            (SAMPLES,
             'Samples',
             "Reconstruct the morphology as a set of samples")
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

