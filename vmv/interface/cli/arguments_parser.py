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
import argparse, os, sys
from argparse import RawTextHelpFormatter


# Internal imports
sys.path.append("%s/" % os.path.dirname(os.path.realpath(__file__)))
from args import *


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments():
    """Parse the command line arguments.

    NOTE: We do not define a destination to facilitate printing to a string and doing another
    iteration of parsing for blender.

    :return:
        A structure with all the system options.
    """

    # Create an argument parser, and then add the options one by one
    app_help = 'VessMorphoVis: Visualization of vascular morphologies'
    parser = argparse.ArgumentParser(description=app_help, formatter_class=RawTextHelpFormatter)

    ################################################################################################
    # Blender arguments
    ################################################################################################
    blender_args = parser.add_argument_group('Blender', 'Blender')

    # Blender executable path, by default we will use the one installed on the system
    arg_help = 'Blender executable \n' \
               'Default: blender, system installed: sudo apt-get install blender'
    blender_args.add_argument(
        Args.BLENDER_EXECUTABLE,
        action='store', default='blender',
        help=arg_help)

    ################################################################################################
    # Input arguments
    ################################################################################################
    input_args = parser.add_argument_group('Input', 'Input')

    # Input source (morphology file, or a directory containing a group of morphologies)
    arg_options = ['file', 'directory']
    arg_help = 'Input morphology sources. \n'\
               'Options: %s' % arg_options
    input_args.add_argument(
        Args.INPUT_SOURCE,
        action='store', default='gid',
        help=arg_help)

    # Morphology file
    arg_help = 'Morphology file (.H5 or .VMV)'
    input_args.add_argument(
        Args.MORPHOLOGY_FILE,
        action='store', default=None,
        help=arg_help)

    # Morphology directory
    arg_help = 'Morphology directory containing (.H5 or .SWC) files'
    input_args.add_argument(
        Args.MORPHOLOGY_DIRECTORY,
        action='store', default=None,
        help=arg_help)

    ################################################################################################
    # Output arguments
    ################################################################################################
    output_args = parser.add_argument_group('Output', 'Output')

    # Output directory
    arg_help = 'Root output directory'
    output_args.add_argument(
        Args.OUTPUT_DIRECTORY,
        action='store', default=None,
        help=arg_help)

    ################################################################################################
    # Analysis and meta-data generation
    ################################################################################################
    analysis_args = parser.add_argument_group('Analysis', 'Analysis')

    # Morphology analysis
    arg_help = 'Analyze the morphology skeleton and report the artifacts.'
    analysis_args.add_argument(
        Args.ANALYZE_MORPHOLOGY,
        action='store_true', default=False,
        help=arg_help)


    ################################################################################################
    # Morphology arguments
    ################################################################################################
    skeletonization_args = parser.add_argument_group('Morphology Skeleton', 'Morphology Skeleton')

    # Reconstruct the morphology of entire vascular
    arg_help = 'Reconstruct morphology skeleton for visualization or analysis.'
    skeletonization_args.add_argument(
        Args.RECONSTRUCT_MORPHOLOGY_SKELETON,
        action='store_true', default=False,
        help=arg_help)

    # Morphology reconstruction algorithm
    arg_options = '[\'connected-sections\', \n' \
                  '\t  \'(connected-sections-repaired)\', \n' \
                  '\t  \'disconnected-sections\', \n' \
                  '\t  \'disconnected-segments\', \n' \
                  '\t  \'articulated-sections\']'
    arg_help = 'Morphology reconstruction algorithm. \n' \
               'Options: %s' % arg_options
    skeletonization_args.add_argument(
        Args.MORPHOLOGY_RECONSTRUCTION_ALGORITHM,
        action='store', default='connected-sections',
        help=arg_help)

    # Morphology skeleton
    arg_options = ['(original)', 'tapered', 'zigzag', 'tapered-zigzag']
    arg_help = 'Morphology skeleton style. \n' \
               'Options: %s' % arg_options
    skeletonization_args.add_argument(
        Args.MORPHOLOGY_SKELETON,
        action='store', default='original',
        help=arg_help)

    # Section radii (default, scaled or fixed)
    arg_options = ['(default)', 'scaled', 'fixed']
    arg_help = 'The radii of the morphological sections.\n' \
               'Options: %s' % arg_options
    skeletonization_args.add_argument(
        Args.SECTIONS_RADII,
        action='store', default='default',
        help=arg_help)

    # Section radii scale factor
    arg_help = 'A scale factor used to scale the radii of the morphology.\n' \
               'Valid only if --sections-radii = scaled.\n' \
               'Default is 1.0'
    skeletonization_args.add_argument(
        Args.RADII_SCALE_FACTOR,
        action='store', type=float, default=1.0,
        help=arg_help)

    # Section fixed radius (to enlarge the thin branches)
    arg_help = 'A fixed radius for all morphology sections.\n'\
               'Valid only if --sections-radii = fixed.\n' \
               'Default is 1.0'
    skeletonization_args.add_argument(
        Args.FIXED_SECTION_RADIUS,
        action='store', type=float, default=1.0,
        help=arg_help)

    # Section minimum radius
    arg_help = 'The minimum radius of a sample in all morphology sections.\n' \
               'Valid only if --sections-radii = minimum.\n' \
               'Default is 1.0'
    skeletonization_args.add_argument(
        Args.MINIMUM_SECTION_RADIUS,
        action='store', type=float, default=1.0,
        help=arg_help)

    # Morphology bevel object sides (sets the quality of the morphology)
    arg_help = 'Number of sides of the bevel object used to reconstruct the morphology. \n' \
               'Default 16 (4: low quality - 64: high quality)'
    skeletonization_args.add_argument(
        Args.MORPHOLOGY_BEVEL_SIDES,
        action='store', type=int, default=16,
        help=arg_help)


    ################################################################################################
    # Materials and colors arguments
    ################################################################################################
    materials_args = parser.add_argument_group('Materials - Colors', 'Materials - Colors')

    # Morphology color
    arg_help = 'Morphology color'
    materials_args.add_argument(
        Args.MORPHOLOGY_COLOR,
        action='store', default='1.0_1.0_1.0',
        help=arg_help)

    # Mesh color
    arg_help = 'Mesh color'
    materials_args.add_argument(
        Args.MESH_COLOR,
        action='store', default='0.0_0.0_0.0',
        help=arg_help)

    # Material used to render the vascular
    arg_options = '(lambert) \n' \
                  '\t electron-light \n' \
                  '\t electron-dark \n' \
                  '\t super-electron-light \n' \
                  '\t super-electron-dark \n' \
                  '\t shadow \n' \
                  '\t flat \n' \
                  '\t subsurface-scattering'
    arg_help = 'Shading mode or material. \n' \
               'Options: %s' % arg_options
    materials_args.add_argument(
        Args.SHADER,
        action='store', default='lambert',
        help=arg_help)

    ################################################################################################
    # Meshing arguments
    ################################################################################################
    meshing_args = parser.add_argument_group('Meshing', 'Meshing')

    # Reconstruct the mesh of entire neuron
    arg_help = 'Reconstruct the mesh of the morphology.'
    meshing_args.add_argument(
        Args.RECONSTRUCT_VASCULAR_MESH,
        action='store_true', default=False,
        help=arg_help)

    # Meshing algorithm
    arg_options = ['(piecewise-watertight)', 'skinning', 'meta-balls']
    arg_help = 'Meshing algorithm. \n' \
               'Options: %s' % arg_options
    meshing_args.add_argument(
        Args.NEURON_MESHING_ALGORITHM,
        action='store', default='meta-balls',
        help=arg_help)

    # The edges of the reconstructed meshes
    arg_options = ['smooth', '(hard)']
    arg_help = 'Arbors edges. \n' \
               'This option only applies to the meshes. \n' \
               'Options: %s' % arg_options
    meshing_args.add_argument(
        Args.MESH_EDGES,
        action='store', default='hard',
        help=arg_help)

    # The edges of the reconstructed meshes
    arg_options = ['rough', '(smooth)']
    arg_help = 'The surface roughness of the vascular mesh. \n' \
               'Options: %s' % arg_options
    meshing_args.add_argument(
        Args.MESH_SURFACE,
        action='store', default='smooth',
        help=arg_help)

    # Mesh tessellation level
    arg_help = 'Mesh tessellation factor between (0.1, 1.0).\n' \
               'Default 1.0.'
    meshing_args.add_argument(
        Args.MESH_TESSELLATION_LEVEL,
        action='store', type=float, default=1.0,
        help=arg_help)

    # MetaBalls resolution setting
    arg_options = ['(auto)', 'user-defined']
    arg_help = 'This parameter defines how the MetaBalls resolution is set.\n' \
               'Options: %s' % arg_options
    meshing_args.add_argument(
        Args.META_BALLS_RESOLUTION_SETTING,
        action='store', default='auto',
        help=arg_help)

    # User-defined MetaBalls resolution value
    arg_help = 'MetaBalls resolution value.\n' \
               'Default 2.0.'
    meshing_args.add_argument(
        Args.META_BALLS_RESOLUTION,
        action='store', type=float, default=2.0,
        help=arg_help)

    ################################################################################################
    # Geometry export arguments
    ################################################################################################
    export_args = parser.add_argument_group(
        'Export Options',
        'You can export morphology skeletons or reconstructed meshes in various \n'
        'file formats.')

    # Export the morphologies in .SWC format
    arg_help = 'Exports the morphology to (.SWC) file. \n'
    export_args.add_argument(
        Args.EXPORT_VMV_MORPHOLOGY,
        action='store_true', default=False,
        help=arg_help)

    # Export the morphologies in .H5 format (after fixing the artifacts)
    arg_help = 'Exports the morphology to (.H5) file. \n'
    export_args.add_argument(
        Args.EXPORT_H5_MORPHOLOGY,
        action='store_true', default=False,
        help=arg_help)

    # Export the morphology as a Blender file in .BLEND format
    arg_help = 'Exports the morphology as a Blender file (.BLEND).'
    export_args.add_argument(
        Args.EXPORT_BLEND_MORPHOLOGY,
        action='store_true', default=False,
        help=arg_help)

    # Export the meshes in .PLY format
    arg_help = 'Exports the vascular mesh to (.PLY) file.'
    export_args.add_argument(
        Args.EXPORT_PLY_MESH,
        action='store_true', default=False,
        help=arg_help)

    # Export the vascular mesh in .OBJ format
    arg_help = 'Exports the vascular mesh to (.OBJ) file.'
    export_args.add_argument(
        Args.EXPORT_OBJ_MESH,
        action='store_true', default=False,
        help=arg_help)

    # Export the vascular mesh in .STL format
    arg_help = 'Exports the vascular mesh to (.STL) file.'
    export_args.add_argument(
        Args.EXPORT_STL_MESH,
        action='store_true', default=False,
        help=arg_help)

    # Export the vascular mesh in .BLEND format
    arg_help = 'Exports the vascular mesh as a Blender file (.BLEND).'
    export_args.add_argument(
        Args.EXPORT_BLEND_MESH,
        action='store_true', default=False,
        help=arg_help)

    # Export the vascular mesh in .BLEND format
    arg_help = 'Exports each part (or component) of the vascular mesh as separate mesh.'
    export_args.add_argument(
        Args.EXPORT_INDIVIDUALS,
        action='store_true', default=False,
        help=arg_help)

    ################################################################################################
    # Rendering arguments
    ################################################################################################
    rendering_args = parser.add_argument_group('Rendering', 'Rendering')

    # Render morphology
    arg_help = 'Render image of the morphology skeleton.'
    rendering_args.add_argument(
        Args.RENDER_VASCULAR_MORPHOLOGY,
        action='store_true', default=False,
        help=arg_help)

    # Render morphology 360 sequence
    arg_help = 'Render a 360 sequence of the morphology skeleton.'
    rendering_args.add_argument(
        Args.RENDER_VASCULAR_MORPHOLOGY_360,
        action='store_true', default=False,
        help=arg_help)

    # Render mesh
    arg_help = 'Render an image of the reconstructed vascular mesh.'
    rendering_args.add_argument(
        Args.RENDER_VASCULAR_MESH,
        action='store_true', default=False,
        help=arg_help)

    # Render morphology close up
    arg_help = 'Render a 360 sequence of the reconstructed vascular mesh.'
    rendering_args.add_argument(
        Args.RENDER_VASCULAR_MESH_360,
        action='store_true', default=False,
        help=arg_help)

    # Render mesh to scale (i.e. resolution is equivalent to size in microns)
    arg_help = 'Render the skeleton to scale.'
    rendering_args.add_argument(
        Args.RENDER_TO_SCALE,
        action='store_true', default=False,
        help=arg_help)

    # Rendering view
    arg_options = ['close-up', 'mid-shot', '(wide-shot)']
    arg_help = 'The rendering view of the skeleton for the skeleton. \n' \
               'Options: %s' % arg_options
    rendering_args.add_argument(
        Args.RENDERING_VIEW,
        action='store', default='wide-shot',
        help=arg_help)

    # Rendering view
    arg_options = ['(front)', 'side', 'top']
    arg_help = 'The camera direction. \n' \
               'Options: %s' % arg_options
    rendering_args.add_argument(
        Args.CAMERA_VIEW,
        action='store', default='front',
        help=arg_help)

    # Rendering projection
    arg_options = ['(orthographic)', 'perspective']
    arg_help = 'The camera projection. \n' \
               'Options: %s' % arg_options
    rendering_args.add_argument(
        Args.CAMERA_PROJECTION,
        action='store', default='orthographic',
        help=arg_help)

    # Full view resolution
    arg_help = 'Base resolution of full view images (wide-shot or mid-shot). \n' \
               'Default 1024.'
    rendering_args.add_argument(
        Args.FULL_VIEW_RESOLUTION,
        action='store', type=int, default=1024,
        help=arg_help)

    # Full view scale factor
    arg_help = 'A factor used to scale the resolution of the image. \n' \
               'Valid only if --render--to-scale is set. \n' \
               'Default 1.'
    rendering_args.add_argument(
        Args.RESOLUTION_SCALE_FACTOR,
        action='store', type=float, default=1.0,
        help=arg_help)

    ################################################################################################
    # Execution arguments
    ################################################################################################
    execution_args = parser.add_argument_group('Execution', 'Execution')

    # Execution node
    arg_options = ['(local)', 'cluster']
    arg_help = 'Execution is local or using cluster nodes. \n' \
               'Options: %s' % arg_options
    execution_args.add_argument(
        Args.EXECUTION_NODE,
        action='store', default='local',
        help=arg_help)

    # Execution cores
    arg_help = 'Number of execution cores on cluster. \n' \
               'Default 256.'
    execution_args.add_argument(
        Args.NUMBER_CORES,
        action='store', type=int, default=256,
        help=arg_help)

    # Job granularity
    arg_options = ['high', '(low)']
    arg_help = 'The granularity of the jobs running on the cluster. \n' \
               'Options: %s' % arg_options
    execution_args.add_argument(
        Args.JOB_GRANULARITY,
        action='store', default='low',
        help=arg_help)

    # Parse the arguments, and return a list of them
    return parser.parse_args()


