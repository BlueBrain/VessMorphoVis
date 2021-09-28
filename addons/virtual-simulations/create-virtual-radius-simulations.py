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
import argparse
import os
import random
import ntpath


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
    description = 'Creates VMV datasets with random radius fluctuations to test the simulation.'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'An input VMV morphology file.'
    parser.add_argument('--morphology',
                        action='store', dest='morphology', help=arg_help)

    arg_help = 'Output directory where the generated results will be written to.'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    arg_help = 'The number of steps in the simulation file.'
    parser.add_argument('--steps',
                        action='store', dest='steps', type=int, default=10, help=arg_help)

    arg_help = 'The percentage of radius variations with respect to time.'
    parser.add_argument('--variation',
                        action='store', dest='variation', type=float, default=10.0, help=arg_help)
                        
    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @read_vmv_file
####################################################################################################
def read_vmv_file(file_path):
    """Reads a given VMV file.

    :param file_path:
        A given VMV file path.
    :return
        The VMV vertex and strand lists inn order
    """

    # Open the morphology file
    file_handler = open(file_path, 'r')

    # Initialize the data size
    number_vertices = 0
    number_strands = 0
    number_attributes_per_vertex = 0

    # Parse the file into a list where it would make it easier to search
    data = list()

    # Get the data sizes from the file
    for line in file_handler:

        # Ignore empty lines
        if not line.strip():
            continue

        # Replace multiple spaces with a single space
        line = ' '.join(line.split())

        # Replace the '\n' with empty
        line = line.replace('\n', '')

        # Add the filtered line to the data list
        data.append(line)

    # Close the file
    file_handler.close()

    # Make sure that the data has all the mandatory fields
    if '$PARAM_BEGIN' in data and '$PARAM_END' in data and \
       '$VERT_LIST_BEGIN' in data and '$VERT_LIST_END' in data and \
       '$STRANDS_LIST_BEGIN' in data and '$STRANDS_LIST_END' in data:
        print('Data set is valid')
    else:
        print('Data set is NOT valid')

    # Get the number of vertices
    for item in data:
        if 'NUM_VERTS' in item:
            item = item.split(' ')
            number_vertices = int(item[1])
            break

    # Get the number of strands
    for item in data:
        if 'NUM_STRANDS' in item:
            item = item.split(' ')
            number_strands = int(item[1])
            break

    # Log
    print('Data contains [%d] vertices, [%d] strands' % (number_vertices, number_strands))

    # If all the sizes are read, simply break and close the file
    if number_vertices == 0 or number_strands == 0:
        print('Invalid data set')
        exit(0)

    # Read the vertices by getting the index of the $VERT_LIST_BEGIN tag
    starting_vertex_index = 0
    for item in data:
        if '$VERT_LIST_BEGIN' in item:

            # Further increment to jump directly to the actual starting index and break
            starting_vertex_index += 1
            break

        # Increment the vertex index
        starting_vertex_index += 1

    # End vertex index
    end_vertex_index = starting_vertex_index + number_vertices

    # Vertex list
    vmv_vertices = list()
    for i in range(starting_vertex_index, end_vertex_index):
        # Split the entry
        vertex_entry = data[i].split(' ')

        index = int(vertex_entry[0])
        x = float(vertex_entry[1])
        y = float(vertex_entry[2])
        z = float(vertex_entry[3])
        radius = float(vertex_entry[4])

        # Add this point to the points list with the position and radius
        vmv_vertices.append([index, x, y, z, radius])

    # Read the strands by getting the index of the STRANDS_LIST_BEGIN tag
    starting_strand_index = 0
    for item in data:
        if '$STRANDS_LIST_BEGIN' in item:
            # Further increment to jump directly to the actual starting index and break
            starting_strand_index += 1
            break

        # Increment the vertex index
        starting_strand_index += 1

    # End strand index
    end_strand_index = starting_strand_index + number_strands

    # Strands list
    vmv_strands = list()
    for i in range(starting_strand_index, end_strand_index):

        # Split the entry
        strand_entry = data[i].split(' ')

        # Get the index
        strand_index = int(strand_entry[0])

        # Remove the item at the first index that accounts for the strand index to end up
        # with the list of points along the strand
        strand_entry.remove(strand_entry[0])

        # Construct the samples list along the strand
        strand = list()
        for vertex_index in strand_entry:
            strand.append(int(vertex_index))

        vmv_strands.append([strand_index, strand])

    return vmv_vertices, vmv_strands


