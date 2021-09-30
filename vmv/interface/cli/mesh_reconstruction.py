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

# System imports
import sys

# Blender imports
import bpy

import os

# Append the internal modules into the system paths to avoid Blender importing conflicts
import_paths = ['vmv']
for import_path in import_paths:
    sys.path.append(('%s/../../..' % (os.path.dirname(os.path.realpath(__file__)))))

# Internal imports
import vmv
import vmv.builders
import vmv.bbox
import vmv.consts
import vmv.enums
import vmv.file
import vmv.mesh
import vmv.skeleton
import vmv.interface
import vmv.options
import vmv.rendering
import vmv.scene


####################################################################################################
# @reconstruct_vascular_mesh
####################################################################################################
def reconstruct_vascular_mesh(cli_morphology,
                            cli_options):
    """Vascular mesh reconstruction and visualization operations.

    :param cli_morphology:
        The morphology loaded from the command line interface (CLI).
    :param cli_options:
        System options parsed from the command line interface (CLI).
    """

    # Clear the scene
    vmv.scene.ops.clear_scene()

    # PiecewiseWatertightBuilder
    if cli_options.mesh.meshing_technique == vmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:
        builder = vmv.builders.mesh.PiecewiseWatertightBuilder(cli_morphology, cli_options)
        builder.build_mesh()
        return True

    # MetaBall builder
    elif cli_options.mesh.meshing_technique == vmv.enums.Meshing.Technique.META_BALLS:
        builder = vmv.builders.MetaBuilder(cli_morphology, cli_options)
        builder.build_mesh()
        return True

    else:

        # Invalid meshing algorithm
        vmv.logger.log('ERROR: INVALID meshing technique')

        # Return False
        return False


####################################################################################################
# @export_neuron_mesh
####################################################################################################
def export_neuron_mesh(cli_morphology,
                       cli_options):
    """Save the reconstructed neuron mesh to a file.

    :param cli_morphology:
        Morphology object.
    :param cli_options:
        CLI options given by the user.
    """

    # Header
    vmv.logger.header('Exporting mesh')

    # Get a list of all the meshes in the scene
    mesh_objects = vmv.scene.get_list_of_meshes_in_scene()

    if len(mesh_objects) == 0:
        return

    elif len(mesh_objects) == 1:
        mesh_object = mesh_objects

    else:
        mesh_object = vmv.mesh.join_mesh_objects(mesh_objects, cli_morphology.name)

    # OBJ
    if cli_options.mesh.export_obj:
        vmv.file.export_mesh_object(
            mesh_object, cli_options.io.meshes_directory, cli_morphology.name,
        cli_options.mesh.export_obj, cli_options.mesh.export_ply, cli_options.mesh.export_stl,
        cli_options.mesh.export_blend)


####################################################################################################
# @render_vascular_mesh_to_static_frame
####################################################################################################
def render_vascular_mesh_to_static_frame(cli_morphology,
                                       cli_options):
    """Renders a static frame of the reconstructed neuron mesh.

    :param cli_options:
        CLI options.
    :param cli_morphology:
        Original morphology.
    """

    # Header
    vmv.logger.header('Rendering static frame of the neuron mesh')

    # Create the images directory if it does not exist
    if not vmv.file.ops.path_exists(cli_options.io.images_directory):
        vmv.file.ops.create_output_tree(cli_options.io.output_directory)

    # Compute the bounding box for the available meshes only
    bounding_box = vmv.bbox.compute_scene_bounding_box_for_meshes()

    # Get the view prefix
    if cli_options.mesh.camera_view == vmv.enums.Rendering.View.FRONT:
        view_prefix = 'FRONT'
    elif cli_options.mesh.camera_view == vmv.enums.Rendering.View.SIDE:
        view_prefix = 'SIDE'
    elif cli_options.mesh.camera_view == vmv.enums.Rendering.View.TOP:
        view_prefix = 'TOP'
    else:
        view_prefix = 'FRONT'

    # Render at a specific resolution
    if cli_options.mesh.resolution_basis == vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the image
        vmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=cli_options.mesh.camera_view,
            camera_projection=cli_options.mesh.camera_projection,
            image_resolution=cli_options.mesh.full_view_resolution,
            image_name='MESH_%s_%s' % (view_prefix, cli_options.morphology.label),
            image_directory=cli_options.io.images_directory)

    # Render at a specific scale factor
    else:

        # Render the image
        vmv.rendering.render_to_scale(
            bounding_box=bounding_box,
            camera_view=cli_options.mesh.camera_view,
            image_scale_factor=cli_options.mesh.resolution_scale_factor,
            image_name='MESH_%s_%s' % (view_prefix, cli_options.morphology.label),
            image_directory=cli_options.io.images_directory)


