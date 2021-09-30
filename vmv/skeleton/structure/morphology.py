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
from mathutils import Vector

# Internal imports
import vmv.bbox
import vmv.consts


####################################################################################################
# Morphology
####################################################################################################
class Morphology:
    """A structure that contains all the data of the morphology.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 name='VESSEL',
                 file_path=None,
                 number_samples=0,
                 number_sections=0,
                 sections_list=None,
                 roots=None,
                 bounding_box=None,
                 radius_simulation_data=None,
                 flow_simulation_data=None,
                 pressure_simulation_data=None):
        """Constructor

        :param name:
            The file name of the morphology.
        :param file_path:
            The full path to the morphology file.
        :param number_samples:
            The original number of samples as loaded from the morphology file.
        :param number_sections:
            The original number of sections as loaded from the morphology file.
        :param sections_list:
            A list of all the sections in the morphology.
        :param roots:
            A list of all the root sections in the morphology.
        :param bounding_box:
            The bounding box of the morphology.
        :param radius_simulation_data:
            Radius simulation data.
        :param flow_simulation_data:
            Flow simulation data.
        :param pressure_simulation_data:
            Pressure simulation data.
        """

        # Morphology name
        self.name = name

        # Number of samples in the morphology (as loaded from the morphology before resampling)
        self.number_samples = number_samples

        # Number of sections in the morphology (as loaded from the morphology before resampling)
        self.number_sections = number_sections

        # Morphology file path
        self.file_path = file_path

        # A list of all the sections that were extracted from the loaded data
        self.sections_list = sections_list

        # A list of all the root nodes
        self.roots = roots

        # Morphology bounding box
        self.bounding_box = bounding_box

        if bounding_box is None:
            self.bounding_box = self.compute_bounding_box()

        # A list of the radius simulation data
        self.radius_simulation_data = radius_simulation_data

        # If the morphology has radius simulations (or variations w.r.t time)
        self.has_radius_simulation = False
        if radius_simulation_data is not None and len(radius_simulation_data) > 0:
            self.has_radius_simulation = True

        # self.has_radius_simulation = True

        # A list of the flow simulation data
        self.flow_simulation_data = flow_simulation_data

        # If the morphology has blood flow simulations (or variations w.r.t time)
        self.has_flow_simulation = False
        if flow_simulation_data is not None and len(flow_simulation_data) > 0:
            self.has_flow_simulation = True

        # self.has_flow_simulation = True

        # A list of the pressure simulation data
        self.pressure_simulation_data = pressure_simulation_data

        # If the morphology has pressure simulations (or variations w.r.t time)
        self.has_pressure_simulation = False
        if pressure_simulation_data is not None and len(pressure_simulation_data) > 0:
            self.has_pressure_simulation = True

        # self.has_pressure_simulation = True

    ################################################################################################
    # @has_simulation_data
    ################################################################################################
    def has_simulation_data(self):
        """Checks if the morphology has any simulation data

        :return:
            True if the morphology has any simulation data or False otherwise.
        """

        # Radius
        if self.has_radius_simulation:
            return True

        # Flow
        if self.has_flow_simulation:
            return True

        # Pressure
        if self.has_pressure_simulation:
            return True

        # Otherwise false
        return False

    ################################################################################################
    # @get_center
    ################################################################################################
    def get_center(self):
        """Returns the origin of the morphology. Note that the @compute_bounding_box function is
        called by the constructor if an already-calculate bounding box is given.

        :return:
            Returns the center of the morphology to load it at the center.
        """
        return self.bounding_box.center

    ################################################################################################
    # @compute_bounding_box
    ################################################################################################
    def compute_bounding_box(self):

        # If the bounding box is already computed, then return it
        if self.bounding_box is not None:
            return self.bounding_box

        # Otherwise, compute it
        # Initialize the min and max points
        infinity = vmv.consts.Math.INFINITY
        p_min = Vector((infinity, infinity, infinity))
        p_max = Vector((-1 * infinity, -1 * infinity, -1 * infinity))

        # Make sure you cover all the sections
        for section in self.sections_list:

            # Make sure you cover all the samples of the section
            for sample in section.samples:

                # Coordinates
                x = sample.point[0]
                y = sample.point[1]
                z = sample.point[2]

                # PMinimum
                if x < p_min[0]:
                    p_min[0] = x
                if y < p_min[1]:
                    p_min[1] = y
                if z < p_min[2]:
                    p_min[2] = z

                # PMaximum
                if x > p_max[0]:
                    p_max[0] = x
                if y > p_max[1]:
                    p_max[1] = y
                if z > p_max[2]:
                    p_max[2] = z

        # Build bounding box object
        self.bounding_box = vmv.bbox.BoundingBox(p_min, p_max)

        # Return the bounding box
        return self.bounding_box

    ################################################################################################
    # @reset_traversal_states
    ################################################################################################
    def reset_traversal_states(self):
        """Resets the traversal state of every section in the morphology tree after the construct
        of the tree.
        """

        # The sections list must not be empty
        if self.sections_list is not None:

            # For every section
            for section in self.sections_list:

                # Reset the traversal list
                section.traversed = False

    ################################################################################################
    # @average_terminal_samples_radii
    ################################################################################################
    def average_terminal_samples_radii(self):
        """Computes the average radii of the terminal samples and update them.
        NOTE: This function is used to smooth the connections between sections. It might be better
        to implement it as a pre-processing step like the resampling.
        """

        # Compute the average radii
        for section in self.sections_list:
            section.compute_terminals_average_radii()

        # Update the radii values
        for section in self.sections_list:
            section.update_terminals_radii()