####################################################################################################
# @create_virtual_radius_variations
####################################################################################################
def create_virtual_radius_variations(vertex_list,
                                     maximum_variation,
                                     number_time_steps):
    """This function will take a list of vertices and create a dummy simulation out of it. The
    resulting simulations will be a list with the same structure and N time steps.

    :param vertex_list:
        A given vertex list.
    :param maximum_variation:
        Maximum radius variation.
    :param number_time_steps:
        Number of simulation steps.
    :return
        A list of lists, where each item in the list accounts for a simulation time step and each
        sublist has the same structure of the input list.
    """

    # A list of variations
    variations_list = list()

    # For every frame
    for i in range(number_time_steps):

        # The time frame
        time_frame = list()

        # The first time frame
        if i == 0:

            # For every vertex
            for vertex in vertex_list:

                # Get the initial radius of the vertex
                value = vertex[4] + vertex[4] * (random.uniform(-1 * maximum_variation, maximum_variation)) * 0.01
                if value < 0: value = 0.1
                time_frame.append(value)

        else:

            previous_time_frame = variations_list[i - 1]

            # For every vertex
            for vertex in previous_time_frame:

                value = vertex + vertex * (
                    random.uniform(-1 * maximum_variation, maximum_variation)) * 0.01
                if value < 0: value = 0.1
                # Get the initial radius of the vertex
                time_frame.append(value)
        # Add the time frame to the simulation list
        variations_list.append(time_frame)

    # Return a reference to the simulation data
    return variations_list


####################################################################################################
# @create_vmv_radius_variation_string
####################################################################################################
def create_vmv_radius_variation_string(vertex_list,
                                       radius_variations_list):

    # First line
    string = '$RADIUS_SIMULATION_BEGIN\n'

    # For every vertex
    for vertex in vertex_list:
        vertex_index = vertex[0]

        # For every frame
        for i in range(len(radius_variations_list)):

            # Construct the string
            string += '%2.2f ' % (radius_variations_list[i][vertex_index - 1])

        string += '\n'

    # Last line
    string += '$RADIUS_SIMULATION_END\n\n'

    # Return the strands string
    return string


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
    for strand in strands:
        string += '%d ' % strand[0]

        for vertex in strand[1]:
            string += '%d ' % vertex
        string += '\n'

    # Last line
    string += '$STRANDS_LIST_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @create_vmv_vertex_string
####################################################################################################
def create_vmv_vertex_string(vertex_list):
    """Creates the VMV vertex string from the data list.

    :param vertex_list:
        Vertex list.
    :return:
        VMV vertex string.
    """

    # First line
    string = '$VERT_LIST_BEGIN\n'

    # Strands
    for i, vertex in enumerate(vertex_list):

        # Construct the string
        string += '%d\t%2.2f\t%2.2f\t%2.2f\t%2.2f\n' % (vertex[0],
                                                        vertex[1], vertex[2], vertex[3],
                                                        vertex[4])

    # Last line
    string += '$VERT_LIST_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @create_vmv_header_string
####################################################################################################
def create_vmv_header_string(vertex_list,
                             strand_list,
                             simulation_time_steps):
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

    # Number of vertices
    string += '%s\t%d\n' % ('NUM_VERTS', len(vertex_list))

    # Number of strands
    string += '%s\t%d\n' % ('NUM_STRANDS', len(strand_list))

    # Radius simulation time steps
    string += '%s\t%d\n' % ('RADIUS_SIMULATION_TIME_STEPS', simulation_time_steps)

    # First line
    string += '$PARAM_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @write_vmv_data_with_radius_variations_to_file
####################################################################################################
def write_vmv_data_with_radius_variations_to_file(file_name,
                                                  output_path,
                                                  vertex_list,
                                                  strand_list,
                                                  radius_variations_list):
    """Creates the VMV string that accounts for the data in the VMV format.

    :param file_name:
        The output file name.
    :param output_path:
        The output path.
    :param vertex_list:
        Vertex list.
    :param strand_list:
        Strand list.
    :param radius_variations_list:
        The radius variations list.
    """

    # Header
    vmv_string = create_vmv_header_string(vertex_list=vertex_list, strand_list=strand_list,
                                          simulation_time_steps=len(radius_variations_list))

    # Create the vertex string
    vmv_string += create_vmv_vertex_string(vertex_list=vertex_list)

    # Create the strands string
    vmv_string += create_vmv_strands_string(strands=strand_list)

    # Creates the radius variations string
    vmv_string += create_vmv_radius_variation_string(
        vertex_list=vertex_list, radius_variations_list=radius_variations_list)

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

    if not os.path.exists(args.morphology):
        print('Wrong morphology path, please specify valid input morphology')
        exit(0)

    if not os.path.exists(args.output_directory):
        print('No output directory, please specify valid output directory')
        exit(0)

    # Read the VMV file and return the vertex and strand list
    vertex_list, strand_list = read_vmv_file(file_path=args.morphology)

    # Create the radius variations
    radius_variations = create_virtual_radius_variations(
        vertex_list=vertex_list, maximum_variation=args.variation, number_time_steps=args.steps)

    # Write the radius variations data
    write_vmv_data_with_radius_variations_to_file(
        file_name=ntpath.basename(args.morphology), output_path=args.output_directory,
        vertex_list=vertex_list, strand_list=strand_list, radius_variations_list=radius_variations)

