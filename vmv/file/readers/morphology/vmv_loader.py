####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
                 mat_file):
        """Constructor

        :param mat_file:
            A given .mat morphology file.
        """

        # Set the path to the given h5 file
        self.morphology_file = mat_file

        # A list of all the points (or samples) in the morphology file
        self.points_list = list()

        # A list of all the structures in the morphology file
        self.structures_list = list()

        # A list of the connectivity data in the morphology file
        self.connectivity_list = list()

        # A list of all the sections that were extracted from the loaded data
        self.sections_list = list()

        # Morphology bounding box, initially None, till being computed
        self.bounding_box = None

        # Graph roots
        # NOTE: The data set could have multiple roots, i.e. sections with no parents. In this case,
        # we should treat each root as an independent object and later group all of then into a
        # single object.
        self.roots = list()

    ################################################################################################
    # @parse_structures_list
    ################################################################################################
    def parse_structures_list(self):
        """Parses the structures list from the data loaded from the morphology file.
        """
        # Parse the structures list
        for i in range(len(self.structures_list)):

            # The structures contain the vertices of the points in each strand (section)
            strand_vertices = self.structures_list[i]

            # A list of samples in the section
            samples_list = list()

            # Add the samples along the section
            for j in range(len(strand_vertices)):

                # Get the point index
                point_index = strand_vertices[j]

                # Get the point from the points list
                # Note that we have to reduce it by 1 to account for the difference in indices
                # between Matlab and Python
                point = self.points_list[point_index - 1]

                # Construct a sample
                sample = vmv.skeleton.Sample(point=Vector((point[0], point[1], point[2])),
                                             radius=point[3],
                                             index=j)

                # Add the sample to the samples list
                samples_list.append(sample)

            # Construct the section, the section index will be the same order
            section = vmv.skeleton.Section(index=i, samples=samples_list)

            # Add the section to the sections list
            self.sections_list.append(section)

    ################################################################################################
    # @build_graph_from_parsed_data
    ################################################################################################
    def build_graph_from_parsed_data(self):
        """Builds the graph from the parsed data.
        """

        # Build the graph from the connectivity list
        for connection in self.connectivity_list:

            # The index of the parent section
            parent_section_index = connection[0]

            # The index of the child section
            child_section_index = connection[1]

            # Parent section
            parent_section = self.sections_list[parent_section_index]

            # Child section
            child_section = self.sections_list[child_section_index]

            # Connect the child to the parent
            parent_section.children.append(child_section)

            # Connect the parent to the child
            child_section.parents.append(parent_section)

        # Detect the root sections and update the list
        for section in self.sections_list:
            if section.is_root():
                self.roots.append(section)

    ################################################################################################
    # @read_data_from_file
    ################################################################################################
    def read_data_from_file(self):
        """Loads the data from the given file in the constructor.
        """

        try:

            # Open the morphology file
            file_handler = open(self.morphology_file, 'r')

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
                vmv.logger.log('Data set is valid')
            else:
                vmv.logger.log('Data set is NOT valid')

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

            # Get the number of attributes per vertex
            for item in data:
                if 'NUM_ATTRIB_PER_VERT' in item:
                    item = item.split(' ')
                    number_attributes_per_vertex = int(item[1])
                    break

            # Log
            vmv.logger.log('Data contains [%d] vertices, [%d] strands and [%d] attributes' %
                           (number_vertices, number_strands, number_attributes_per_vertex))

            # If all the sizes are read, simply break and close the file
            if number_vertices == 0 or number_strands == 0 or number_attributes_per_vertex == 0:
                vmv.logger.log('Invalid data set')

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

            # Parse the vertices
            for i in range(starting_vertex_index, end_vertex_index):

                # Split the entry
                vertex_entry = data[i].split(' ')

                index = int(vertex_entry[0])
                x = float(vertex_entry[1])
                y = float(vertex_entry[2])
                z = float(vertex_entry[3])
                radius = float(vertex_entry[4])

                # Add this point to the points list with the position and radius
                self.points_list.append([x, y, z, radius, index])

            # Compute the bounding box of the morphology
            self.bounding_box = vmv.bbox.compute_bounding_box_for_list_of_points(
                self.points_list)

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

                    # Construct a sample
                    sample = vmv.skeleton.Sample(point=Vector((point[0], point[1], point[2])),
                                                 radius=point[3],
                                                 index=point[4])

                    # Add the sample to the samples list
                    samples_list.append(sample)

                # Construct the section, the section index will be the same order
                section = vmv.skeleton.Section(index=strand_index, samples=samples_list)

                # Add the section to the sections list
                self.sections_list.append(section)

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
        for point in self.points_list:
            point[0] -= self.bounding_box.center[0]
            point[1] -= self.bounding_box.center[1]
            point[2] -= self.bounding_box.center[2]

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
        self.read_data_from_file()

        # Center the morphology at the origin if required by the user
        if center_at_origin:
            self.center_morphology_at_origin()

        # Parse the structures list
        self.parse_structures_list()

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
            morphology_name=morphology_name, morphology_file_path=self.morphology_file,
            points_list=self.points_list, structures_list=self.structures_list,
            connectivity_list=self.connectivity_list, sections_list=self.sections_list,
            roots=self.roots)

        # Return the object
        return morphology_object
