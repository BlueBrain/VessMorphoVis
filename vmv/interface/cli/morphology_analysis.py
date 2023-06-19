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
import vmv.enums
import vmv.file
import vmv.interface
import vmv.options
import vmv.rendering
import vmv.scene


####################################################################################################
# @analyze_morphology
####################################################################################################
def analyze_morphology_skeleton(cli_morphology,
                                cli_options):
    """Morphology analysis operations.

    :param cli_morphology:
        The morphology loaded from the command line interface (CLI).
    :param cli_options:
        System options parsed from the command line interface (CLI).
    """

    # Register the analysis components, apply the kernel functions and update the UI
    morphology_analysis_flag, analysis_string = vmv.analysis.analyze_morphology(cli_morphology)

    print('Done')
    # Export the analysis result 
    if morphology_analysis_flag:
        
        # Create the analysis directory if it does not exist
        if not vmv.file.ops.path_exists(cli_options.io.analysis_directory):
            vmv.file.ops.vmv.file.ops.create_output_tree(cli_options.io.output_directory)

        # Export the analysis results
        #vmv.interface.ui.export_analysis_results(
        #    morphology=cli_morphology, directory=cli_options.io.analysis_directory)

    else:
        vmv.logger.log('ERROR: Cannot analyze the morphology file [%s]' %
                       cli_options.morphology.label)


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
            vmv.logger.log('ERROR: Cannot load the morphology file [%s]' %
                           str(cli_options.morphology.file_path))
            exit(0)

    else:
        vmv.logger.log('ERROR: Invalid input option')
        exit(0)

    # Morphology analysis
    analyze_morphology_skeleton(cli_morphology=cli_morphology, cli_options=cli_options)