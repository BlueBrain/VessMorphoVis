####################################################################################################
# Copyright (c) 2019 - 2023, EPFL / Blue Brain Project
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
    # @Technique
    ################################################################################################
    class Technique:
        """Meshing techniques
        """

        # Piecewise watertight meshing
        PIECEWISE_WATERTIGHT = 'MESHING_TECHNIQUE_PIECEWISE_WATERTIGHT'

        # Meta balls-based meshing
        META_BALLS = 'MESHING_TECHNIQUE_META_BALLS'

        # Skin-modifier based meshing
        SKIN_MODIFIER = 'MESHING_TECHNIQUE_SKIN_MODIFIER'

        # Voxelization
        VOXELIZATION = 'MESHING_TECHNIQUE_VOXELIZATION'

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

            # Metaballs
            elif argument == 'meta-balls':
                return Meshing.Technique.META_BALLS

            # Skinning modifier
            elif argument == 'skin-modifier':
                return Meshing.Technique.SKIN_MODIFIER

            # Voxelization-based remeshing
            elif argument == 'voxelization':
                return Meshing.Technique.VOXELIZATION

            # By default use piecewise-watertight
            else:
                return Meshing.Technique.PIECEWISE_WATERTIGHT

        # Meshing techniques items for the list
        MESHING_TECHNIQUES_ITEMS = [
            (PIECEWISE_WATERTIGHT,
             'Polylines (Sections)',
             'Piecewise watertight meshing, where a group of connected segments will be created '
             'as a single watertight mesh, but the whole mesh will not be watertight. '
             'This approach is relatively fast for large scale morphologies and us used to create '
             'a proxy mesh for visualization'),
            (SKIN_MODIFIER,
             'Skin Modifier',
             'Use skin modifier to create a high quality mesh with smooth branching geometries '
             'and nice topology'),
            (VOXELIZATION,
             'Voxelization',
             'Use voxelization-based remeshing to construct a watertight mesh'),
            (META_BALLS,
             'Meta Balls',
             'Creates watertight mesh models using the meta balls algorithm. '
             'This method is SLOW and can take few hours to make a mesh based on the resolution '
             'and setting')
        ]

    class MetaBalls:
        """MetaBalls options
        """

        # Set the MetaBalls resolution automatically after building the proxy object
        AUTO_RESOLUTION = 'META_BALL_AUTO_RESOLUTION'

        # Use the resolution specified by the user in the input configuration
        USER_DEFINED_RESOLUTION = 'META_BALL_USER_DEFINED_RESOLUTION'

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

            # Set the MetaBalls resolution automatically after building the proxy object
            if argument == 'auto':
                return Meshing.MetaBalls.AUTO_RESOLUTION

            # User defined resolution
            elif argument == 'user-defined':
                return Meshing.MetaBalls.USER_DEFINED_RESOLUTION

            # By default use auto-resolution
            else:
                return Meshing.MetaBalls.AUTO_RESOLUTION

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

        # .blend
        BLEND = 'EXPORT_FORMAT_BLEND'

        FILE_FORMATS_ITEMS = [
            (PLY, 'Stanford (.ply)', 'Export the mesh to a .ply file'),
            (OBJ, 'Wavefront(.obj)', 'Export the mesh to a .obj file'),
            (STL, 'Stereolithography CAD (.stl)', 'Export the mesh to an .stl file'),
            (BLEND, 'Blender File (.blend)', 'Export the mesh as a .blend file')
        ]

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass