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
class MATReader:
    """Matlab files morphology reader for the vasculature.
    NOTE: This solution is implemented to provide a direct interface for Pablo Blender.
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

            # Import the h5py module
            import scipy.io
            import vmv.utilities

            # Ignore the console warning and output
            # vmv.utilities.disable_std_output()

            # Read the .mat file using the python module into a data array
            data = scipy.io.loadmat(self.morphology_file)

            # Structure array
            structure_array = data['allProject']['db'][0][0]['vectorizedStructure'][0][0]

            # The strands array as given in the .mat format
            strands_array = structure_array['Strands'][0][0][0]

            # The vertices' coordinates array as given in the .mat format
            vertices_array = structure_array['Vertices'][0][0]['AllVerts'][0][0]

            # The radii array as given in the .mat format
            radii_array = structure_array['Vertices'][0][0]['AllRadii'][0][0]

            # Verify that the array of the radii has the same length of the vertices array
            radii_array_length = len(radii_array)
            vertices_array_length = len(vertices_array)

            if not radii_array_length == vertices_array_length:
                vmv.logger.log('ERROR: The data set has inconsistent arrays')

            # Construct the points list
            for i in range(vertices_array_length):
                x = vertices_array[i][0]
                y = vertices_array[i][1]
                z = vertices_array[i][2]
                radius = radii_array[i][0]

                # Add this point to the points list with the position and radius
                self.points_list.append([x, y, z, radius])

            # Construct the structures list
            '''
                [0] StartVertexIndex
                [1] EndVertexIndex
                [2] InteriorVertices
                [3] StartToEndIndices
                [4] StartVertexNeighborStrands
                [5] EndVertexNeighborStrands
                [6] Active
                [7] YXZLimits
                [8] MedianRadius
                [9] MedianLabel
                [10] strandConductance
                [11] strandCurrent
                [12] MedianVoltage
                [13] StartVoltage
                [14] EndVoltage
                [15] VoltageDrop
            '''
            # This is a reflection to the StartToEndIndices array in the .mat file
            for i in range(len(strands_array)):

                # Get the .mat array
                strand_array = strands_array[i][3][0]

                # Convert the array directly to a list and append the list to the structures list
                self.structures_list.append(strand_array.tolist())

            # TODO: A list of all the sections (called structures) in the data set
            # self.connectivity_list = data['connectivity'].value

            # Reset the std output
            # vmv.utilities.enable_std_output()

            # Compute the bounding box of the morphology
            self.bounding_box = vmv.bbox.compute_bounding_box_for_list_of_points(self.points_list)

        # Raise an exception if we cannot import the h5py module
        except ImportError:

            print('ERROR: Cannot *import scipy.io* to read the file [%s]' % self.morphology_file)
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
