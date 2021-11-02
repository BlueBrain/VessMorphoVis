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
import copy
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
    description = 'Converts an h5 file with sonata structure and simulation data into a vmv file.'
    parser = argparse.ArgumentParser(description=description)

    arg_help = 'The file that contains the structure of the morphology'
    parser.add_argument('--structure-file',
                        action='store', dest='structure_file', help=arg_help)

    arg_help = 'Radius simulation report in sonata format'
    parser.add_argument('--radius-report',
                        action='store', dest='radius_report', help=arg_help, default=None)

    arg_help = 'Flow simulation report in sonata format'
    parser.add_argument('--flow-report',
                        action='store', dest='flow_report', help=arg_help, default=None)

    arg_help = 'Pressure simulation report in sonata format'
    parser.add_argument('--pressure-report',
                        action='store', dest='pressure_report', help=arg_help, default=None)

    arg_help = 'Output directory where the generated VMV morphologies will be written'
    parser.add_argument('--output-directory',
                        action='store', dest='output_directory', help=arg_help)

    # Parse the arguments
    return parser.parse_args()


####################################################################################################
# @create_vmv_vertex_string
####################################################################################################
def create_vmv_vertex_string(points,
                             diameters):
    """Creates the VMV vertex string from the points and diameters lists.

    :param points:
        A list of all the points in the file.
    :param diameters:
        A list of the diameters of all the vertices in the list.
    :return:
        VMV vertex string.
    """

    # First line
    string = '$VERT_LIST_BEGIN\n'

    # Strands
    for i, vertex in enumerate(points):

        # Construct the string
        string += '%d\t%2.2f\t%2.2f\t%2.2f\t%2.2f\n' % (i + 1,
                                                        vertex[0], vertex[1], vertex[2],
                                                        0.5 * diameters[i])

    # Last line
    string += '$VERT_LIST_END\n\n'

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
    for i, strand in enumerate(strands):
        string += '%d ' % (i + 1)
        for vertex in strand:
            string += '%d ' % vertex
        string += '\n'

    # Last line
    string += '$STRANDS_LIST_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @create_vmv_radius_simulation_string
####################################################################################################
def create_vmv_radius_simulation_string(radius_simulations,
                                        points,
                                        segments):

    # Get the number of steps from the radius_simulations
    number_simulation_steps = len(radius_simulations)

    # Get the number of points
    number_points = len(points)

    # Create an empty matrix to do the mapping
    w, h = number_simulation_steps, number_points
    simulation_matrix = [[0 for x in range(w)] for y in range(h)]

    # First line
    string = '$RADIUS_SIMULATION_BEGIN\n'

    # For every step
    for step, data in enumerate(radius_simulations):

        # The index here is the segment index, and the value is the radius value
        for i, value in enumerate(data):

            # Use the index (i) to index the segments array to get the segment points indices
            segment_nodes = segments[i]

            # Use the last point of the segment for the reference
            point_index = segment_nodes[1]

            # Add the value to the simulation matrix
            simulation_matrix[point_index][step] = value

    # Create the string from the matrix
    # For every point in the matrix
    for i in range(number_points):

        # For every
        for j in range(number_simulation_steps):

            # Append the value to the string
            string += '%2.2f ' % simulation_matrix[i][j]

        string += '\n'

    # Last line
    string += '$RADIUS_SIMULATION_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @create_vmv_header_string
####################################################################################################
def create_vmv_header_string(vertex_list,
                             strand_list,
                             radius_simulations=None,
                             flow_simulations=None,
                             pressure_simulations=None):
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
    string += '%s\t%d\n' % ('NUM_VERTS', len(vertex_list))

    # Number of strands
    string += '%s\t%d\n' % ('NUM_STRANDS', len(strand_list))

    # Number of attributes
    string += '%s\t%d\n' % ('NUM_ATTRIB_PER_VERT', 4)

    # Radius simulation time steps
    if radius_simulations is not None:
        string += '%s\t%d\n' % ('RADIUS_SIMULATION_TIME_STEPS', len(radius_simulations))

    # Flow simulation time steps
    if flow_simulations is not None:
        string += '%s\t%d\n' % ('FLOW_SIMULATION_TIME_STEPS', len(flow_simulations))

    # Pressure simulation time steps
    if pressure_simulations is not None:
        string += '%s\t%d\n' % ('PRESSURE_SIMULATION_TIME_STEPS', len(pressure_simulations))

    # First line
    string += '$PARAM_END\n\n'

    # Return the strands string
    return string


