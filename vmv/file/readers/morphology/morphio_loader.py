####################################################################################################
# Copyright (c) 2019, Ecole Polytechnique Federale de Lausanne / Blue Brain Project
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
import copy

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
class MorphIOLoader:
    """A generic morphology reader based on the MorphIO library.
    """

    ################################################################################################
    # @SectionMorphIO
    ################################################################################################
    class SectionMorphIO:
        """An auxiliary structure to keep track on the structure.
        """

        def __init__(self, id, points, radii, predecessors, successors):
            self.id = id
            self.points = points
            self.radii = radii
            self.predecessors = predecessors
            self.successors = successors

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology_file):
        """Constructor

        :param morphology_file:
            A given .H5 morphology file.
        """

        # Set the path to the given morphology file irrespective to its extension
        self.morphology_file = morphology_file

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

    ################################################################################################
    # @read_data_from_file
    ################################################################################################
    def read_data_from_file(self,
                            center_at_origin=False):
        """Loads the data from the given file in the constructor.

        :param: center_at_origin:
            Centers the morphology at the origin.
        """

        try:

            # Import the required module
            import numpy
            import vmv.utilities
            import vmv.skeleton
            import morphio.vasculature as vasculature
            from morphio import RawDataError, VasculatureSectionType

            # Ignore the console warning and output
            vmv.utilities.disable_std_output()

            # Load the morphology data using MorphIO
            morphology_data = vasculature.Vasculature(self.morphology_file)

            # Get a list of points using the iterator
            points = numpy.vstack([section.points for section in morphology_data.iter()])

            # Get a list of all the points to compute the bounding box quickly
            points_list = [Vector((point[0], point[1], point[2])) for point in points]

            # Compute the bounding box of the morphology
            self.bounding_box = vmv.bbox.compute_bounding_box_for_list_of_points(points_list)

            # Update the number of samples
            self.number_loaded_vertices = copy.deepcopy(len(points_list))

            # Delete the points list
            points_list.clear()

            # Transform the data of the morphology into a normal structure
            sections_morphio = numpy.vstack(
                [self.SectionMorphIO(section.id, section.points, 0.5 * section.diameters,
                                     section.predecessors, section.successors) for section in
                 morphology_data.iter()])

            # A dictionary to keep track on the indices of the parents in the array
            index_parent_dictionary = {}
            for i_section, sec in enumerate(sections_morphio):
                index_parent_dictionary[sec[0].id] = i_section

            # Construct a list of sections to be given to the Morphology constructor
            sections_list = list()

            # On-a-per-section basis
            for section_morphio in sections_morphio:

                # Just construct the section
                section = vmv.skeleton.Section(index=section_morphio[0].id)

                # Build the Samples list
                samples = list()
                for i in range(len(section_morphio[0].points)):

                    # A reference to the point
                    point = Vector((section_morphio[0].points[i][0],
                                    section_morphio[0].points[i][1],
                                    section_morphio[0].points[i][2]))

                    # Center the morphology at the origin if required by the user
                    if center_at_origin:
                        point[0] -= self.bounding_box.center[0]
                        point[1] -= self.bounding_box.center[1]
                        point[2] -= self.bounding_box.center[2]

                    # Build the sample
                    sample = vmv.skeleton.Sample(point=point, radius=section_morphio[0].radii[i])

                    # Add it to the samples list
                    samples.append(sample)

                # Link the samples list to the section
                section.samples = samples

                # Append the section to the sections list
                sections_list.append(section)

            # Updating parents and children
            # This is only needed in case we use the ConnectedSectionsBuilder
            for i in range(len(sections_list)):

                # Update the parents IDs
                parents_ids = [j.id for j in sections_morphio[i][0].predecessors]

                # Update the children IDs
                children_ids = [k.id for k in sections_morphio[i][0].successors]

                # Update the parents list
                sections_list[i].parents = [sections_list[index_parent_dictionary[parent_id]]
                                            for parent_id in parents_ids]
                # Update the children list
                sections_list[i].children = [sections_list[index_parent_dictionary[children_id]]
                                             for children_id in children_ids]
            # Data
            self.sections_list = sections_list

            # Number of strands
            self.number_loaded_strands = len(sections_list)

            # Detect the root sections and update the list
            for section in self.sections_list:
                if section.is_root():
                    self.roots.append(section)

            # Enable std output again
            vmv.utilities.enable_std_output()

        # Raise an exception if we cannot import the h5py module
        except ImportError:

            print('ERROR: Cannot *import h5py* to read the file [%s]' % self.morphology_file)
            exit(0)

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
        self.read_data_from_file(center_at_origin=center_at_origin)

        # Resample the morphology skeleton if required
        if resample_morphology:
            for section in self.sections_list:
                vmv.skeleton.resample_section_adaptively(section)

        # Get the morphology name from the file
        morphology_name = vmv.file.ops.get_file_name_from_path(self.morphology_file)

        # Construct the morphology object following to reading the file
        morphology_object = vmv.skeleton.Morphology(
            name=morphology_name,
            file_path=self.morphology_file,
            number_samples=self.number_loaded_vertices,
            number_sections=self.number_loaded_strands,
            sections_list=self.sections_list, roots=self.roots)

        # Return the object
        return morphology_object
