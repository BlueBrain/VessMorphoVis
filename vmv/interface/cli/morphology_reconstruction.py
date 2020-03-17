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
import vmv.consts
import vmv.bbox
import vmv.enums
import vmv.file
import vmv.skeleton
import vmv.interface
import vmv.options
import vmv.rendering
import vmv.scene


####################################################################################################
# @proceed_morphology_reconstruction_visualization
####################################################################################################
def reconstruct_neuron_morphology(cli_morphology,
                                  cli_options):
    """Morphology reconstruction and visualization operations.

    :param cli_morphology:
        The morphology loaded from the command line interface (CLI).
    :param cli_options:
        System options parsed from the command line interface (CLI).
    """

    # Clear the scene
    vmv.scene.ops.clear_scene()

    cli_options.morphology.connect_to_soma = True

    # Skeleton builder
    skeleton_builder = vmv.builders.SkeletonBuilder(morphology=cli_morphology,
                                                    options=cli_options)

    # Reconstruct the reconstructed morphology skeleton
    morphology_skeleton_objects = skeleton_builder.draw_morphology_skeleton()

    # Export to .BLEND file
    if cli_options.morphology.export_blend:
        # Export the morphology to a .BLEND file, None indicates all components the scene
        vmv.file.export_mesh_object(
            None, cli_options.io.morphologies_directory, cli_morphology.label,
            blend=cli_options.morphology.export_blend)

    # Render a static image of the reconstructed morphology skeleton
    if cli_options.morphology.render:

        # Compute the bounding box for a close up view
        if cli_options.morphology.rendering_view == \
                vmv.enums.Skeleton.Rendering.View.CLOSE_UP_VIEW:

            # Compute the bounding box for a close up view
            bounding_box = vmv.bbox.compute_unified_extent_bounding_box(
                extent=cli_options.morphology.close_up_dimensions)

        # Compute the bounding box for a mid shot view
        elif cli_options.morphology.rendering_view == \
                vmv.enums.Skeleton.Rendering.View.MID_SHOT_VIEW:

            # Compute the bounding box for the available meshes only
            bounding_box = vmv.bbox.compute_scene_bounding_box_for_curves()

        # Compute the bounding box for the wide shot view that correspond to the whole morphology
        else:

            # Compute the full morphology bounding box
            bounding_box = vmv.skeleton.compute_full_morphology_bounding_box(
                morphology=cli_morphology)

        # Render at a specific resolution
        if cli_options.morphology.resolution_basis == \
                vmv.enums.Skeleton.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the image
            vmv.rendering.NeuronSkeletonRenderer.render(
                bounding_box=bounding_box,
                camera_view=vmv.enums.Camera.View.FRONT,
                image_resolution=cli_options.morphology.full_view_resolution,
                image_name='MORPHOLOGY_FRONT_%s' % cli_morphology.label,
                image_directory=cli_options.io.images_directory)

        # Render at a specific scale factor
        else:

            # Render the image
            vmv.rendering.NeuronSkeletonRenderer.render_to_scale(
                bounding_box=bounding_box,
                camera_view=vmv.enums.Camera.View.FRONT,
                image_scale_factor=cli_options.mesh.resolution_scale_factor,
                image_name='MESH_FRONT_%s' % cli_morphology.label,
                image_directory=cli_options.io.images_directory)

    # Render a 360 sequence of the reconstructed morphology skeleton
    if cli_options.morphology.render_360:
        # TODO: implement this option
        pass

    # Render a sequence of the progressive reconstruction of the morphology skeleton
    if cli_options.morphology.render_progressive:
        # TODO: implement this option
        pass


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
        print('Output: [%s]' % arguments.output_directory)

    # Get the options from the arguments
    cli_options = vmv.options.NeuroMorphoVisOptions()

    # Convert the CLI arguments to system options
    cli_options.consume_arguments(arguments=arguments)

    # Read the morphology
    cli_morphology = None

    # If the input is a GID, then open the circuit and read it
    if arguments.input == 'gid':

        # Load the morphology from the file
        loading_flag, cli_morphology = vmv.file.BBPReader.load_morphology_from_circuit(
            blue_config=cli_options.morphology.blue_config,
            gid=cli_options.morphology.gid)

        if not loading_flag:
            vmv.logger.log('ERROR: Cannot load the GID [%s] from the circuit [%s]' %
                           cli_options.morphology.blue_config, str(cli_options.morphology.gid))
            exit(0)

    # If the input is a morphology file, then use the parser to load it directly
    elif arguments.input == 'file':

        # Read the morphology file
        loading_flag, cli_morphology = vmv.file.read_morphology_from_file(options=cli_options)

        if not loading_flag:
            vmv.logger.log('ERROR: Cannot load the morphology file [%s]' %
                           str(cli_options.morphology.morphology_file_path))
            exit(0)

    else:
        vmv.logger.log('ERROR: Invalid input option')
        exit(0)

    # TODO: Implement the render_soma_two_dimensional_profile() function
    # render_soma_two_dimensional_profile(cli_morphology=cli_morphology, cli_options=cli_options)

    # Neuron morphology reconstruction and visualization
    reconstruct_neuron_morphology(cli_morphology=cli_morphology, cli_options=cli_options)
    vmv.logger.log('NMV Done')