####################################################################################################
# @get_arguments_string_as_list
####################################################################################################
def get_arguments_string_as_list(arguments):
    """Convert the system parsed arguments into a list of strings to be given to an instance when
    we use the cluster to launch parallel jobs.

    :param arguments:
        Parsed arguments.
    :return:
        A list of all the arguments that were originally given to the system.
    """

    # A list of all the arguments that were originally given to the system.
    arguments_string = []

    # Compose the arguments string list
    for arg in vars(arguments):

        # Make the argument name by replacing the '_' with a '-'
        arg_option_name = arg.replace('_', '-')

        # Get the argument value
        arg_value = getattr(arguments, arg)

        # Ignore the unset flags
        if arg_value is False:
            continue

        elif arg_value is True:
            arguments_string.append('--%s ' % arg_option_name)
        else:

            # Add them to the argument string, and prepend the argument with '--'
            arguments_string.append('--%s=%s ' % (arg_option_name, arg_value))

    return arguments_string


####################################################################################################
# @get_arguments_string
####################################################################################################
def get_arguments_string(arguments):
    """Convert the system parsed arguments into a stream of strings to be given to an instance when
    we use the cluster to launch parallel jobs.

    :param arguments:
        System parsed arguments.
    :return:
        A string of all the arguments that were originally given to the system.
    """

    # A string of all the arguments that were originally given to the system.
    arguments_string = ''

    # Get the arguments string list
    arguments_string_list = get_arguments_string_as_list(arguments=arguments)

    # Compose the arguments string
    for string in arguments_string_list:
        arguments_string += string

    # Return the arguments string
    return arguments_string


