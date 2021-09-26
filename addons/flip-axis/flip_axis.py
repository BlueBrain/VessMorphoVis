#!/usr/bin/python
####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
#               Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# Imports
import os 
import sys 
import glob
import ntpath 
import argparse


####################################################################################################
# @parse_command_line_arguments
####################################################################################################
def parse_command_line_arguments(arguments=None):
    """Parses the input arguments.

    :param arguments:
        Command line arguments.
    :return:
        Arguments list.
    """

    # add all the options
    description = 'Flipping the Y-axis of the BraVa datasets'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'An input morphology'
    parser.add_argument('--morphology-directory',
                        action='store', dest='morphology_directory', help=arg_help)

    arg_help = 'Output directory where the generated morphologies will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)
                        
    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    
    # Parse the command line arguments
    args = parse_command_line_arguments()

    if args.morphology_directory is None:
        print('None morphology directory, please specify valid input directory')
        exit(0)

    if args.output_directory is None:
        print('None output directory, please specify valid output directory')
        exit(0)

    # Getting all the files 
    morphologies = glob.glob('%s/*.swc' % args.morphology_directory)

    # Do it one by one 
    for morphology in morphologies:
        
        # Store the data in a list 
        data_list = list()

        # Open the file 
        swc_file = open(morphology, 'r')

        # Store every line 
        for line in swc_file:

            # Ignore comments 
            if '#' in line:
                continue

            # Split 
            data = ' '.join(line.split())
            data = data.split(' ')
            
            if len(data) == 0:
                continue

            # The Y-axis is element number 3 in the list
            data[3] = str(float(data[3]) * -1)

            # Add to the data list 
            data_list.append(data)
        
        # Close the file
        swc_file.close()

        # Write the output file
        output_file =  '%s/%s' % (args.output_directory, ntpath.basename(morphology))

        # Store the file 
        swc_file = open(output_file, 'w')

        for sample in data_list:

            # Make the sample 
            string = ''
            for element in sample:
                string += element + ' '
            
            # New line 
            string += '\n'

            # Add it to the file
            swc_file.write(string)
        
        # Close the file 
        swc_file.close()