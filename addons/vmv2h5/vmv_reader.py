####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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

####################################################################################################
# @VMVReader
####################################################################################################
class VMVReader:
    """VMV reader.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 vmv_file):
        """Constructor

        :param vmv_file:
            A given .vmv morphology file.
        """

        # Set the path to the given vmv text file
        self.morphology_file = vmv_file

        # The number of loaded vertices or samples
        self.number_loaded_vertices = None

        # The number of loaded strands or sections
        self.number_loaded_strands = None

        # A list containing all the points of the morphology in a Cartesian format(X, Y, Z)
        self.points_list = list()

        # A list containing all the radii of the morphology
        self.radii_list = list()

        # A list containing all the strands in the morphology
        self.strands_list = list()

        # Number of steps for radius simulation, if existing
        self.radius_simulation_steps = 0

        # Radius simulation data
        self.radius_simulation_data = None

        # Number of steps for flow simulation, if existing
        self.flow_simulation_steps = 0

        # Flow simulation data
        self.flow_simulation_data = None

        # Number of steps for pressure simulation, if existing
        self.pressure_simulation_steps = 0

        # Pressure simulation data
        self.pressure_simulation_data = None

        # Read the data from the file ##############################################################
        self.read_data_from_file()

    ################################################################################################
    # @load_data_from_file
    ################################################################################################
    def load_data_from_file(self):
        """Only loads the data from the given morphology file, silently.

        :return
            Returns the loaded data from the file in the form of a list that is easier to index.
        """

        # Open the morphology file
        file_handler = open(self.morphology_file, 'r')

        # Load the file into a LIST where it would make it easier to search and index
        data = list()

        # Get the data sizes from the file
        for line in file_handler:

            # Ignore comments
            if '#' in line:
                continue

            # Ignore empty lines
            if not line.strip():
                continue

            # Replace multiple spaces with a single space
            line = ' '.join(line.split())

            # Replace the '\n' with empty
            line = line.replace('\n', '')

            # # Add the filtered line to the data list, if it is not an empty line
            if len(line) > 0:
                data.append(line)

        # Close the file
        file_handler.close()

        # Return a reference to the data
        return data

    ################################################################################################
    # @verify_morphology_structure
    ################################################################################################
    def verify_morphology_structure(self,
                                    data):
        """Verifies the structure of the morphology file.

        :param:
            Loaded data list that contains all the elements of the morphology.
        """

        # Make sure that the data has all the mandatory fields
        if '$PARAM_BEGIN' in data and '$PARAM_END' in data and \
           '$STRANDS_LIST_BEGIN' in data and '$STRANDS_LIST_END' in data and \
           '$VERT_LIST_BEGIN' in data and '$VERT_LIST_END' in data:
            print('Data set is valid')
        else:
            print('Data set is NOT valid')
            exit(0)

        # Get the number of vertices
        for item in data:
            if 'NUM_VERTS' in item:
                item = item.split(' ')
                self.number_loaded_vertices = int(item[1])
                break

        # Get the number of strands
        for item in data:
            if 'NUM_STRANDS' in item:
                item = item.split(' ')
                self.number_loaded_strands = int(item[1])
                break

        # Radius simulation time steps
        for item in data:
            if 'RADIUS_SIMULATION_TIME_STEPS' in item:
                item = item.split(' ')
                self.radius_simulation_steps = int(item[1])
                break

        # Flow simulation time steps
        for item in data:
            if 'FLOW_SIMULATION_TIME_STEPS' in item:
                item = item.split(' ')
                self.flow_simulation_steps = int(item[1])
                break

        # Pressure simulation time steps
        for item in data:
            if 'PRESSURE_SIMULATION_TIME_STEPS' in item:
                item = item.split(' ')
                self.pressure_simulation_steps = int(item[1])
                break

        # Log
        print('Morphology contains [%d] vertices, [%d] strands' %
              (self.number_loaded_vertices, self.number_loaded_strands))

        # If all the sizes are read, simply break and close the file
        if self.number_loaded_vertices == 0 or self.number_loaded_strands == 0:
            print('Invalid morphology structure!')
            exit(0)

        # Radius simulation
        if self.radius_simulation_steps > 0:
            print('Morphology has [%d] radius simulation time steps' % self.radius_simulation_steps)

        # Flow simulation
        if self.flow_simulation_steps > 0:
            print('Morphology has [%d] flow simulation time steps' % self.flow_simulation_steps)

        # Pressure simulation
        if self.pressure_simulation_steps > 0:
            print('Morphology has [%d] pressure simulation time steps' %
                  self.pressure_simulation_steps)

    ################################################################################################
    # @parse_vertices
    ################################################################################################
    def parse_vertices(self,
                       data):
        """Parses the vertices from the VMV file.

        :param data:
            Input data table that contains all the data of the morphology, where we will extract
            the vertex information.
        """

        # Read the vertices by getting the index of the $VERT_LIST_BEGIN tag
        starting_vertex_index = 0

        # Iterate over evert element in the data list
        for item in data:

            # If the '$VERT_LIST_BEGIN' is there, voila!
            if '$VERT_LIST_BEGIN' in item:

                # Further increment to jump directly to the actual starting index and break
                starting_vertex_index += 1
                break

            # Increment the vertex index
            starting_vertex_index += 1

        # End vertex index, by adding the total number of loaded vertices
        end_vertex_index = starting_vertex_index + self.number_loaded_vertices

        # Initialize the point list, originally None
        self.points_list = list()

        # Initialize the radii list, originally None
        self.radii_list = list()

        # Iterate on the data list only within the vertex indices
        for i in range(starting_vertex_index, end_vertex_index):

            # Split the entry
            vertex_entry = data[i].split(' ')

            # Vertex index
            index = int(vertex_entry[0])

            # Vertex coordinates
            x = float(vertex_entry[1])
            y = float(vertex_entry[2])
            z = float(vertex_entry[3])

            # Vertex radius
            radius = float(vertex_entry[4])

            # Add this point to the points list with the position and radius
            self.points_list.append([x, y, z, index])

            # Radii
            self.radii_list.append(radius)

        # Update the meta-data
        self.number_loaded_vertices = len(self.points_list)

    ################################################################################################
    # @parse_strands
    ################################################################################################
    def parse_strands(self,
                      data):
        """Parses the strands or sections of the vascular morphology from the VMV file.

        :param data:
            Input data table that contains all the data of the morphology, where we will extract
            the sections information.
        """

        # Read the strands by getting the index of the STRANDS_LIST_BEGIN tag
        starting_strand_index = 0

        # Iterate over evert element in the data list
        for item in data:

            # If the '$STRANDS_LIST_BEGIN' is there, voila!
            if '$STRANDS_LIST_BEGIN' in item:

                # Further increment to jump directly to the actual starting index and break
                starting_strand_index += 1
                break

            # Increment the vertex index
            starting_strand_index += 1

        # End strand index
        end_strand_index = starting_strand_index + self.number_loaded_strands

        # Iterate on the data list only within the strand indices
        for i in range(starting_strand_index, end_strand_index):

            # Split the entry
            strand_entry = data[i].split(' ')

            # Get the index
            strand_index = int(strand_entry[0])

            # Remove the item at the first index that accounts for the strand index to end up
            # with the list of points along the strand
            strand_entry.remove(strand_entry[0])

            # Append to the strand list
            self.strands_list.append(strand_entry)

        # Update the meta-data
        self.number_loaded_strands = len(self.strands_list)

    ################################################################################################
    # @parse_radius_simulation_data
    ################################################################################################
    def parse_radius_simulation_data(self,
                                     data):
        """Note that the radius variation data will have N time frames and M data points, where M
        is the number of samples or vertices in the morphology.
        The simulation data is always stored on a per-sample or per-vertex basis.
        """

        # If the simulation time steps are greater than zero
        if self.radius_simulation_steps > 0:

            # Read the simulation data by getting the index of the $RADIUS_SIMULATION_BEGIN tag
            starting_index = 0

            # Iterate over evert element in the data list
            for item in data:

                # If the '$RADIUS_SIMULATION_BEGIN' is there, voila!
                if '$RADIUS_SIMULATION_BEGIN' in item:

                    # Further increment to jump directly to the actual starting index and break
                    starting_index += 1
                    break

                    # Increment the vertex index
                starting_index += 1

            # If the starting index is still zero, then there is no simulation data
            if starting_index == 0:

                # Set the number of simulation steps to zero
                self.radius_simulation_steps = 0

                # Return
                return

            # End vertex index, by adding the total number of loaded vertices
            end_index = starting_index + self.number_loaded_vertices

            # Initialize the simulation data list, originally None
            self.radius_simulation_data = list()

            # Iterate on the data list only within the vertex indices
            for i in range(starting_index, end_index):

                # Split the entry, at a specific vertex
                vertex_entry = data[i].split(' ')

                # Convert the string list to a float
                for j in range(len(vertex_entry)):
                    value = float(vertex_entry[j])
                    vertex_entry[j] = value

                # Add the list to the simulation table
                self.radius_simulation_data.append(vertex_entry)

    ################################################################################################
    # @read_data_from_file
    ################################################################################################
    def read_data_from_file(self):
        """Loads the data from the given file in the constructor.
        """

        # Make sure you get the data, otherwise, report an ERROR!
        try:

            # Load the data from the file
            data = self.load_data_from_file()

            # Verify the morphology structure to avoid issues later during the visualization
            self.verify_morphology_structure(data=data)

            # Parse the vertices, or samples
            self.parse_vertices(data=data)

            # Parse the strands or the sections
            self.parse_strands(data=data)

            # Radius simulation data
            self.parse_radius_simulation_data(data=data)

        # Raise an exception if we cannot import the h5py module
        except ImportError:

            print('ERROR: Cannot read the file [%s]' % self.morphology_file)
            exit(0)