####################################################################################################
# @get_arguments_string_for_individual_file
####################################################################################################
def get_arguments_string_for_individual_file(arguments,
                                             morphology_file):
    """Get the arguments string for an individual morphology file by replacing the --input to file
    and update the --morphology-file option.

    :param arguments:
        Parsed arguments
    :param morphology_file:
        Input morphology file.
    :return:
        A string of the updated arguments.
    """

    # Get the arguments string list
    arguments_string_list = get_arguments_string_as_list(arguments=arguments)

    # Replace the input argument
    for i, argument in enumerate(arguments_string_list):
        if '--input=' in argument:
            arguments_string_list[i] = '--input=file '

    # Add the absolute path of the file
    arguments_string_list.append('--morphology-file=%s/%s' % (
        arguments.morphology_directory, morphology_file))

    # Compose the arguments string
    arguments_string = ''
    for string in arguments_string_list:
        arguments_string += '\t' + string + ' '

    print(arguments_string)

    # Return the arguments string
    return arguments_string


####################################################################################################
# @create_shell_commands
####################################################################################################
def create_shell_commands(arguments,
                          arguments_string):
    """Creates a list of all the shell commands that are needed to run the different tasks set
    in the configuration file.

    :param arguments:
        Input arguments.
    :param arguments_string:
        A string that will be given to each CLI command.
    :return:
        A list of commands to be appended to the SLURM scripts or directly executed on a local node.
    """

    shell_commands = list()

    # Retrieve the path to the CLIs
    cli_interface_path = os.path.dirname(os.path.realpath(__file__))
    cli_morphology_reconstruction = '%s/morphology_reconstruction.py' % cli_interface_path
    cli_morphology_analysis = '%s/analysis.py' % cli_interface_path
    cli_mesh_reconstruction = '%s/mesh_reconstruction.py' % cli_interface_path

    # Morphology analysis task: call the @cli_morphology_analysis interface
    if arguments.analyze_morphology:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_morphology_analysis, arguments_string))

    # Morphology reconstruction task: call the @cli_morphology_reconstruction interface
    if arguments.reconstruct_morphology_skeleton or         \
       arguments.render_vascular_morphology or                \
       arguments.render_vascular_morphology_360 or            \
       arguments.export_morphology_vmv or                   \
       arguments.export_morphology_h5 or                    \
       arguments.export_morphology_blend:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_morphology_reconstruction, arguments_string))
        
    # Neuron mesh reconstruction related task: call the @cli_mesh_reconstruction interface
    if arguments.reconstruct_neuron_mesh or                 \
       arguments.render_neuron_mesh or                      \
       arguments.render_neuron_mesh_360 or                  \
       arguments.export_neuron_mesh_ply or                  \
       arguments.export_neuron_mesh_obj or                  \
       arguments.export_neuron_mesh_stl or                  \
       arguments.export_neuron_mesh_blend:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_mesh_reconstruction, arguments_string))

    # Return a list of commands
    return shell_commands


####################################################################################################
# @create_executable_for_single_morphology_file
####################################################################################################
def create_executable_for_single_morphology_file(arguments,
                                                 morphology_file):
    """Create an EXECUTABLE command for processing a single morphology file in a directory.

    :param arguments:
        Command line arguments.
    :param morphology_file:
        The path to the morphology file.
    :return:
        An executable shell command to call NeuroMorphoVis for a single morphology file.
    """

    # Format a string with blender arguments
    arguments_string = get_arguments_string_for_individual_file(arguments, morphology_file)

    # Create the shell commands and return it
    return create_shell_commands(arguments=arguments, arguments_string=arguments_string)




