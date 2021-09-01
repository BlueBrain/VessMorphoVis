####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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
from mathutils import Vector

# Internal imports
import vmv
import vmv.bbox
import vmv.consts
import vmv.file
import vmv.skeleton


####################################################################################################
# @SWCLoader
####################################################################################################
class SWCLoader:
    """SWC morphology loader for reading vasculature datasets with the same structure like neurons.

    NOTE: This loader is mainly added to load datasets obtained from the BraVa database available at
    http://cng.gmu.edu/brava/home.php?s=1&name_browser=false.
    NOTE: This representation is using acyclic graphs and therefore it ignores any loops in
    the dataset.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology_file):
        """Constructor

        :param morphology_file:
            A given .SWC morphology file.
        """

        # Set the path to the given h5 file
        self.morphology_file = morphology_file

        # A list of all the points (or samples) in the morphology file
        self.points_list = list()

        # A list of radii of all the samples in the morphology
        self.radii_list = list()

        # A list of all the sections that were extracted from the loaded data
        self.sections_list = list()

        # Morphology bounding box, initially None, till being computed
        self.bounding_box = None

        # Graph roots
        # NOTE: The data set could have multiple roots, i.e. sections with no parents. In this case,
        # we should treat each root as an independent object and later group all of then into a
        # single object.
        self.roots = list()

        # The number of loaded vertices or samples
        self.number_loaded_vertices = None

        # The number of loaded strands or segments
        self.number_loaded_strands = None

        # The samples list parsed from the morphology file
        self.parsed_samples_list = list()

        # A list of all the samples parsed from the morphology file, to be used as a lookup table
        # to construct the morphology skeleton directly
        # http://www.neuronland.org/NLMorphologyConverter/MorphologyFormats/SWC/Spec.html
        # Each sample in this list has the following structure:
        #       [0] The index of the sample or sample number
        #       [1] The type of the sample or structure identifier
        #       [2] Sample x-coordinates
        #       [3] Sample y-coordinates
        #       [4] Sample z-coordinates
        #       [5] Sample radius
        #       [6] The index of the parent sample
        self.samples_list = list()

        # A list of the indices of the terminals of the sections
        # This list is only updated once during the morphology loading, and then used to build the
        # sections later in an accelerated way
        self.sections_terminal_samples_indices = list()

        # A list of the indices of each 'disconnected' section in the morphology
        self.sections_samples_indices_list = list()

        # A list of continuous paths extracted from the morphology file
        self.paths = list()

    ################################################################################################
    # @build_connected_paths_from_samples
    ################################################################################################
    def build_connected_paths_from_samples(self):
        """Construct a list of connected paths from the samples.
        """

        # Since we have the soma index equal to 1, then start from index number 2
        index = 2

        # A temporary list to append the indices of each path
        path = list()

        # Process the entire samples list
        while True:

            # Iterate over two samples to verify their connectivity
            sample_i = self.samples_list[index]
            sample_j = self.samples_list[index + 1]

            if sample_i is None or sample_j is None:
                index = index + 1
                continue

            # Ensure that this is not a soma profile point
            if sample_i[vmv.consts.Skeleton.SWC_SAMPLE_TYPE_IDX] == \
                    vmv.consts.Skeleton.SWC_SOMA_SAMPLE_TYPE:
                index = index + 1
                continue

            # If the two samples are connected
            if sample_j[-1] == sample_i[0]:

                # Add the first sample to the path
                path.append(sample_i[0])

                # Append the last sample in the morphology file
                if index + 1 == self.samples_list[-1][0]:
                    path.append(sample_j[0])

            # Otherwise
            else:

                # Append the last sample to the path
                # path.append(sample_j[-1])
                path.append(sample_i[0])

                # Append the path to the paths list
                if len(path) > 0:
                    self.paths.append(path)

                # Clear the path list to search for a new path
                path = list()

            # Increment the path
            index = index + 1

            # If processing the list is break
            if index > len(self.samples_list) - 2:

                # Append the last path
                if len(path) > 0:
                    self.paths.append(path)

                # Then break
                break

        # Add the starting points and mark the terminals
        for path in self.paths:
            # Get the index of the first sample along the path
            first_sample_index = path[0]

            # Then add the parent sample index at the beginning of the path
            path.insert(0, self.samples_list[first_sample_index][-1])

            # Marking the terminals by adding the indices of the first and last samples
            self.sections_terminal_samples_indices.append(path[0])
            self.sections_terminal_samples_indices.append(path[-1])

        # Sort the sections_terminal_samples_indices list
        self.sections_terminal_samples_indices = sorted(self.sections_terminal_samples_indices)

        # Filter the repeated entries in the sections_terminal_samples_indices list
        self.sections_terminal_samples_indices = list(
            set(self.sections_terminal_samples_indices))

    ################################################################################################
    # @build_sections_from_paths
    ################################################################################################
    def build_sections_from_paths(self):
        """Builds a list of sections from the paths reconstructed during the reading of the
        morphology.
        """

        for path in self.paths:

            # A list of all the samples located along the path
            samples_located_along_path = list()

            # Get the list
            for sample_index in self.sections_terminal_samples_indices:

                # If the sample index exists in the path
                if sample_index in path:
                    # Append it to the list
                    samples_located_along_path.append(sample_index)

            # Order the list
            samples_located_along_path = sorted(samples_located_along_path)

            # Build the sections
            for i in range(0, len(samples_located_along_path) - 1):

                # A list of the section indices
                section_indices = list()

                # Get the first index along the section
                first_sample = samples_located_along_path[i]

                # Get the last index along the section
                last_sample = samples_located_along_path[i + 1]

                # Get the index of the first sample
                first_sample_index = path.index(first_sample)

                # Get the index of the last sample
                last_sample_index = path.index(last_sample)

                for j in range(first_sample_index, last_sample_index + 1):
                    section_indices.append(path[j])

                self.sections_samples_indices_list.append(section_indices)

    ################################################################################################
    # @read_samples
    ################################################################################################
    def read_samples(self,
                     center_at_origin=False):
        """Reads an SWC files and returns a list of all the samples in the file

        :param center_at_origin:
            Center the morphology at the origin.
        """

        # Open the file, read it line by line and store the result in list.
        morphology_file = open(self.morphology_file, 'r')

        # Add a dummy sample to the list at index 0 to match the indices
        # The zeroth sample always defines the soma parameters, and it is parsed independently
        self.parsed_samples_list.append([0, 0, 0.0, 0.0, 0.0, 0.0, 0])

        # Translation vector in case the file is not centered at the origin
        translation = Vector((0.0, 0.0, 0.0))

        # Construct a string from each line in the morphology file
        string_list = list()
        for line in morphology_file:
            string_list.append(line)

        # For each line in the string list
        for line in string_list:

            # Ignore lines with comments that have '#'
            # TODO: Possibly a bug
            if '#' in line:
                continue

            # Ignore empty lines
            if not line.strip():
                continue

            # Extract the data from the line
            data = ' '.join(line.split())
            data = data.strip('\n').split(' ')

            # If unwanted characters exit, remove them
            for i in data:

                # Unwanted spaces
                if i == '':
                    data.remove(i)

                # Unwanted new lines
                if '\n' in i:
                    i.replace('\n', '')

            # Get the index
            index = int(data[vmv.consts.Skeleton.SWC_SAMPLE_INDEX_IDX])

            # Get the branch type
            sample_type = int(data[vmv.consts.Skeleton.SWC_SAMPLE_TYPE_IDX])

            # If the sample type doesn't match a soma, an axon, a basal dendrite or an apical
            # dendrite, just consider it a basal dendrite
            if sample_type > 4:
                sample_type = vmv.consts.Skeleton.SWC_BASAL_DENDRITE_SAMPLE_TYPE

                # Get the X-coordinate
            x = float(data[vmv.consts.Skeleton.SWC_SAMPLE_X_COORDINATES_IDX])

            # Get the Y-coordinate
            y = float(data[vmv.consts.Skeleton.SWC_SAMPLE_Y_COORDINATES_IDX])

            # Get the Z-coordinate
            z = float(data[vmv.consts.Skeleton.SWC_SAMPLE_Z_COORDINATES_IDX])

            # Get the sample radius
            radius = float(data[vmv.consts.Skeleton.SWC_SAMPLE_RADIUS_IDX])

            # Get the sample parent index
            parent_index = int(data[vmv.consts.Skeleton.SWC_SAMPLE_PARENT_INDEX_IDX])

            # If this is the first (centric) sample, get the translation vector
            if parent_index == -1:
                translation[0] = x
                translation[1] = y
                translation[2] = z

            # Update the coordinates if the morphology is transformed
            if center_at_origin:
                x = x - translation[0]
                y = y - translation[1]
                z = z - translation[2]

            if sample_type == 0 and parent_index > -1:
                sample_type = vmv.consts.Skeleton.SWC_BASAL_DENDRITE_SAMPLE_TYPE

            # Add the sample to the list
            self.parsed_samples_list.append([index, sample_type, x, y, z, radius, parent_index])

            # Add this point to the points list with the position and radius
            self.points_list.append([x, y, z, index])

            # Radii
            self.radii_list.append(radius)

        # Search for the largest index of the samples
        largest_index = 0
        for i_sample in self.parsed_samples_list:
            if i_sample[0] > largest_index:
                largest_index = i_sample[0]

        # Create the actual samples list, and take into consideration the added soma sample
        for i in range(largest_index + 1):
            self.samples_list.append(None)

        # Set the samples at their corresponding indices to make it easy to index them, and keep
        # the rest to Null and double check them later
        for i_sample in self.parsed_samples_list:
            self.samples_list[i_sample[0]] = i_sample

        # Update the meta-data
        self.number_loaded_vertices = len(self.samples_list)

    ################################################################################################
    # @get_vmv_sample_from_samples_list
    ################################################################################################
    def get_vmv_sample_from_samples_list(self,
                                         sample_index):
        """Gets a VessMorphoVis sample from the original list of samples that was parsed from
        the SWC morphology file.

        :param sample_index:
            The index of the sample.
        :return:
            A VessMorphoVis sample object.
        """

        # Get the sample and its data
        sample_data = self.samples_list[sample_index]

        # Index of the sample
        sample_id = sample_data[0]

        # The cartesian coordinates of the sample
        sample_point = Vector((sample_data[2], sample_data[3], sample_data[4]))

        # Sample radius
        sample_radius = sample_data[5]

        # The index of the parent sample
        parent_sample_id = sample_data[6]

        # Construct a VMV sample object
        vmv_sample = vmv.skeleton.Sample(point=sample_point, radius=sample_radius, index=sample_id,
                                         parent_index=parent_sample_id)

        # Return a reference to the reconstructed object
        return vmv_sample

    ################################################################################################
    # @build_arbors_from_samples
    ################################################################################################
    def build_arbors_from_samples(self,
                                  arbor_type):
        """Builds a list of connected arbors from a list of disconnected samples for a given or
        specific type

        :param arbor_type:
            The type of the arbor.

        :return:
            A list of trees, each representing an arbor of the morphology skeleton.
        """

        # Get the sections that are specific to the arbor
        sections = self.get_sections_of_specific_type(arbor_type)

        # Build a list of arbors from a list of sections
        arbors = vmv.skeleton.ops.build_arbors_from_sections(sections)

        # Return a reference to the constructed arbors
        return arbors

    ################################################################################################
    # @get_samples_list_by_type
    ################################################################################################
    def get_samples_list_by_type(self,
                                 sample_type):
        """Gets a list of samples of a specific type from the list of morphological samples that
        was constructed after reading the SWC file.

        :param sample_type:
            The type of samples, belonging to which branch.
        :return:
            A list of samples that are of specific type.
        """

        # A list of samples that are similar to the given type
        selected_samples_list = list()

        # For each sample in the given samples list
        for sample in self.samples_list:

            if sample is None:
                continue

            # If the types are matching
            if sample[1] == sample_type:

                # Append the sample to the list
                selected_samples_list.append(sample)

        # Return the list of samples
        return selected_samples_list

    ################################################################################################
    # @get_sections_of_specific_type
    ################################################################################################
    def get_sections_of_specific_type(self,
                                      arbor_type):
        """Returns a list of sections of specific type.

        :param arbor_type:
            The type of the requested sections.
        :return:
            A list of all the sections that have specific type.
        """

        # Sections list
        sections_list = list()

        # A list that only contains the samples of the arbor of the requested type
        arbor_sections_samples_indices_list = list()

        # For each section
        for section_samples_indices in self.sections_samples_indices_list:

            # Get the last sample along this section
            last_sample = self.samples_list[section_samples_indices[-1]]

            # If the type is matching, just randomly take the last sample
            if str(last_sample[1]) == str(arbor_type):

                # Append to the list
                arbor_sections_samples_indices_list.append(section_samples_indices)

        # For each section
        for arbor_section in arbor_sections_samples_indices_list:

            # Construct the samples list
            samples_list = list()

            # A flag to indicate whether this section is root or not
            is_root_section = False

            # For each sample in the section
            for arbor_sample_index in arbor_section:

                # If this is a root sample, indicate that this section is a root
                if str(arbor_sample_index) == str(-1):
                    continue

                # Ignore the soma sample
                if str(self.samples_list[arbor_sample_index][0]) == str(1):
                    continue

                if self.samples_list[arbor_sample_index][-1] == -1:
                    is_root_section = True
                    continue

                # Get the a VMV sample based on its index
                vmv_sample = self.get_vmv_sample_from_samples_list(arbor_sample_index)

                # Add a new NMV sample
                samples_list.append(vmv_sample)

            # Construct a VMV section that ONLY contains the samples list, and UPDATE its other
            # members later when all the other sections are reconstructed
            vmv_section = vmv.skeleton.Section(samples=samples_list)

            # If this is a root sample, indicate that this section is a root
            if is_root_section:
                vmv_section.parent_index = -1
                vmv_section.parent = None

            # Append the reconstructed sections to the sections list
            sections_list.append(vmv_section)

        # Label the sections and set different indices to them
        for i, section in enumerate(sections_list):
            # Update the section index
            section.index = i

            # Update the section type
            section.type = arbor_type

        # Updates the sections parenting
        for section in sections_list:
            vmv.skeleton.ops.update_section_parenting(section, sections_list)

        # Return a list of sections
        return sections_list

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
            Re-samples the morphology skeleton to reduce the number of samples along the
            section and remove the redundant samples.
        :return:
            A reference to the morphology object.
        """

        # Read all the samples from the morphology file an store them into a list
        self.read_samples(center_at_origin=center_at_origin)

        # Construct the connected paths from the samples list
        self.build_connected_paths_from_samples()

        # Construct the individual sections from the paths
        self.build_sections_from_paths()

        # Construct the sections list from apical dendrites
        self.sections_list.extend(self.get_sections_of_specific_type(
            vmv.consts.Skeleton.SWC_APICAL_DENDRITE_SAMPLE_TYPE))

        # From basal dendrites
        self.sections_list.extend(self.get_sections_of_specific_type(
            vmv.consts.Skeleton.SWC_BASAL_DENDRITE_SAMPLE_TYPE))

        # From axon
        self.sections_list.extend(self.get_sections_of_specific_type(
            vmv.consts.Skeleton.SWC_AXON_SAMPLE_TYPE))

        # Update the meta-data, regarding the sections
        self.number_loaded_strands = len(self.sections_list)

        # Resample the morphology skeleton, if needed
        if resample_morphology:
            for section in self.sections_list:
                vmv.skeleton.resample_section_adaptively(section)

        # Get the morphology name from the file
        morphology_name = vmv.file.ops.get_file_name_from_path(self.morphology_file)

        # Construct the morphology object following to reading the file
        morphology_object = vmv.skeleton.Morphology(
            name=morphology_name, file_path=self.morphology_file,
            number_samples=self.number_loaded_vertices,
            number_sections=self.number_loaded_strands,
            sections_list=self.sections_list, roots=self.roots)

        # Return the object
        return morphology_object
