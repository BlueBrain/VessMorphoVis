####################################################################################################
# Copyright (c) 2019 - 2023, EPFL / Blue Brain Project
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

# Internal modules
import vmv.bmeshi
import vmv.builders
import vmv.enums
import vmv.mesh
import vmv.skeleton
import vmv.utilities
import vmv.scene
from .base import MeshBuilder


####################################################################################################
# @SkinningBuilder
####################################################################################################
class SkinningBuilder(MeshBuilder):

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology skeleton to create the mesh for.
        :param options:
            Loaded options from VessMorphoVis.
        """

        # Base
        MeshBuilder.__init__(self, morphology=morphology, options=options)

        # The mesh builder name
        self.builder_name = 'SkinningBuilder'

        # Final mesh center
        self.center = (0.0, 0.0, 0.0)

        # Create the skeleton materials during the initialization
        self.create_skeleton_materials()

        # A list containing the radii of the vertices in order
        self.indexed_samples_list = list()

    ################################################################################################
    # @skin_morphology_into_mesh
    ################################################################################################
    def skin_morphology_into_mesh(self):
        """Generate a vascular mesh from the morphology using Skinning modifier."""

        # Create the bmesh object
        bmesh_object = vmv.bmeshi.create_bmesh_object()

        tqdm = vmv.utilities.import_module('tqdm')
        if tqdm:
            _loop = tqdm.tqdm(self.morphology.sections_list,
                              desc='\t* Building Graph (Vertices)',
                              bar_format=vmv.consts.String.BAR_FORMAT)
        else:
            _loop = self.morphology.sections_list

        # Build the graph bmesh from the sections
        vertex_index = 0
        for i_section in _loop:

            # The section must have at least two samples to be considered
            if len(i_section.samples) < 2:
                continue

            # Add the corresponding vertex of the first sample of the section
            vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
                bmesh_object, i_section.samples[0].point)
            self.indexed_samples_list.append(i_section.samples[0].radius)
            vertex_index += 1

            # Add the vertices of the rest of samples
            for j in range(1, len(i_section.samples)):
                vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
                    bmesh_object, i_section.samples[j].point)
                self.indexed_samples_list.append(i_section.samples[j].radius)
                vertex_index += 1

        # Update the geometry of the bmesh to be able to query it
        bmesh_object.verts.ensure_lookup_table()

        # Reconstruct the edges of the graph
        vertex_index = 0
        if tqdm:
            _loop = tqdm.tqdm(self.morphology.sections_list,
                              desc='\t* Building Graph (Edges)',
                              bar_format=vmv.consts.String.BAR_FORMAT)
        else:
            _loop = self.morphology.sections_list
        for i_section in _loop:
            for j in range(0, len(i_section.samples) - 1):
                v1 = bmesh_object.verts[j + vertex_index]
                v2 = bmesh_object.verts[j + vertex_index + 1]
                bmesh_object.edges.new((v1, v2))
            vertex_index += len(i_section.samples)

        # Convert the bmesh to a mesh
        self.mesh = vmv.bmeshi.convert_bmesh_to_mesh(bmesh_object=bmesh_object, name='Graph')
        vmv.scene.set_active_object(self.mesh)

        # Store the radii within the local bevel_weight parameter of the mesh before losing them
        for i in range(len(self.mesh.data.vertices)):
            self.mesh.data.vertices[i].bevel_weight = self.indexed_samples_list[i] * 0.001

        # The graph mesh must be active
        vmv.scene.set_active_object(self.mesh)

        # Remove the duplicate vertices from the graph
        vmv.mesh.remove_doubles(mesh_object=self.mesh, distance=0.01)

        # The graph mesh must be active
        vmv.scene.set_active_object(self.mesh)

        # Separate the graph mesh into partitions
        vmv.bops.separate_mesh_partitions()

        # Get a list of all the graph partitions meshes
        graph_partitions = vmv.scene.get_list_of_objects_containing_string('Graph')

        # Deselect all objects in the scene
        vmv.scene.deselect_all()

        tqdm = vmv.utilities.import_module('tqdm')
        if tqdm:
            _loop = tqdm.tqdm(enumerate(graph_partitions),
                              desc='\t* Skinning Graph Partitions',
                              bar_format=vmv.consts.String.BAR_FORMAT)
        else:
            _loop = self.morphology.sections_list

        for i, graph_partition in _loop:

            # Select the graph partition mesh
            graph_partition.select_set(True)

            # Set this mesh partition to be active
            vmv.scene.set_active_object(graph_partition)

            # Update the radii of the branching points
            vmv.skeleton.adjust_branching_points_radii(mesh_object=graph_partition)

            # Add the Skinning modifier
            # graph_partition.modifiers.new(name="Skin", type='SKIN')
            vmv.bops.create_skin_modifier(mesh_object=graph_partition)

            # Update the radii of the resulting skinned mesh
            for j in range(0, len(graph_partition.data.skin_vertices[0].data)):
                vertex = graph_partition.data.skin_vertices[0].data[j]
                radius = graph_partition.data.vertices[j].bevel_weight * 1000
                vertex.radius = radius, radius

            # Apply the skinning modifier
            vmv.bops.apply_skin_modifier()

            # Subdivide the mesh
            vmv.mesh.apply_surface_subdivision(graph_partition, level=2)

        # Join all the meshes into a single mesh object
        self.mesh = vmv.mesh.join_mesh_objects(
            mesh_list=graph_partitions, name='%s' % self.morphology.name)

        # Select the resulting joint mesh
        vmv.scene.set_active_object(scene_object=self.mesh)

        # Shade the mesh object
        vmv.bops.shade_smooth()

    ################################################################################################
    # @build_mesh
    ################################################################################################
    def build_mesh(self):
        """Reconstructs the vascular mesh.

        :return:
            A reference to the reconstructed vascular mesh.
        """

        # Verify and repair the morphology
        # self.verify_and_repair_morphology()

        vmv.logger.header('Building Mesh: %s' % self.builder_name)

        # Update the center of the mesh to the center of the bounding box of the morphology
        self.center = self.morphology.bounding_box.center

        # Generate a vascular mesh from the morphology using Skinning modifier
        self.skin_morphology_into_mesh()

        # Update its name with the mesh suffix to be able to locate it
        self.set_default_mesh_name()

        # Assign the material to the mesh
        self.assign_material_to_mesh()

        # Tessellate Mesh
        self.tessellate_mesh()

        # Mission done
        vmv.logger.header('Done!')

        # Return a reference to the created mesh
        return self.mesh