####################################################################################################
# @ Main
####################################################################################################
def create_vmv_string(points,
                      diameters,
                      segments,
                      sections,
                      radius_simulations=None,
                      flow_simulations=None,
                      pressure_simulations=None):
    """Creates a VMV string that represents the morphology including the simulation data.

    :param points:
        A list of points (XYZ coordinates), or nodes (for the sonata structure).
    :param diameters:
        A list of diameters.
    :param segments:
        A list of segments or edges.
    :param sections:
        A list of sections, where each section is a list of points, irrespective to the edges.
    :param radius_simulations:
        Radius simulation data, edges with respect to time. If None, it will be ignored.
    :param flow_simulations:
        Flow simulation data, edges with respect to time. If None, it will be ignored.
    :param pressure_simulations:
        Pressure simulation data, edges with respect to time. If None, it will be ignored.
    :return:
        The VMV string that represents the morphology.
    """

    # Header
    vmv_string = create_vmv_header_string(vertex_list=points, strand_list=sections,
                                          radius_simulations=radius_simulations,
                                          flow_simulations=flow_simulations,
                                          pressure_simulations=pressure_simulations)

    # Create the vertex string
    vertex_string = create_vmv_vertex_string(points=points, diameters=diameters)
    vmv_string += vertex_string

    # Create the strands string
    strands_string = create_vmv_strands_string(strands=sections)
    vmv_string += strands_string

    # Create the radius simulations
    if radius_simulations is not None:
        radius_simulation_strings = create_vmv_radius_simulation_string(
            radius_simulations=radius_simulations, points=points, segments=segments)
        vmv_string += radius_simulation_strings

    '''
    # Create the flow simulations
    if flow_simulations is not None:
        flow_simulation_string = create_vmv_flow_simulation_string(flow_simulations)

    # Create the flow simulations
    if pressure_simulations is not None:
        pressure_simulation_string = create_vmv_pressure_simulation_string(flow_simulations)

    '''

    return vmv_string


####################################################################################################
# @write_vmv_string_to_file
####################################################################################################
def write_vmv_string_to_file(file_name,
                             output_path,
                             vmv_string):
    """Creates the VMV string that accounts for the data in the VMV format.

    :param file_name:
        The output file name.
    :param output_path:
        The output path.
    :param swc_data_list:
        The data list loaded from the SWC file.
    """

    # Write the output file
    output_file = open('%s/%s' % (output_path, file_name), 'w')
    output_file.write(vmv_string)
    output_file.close()


####################################################################################################
# @write_vmv_string_to_file
####################################################################################################
def run_sonata2vmv(args):
    # Some imports
    try:
        import numpy
    except ImportError:
        print('Cannot import numpy, please install [ pip install numpy ]')
        exit(0)

    try:
        import h5py
    except ImportError:
        print('Cannot import h5py, please install [ pip install h5py ]')
        exit(0)

    try:
        from vasculatureapi import PointVasculature
        from vasculatureapi import SectionVasculature
    except ImportError:
        print('Cannot import PointVasculature, please install vasculatureapi using BBP VPN')
        exit(0)

    # Load the structure file
    graph = PointVasculature.load_sonata(args.structure_file)

    # The properties
    edge_properties = graph.edge_properties

    # Section id properties
    section_id_prop = edge_properties['section_id']

    # Nodes or vertices, basically samples
    start_nodes = edge_properties['start_node']
    end_nodes = edge_properties['end_node']

    # Get a reference to the points, or samples, only XYZ coordinates without diameters
    points = graph.points

    # Get a reference to the diameters
    diameters = graph.diameters

    # Edges, this is the global one, where it has a unique identifier in the entire morphology
    segments = graph.edges

    # A list of all the section nodes, for a single section
    section_nodes = list()

    # A list of sections with respect to their nodes or samples
    sections = list()

    # Figure out the mapping
    counter = 0
    current_section_id = 0
    while True:
        if counter >= len(section_id_prop):
            break
        section_id = section_id_prop[counter]
        if current_section_id == section_id:
            section_nodes.append(end_nodes[counter])
        else:
            current_section_id = section_id
            sections.append(copy.deepcopy(section_nodes))
            section_nodes.clear()
        counter += 1

    # If all the reports are None, then there is nothing we can do
    radius_simulation_data = None
    flow_simulation_data = None
    pressure_simulation_data = None

    # Just notify the users that no reports are available
    if args.radius_report is None and args.flow_report is None and args.pressure_report is None:
        print('WARNING: There are no simulation reports! File will be purely structural')

    # Radii simulations
    if args.radius_report is not None:
        radius_report = h5py.File(args.radius_report, 'r')
        radius_simulation_data = radius_report['report']['vasculature']['data']

    # Flow simulations
    if args.flow_report is not None:
        flow_report = h5py.File(args.flow_report, 'r')
        flow_simulation_data = flow_report['report']['vasculature']['data']

    # Pressure simulations
    if args.pressure_report is not None:
        pressure_report = h5py.File(args.pressure_report, 'r')
        pressure_simulation_data = pressure_report['report']['vasculature']['data']

    # Construct the vmv file from the sonata files
    vmv_string = create_vmv_string(points=points, diameters=diameters,
                                   segments=segments, sections=sections,
                                   radius_simulations=radius_simulation_data,
                                   flow_simulations=flow_simulation_data,
                                   pressure_simulations=pressure_simulation_data)

    # Write the corresponding VMV file to the output directory
    write_vmv_string_to_file(file_name=ntpath.basename(args.structure_file).replace('.h5', '.vmv'),
                             output_path=args.output_directory,
                             vmv_string=vmv_string)


####################################################################################################
# @ Main
####################################################################################################
if __name__ == "__main__":

    # Get all arguments after the '--'
    
    # Parse the command line arguments
    arguments = parse_command_line_arguments()

    if arguments.structure_file is None:
        print('No structure file is given. Please provide a structure file to proceed.')
        exit(0)

    if arguments.output_directory is None:
        print('No output directory, please specify valid output directory')
        exit(0)

    # Run the script
    run_sonata2vmv(args=arguments)
