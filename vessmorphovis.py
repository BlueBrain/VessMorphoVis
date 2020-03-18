#!/usr/bin/python
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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

####################################################################################################

# System imports
import os
import sys
import subprocess

# Append the internal modules into the system paths to avoid Blender importing conflicts
import_paths = ['vmv/interface/cli', 'vmv/file/ops']
for import_path in import_paths:
    sys.path.append(('%s/%s' %(os.path.dirname(os.path.realpath(__file__)), import_path)))
    
# Internal imports
import arguments_parser
import file_ops


####################################################################################################
# @execute_shell_command
####################################################################################################
def execute_shell_command(shell_command):
    subprocess.call(shell_command, shell=True)


####################################################################################################
# @create_shell_commands
####################################################################################################
def create_shell_commands_for_local_execution(arguments,
                                              arguments_string):
    """Creates a list of all the shell commands that are needed to run the different tasks set
    in the configuration file.

    Notes:
        # -b : Blender background mode
        # --verbose : Turn off all the verbose messages
        # -- : Separate the framework arguments from those given to Blender
    :param arguments:
        Input arguments.
    :param arguments_string:
        A string that will be given to each CLI command.
    :return:
        A list of commands to be appended to the SLURM scripts or directly executed on a local node.
    """

    shell_commands = list()

    # Retrieve the path to the CLIs
    cli_interface_path = os.path.dirname(os.path.realpath(__file__)) + '/vmv/interface/cli'
    cli_morphology_reconstruction = '%s/morphology_reconstruction.py' % cli_interface_path
    cli_morphology_analysis = '%s/morphology_analysis.py' % cli_interface_path
    cli_mesh_reconstruction = '%s/mesh_reconstruction.py' % cli_interface_path

    # Morphology analysis task
    if arguments.analyze_morphology:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_morphology_analysis, arguments_string))

        # Return a list of commands
        return shell_commands

    # Morphology reconstruction task: call the @cli_morphology_reconstruction interface
    if arguments.reconstruct_morphology_skeleton or         \
       arguments.render_vascular_morphology or              \
       arguments.render_vascular_morphology_360 or          \
       arguments.export_morphology_vmv or                   \
       arguments.export_morphology_h5 or                    \
       arguments.export_morphology_blend:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_morphology_reconstruction, arguments_string))

    # Neuron mesh reconstruction related task: call the @cli_mesh_reconstruction interface
    if arguments.reconstruct_vascular_mesh or               \
       arguments.render_vascular_mesh or                    \
       arguments.render_vascular_mesh_360 or                \
       arguments.export_vascular_mesh_ply or                \
       arguments.export_vascular_mesh_obj or                \
       arguments.export_vascular_mesh_stl or                \
       arguments.export_vascular_mesh_blend:

        # Add this command to the list
        shell_commands.append('%s -b --verbose 0 --python %s -- %s' %
                              (arguments.blender, cli_mesh_reconstruction, arguments_string))

    # Return a list of commands
    return shell_commands


####################################################################################################
# @run_local_vessmorphovis
####################################################################################################
def run_local_vessmorphovis(arguments):
    """Run the framework on a local node, basically your machine.

    :param arguments:
        Command line arguments.
    """

    # Target and GID options are only available on the BBP visualization clusters
    if arguments.input == 'target' or arguments.input == 'gid':
        print('ERROR, Target and GID options are only available on the BBP visualization clusters')
        exit(0)

    # Load morphology files (.H5 or .SWC)
    elif arguments.input == 'file':

        # Get the arguments string list
        arguments_string = arguments_parser.get_arguments_string(arguments=arguments)

        # NOTE: Using a morphology file, either in .H5 or .SWC formats is straightforward and
        # therefore the arguments will not change at all. In this case it is safe to pass the
        # arguments as they were received without any change.

        # Construct the shell command to run the workflow
        shell_commands = create_shell_commands_for_local_execution(arguments, arguments_string)

        # Run VessMorphoVis from Blender in the background mode
        for shell_command in shell_commands:
            print('RUNNING: ' + shell_command)
            subprocess.call(shell_command, shell=True)

    # Load a directory morphology files (.H5 or .SWC)
    elif arguments.input == 'directory':

        # Get all the morphology files in this directory
        # TODO: Verify the installation of H5Py before running the workflow
        # TODO: Add the support to load .SWC files from a directory at the same time
        morphology_files = file_ops.get_files_in_directory(arguments.morphology_directory, '.h5')

        # If the directory is empty, give an error message
        if len(morphology_files) == 0:
            print('ERROR: The directory [%s] does NOT contain any morphology files' %
                  arguments.morphology_directory)

        # A list of all the commands to be executed
        shell_commands = list()

        # Construct the commands for every individual morphology file
        for morphology_file in morphology_files:

            # Get the argument string for an individual file
            arguments_string = arguments_parser.get_arguments_string_for_individual_file(
                arguments=arguments, morphology_file=morphology_file)

            # Construct the shell command to run the workflow
            shell_commands.extend(
                create_shell_commands_for_local_execution(arguments, arguments_string))

        # Parallel execution
        from joblib import Parallel, delayed
        #import multiprocessing
        #Parallel(n_jobs=6)(
        #    delayed(execute_shell_command)(command) for command in shell_commands)

        # Run VessMorphoVis from Blender in the background mode
        for shell_command in shell_commands:
            # print('RUNNING: ' + shell_command)
            subprocess.call(shell_command, shell=True)

    else:
        print('ERROR: Input data source, use \'file, gid, target or directory\'')
        exit(0)


####################################################################################################
# @run_cluster_vessmorphovis
####################################################################################################
def run_cluster_vessmorphovis(arguments):
    """Run the VessMorphoVis framework on the BBP visualization cluster using SLURM.

    :param arguments:
        Command line arguments.
    """

    # Use the morphology file (.H5 or .VMV)
    if arguments.input == 'file':

        # Get the arguments string list
        arguments_string = arguments_parser.get_arguments_string(arguments=arguments)

        # Run the job on the cluster
        slurm.run_morphology_files_jobs_on_cluster(
            arguments=arguments, morphology_files=arguments.morphology_file)

    # Operate on a directory
    elif arguments.input == 'directory':

        # Get all the morphology files in this directory
        morphology_files = file_ops.get_files_in_directory(arguments.morphology_directory, '.h5')

        # Run the jobs on the cluster
        slurm.run_morphology_files_jobs_on_cluster(
            arguments=arguments, morphology_files=morphology_files)

    else:
        print('ERROR: Input data source, use [file, gid, target or directory]')
        exit(0)


####################################################################################################
# @ Run the main function if invoked from the command line.
####################################################################################################
if __name__ == "__main__":

    # Parse the command line arguments
    arguments = arguments_parser.parse_command_line_arguments()

    # Verify the output directory before screwing things !
    file_ops.create_directory(arguments.output_directory)
    if not file_ops.path_exists(arguments.output_directory):
        print('ERROR: Please set the output directory to a valid path')
        exit(0)

    # Otherwise, create the output tree
    else:
        file_ops.create_output_tree(arguments.output_directory)

    # LOCAL EXECUTION: Compile the corresponding command and launch it on the current machine
    if arguments.execution_node == 'local':
        run_local_vessmorphovis(arguments=arguments)

    # BBP CLUSTER EXECUTION: Create the SLURM scripts and run them on the cluster (only @ BBP)
    else:
        run_cluster_vessmorphovis(arguments=arguments)
