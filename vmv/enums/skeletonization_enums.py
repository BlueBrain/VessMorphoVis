####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
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
# @Skeletonization
####################################################################################################
class Skeletonization:
    """Skeletonization enumerators
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Skeleton
    ################################################################################################
    class Style:
        """Style
        """

        # Use the original morphology skeleton
        ORIGINAL = 'MORPHOLOGY_SKELETON_STYLE_ORIGINAL'

        # Create a tapered morphology skeleton
        TAPERED = 'MORPHOLOGY_SKELETON_STYLE_TAPERED'

        # Create a zigzagged morphology skeleton
        ZIGZAG = 'MORPHOLOGY_SKELETON_STYLE_ZIGZAG'

        # Create a zigzagged and ta[ered morphology skeleton
        TAPERED_ZIGZAG = 'MORPHOLOGY_SKELETON_STYLE_TAPERED_ZIGZAG'

        # Simplified
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
                return Skeletonization.Style.ORIGINAL

            # Tapered
            elif argument == 'tapered':
                return Skeletonization.Style.TAPERED

            # Zigzag
            elif argument == 'zigzag':
                return Skeletonization.Style.ZIGZAG

            # Tapered zigzag
            elif argument == 'tapered-zigzag':
                return Skeletonization.Style.TAPERED_ZIGZAG

            # Tapered zigzag
            elif argument == 'simplified':
                return Skeletonization.Style.SIMPLIFIED

            # By default use the original skeleton
            else:
                return Skeletonization.Style.ORIGINAL

        ############################################################################################
        # @Radii
        ############################################################################################
        class Radii:
            """Vessels radii enumerators
            """

            ########################################################################################
            # @__init__
            ########################################################################################
            def __init__(self):
                pass

            # Set the radii of the arbors as specified in the morphology file
            AS_SPECIFIED = 'RADII_AS_SPECIFIED'

            # Set the radii of the arbors to a fixed value
            FIXED = 'RADII_FIXED'

            # Scale the radii of the arbors using a constant factor
            SCALED = 'RADII_SCALED'

            # Filter sections with radii smaller than a threshold value given
            FILTERED = 'RADII_FILTERED'

            ########################################################################################
            # @get_enum
            ########################################################################################
            @staticmethod
            def get_enum(argument):

                # Fixed radii arbors
                if argument == 'fixed':
                    return Skeletonization.Skeleton.Radii.FIXED

                # Scaled radii
                elif argument == 'scaled':
                    return Skeletonization.Skeleton.Radii.SCALED

                # Scaled radii
                elif argument == 'filtered':
                    return Skeletonization.Skeleton.Radii.SCALED

                # By default, use the original skeleton radii as specified in the morphology
                else:
                    return Skeletonization.Skeleton.Radii.AS_SPECIFIED

    ################################################################################################
    # @Method
    ################################################################################################
    class Method:

        # Connect the skeleton into pieces without being concerned with the radii
        CONNECTED_SKELETON = 'SKELETONIZATION_CONNECTED_SKELETON'

        # Connect the original sections without repairing any artifacts in the morphology
        CONNECTED_SECTIONS = 'SKELETONIZATION_CONNECTED_SECTIONS'

        # Disconnect the sections and draw each of them as an independent object
        DISCONNECTED_SECTIONS = 'SKELETONIZATION_DISCONNECTED_SECTIONS'

        # Similar to DISCONNECTED_SECTIONS, and add an articulation sphere to connect the sections
        ARTICULATED_SECTIONS = 'SKELETONIZATION_ARTICULATED_SECTIONS'

        # Disconnect the segments and draw each of them as an independent object
        DISCONNECTED_SEGMENTS = 'SKELETONIZATION_DISCONNECTED_SEGMENTS'

        # Drawing samples only as spheres
        SAMPLES = 'SKELETONIZATION_SAMPLES'

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

            # Disconnected segments
            if argument == 'disconnected-segments':
                return Skeletonization.Method.DISCONNECTED_SEGMENTS

            # Disconnected sections
            elif argument == 'disconnected-sections':
                return Skeletonization.Method.DISCONNECTED_SECTIONS

            # Articulated sections
            elif argument == 'articulated-sections':
                return Skeletonization.Method.ARTICULATED_SECTIONS

            # Connected sections
            elif argument == 'connected-sections':
                return Skeletonization.Method.CONNECTED_SECTIONS

            # Connected sections
            elif argument == 'connected-skeleton':
                return Skeletonization.Method.CONNECTED_SKELETON

            # Samples
            elif argument == 'samples':
                return Skeletonization.Method.SAMPLES

            # Default
            else:
                return Skeletonization.Method.DISCONNECTED_SECTIONS

    ################################################################################################
    # @Branching
    ################################################################################################
    class Branching:
        """Branching method
        """

        # Make the branching based on the angles between the branches
        ANGLES = 'ANGLE_BASED_BRANCHING'

        # Make the branching based in the radii between the branches
        RADII = 'RADII_BASED_BRANCHING'

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

            # Angles
            if argument == 'radii':
                return Skeletonization.Branching.ANGLES

            # Radii
            elif argument == 'radii':
                return Skeletonization.Branching.RADII

            # By default angles
            else:
                return Skeletonization.Branching.ANGLES

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
                return Skeletonization.Radii.AS_SPECIFIED

            # Scaled
            elif argument == 'scaled':
                return Skeletonization.Radii.SCALED

            # Fixed
            elif argument == 'fixed':
                return Skeletonization.Radii.FIXED

            # Filtered
            elif argument == 'filtered':
                return Skeletonization.Radii.FILTERED

            # By default, as specified in the morphology file
            else:
                return Skeletonization.Radii.AS_SPECIFIED

