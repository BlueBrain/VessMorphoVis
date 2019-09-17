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
# @Meshing
####################################################################################################
class Meshing:
    """Meshing enumerators
    """

    ############################################################################################
    # @__init__
    ############################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Skeleton
    ################################################################################################
    class Skeleton:
        """Skeletonization
        """

        # Use the original morphology skeleton
        ORIGINAL = 'MESHING_SKELETON_ORIGINAL'

        # Create a tapered morphology skeleton
        TAPERED = 'MESHING_SKELETON_TAPERED'

        # Create a zigzagged morphology skeleton
        ZIGZAG = 'MESHING_SKELETON_ZIGZAG'

        # Create a zigzagged and tapered morphology skeleton
        TAPERED_ZIGZAG = 'MESHING_SKELETON_TAPERED_ZIGZAG'

        # Simplified
        SIMPLIFIED = 'MESHING_SKELETON_SIMPLIFIED'

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
                return Meshing.Skeleton.ORIGINAL

            # Tapered
            elif argument == 'tapered':
                return Meshing.Skeleton.TAPERED

            # Zigzag
            elif argument == 'zigzag':
                return Meshing.Skeleton.ZIGZAG

            # Tapered zigzag
            elif argument == 'tapered-zigzag':
                return Meshing.Skeleton.TAPERED_ZIGZAG

            # Tapered zigzag
            elif argument == 'simplified':
                return Meshing.Skeleton.SIMPLIFIED

            # By default use the original skeleton
            else:
                return Meshing.Skeleton.ORIGINAL

    ################################################################################################
    # @Technique
    ################################################################################################
    class Technique:
        """Meshing techniques
        """

        # Piecewise watertight meshing
        PIECEWISE_WATERTIGHT = 'MESHING_TECHNIQUE_PIECEWISE_WATERTIGHT'

        # Bridging meshing
        META_BALLS = 'MESHING_TECHNIQUE_BRIDGING'

        # Skinning-based meshing
        SKINNING = 'MESHING_TECHNIQUE_SKINNING'

        # Meta balls-based meshing
        META_BALLS = 'MESHING_TECHNIQUE_META_BALLS'

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

            # Piecewise-watertight
            if argument == 'piecewise-watertight':
                return Meshing.Technique.PIECEWISE_WATERTIGHT

            # Union
            elif argument == 'skinning':
                return Meshing.Technique.SKINNING

            # Bridging
            elif argument == 'meta-balls':
                return Meshing.Technique.META_BALLS

            # By default use piecewise-watertight
            else:
                return Meshing.Technique.PIECEWISE_WATERTIGHT

    ################################################################################################
    # @ArborsConnection
    ################################################################################################
    class ObjectsConnection:
        """Objects connected to each others via joint operation
        """

        # Connected
        CONNECTED = 'CONNECTED_OBJECTS'

        # Disconnected
        DISCONNECTED = 'DISCONNECTED_OBJECTS'

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

            # All the objects are connected to a single mesh object
            if argument == 'connected':
                return Meshing.ObjectsConnection.CONNECTED

            # The objects are disconnected from each others
            elif argument == 'disconnected':
                return Meshing.ObjectsConnection.DISCONNECTED

            # By default use the mesh objects are disconnected
            else:
                return Meshing.ObjectsConnection.DISCONNECTED

    ################################################################################################
    # @Edges
    ################################################################################################
    class Edges:
        """Arbors edges
        """

        # Smooth edges
        SMOOTH = 'SMOOTH_EDGES'

        # Hard edges
        HARD = 'HARD_EDGES'

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

            # Use smooth edges
            if argument == 'smooth':
                return Meshing.Edges.SMOOTH

            # Use hard edges
            elif argument == 'hard':
                return Meshing.Edges.HARD

            # By default use hard edges
            else:
                return Meshing.Edges.HARD

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

            # Angle
            if argument == 'angles':
                return Meshing.Branching.ANGLES

            # Radii
            elif argument == 'radii':
                return Meshing.Branching.RADII

            # By default return angles
            else:
                return Meshing.Branching.ANGLES

    ################################################################################################
    # @Model
    ################################################################################################
    class Surface:
        """Reconstructed model quality, is it realistic quality or beauty
        """

        # Add noise to the surface to make it rough
        SMOOTH = 'SURFACE_ROUGH'

        # Smooth surface
        ROUGH = 'SURFACE_SMOOTH'

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

            # Rough surface
            if argument == 'rough':
                return Meshing.Surface.ROUGH

            # Smooth surface
            elif argument == 'smooth':
                return Meshing.Surface.SMOOTH

            # By default construct a smooth surface
            else:
                return Meshing.Surface.SMOOTH

    ################################################################################################
    # @ExportFormat
    ################################################################################################
    class ExportFormat:
        """The file format of the exported meshes
        """

        # .ply
        PLY = 'EXPORT_FORMAT_PLY'

        # .stl
        STL = 'EXPORT_FORMAT_STL'

        # .obj
        OBJ = 'EXPORT_FORMAT_OBJ'

        # .off
        OFF = 'EXPORT_FORMAT_OFF'

        # .blend
        BLEND = 'EXPORT_FORMAT_BLEND'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass
