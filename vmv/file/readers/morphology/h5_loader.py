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
class H5Reader:
    """H5 morphology reader for the vasculature.

    NOTE: This solution should be replaced by MorphoIO.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 h5_file):
        """Constructor

        :param h5_file:
            A given .H5 morphology file.
        """

        # Set the path to the given h5 file
        self.morphology_file = h5_file

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

            # The starting sample of the section is at index i
            start_index = int(self.structures_list[i][0])

            # The last sample of the section is at index i + 1
            if i < len(self.structures_list) - 1:
                end_index = int(self.structures_list[i + 1][0])
            else:
                end_index = int(len(self.points_list))

            # A list of all the samples that belong to the section
            samples_list = list()

            # Add the samples along the section
            for j in range(start_index, end_index):

                # Get the point from the points list
                point = self.points_list[j]

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

        # Re-sample
        # for section in self.sections_list:
        #     vmv.skeleton.resample_section_adaptively(section)

    ################################################################################################
    # @read_data_from_file
    ################################################################################################
    def read_data_from_file(self):
        """Loads the data from the given file in the constructor.
        """

        try:

            # Import the h5py module
            import h5py
            import vmv.utilities

            # Ignore the console warning and output
            vmv.utilities.disable_std_output()

            # Read the h5 file using the python module into a data array
            data = h5py.File(self.morphology_file, 'r')

            # A list of all the samples in the data set
            self.points_list = data['points'].value

            # A list of all the sections in the data set
            self.structures_list = data['structure'].value

            # A list of all the sections (called structures) in the data set
            self.connectivity_list = data['connectivity'].value

            # Reset the std output
            vmv.utilities.enable_std_output()

            # Compute the bounding box of the morphology
            self.bounding_box = vmv.bbox.compute_bounding_box_for_list_of_points(self.points_list)

        # Raise an exception if we cannot import the h5py module
        except ImportError:

            print('ERROR: Cannot *import h5py* to read the file [%s]' % self.morphology_file)
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
                             center_at_origin=False):
        """Reads the file and constructs a root node that we can use to traverse the tree

        :param center_at_origin:
            Centers the morphology at the origin.
        """

        # Read the morphology skeleton from the file
        self.read_data_from_file()

        # Center the morphology at the origin if required by the user
        if center_at_origin:
            self.center_morphology_at_origin()

        # Parse the structures list
        self.parse_structures_list()

        # Build the graph from the parsed data
        self.build_graph_from_parsed_data()

    ################################################################################################
    # @construct_morphology_object
    ################################################################################################
    def construct_morphology_object(self,
                                    center_at_origin=False):
        """Reconstructs the morphology object after loading it from file and centers it at
        the origin if required.

        :param center_at_origin:
            A flag that indicates that the morphology will be centered at the origin.
        :return:
            A reference to the morphology object.
        """

        # Load the morphology file
        self.load_morphology_file(center_at_origin=center_at_origin)

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
