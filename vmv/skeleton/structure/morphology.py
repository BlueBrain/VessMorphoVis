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
import vmv.bmeshi
import vmv.consts
import vmv.mesh
import vmv.utilities


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
                 section_connectivity_available=False,
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
        :param section_connectivity_available:
            A flag to indicate whether sections connectivity is available or not.
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

        # Is the connectivity between the sections available?
        self.section_connectivity_available = section_connectivity_available

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

    ################################################################################################
    # @construct_graph_mesh
    ################################################################################################
    def construct_graph_mesh(self):

        # Create the bmesh object
        graph_bmesh = vmv.bmeshi.create_bmesh_object()

        # A linear list containing all the radii of the samples in the graph
        radii_list = list()

        # Iterate over the sections, and then the samples, and then build the bmesh
        for i_section in self.sections_list:

            # Create the first sample (or corresponding vertex)
            vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
                graph_bmesh, i_section.samples[0].point)
            radii_list.append(i_section.samples[0].radius)

            for j in range(1, len(i_section.samples)):
                vmv.bmeshi.add_vertex_to_bmesh_without_lookup(graph_bmesh,
                                                              i_section.samples[j].point)
                radii_list.append(i_section.samples[j].radius)

        graph_bmesh.verts.ensure_lookup_table()

        # Construct from the edges
        vertex_index = 0
        for i_section in self.sections_list:
            for j in range(0, len(i_section.samples) - 1):
                v1 = graph_bmesh.verts[j + vertex_index]
                v2 = graph_bmesh.verts[j + vertex_index + 1]
                graph_bmesh.edges.new((v1, v2))
            vertex_index += len(i_section.samples)

        graph_bmesh.edges.ensure_lookup_table()

        # Convert the bmesh to a mesh
        graph_mesh = vmv.bmeshi.convert_bmesh_to_mesh(bmesh_object=graph_bmesh,
                                                      name='%s Graph' % self.name)

        for i in range(len(graph_mesh.data.vertices)):
            graph_mesh.data.vertices[i].bevel_weight = (
                    radii_list[i] * vmv.consts.Skeleton.RADIUS_SCALE_DOWN_FACTOR)

        # Remove doubles
        vmv.utilities.disable_std_output()
        vmv.mesh.remove_double_points(mesh_object=graph_mesh)
        vmv.utilities.enable_std_output()

        # Return a reference to the graph mesh
        return graph_mesh

    ################################################################################################
    # @get_graph_mesh_partitions
    ################################################################################################
    def get_graph_mesh_partitions(self):

        # Return a list of the mesh partitions
        return vmv.mesh.separate_mesh_to_partitions(self.construct_graph_mesh())

    ################################################################################################
    # @get_branching_samples
    ################################################################################################
    def get_branching_samples_data(self):

        # A list to collect the branching samples data
        branching_samples_data = list()

        # Construct the graph mesh
        graph_mesh = self.construct_graph_mesh()

        # Find the vertices that have more than 3 linked edges

        # Construct a bmesh object
        graph_bmesh = vmv.bmeshi.create_bmesh_object_from_mesh_object(mesh_object=graph_mesh)

        # Compile a list of the branching sample indices
        branching_samples_indices = list()
        for v in graph_bmesh.verts:
            if len(v.link_edges) > 2:
                branching_samples_indices.append(v.index)

        # Release the bmesh object of the graph as it is not needed
        graph_bmesh.free()
        del graph_bmesh

        # Query the radii and coordinates from the graph mesh
        factor = vmv.consts.Skeleton.RADIUS_SCALE_UP_FACTOR
        for i in branching_samples_indices:
            branching_samples_data.append([graph_mesh.data.vertices[i].co,
                                           graph_mesh.data.vertices[i].bevel_weight * factor])

        # Delete the graph mesh from the scene
        vmv.scene.delete_object_in_scene(graph_mesh)

        # Return the samples list
        return branching_samples_data

    ################################################################################################
    # @construct_branching_connectivity
    ################################################################################################
    def construct_branching_connectivity(self,
                                         threshold=0.0001):
        """Constructs the connectivity between the branches (sections) if this connectivity is not
        already loaded (or existing) from the input morphology file.

        Parameters
        ----------
        threshold :
            The threshold distance between the terminal samples of the sections to consider
            them connecting branches. Default value is 0.0001.
        """

        # If the connectivity between the sections is available, then return!
        if self.section_connectivity_available:
            return

        # Verify the installation of the tqdm module in the system
        tqdm = vmv.utilities.import_module('tqdm')
        if tqdm:
            _loop = tqdm.tqdm(self.sections_list, desc='\t* Establishing Connectivity')
        else:
            _loop = self.sections_list

        # Do it on a per-section-basis
        for i_section in _loop:
            i_first_sample = i_section.samples[0]
            i_last_sample = i_section.samples[-1]

            for j_section in self.sections_list:
                if i_section.index == j_section.index:

                    # This is the same section, continue
                    continue

                j_first_sample = j_section.samples[0]
                j_last_sample = j_section.samples[-1]

                if (i_first_sample.point - j_first_sample.point).length < threshold:
                    i_section.parents.append(j_section)
                    j_section.children.append(i_section)

                if (i_first_sample.point - j_last_sample.point).length < threshold:
                    i_section.parents.append(j_section)
                    j_section.children.append(i_section)

                if (i_last_sample.point - j_first_sample.point).length < threshold:
                    i_section.children.append(j_section)
                    j_section.parents.append(i_section)

                if (i_last_sample.point - j_last_sample.point).length < threshold:
                    i_section.children.append(j_section)
                    j_section.parents.append(i_section)

    ################################################################################################
    # @construct_edge_sections
    ################################################################################################
    def construct_edge_sections(self):
        """Constructs and returns an EdgeSection list that reflect a simplified version of the
        morphology.

        Returns
        -------
            A list of EdgeSection's that reflect a simplified version of the morphology, where
            each section is only represented by two samples only.
        """

        edge_sections_list = list()
        for i_section in self.sections_list:
            edge_sections_list.append(i_section.construct_edge_section())
        return edge_sections_list