####################################################################################################
# @render_mesh_360
####################################################################################################
def render_vascular_mesh_360(cli_options,
                             cli_morphology):
    """Renders a 360 sequence of the reconstructed vascular mesh.

    :param cli_options:
        CLI options.
    :param cli_morphology:
        The original morphology.
    """

    # Header
    vmv.logger.header('Rendering a 360 sequence of the neuron mesh')

    # Create the sequences directory if it does not exist
    if not vmv.file.ops.path_exists(cli_options.io.sequences_directory):
        vmv.file.ops.clean_and_create_directory(cli_options.io.sequences_directory)

    # Render a 360 sequence
    if cli_options.mesh.render_360:

        # Compute the bounding box for a close up view
        if cli_options.mesh.rendering_view == vmv.enums.Meshing.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            bounding_box = vmv.bbox.compute_unified_extent_bounding_box(
                extent=cli_options.mesh.close_up_dimensions)

        # Compute the bounding box for a mid shot view
        elif cli_options.mesh.rendering_view == vmv.enums.Meshing.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            bounding_box = vmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute the bounding box for the wide shot view that correspond to whole morphology
        else:

            # Compute the full morphology bounding box
            bounding_box = vmv.skeleton.compute_full_morphology_bounding_box(
                morphology=cli_morphology)

        # Compute a 360 bounding box to fit the arbors
        bounding_box_360 = vmv.bbox.compute_360_bounding_box(bounding_box,
                                                             cli_morphology.soma.centroid)

        # Stretch the bounding box by few microns
        bounding_box_360.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        output_directory = '%s/%s_mesh_360' % (
            cli_options.io.sequences_directory, cli_options.morphology.label)
        vmv.file.ops.clean_and_create_directory(output_directory)

        # Get a list of all the meshes in the scene
        scene_meshes = vmv.scene.get_list_of_meshes_in_scene()

        # Render 360
        for i in range(360):

            # Set the frame name
            image_name = '%s/%s' % (output_directory, '{0:05d}'.format(i))

            # Render at a specific resolution
            if cli_options.mesh.resolution_basis == \
                    vmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

                # Render the image
                vmv.rendering.renderer.render_at_angle(
                    scene_objects=scene_meshes,
                    angle=i,
                    bounding_box=bounding_box_360,
                    camera_view=vmv.enums.Camera.View.FRONT_360,
                    image_resolution=cli_options.mesh.full_view_resolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                vmv.rendering.renderer.render_at_angle_to_scale(
                    scene_objects=scene_meshes,
                    angle=i,
                    bounding_box=bounding_box_360,
                    camera_view=vmv.enums.Camera.View.FRONT_360,
                    image_scale_factor=cli_options.mesh.resolution_scale_facto,
                    image_name=image_name)


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Ignore blender extra arguments required to launch blender given to the command line interface
    args = sys.argv
    sys.argv = args[args.index("--") + 1:]

    # Parse the command line arguments, filter them and report the errors
    arguments = vmv.interface.cli.parse_command_line_arguments()

    # Verify the output directory before screwing things !
    if not vmv.file.ops.path_exists(arguments.output_directory):
        vmv.logger.log('ERROR: Please set the output directory to a valid path')
        exit(0)
    else:
        print('      * Output will be generated to [%s]' % arguments.output_directory)

    # Get the options from the arguments
    cli_options = vmv.options.VessMorphoVisOptions()

    # Convert the CLI arguments to system options
    cli_options.consume_arguments(arguments=arguments)

    # Read the morphology
    cli_morphology = None

    # If the input is a morphology file, then use the parser to load it directly
    if arguments.input == 'file':

        # Read the morphology file
        loading_flag, cli_morphology = vmv.file.read_morphology_from_file(options=cli_options)

        if not loading_flag:
            vmv.logger.log('ERROR: Cannot load the morphology file [%s]. Terminating!' %
                           str(cli_options.morphology.file_path))
            exit(0)

    else:
        vmv.logger.log('ERROR: Invalid input option')
        exit(0)

    # Vascular mesh reconstruction
    neuron_mesh = reconstruct_vascular_mesh(cli_morphology=cli_morphology, cli_options=cli_options)

    # Saving the mesh
    if cli_options.mesh.export_ply or cli_options.mesh.export_obj or \
       cli_options.mesh.export_stl or cli_options.mesh.export_blend:

        # Export the neuron mesh
        export_neuron_mesh(cli_morphology=cli_morphology, cli_options=cli_options)

    # Render the mesh
    if cli_options.mesh.render:
        render_vascular_mesh_to_static_frame(cli_options=cli_options, cli_morphology=cli_morphology)

    # Render 360 of the mesh
    if cli_options.mesh.render_360:
        render_vascular_mesh_360(cli_options=cli_options, cli_morphology=cli_morphology)


