#!/usr/bin/python
####################################################################################################
# Copyright (c) 2021, EPFL / Blue Brain Project
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
    description = 'Converts a list of SWC morphologies from the BraVa database into VMV format'
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
# @raed_swc_data_into_list
####################################################################################################
def raed_swc_data_into_list(morphology_path):
    """
    :param morphology_path:
        The absolute path to the morphology file.
    :return:
        Data parsed from the SWC file.

    NOTE: For further information concerning the structure, please refer to the following
        # http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
        # Each sample in this list has the following structure:
        #       [0] The index of the sample or sample number
        #       [1] The type of the sample or structure identifier
        #       [2] Sample x-coordinates
        #       [3] Sample y-coordinates
        #       [4] Sample z-coordinates
        #       [5] Sample radius
        #       [6] The index of the parent sample
    """

    # Store the data in a list
    data_list = list()

    # Add a ZERO entry to match the indices
    data_list.append([0, 0, 0, 0, 0, 0])

    # Open the file
    swc_file = open(morphology_path, 'r')

    # Store every line
    for line in swc_file:

        # Ignore comments
        if '#' in line:
            continue

        # Ignore empty lines
        if not line.strip():
            continue

        # Extract the data from the line
        data = ' '.join(line.split())
        data = data.strip('\n').split(' ')

        # Empty list
        if len(data) == 0:
            continue

        # If unwanted characters exit, remove them
        for i in data:
            if i == '':
                data.remove(i)
            if '\n' in i:
                i.replace('\n', '')

        # An item in the data list
        data_entry = list()

        # Get the index
        index = int(data[0])
        data_entry.append(index)

        # The sample type is not really needed here, but we just add it for consistency
        sample_type = int(data[1])
        data_entry.append(sample_type)

        # Get the X-coordinate
        x = float(data[2])
        data_entry.append(x)

        # Get the Y-coordinate
        y = float(data[3])
        data_entry.append(y)

        # Get the Z-coordinate
        z = float(data[4])
        data_entry.append(z)

        # Get the sample radius
        radius = float(data[5])
        data_entry.append(radius)

        # Get the sample parent index
        parent_index = int(data[6])
        data_entry.append(parent_index)

        # Add to the data list
        data_list.append(data_entry)

    # Close the file
    swc_file.close()

    # Return a reference to the data list
    return data_list


####################################################################################################
# @convert_swc_data_to_vmv_strands
####################################################################################################
def convert_swc_data_to_vmv_strands(vertex_list):
    """Converts SWC data to a VMV strand list.

    :param vertex_list:
        Vertex list parsed from SWC file.
    :return:
        VMV strand list.
    """

    # A list of strands that will be filled later
    strands = list()

    # Starting from index 1
    index = 1
    while True:

        # This is a single strand only, i.e. single section
        strand = list()

        # Add the first sample (or vertex) along the strand
        strand.append(vertex_list[index])

        # Increment the index
        index += 1

        # Scan the list
        while True:

            # If we have reached the end of the file, then break
            if index > len(vertex_list) - 1:
                break

            # If the parent index is matching the previous index, then append it to the strand
            if vertex_list[index][6] == vertex_list[index - 1][0]:

                # Append the sample to the strand and increment the index
                strand.append(vertex_list[index])
                index += 1

            # Otherwise, append the strand to the list of strand, and break to proceed
            else:
                strands.append(strand)
                break

        # If we have reached the end of the file, then add the last collected strand and break
        if index > len(vertex_list) - 1:

            # Add the last strand
            if len(strand):
                strands.append(strand)
            break

    # Return the vmv data list
    return strands


####################################################################################################
# @create_vmv_strands_string
####################################################################################################
def create_vmv_strands_string(strands):
    """Creates the VMV strand string.

    :param strands:
        VMV strand list.
    :return:
        VMV strand string.
    """

    # First line
    string = '$STRANDS_LIST_BEGIN\n'

    # Strands
    for i, strand in enumerate(strands):
        string += '%d ' % (i + 1)
        for vertex in strand:
            string += '%d ' % vertex[0]
        string += '\n'

    # Last line
    string += '$STRANDS_LIST_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @create_vmv_vertex_string
