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

# System Imports
import sys

# Internal imports
import vmv
import vmv.options


####################################################################################################
# @VessMorphoVisOptions
####################################################################################################
class VessMorphoVisOptions:
    """Workflow options all combined in a single structure.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Input / output options
        self.io = vmv.options.io_options.IOOptions()

        # Morphology options
        self.morphology = vmv.options.morphology_options.MorphologyOptions()

        # Mesh options
        self.mesh = vmv.options.mesh_options.MeshOptions()

    ################################################################################################
    # @consume_arguments
    ################################################################################################
    def consume_arguments(self,
                          arguments):
        """Convert the command line arguments to options.

        :param arguments:
            Input command line arguments.
        """

        # Internal imports
        import vmv.consts
        import vmv.enums
        import vmv.file
        import vmv.utilities

        ############################################################################################
        # Output options
        ############################################################################################
        # Main output directory
        self.io.output_directory = arguments.output_directory

        # Images directory
        self.io.images_directory = '%s/%s' % (arguments.output_directory,
                                              vmv.consts.Paths.IMAGES_FOLDER)

        # Sequences directory
        self.io.sequences_directory = '%s/%s' % (arguments.output_directory,
                                                 vmv.consts.Paths.SEQUENCES_FOLDER)

        # Meshes directory
        self.io.meshes_directory = '%s/%s' % (arguments.output_directory,
                                              vmv.consts.Paths.MESHES_FOLDER)

        # Morphologies directory
        self.io.morphologies_directory = '%s/%s' % (arguments.output_directory,
                                                    vmv.consts.Paths.MORPHOLOGIES_FOLDER)

        # Morphologies directory
        self.io.analysis_directory = '%s/%s' % (arguments.output_directory,
                                                vmv.consts.Paths.ANALYSIS_FOLDER)

        ############################################################################################
        # Morphology options
        ############################################################################################
        # Morphology reconstruction flag
        self.morphology.reconstruct_morphology = arguments.reconstruct_morphology_skeleton

        # Morphology reconstruction method
        self.morphology.builder = vmv.enums.Morphology.Builder.get_enum(
           argument=arguments.morphology_reconstruction_algorithm)

        # Morphology file
        if arguments.input == 'file':

            # Update the file
            self.morphology.file_path = arguments.morphology_file

            # Update the morphology label
            self.morphology.label = vmv.file.ops.get_file_name_from_path(arguments.morphology_file)

        # Morphology material
        self.morphology.material = vmv.enums.Shader.get_enum(arguments.shader)

        # Morphology color
        self.morphology.color = vmv.utilities.parse_color_from_argument(arguments.morphology_color)

        # Bevel object sides used for the branches reconstruction
        self.morphology.bevel_object_sides = arguments.bevel_sides

        # Sections radii
        self.morphology.radii = vmv.enums.Morphology.Radii.get_enum(arguments.sections_radii)

        # Fixed radius across all the arbors
        self.morphology.sections_fixed_radii_value = arguments.fixed_section_radius

        # Radii scale factor
        self.morphology.sections_radii_scale = arguments.radii_scale_factor

        # Minimum section radius
        self.morphology.sections_radii_minimum = arguments.minimum_section_radius

        # Camera view [FRONT, SIDE or TOP]
        self.morphology.camera_view = vmv.enums.Rendering.View.get_enum(arguments.camera_view)

        # Rendering view
        self.morphology.rendering_view = vmv.enums.Rendering.View.get_enum(
            arguments.rendering_view)

        # Resolution basis
        self.morphology.resolution_basis = vmv.enums.Rendering.Resolution.TO_SCALE if \
            arguments.render_to_scale else vmv.enums.Rendering.Resolution.FIXED_RESOLUTION

        # Render a close up view of the morphology
        self.morphology.render = arguments.render_vascular_morphology

        # Render a close up view of the morphology
        self.morphology.render_360 = arguments.render_vascular_morphology_360

        # Full view image resolution
        self.morphology.full_view_resolution = arguments.full_view_resolution

        # Resolution scale factor
        self.morphology.resolution_scale_factor = arguments.resolution_scale_factor

        # Export the morphology to .h5 file
        self.morphology.export_h5 = arguments.export_morphology_h5

        # Export the morphology to .vmv file
        self.morphology.export_vmv = arguments.export_morphology_vmv

        # Export the morphology skeleton to .blend file for rendering using tubes
        self.morphology.export_blend = arguments.export_morphology_blend

        ############################################################################################
        # Mesh options
        ############################################################################################
        # Reconstruct vascular mesh for exporting
        self.mesh.reconstruct_vascular_mesh = arguments.reconstruct_vascular_mesh

        # Tessellation level (between 0.01 and 1.0)
        self.mesh.tessellation_ratio = float(arguments.tessellation_ratio)

        # Meshing technique
        self.mesh.meshing_technique = vmv.enums.Meshing.Technique.get_enum(
            arguments.meshing_algorithm)

        # MetaBalls resolution setting
        if vmv.enums.Meshing.MetaBalls.get_enum(arguments.meta_balls_resolution_setting) == \
                vmv.enums.Meshing.MetaBalls.AUTO_RESOLUTION:

            # Set the auto resolution
            self.mesh.meta_auto_resolution = True

            # Set to the default resolution for later
            self.mesh.meta_resolution = vmv.consts.Meshing.META_RESOLUTION

        else:

            # Unset the auto resolution
            self.mesh.meta_auto_resolution = False

            # Set the value of the MetaBalls resolution as per given by the user
            self.mesh.meta_resolution = float(arguments.meta_balls_resolution)

        # Edges of the meshes, either hard or smooth
        self.mesh.edges = vmv.enums.Meshing.Edges.get_enum(arguments.edges)

        # Surface
        self.mesh.surface = vmv.enums.Meshing.Surface.get_enum(arguments.surface)

        # Render a static image of the mesh
        self.mesh.render = arguments.render_vascular_mesh

        # Render a 360 sequence of the mesh
        self.mesh.render_360 = arguments.render_vascular_mesh_360

        # Camera view [FRONT, SIDE or TOP]
        self.mesh.camera_view = vmv.enums.Rendering.View.get_enum(arguments.camera_view)

        # Camera view [orthographic or perspective]
        self.mesh.camera_projection = \
            vmv.enums.Rendering.Projection.get_enum(arguments.camera_projection)

        # Rendering view
        self.mesh.rendering_view = vmv.enums.Rendering.View.get_enum(arguments.rendering_view)

        # Resolution basis
        self.mesh.resolution_basis = vmv.enums.Rendering.Resolution.TO_SCALE if \
            arguments.render_to_scale else vmv.enums.Rendering.Resolution.FIXED_RESOLUTION

        # Resolution scale factor
        self.mesh.resolution_scale_factor = arguments.resolution_scale_factor

        # Full view image resolution
        self.mesh.full_view_resolution = arguments.full_view_resolution

        # Mesh material
        self.mesh.material = vmv.enums.Shader.get_enum(arguments.shader)

        # Mesh color
        self.mesh.color = vmv.utilities.parse_color_from_argument(arguments.mesh_color)

        # Save the reconstructed mesh as a .PLY file to the meshes directory
        self.mesh.export_ply = arguments.export_vascular_mesh_ply

        # Save the reconstructed mesh as a .OBJ file to the meshes directory
        self.mesh.export_obj = arguments.export_vascular_mesh_obj

        # Save the reconstructed mesh as a .STL file to the meshes directory
        self.mesh.export_stl = arguments.export_vascular_mesh_stl

        # Save the reconstructed mesh as a .BLEND file to the meshes directory
        self.mesh.export_blend = arguments.export_vascular_mesh_blend
