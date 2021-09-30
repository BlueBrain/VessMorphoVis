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
import sys
import h5py
import glob
import ntpath
import argparse
from vmv_reader import VMVReader


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
    description = 'Converts VMV files into H5 files'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'An input morphology in VMV format'
    parser.add_argument('--morphology-directory',
                        action='store', dest='morphology_directory', help=arg_help)

    arg_help = 'Output directory where the generated H5 morphologies will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)
                        
    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @write_h5_file
####################################################################################################
def write_h5_file(file_name, output_path, vmv):

    # Every item in the h5 strands list will contain only two elements
    h5_strands = list()

    # This list will contain duplicates
    # Logical index, or key, is the h5_vertex index, the value is the vmv_vertex index
    h5_vertices_indices = list()

    # A reference to keep track on the current vertex index
    current_index = 0

    # Iterate over the vmv_strands in the stands list
    for i_strand in range(len(vmv.strands_list)):

        # Simply a reference to the current strand
        strand = vmv.strands_list[i_strand]
        for i in range(len(strand)):
            strand[i] = int(strand[i])

        # If the first strand
        if i_strand == 0:

            # If the first element in the strand is NOT zero
            h5_vertices_indices.append(strand[0])

            # Add to the strand
            h5_strands.append([current_index, 1])

            # Increment the index
            current_index += 1

        # Otherwise compare the terminal vertex of s0 with the first index of s1
        else:

            # Simply a reference to the previous strand
            previous_strand = vmv.strands_list[i_strand - 1]
            for i in range(len(previous_strand)):
                previous_strand[i] = int(previous_strand[i])

            # If the first sample of the current strand is an increment of the last sample of
            # the previous strand
            h5_vertices_indices.append(strand[0])

            # Add to the strand
            h5_strands.append([current_index, 1])

            # Increment the index
            current_index += 1

        # Iterate over the rest of the strand
        for i_vertex in range(1, len(strand)):

            # Simply a reference to the indices
            previous_vertex = strand[i_vertex - 1]
            current_vertex = strand[i_vertex]

            # If the logical sequence, simply append the index to the list
            h5_vertices_indices.append(current_vertex)

            # Increment the index
            current_index += 1

    # Construct the vertices list
    h5_vertex_list = list()
    for vertex_index in h5_vertices_indices:
        point = vmv.points_list[vertex_index - 1]
        radius = vmv.radii_list[vertex_index - 1]
        h5_vertex_list.append([point[0], point[1], point[2], radius])

    # Create an h5 file
    h5_file = h5py.File('%s/%s' % (output_path, file_name), 'w')

    # Create the points data set
    points_dataset = h5_file.create_dataset("/points", data=h5_vertex_list, compression="gzip")

    # Create the structure (or the strands) dataset
    structure_dataset = h5_file.create_dataset("/structure", data=h5_strands, compression="gzip")

    # Create the connectivity dataset
    connectivity = [[1, 2]]
    structure_dataset = h5_file.create_dataset("/connectivity", data=connectivity, compression="gzip")

    # Create the connectivity dataset
    # connectivity_dataset = h5_file.create_dataset("/connectivity", (4, vmv.number_loaded_vertices),
    #                                             dtype=h5py.h5t.NATIVE_INT64)

    # Close the file
    h5_file.close()


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
    morphologies = glob.glob('%s/*.vmv' % args.morphology_directory)

    # Do it one by one 
    for morphology in morphologies:

        print('Input [%s]' % morphology)
        vmv_structure = VMVReader(vmv_file=morphology)

        # Write the H5 file
        write_h5_file(file_name=ntpath.basename(morphology).replace('.vmv', '.h5'),
                      output_path=args.output_directory,
                      vmv=vmv_structure)