####################################################################################################
def create_vmv_vertex_string(data_list):
    """Creates the VMV vertex string from the data list.

    :param data_list:
        SWC data list.
    :return:
        VMV vertex string.
    """

    # First line
    string = '$VERT_LIST_BEGIN\n'

    # Strands
    for i, vertex in enumerate(data_list):

        # Skip the first element
        if i == 0:
            continue

        # Construct the string
        string += '%d\t%2.2f\t%2.2f\t%2.2f\t%2.2f\n' % (vertex[0],
                                                        vertex[2], vertex[3], vertex[4],
                                                        vertex[5])

    # Last line
    string += '$VERT_LIST_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @create_vmv_header_string
####################################################################################################
def create_vmv_header_string(vertex_list,
                             strand_list):
    """Creates the VMV vertex string from the data list.

    :param vertex_list:
        Vertex list.
    :param strand_list:
        Strand list.
    :return:
        VMV header string.
    """

    # First line
    string = '$PARAM_BEGIN\n'

    # Number of vertices, we reduce it by 1 to remove the Zero sample
    string += '%s\t%d\n' % ('NUM_VERTS', len(vertex_list) - 1)

    # Number of strands
    string += '%s\t%d\n' % ('NUM_STRANDS', len(strand_list))

    # Number of attributes
    string += '%s\t%d\n' % ('NUM_ATTRIB_PER_VERT', 4)

    # First line
    string += '$PARAM_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @create_vmv_string
####################################################################################################
def create_vmv_string(vertex_list,
                      strand_list):
    """Creates the VMV string that accounts for the data in the VMV format.

    :param vertex_list:
        Vertex list.
    :param strand_list:
        Strand list.
    :return:
        VMV data string.
    """

    # Header
    vmv_string = create_vmv_header_string(vertex_list=vertex_list, strand_list=strand_list)

    # Create the vertex string
    vmv_string += create_vmv_vertex_string(data_list=vertex_list)

    # Create the strands string
    vmv_string += create_vmv_strands_string(strands=strand_list)

    # Return the vmv string
    return vmv_string


####################################################################################################
# @write_vmv_data_to_file
####################################################################################################
def write_vmv_data_to_file(file_name,
                           output_path,
                           swc_data_list):
    """Creates the VMV string that accounts for the data in the VMV format.

    :param file_name:
        The output file name.
    :param output_path:
        The output path.
    :param swc_data_list:
        The data list loaded from the SWC file.
    """

    # Convert the SWC data format into VMV format
    vmv_strands = convert_swc_data_to_vmv_strands(vertex_list=swc_data_list)

    # Data in the vmv format in a string
    vmv_string = create_vmv_string(vertex_list=swc_data_list, strand_list=vmv_strands)

    # Write the output file
    output_file = open('%s/%s' % (output_path, file_name), 'w')
    output_file.write(vmv_string)
    output_file.close()


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    
    # Parse the command line arguments
    args = parse_command_line_arguments()

    if args.morphology_directory is None:
        print('Wrong morphology directory, please specify valid input directory')
        exit(0)

    if args.output_directory is None:
        print('No output directory, please specify valid output directory')
        exit(0)

    # Getting all the files 
    morphologies = glob.glob('%s/*.swc' % args.morphology_directory)

    # Do it one by one 
    for morphology in morphologies:
        
        # Read the SWC file
        swc_data = raed_swc_data_into_list(morphology_path=morphology)

        # Write the VMV data into a file
        write_vmv_data_to_file(file_name=ntpath.basename(morphology).replace('.swc', '.vmv'),
                               output_path=args.output_directory,
                               swc_data_list=swc_data)

