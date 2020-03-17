####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
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

# Internal imports
import vmv
import vmv.utilities



def create_bmesh_object():

    # Create a new bmesh object
    bmesh_object = bmesh.new()

    # Return a reference to the bmesh
    return bmesh_object


####################################################################################################
# @create_vertex
####################################################################################################
def create_vertex(location=(0, 0, 0)):

    # Create a new bmesh object
    bmesh_vertex = bmesh.new()

    # Create a new vertex
    bmesh.ops.create_vert(bmesh_vertex)

    bmesh.ops.translate(bmesh_vertex, verts=bmesh_vertex.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_vertex


####################################################################################################
# @add_new_vertex_to_bmesh
####################################################################################################
def add_new_vertex_to_bmesh(bmesh_object,
                            vertex_index,
                            location=(0.0, 0.0, 0.0)):


    # Create a new vertex
    bmesh.ops.create_vert(bmesh_object)

    ## Update the bmesh vertices
    bmesh_object.verts.ensure_lookup_table()
    #bmesh.ops.translate(bmesh_object, verts=[bmesh_object.verts[vertex_index]], vec=location)
    vertex = bmesh_object.verts[vertex_index]
    vertex.co = location


def add_line_segment_to_bmesh(bmesh_object,
                              point_1,
                              point_2):

    # Create a new vertex at point 1
    #v = bmesh.ops.create_vert(bmesh_object, co=point_1)

    # Update the bmesh vertices
    #bmesh_object.verts.ensure_lookup_table()

    # Extrude to the auxiliary sample
    #vmv.bmeshi.ops.extrude_vertex_towards_point(bmesh_object, v['vert'][0].index, point_2)

    vert1 = bmesh_object.verts.new(point_1)
    vert2 = bmesh_object.verts.new(point_2)
    edge = bmesh_object.edges.new([vert1, vert2])


####################################################################################################
# @create_uv_sphere
####################################################################################################
def create_uv_sphere(radius=1,
                     location=(0, 0, 0),
                     subdivisions=10):
    """Create a uv sphere bmesh object and returns a reference to that object.

    :param radius:
        The radius of the sphere.
    :param location:
        The location of the sphere, by default the origin.
    :param subdivisions:
        The number of the subdivisions of the sphere, by default 1.
    :return:
        A reference to the created ico-sphere.
    """

    # Create a new bmesh object
    bmesh_uv_sphere = bmesh.new()

    # Create a uv-sphere
    bmesh.ops.create_uvsphere(bmesh_uv_sphere, u_segments=subdivisions, v_segments=subdivisions, diameter=radius)
    # bmesh.ops.create_icosphere(bmesh_uv_sphere, subdivisions=subdivisions, diameter=radius)

    # Translate it to the specified position
    bmesh.ops.translate(bmesh_uv_sphere, verts=bmesh_uv_sphere.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_uv_sphere


####################################################################################################
# @create_ico_sphere
####################################################################################################
def create_ico_sphere(radius=1,
                      location=(0, 0, 0),
                      subdivisions=1):
    """Create an ico-sphere bmesh object and returns a reference to that object.

    :param radius:
        The radius of the sphere.
    :param location:
        The location of the sphere, by default the origin.
    :param subdivisions:
        The number of the subdivisions of the sphere, by default 1.
    :return:
        A reference to the created ico-sphere.
    """

    # Create a new bmesh object
    bmesh_ico_sphere = bmesh.new()

    # Create an ico-sphere
    bmesh.ops.create_icosphere(bmesh_ico_sphere, subdivisions=subdivisions, diameter=radius)

    # Translate it to the specified position
    bmesh.ops.translate(bmesh_ico_sphere, verts=bmesh_ico_sphere.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_ico_sphere


####################################################################################################
# @create_circle
####################################################################################################
def create_circle(radius=1,
                  location=(0, 0, 0),
                  vertices=4,
                  caps=True):
    """Create a circle bmesh object and returns a reference to that object.

    :param radius:
        The radius of the circle.
    :param location:
        The location of the circle, by default the origin.
    :param vertices:
        Number of vertices composing the circle, by default 4.
    :param caps:
        If the caps option is set to True, the circle will be covered.
    :return:
        A reference to the circle.
    """

    # Create a new bmesh object
    bmesh_circle = bmesh.new()

    # Get the version of the running Blender [MAJOR, MINOR, PATCH]
    blender_version = vmv.utilities.get_blender_version()

    # NOTE: Previous versions of blender were mistaken for the argument diameter
    if int(blender_version[0]) >= 2 and int(blender_version[1]) > 78:

        # Create a circle
        bmesh.ops.create_circle(bmesh_circle, cap_ends=caps, diameter=radius, segments=vertices)

    else:

        # Create a circle
        bmesh.ops.create_circle(bmesh_circle, cap_ends=caps, diameter=radius, segments=vertices)

    # Translate it to the specified position
    bmesh.ops.translate(bmesh_circle, verts=bmesh_circle.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_circle


####################################################################################################
# @create_bmesh_cube
####################################################################################################
def create_cube(radius=1,
                location=(0, 0, 0)):
    """Create a cube bmesh object and returns a reference to that object.

    :param radius:
        The radius (diagonal) of the cube.
    :param location:
        The location of the cube, by default the origin.
    :return:
        A reference to the cube.
    """

    # Create a new bmesh object
    bmesh_cube = bmesh.new()

    # Create a cube
    bmesh.ops.create_cube(bmesh_cube, size=radius)

    # Translate it to the specified position.
    bmesh.ops.translate(bmesh_cube, verts=bmesh_cube.verts[:], vec=location)

    # Return a reference to the bmesh
    return bmesh_cube
