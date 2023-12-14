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
import bmesh


####################################################################################################
# @add_new_vertex_to_bmesh
####################################################################################################
def add_new_vertex_to_bmesh(bmesh_object,
                            vertex_index,
                            location=(0.0, 0.0, 0.0)):
    """Adds a new vertex to the given bmesh object. This function is relatively slower than the
    @add_vertex_to_bmesh_without_lookup function due to calling the lookup function that updates
    the indices of the arrays of the bmesh object.

    :param bmesh_object:
        A given bmesh object to append a vertex to it.
    :param vertex_index:
        The index of the new vertex.
    :param location:
        The location of the input vertex.
    """

    # Create a new vertex
    bmesh.ops.create_vert(bmesh_object)

    # Update the bmesh vertices
    bmesh_object.verts.ensure_lookup_table()

    # Get a reference to the newly created vertex
    vertex = bmesh_object.verts[vertex_index]

    # Update the location of the newly created vertex
    vertex.co = location


####################################################################################################
# @add_vertex_to_bmesh_without_lookup
####################################################################################################
def add_vertex_to_bmesh_without_lookup(bmesh_object,
                                       location):
    """Adds a new vertex to the given bmesh object at the given location. This function is much
    faster that the normal @add_new_vertex_to_bmesh function because it does not require any lookup
    function which kills the performance.

    :param bmesh_object:
        A given bmesh object to append a vertex to it.
    :param location:
        The location of the new vertex to be added to the object.
    """

    bmesh_object.verts.new(location)


####################################################################################################
# @get_vertex_from_index
####################################################################################################
def get_vertex_from_index(bmesh_object,
                          vertex_index):
    """Gets a vertex of a bmesh object from its index.

    :param bmesh_object:
        A given bmesh object.
    :param vertex_index:
        The index of the vertex we need to get.
    :return:
        A reference to the vertex.
    """

    # Update the bmesh vertices
    bmesh_object.verts.ensure_lookup_table()

    # Get the vertex from its index
    vertex = bmesh_object.verts[vertex_index]

    # Return a reference to the vertex
    return vertex


####################################################################################################
# @extrude_vertex_towards_point
####################################################################################################
def extrude_vertex_towards_point(bmesh_object,
                                 index,
                                 point):
    """Extrude a vertex of a bmesh object to a given point in space.

    :param bmesh_object:
        A given bmesh object.
    :param index:
        The index of the vertex that will be extruded.
    :param point:
        A point in three-dimensional space.
    :return:
    """

    # Get a reference to the vertex
    vertex = get_vertex_from_index(bmesh_object, index)

    # Extrude the vertex (sort of via duplication)
    extruded_vertex = bmesh.ops.extrude_vert_indiv(bmesh_object, verts=[vertex])
    extruded_vertex = extruded_vertex['verts'][0]

    # Note that the extruded vertex is located at the same position of the original one
    # So we should update the coordinate of the extruded vertex to the given point
    extruded_vertex.co = point

    # Return a reference to the extruded vertex
    return extruded_vertex
