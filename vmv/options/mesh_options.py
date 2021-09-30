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

# Internal imports
import vmv
import vmv.consts
import vmv.enums


####################################################################################################
# @MeshOptions
####################################################################################################
class MeshOptions:
    """Mesh options
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # DATA #####################################################################################
        # This flag must be set to reconstruct a mesh
        self.reconstruct_neuron_mesh = False

        # MESHING OPTIONS ##########################################################################
        # Tessellation level (between 0.01 and 1.0)
        self.tessellation_ratio = vmv.consts.Meshing.MAX_TESSELLATION_LEVEL

        # Fixing morphology artifacts
        self.fix_morphology_artifacts = True

        # Meshing technique
        self.meshing_technique = vmv.enums.Meshing.Technique.META_BALLS

        # Meta ball resolution value
        self.meta_resolution = vmv.consts.Meshing.META_RESOLUTION

        # Automatically detect the resolution of the meta ball object
        self.meta_auto_resolution = True

        # Export in circuit coordinates, by default no unless there is a circuit file given
        self.global_coordinates = False

        # Connecting the different objects of the vasculature into a single mesh
        self.objects_connection = vmv.enums.Meshing.ObjectsConnection.DISCONNECTED

        # Create the mesh to look like a real neuron or more for visualization
        self.surface = vmv.enums.Meshing.Surface.SMOOTH

        # Edges of the meshes, either hard or smooth
        self.edges = vmv.enums.Meshing.Edges.HARD

        # COLOR & MATERIALS OPTIONS ################################################################
        # Morphology material
        self.material = vmv.enums.Shader.LAMBERT_WARD

        # Morphology color
        self.color = vmv.consts.Color.LIGHT_RED_COLOR

        # MESH RENDERING ###########################################################################
        # Camera view
        self.camera_view = vmv.enums.Rendering.View.FRONT

        # Camera projection
        self.camera_projection = vmv.enums.Rendering.Projection.ORTHOGRAPHIC

        # Image resolution is based on scale or to a fixed resolution
        self.resolution_basis = vmv.enums.Rendering.Resolution.FIXED_RESOLUTION

        # Render scale bar on the image
        self.render_scale_bar = False

        # Use transparent background
        self.transparent_background = True

        # Render a static frame of the mesh
        self.render = False

        # Render a 360 sequence of the reconstructed mesh
        self.render_360 = False

        # The scale factor used to scale the morphology rendering frame, default 1.0
        self.resolution_scale_factor = 1.0

        # MESH EXPORT ##############################################################################
        # Save the reconstructed mesh as a .ply file to the output directory
        self.export_ply = False

        # Save the reconstructed mesh as a .obj file to the output directory
        self.export_obj = False

        # Save the reconstructed mesh as a .stl file to the output directory
        self.export_stl = False

        # Save the reconstructed mesh as an .off file to the output directory
        self.export_off = False

        # Save the reconstructed mesh as a .blend file to the output directory
        self.export_blend = False
