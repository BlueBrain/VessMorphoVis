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
    # @ReconstructionMethod
    ################################################################################################
    class ReconstructionMethod:
        """The reconstruction method used to build the morphology.
        """

        # Use the ConnectedSections builder
        CONNECTED_SECTIONS = 'CONNECTED_SECTIONS_RECONSTRUCTION'

        # Use the DisconnectedSections builder
        DISCONNECTED_SECTIONS = 'DISCONNECTED_SECTIONS_RECONSTRUCTION'

        # Use the DisconnectedSegments builder
        DISCONNECTED_SEGMENTS = 'DISCONNECTED_SEGMENTS_RECONSTRUCTION'

        # Use the SamplesBuilder Drawing samples only as spheres
        SAMPLES = 'SAMPLES_RECONSTRUCTION'

        # The list that will appear in the GUI
        METHOD_ITEMS = [
            (DISCONNECTED_SEGMENTS,
             'Disconnected Segments',
             "Each segment is an independent object (this approach is time consuming)"),
            (DISCONNECTED_SECTIONS,
             'Disconnected Sections',
             "Each section is an independent object"),
            (CONNECTED_SECTIONS,
             'Connected Sections',
             "The sections of a single arbor are connected together"),
            (SAMPLES,
             'Samples',
             "The morphology is reconstructed as a list of samples")
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

            # Disconnected segments
            if argument == 'disconnected-segments':
                return Morphology.ReconstructionMethod.DISCONNECTED_SEGMENTS

            # Disconnected sections
            elif argument == 'disconnected-sections':
                return Morphology.ReconstructionMethod.DISCONNECTED_SECTIONS

            # Connected sections
            elif argument == 'connected-sections':
                return Morphology.ReconstructionMethod.CONNECTED_SECTIONS

            # Samples
            elif argument == 'samples':
                return Morphology.ReconstructionMethod.SAMPLES

            # Default
            else:
                return Morphology.ReconstructionMethod.DISCONNECTED_SECTIONS

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

