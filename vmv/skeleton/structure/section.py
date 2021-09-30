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
# Section
####################################################################################################
class Section:
    """Vasculature morphology section or strand.

    The section is composed of a set of segments, and each segment is composed of two samples.
    Each sample has a point in the cartesian coordinates and a radius that reflects the cross
    sectional area of the morphology at a certain point.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 index=None,
                 samples=None):
        """Constructor.

        :param index:
            Unique section index in the morphology.
        :param samples:
            A list of samples along the section.
        """

        # Section index
        self.index = index

        # The list of samples the section composes 
        self.samples = samples if samples is not None else list()

        # Parent sections, initially empty list till the reconstruction of the entire data set
        self.parents = list()

        # Children sections, initially empty list till the reconstruction of the entire data set
        self.children = list()

        # A flag that indicates whether the section is traversed during the construction of the
        # tree or not. This flag is reset after each traversal to False.
        self.traversed = False

        # The average radius of the first sample w.r.t to pre-connected-sections
        self.first_sample_average_radius = 0

        # The average radius of the last sample w.r.t post-connected sections
        self.last_sample_average_radius = 0

    ################################################################################################
    # @has_children
    ################################################################################################
    def has_children(self):
        """Checks if the section has children or not.

        :return:
            True or False
        """

        if len(self.children) > 0:
            return True
        return False

    ################################################################################################
    # @has_parent
    ################################################################################################
    def has_parent(self):
        """Checks if the section has any parents or not.

        :return:
            True or False
        """

        if len(self.parents) > 0:
            return True
        return False

    ################################################################################################
    # @is_root
    ################################################################################################
    def is_root(self):
        """Checks if the section is root or not.

        :return:
            True or False
        """

        if len(self.parents) == 0:
            return True
        return False

    ################################################################################################
    # @is_leaf
    ################################################################################################
    def is_leaf(self):
        """Checks if the section is leaf or not.

        :return:
            True or False
        """

        if len(self.children) == 0:
            return True
        return False

    ################################################################################################
    # @all_children_traversed
    ################################################################################################
    def all_children_traversed(self):
        """Checks if all the children sections have been traversed or not.

        :return:
            True or False
        """

        for child in self.children:
            if not child.traversed:
                return False

    ################################################################################################
    # @has_single_parent
    ################################################################################################
    def has_single_parent(self):
        """Checks if the section has a single parent or not.

        :return:
            True or False.
        """
        if len(self.parents) == 1:
            return True
        return False

    ################################################################################################
    # @has_multiple_parents
    ################################################################################################
    def has_multiple_parents(self):
        """Checks if the section has multiple parents or not.

        :return:
            True or False.
        """
        if len(self.parents) > 1:
            return True
        return False

    ################################################################################################
    # @has_siblings
    ################################################################################################
    def has_siblings(self):
        """Checks if the section has siblings ot not.

        :return:
            True or False.
        """

        if not self.has_children() or len(self.children) > 1:
            return False

        if len(self.children[0].parents) > 1:
            return True

    ################################################################################################
    # @compute_terminals_average_radii
    ################################################################################################
    def compute_terminals_average_radii(self):
        """Compute the average radii of the terminal samples.
        """

        # First sample
        self.first_sample_average_radius = self.samples[0].radius

        # If parents exist
        if len(self.parents) > 0:
            for parent in self.parents:
                self.first_sample_average_radius += parent.samples[-1].radius
            self.first_sample_average_radius /= (len(self.parents) + 1)

        # Last sample
        self.last_sample_average_radius = self.samples[-1].radius

        # If children exist
        if len(self.children) > 0:
            for child in self.children:
                self.last_sample_average_radius += child.samples[0].radius
            self.last_sample_average_radius /= (len(self.children) + 1)

    ################################################################################################
    # @update_terminals_radii
    ################################################################################################
    def update_terminals_radii(self):
        """Updates the radii of the terminal samples after computing the average.
        """

        # First sample
        self.samples[0].radius = self.first_sample_average_radius

        # Last sample
        self.samples[-1].radius = self.last_sample_average_radius




