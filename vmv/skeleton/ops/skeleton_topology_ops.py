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

# Internal imports
import vmv.bmeshi
import vmv.bops
import vmv.scene


####################################################################################################
# @adjust_branching_points_radii
####################################################################################################
def adjust_branching_points_radii(mesh_object):
    """Adjust the radii of the branching samples.

    :param mesh_object:
        A given mesh object representing the vascular graph centerline.
    """

    # Deselect all the objects in the scene
    vmv.scene.deselect_all()

    # Activate the given mesh object
    vmv.scene.set_active_object(scene_object=mesh_object)

    # Switch to edit mode to be able to select the vertices, the mesh must be selected and active
    vmv.bops.switch_to_edit_mode()

    # Converts the mesh object into a bmesh object
    bmesh_object = vmv.bmeshi.convert_from_mesh_object(mesh_object=mesh_object)

    # Find the vertices that have at least three edges (branching vertices)
    branching_vertices = list()
    for vertex in bmesh_object.verts:

        # For a vertex to be a branching point, it must have at least 3 connected edges
        if len(vertex.link_edges) > 2:

            # A list that will contain the connecting vertices
            connecting_vertices = list()

            # Get the index of this branching vertex
            branching_vertex_index = vertex.index

            # Get the index of the other vertex
            for edge in vertex.link_edges:

                # Get the two vertices of the edge
                v1_index = edge.verts[0].index
                v2_index = edge.verts[1].index

                if v1_index == branching_vertex_index:
                    connecting_vertices.append(v2_index)
                else:
                    connecting_vertices.append(v1_index)

            # Construct the branching vertices
            branching_vertices.append([branching_vertex_index, connecting_vertices])

    # Switch back to the object mode
    vmv.bops.switch_to_object_mode()

    # Update the radii
    for element in branching_vertices:

        # Get the index of the branching vertex
        branching_vertex_index = element[0]

        # Get the indices of the edge vertices
        v1_index = element[1][0]
        v2_index = element[1][1]
        v3_index = element[1][2]

        # Get the branching vertex
        branching_vertex = mesh_object.data.vertices[branching_vertex_index]

        # Get the vertices
        v1 = mesh_object.data.vertices[v1_index]
        v2 = mesh_object.data.vertices[v2_index]
        v3 = mesh_object.data.vertices[v3_index]

        # Get the largest radius (the radius data is stored in the @bevel_weight member)
        largest_radius = max([v1.bevel_weight, v2.bevel_weight, v3.bevel_weight])

        # Adjust the radius of the branching vertex to the largest one
        branching_vertex.bevel_weight = largest_radius
