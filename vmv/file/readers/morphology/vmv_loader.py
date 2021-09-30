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

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.bbox
import vmv.consts
import vmv.file
import vmv.skeleton


####################################################################################################
# @H5Reader
####################################################################################################
class VMVReader:
    """A customized reader to be able to parse .VMV files that are created from converting the
    reconstructions created by Pablo Blinder.
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

        # Morphology bounding box, initially None, till being computed
        self.bounding_box = None

        # Graph roots
        # NOTE: The data set could have multiple roots, i.e. sections with no parents. In this case,
        # we should treat each root as an independent object and later group all of then into a
        # single object.
        self.roots = list()

        # The number of loaded vertices or samples
        self.number_loaded_vertices = None

        # The number of loaded strands or sections
        self.number_loaded_strands = None

        # A list containing all the points of the morphology in a Cartesian format(X, Y, Z)
        self.points_list = None

        # A list containing all the radii of the morphology
        self.radii_list = None

        # A list of all the sections that were extracted from the loaded data, input to VMV
        self.sections_list = list()

        # A list containing all the strands in the morphology
        self.strands_list = None

        # Number of steps for radius simulation, if existing
        self.radius_simulation_steps = 0

        #
        self.radius_simulation_data = None

        # Number of steps for flow simulation, if existing
        self.flow_simulation_steps = 0

        # Number of steps for pressure simulation, if existing
        self.pressure_simulation_steps = 0

    ################################################################################################
    # @build_graph_from_parsed_data
    ################################################################################################
    def build_graph_from_parsed_data(self):
        """Builds the graph from the parsed data.
        """

        self.sections_list = set(self.sections_list)

        # Build the graph from the connectivity list
        for i_section in range(len(self.sections_list)):

            # The index of the first sample on the section
            i_first_sample_index = self.sections_list[i_section].samples[0].index

            # The index of the last sample on the section
            i_last_sample_index = self.sections_list[i_section].samples[-1].index

            for j_section in range(len(self.sections_list)):

                # Parenting of the same section is not valid, indeed
                if i_section == j_section:
                    continue

                # The index of the first sample on the section
                j_first_sample_index = self.sections_list[j_section].samples[0].index

                # The index of the last sample on the section
                j_last_sample_index = self.sections_list[j_section].samples[-1].index

                # J is parent to I
                if i_first_sample_index == j_last_sample_index:
                    self.sections_list[i_section].parents.append(self.sections_list[j_section])

                # J is a child of I
                if i_last_sample_index == j_first_sample_index:
                    self.sections_list[i_section].children.append(self.sections_list[j_section])

        # Detect the root sections and update the list
        for section in self.sections_list:
            if section.is_root():
                self.roots.append(section)

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
           '$VERT_LIST_BEGIN' in data and '$VERT_LIST_END' in data:
            vmv.logger.info('Data set is valid')
        else:
            vmv.logger.info('Data set is NOT valid')

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
        vmv.logger.info('Morphology contains [%d] vertices, [%d] strands' %
                        (self.number_loaded_vertices, self.number_loaded_strands))

        # If all the sizes are read, simply break and close the file
        if self.number_loaded_vertices == 0 or self.number_loaded_strands == 0:
            vmv.logger.info('Invalid morphology structure!')

        # Radius simulation
        if self.radius_simulation_steps > 0:
            vmv.logger.info('Morphology has [%d] radius simulation time steps' %
                            self.radius_simulation_steps)

        # Flow simulation
        if self.flow_simulation_steps > 0:
            vmv.logger.info('Morphology has [%d] flow simulation time steps' %
                            self.flow_simulation_steps)

        # Pressure simulation
        if self.pressure_simulation_steps > 0:
            vmv.logger.info('Morphology has [%d] pressure simulation time steps' %
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

            # Construct the samples list along the strand
            samples_list = list()
            for i_point in strand_entry:

                # Get the point
                point = self.points_list[int(i_point) - 1]

                # Radius
                radius = self.radii_list[int(i_point) - 1]

                # Construct a sample
                sample = vmv.skeleton.Sample(point=Vector((point[0], point[1], point[2])),
                                             radius=radius,
                                             index=point[3])

                # Add the sample to the samples list
                samples_list.append(sample)

            # Construct the section, the section index will be the same order
            section = vmv.skeleton.Section(index=strand_index, samples=samples_list)

            # Add the section to the sections list
            self.sections_list.append(section)

        # Update the meta-data
        self.number_loaded_strands = len(self.sections_list)

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

            bpy.context.scene.VMV_RadiusVariationsSteps = len(self.radius_simulation_data[0])

    ################################################################################################
    # @read_data_from_file
    ################################################################################################
    def read_data_from_file(self,
                            center_at_origin=False):
        """Loads the data from the given file in the constructor.

        :param center_at_origin:
            Center the morphology at the center.
        """

        # Make sure you get the data, otherwise, report an ERROR!
        # TODO: Propagate this error to the interface
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

            # Compute the bounding box of the morphology
            self.bounding_box = vmv.bbox.compute_bounding_box_for_list_of_points(self.points_list)

            # Center the morphology at the origin if required by the user
            if center_at_origin:
                self.center_morphology_at_origin()

        # Raise an exception if we cannot import the h5py module
        except ImportError:

            print('ERROR: Cannot read the file [%s]' % self.morphology_file)
            exit(0)

    ################################################################################################
    # @center_morphology_at_origin
    ################################################################################################
    def center_morphology_at_origin(self):
        """Centers the morphology at the origin.
        """

        # Center each point in the points list
        for section in self.sections_list:
            for sample in section.samples:
                sample.point[0] -= self.bounding_box.center[0]
                sample.point[1] -= self.bounding_box.center[1]
                sample.point[2] -= self.bounding_box.center[2]

    ################################################################################################
    # @load_morphology_file
    ################################################################################################
    def load_morphology_file(self,
                             center_at_origin=False,
                             resample_morphology=False):
        """Reads the file and constructs a root node that we can use to traverse the tree

        :param center_at_origin:
            Centers the morphology at the origin.
        :param resample_morphology:
            Re-samples the morphology skeleton to reduce the number of samples along the section and
            remove the redundant samples.
        """

        # Read the morphology skeleton from the file
        self.read_data_from_file(center_at_origin=center_at_origin)

        # Build the graph from the parsed data
        # self.build_graph_from_parsed_data()

        # Resample the morphology skeleton if required
        if resample_morphology:
            for section in self.sections_list:
                vmv.skeleton.resample_section_adaptively(section)

    ################################################################################################
    # @construct_morphology_object
    ################################################################################################
    def construct_morphology_object(self,
                                    center_at_origin=False,
                                    resample_morphology=False):
        """Reconstructs the morphology object after loading it from file and centers it at
        the origin if required.

        :param center_at_origin:
            A flag that indicates that the morphology will be centered at the origin.
        :param resample_morphology:
            Re-samples the morphology skeleton to reduce the number of samples along the section and
            remove the redundant samples.
        :return:
            A reference to the morphology object.
        """

        # Load the morphology file
        self.load_morphology_file(center_at_origin=center_at_origin,
                                  resample_morphology=resample_morphology)

        # Get the morphology name from the file
        morphology_name = vmv.file.ops.get_file_name_from_path(self.morphology_file)

        # Construct the morphology object following to reading the file
        morphology_object = vmv.skeleton.Morphology(
            name=morphology_name,
            file_path=self.morphology_file,
            number_samples=self.number_loaded_vertices,
            number_sections=self.number_loaded_strands,
            sections_list=self.sections_list,
            roots=self.roots,
            radius_simulation_data=self.radius_simulation_data)

        # Return the object
        return morphology_object
