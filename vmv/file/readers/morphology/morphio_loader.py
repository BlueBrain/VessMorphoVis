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
from pathlib import Path
from itertools import chain

# Blender imports
from mathutils import Vector

# Internal imports
import vmv
import vmv.bbox
import vmv.consts
import vmv.file
import vmv.skeleton


################################################################################################
# @SectionMorphIO
################################################################################################
class SectionMorphIO:
    """An auxilliary structure to keep track on the

    """
    def __init__(self, section):
        self.id = section.id
        self.points = section.points
        self.radii = section.diameters * 0.5
        self.predecessors = section.predecessors
        self.successors = section.successors

####################################################################################################
# @H5Reader
####################################################################################################
class MorphIOLoader:
    """A generic morphology reader based on the MorphIO library.
    """

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

        # A list of all the points (or samples) in the morphology file
        self.points_list = list()

        # A list of all the radii in the morphology
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

    ################################################################################################
    # @read_data_from_file
    ################################################################################################
    def read_data_from_file(self,
                            center_at_origin=False,
                            resample_morphology=False):
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
        # Raise an exception if we cannot import the h5py module
        except ImportError as e:
            print('ERROR: Cannot read the file [%s]' % self.morphology_file)
            print(str(e))
            exit(0)

        # Ignore the console warning and output
        vmv.utilities.disable_std_output()

        morphology_data = vasculature.Vasculature(self.morphology_file)

        # Get a list of points using the iterator
        points = chain.from_iterable(section.points for section in morphology_data.iter())
        points_list = list(map(Vector, points))

        # Compute the bounding box of the morphology
        self.bounding_box = vmv.bbox.compute_bounding_box_for_list_of_points(
            points_list)

        # Transform the data of the morphology into a normal structure
        sections_morphio = list(map(SectionMorphIO, morphology_data.iter()))

        index_parent_dictionary = {
            sec.id: i_section
            for i_section, sec in enumerate(sections_morphio)
        }

        # Construct a list of sections to be given to the constructor
        sections_list = list()
        for section_morphio in sections_morphio:

            # Section id
            section = vmv.skeleton.Section(index=section_morphio.id)

            # Samples list
            samples = list()
            for point, radius in zip(section_morphio.points, section_morphio.radii):
                point = Vector(point)

                # Center the morphology at the origin if required by the user
                if center_at_origin:
                    point -= Vector(self.bounding_box.center)

                samples.append(vmv.skeleton.Sample(
                    point=point,
                    radius=radius))
            section.samples = samples
            sections_list.append(section)

        # Updating parents and children
        for section_morphio, section in zip(sections_morphio, sections_list):
            for parent in section_morphio.predecessors:
                section.parents.append(sections_list[index_parent_dictionary[parent.id]])

            for child in section_morphio.successors:
                section.children.append(sections_list[index_parent_dictionary[child.id]])

        # Data
        self.sections_list = sections_list
        self.points_list = points_list
        self.radii_list = np.hstack([0.5 * section.diameters for section in
                                     morphology_data.iter()]).tolist()

        self.roots = [section for section in self.sections_list if section.is_root()]

        # Enable std output again
        vmv.utilities.enable_std_output()


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
        self.read_data_from_file(resample_morphology=resample_morphology,
                                 center_at_origin=center_at_origin)

        # Resample the morphology skeleton if required
        if resample_morphology:
            for section in self.sections_list:
                vmv.skeleton.resample_section_adaptively(section)

        # Construct the morphology object following to reading the file
        morphology_object = vmv.skeleton.Morphology(
            morphology_name=Path(self.morphology_file).name,
            morphology_file_path=self.morphology_file,
            points_list=self.points_list,
            sections_list=self.sections_list,
            radii_list=self.radii_list,
            roots=self.roots)

        # Return the object
        return morphology_object
