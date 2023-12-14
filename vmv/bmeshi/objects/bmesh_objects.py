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

# Blender imports
import bmesh
from mathutils import Vector

# Internal imports
import vmv.mesh
import vmv.utilities


####################################################################################################
# @create_vertex
####################################################################################################
def create_bmesh_object():
    """Creates a new bmesh object and returns a reference to it.

    :return:
        A reference to the created bmesh object.
    """

    # Create a new bmesh object
    return bmesh.new()


####################################################################################################
# @create_vertex
####################################################################################################
def create_vertex(location=(0, 0, 0)):
    """Creates a bmesh vertex object.

    :param location:
        The vertex location, by default at the origin.
    :return:
        A reference to the created bmesh vertex object.
    """

    # Create a new bmesh object
    bmesh_vertex = bmesh.new()

    # Create a new vertex within the given object
    bmesh.ops.create_vert(bmesh_vertex)

    # Translate the vertex to the given location
    bmesh.ops.translate(bmesh_vertex, verts=bmesh_vertex.verts[:], vec=location)

    # Return a reference to the created bmesh vertex object
    return bmesh_vertex


####################################################################################################
# @create_uv_sphere
####################################################################################################
def create_uv_sphere(radius=1,
                     location=(0, 0, 0),
                     subdivisions=16):
    """Creates a uv sphere bmesh object and returns a reference to that object.

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
    bmesh.ops.create_uvsphere(bmesh_uv_sphere,
                              u_segments=subdivisions, v_segments=subdivisions, radius=radius)

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
    bmesh.ops.create_icosphere(bmesh_ico_sphere, subdivisions=subdivisions, radius=radius)

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


####################################################################################################
# @create_icosphere_template
####################################################################################################
def create_icosphere_template(subdivisions=1,
                              center=Vector((0, 0, 0)),
                              radius=1):
    """Creates an icosphere template using the bmesh API.

    :param subdivisions:
        Number of sphere subdivisions.
    :param center:
        The center of the sphere, by default at the origin.
    :param radius:
        The radius of the sphere, by default 1.
    :return:
        Data list, the first element is a list of vertices and the second one is the faces.
    """

    # Create the icosphere bmesh
    icosphere_bmesh = create_ico_sphere(radius=radius, location=center, subdivisions=subdivisions)

    # Update the look-up tables before making the queries
    icosphere_bmesh.verts.ensure_lookup_table()
    icosphere_bmesh.faces.ensure_lookup_table()

    # Fill-up the vertices list
    vertices = list()
    for v in icosphere_bmesh.verts:
        vertices.append(v.co)

    # Fill-up the faces list
    faces = list()
    for f in icosphere_bmesh.faces:
        faces.append([f.verts[0].index, f.verts[1].index, f.verts[2].index])

    # Return the vertices and faces list
    return [vertices, faces]


####################################################################################################
# @append_icosphere_vertices_to_bmesh
####################################################################################################
def append_icosphere_vertices_to_bmesh(bmesh_object,
                                       center,
                                       radius,
                                       icosphere_template):

    # Add the vertices of the template to the input bmesh object
    for v in icosphere_template[0]:
        bmesh_object.verts.new((v * radius) + center)


####################################################################################################
# @append_icosphere_faces_to_bmesh
####################################################################################################
def append_icosphere_faces_to_bmesh(bmesh_object,
                                    i,
                                    icosphere_template):

    # Compute the face offset limit
    offset = len(icosphere_template[0])

    # Add the faces of the template to the input bmesh object
    for f in icosphere_template[1]:

        # Compute the corresponding indices
        v1_index = f[0] + (i * offset)
        v2_index = f[1] + (i * offset)
        v3_index = f[2] + (i * offset)

        # Get references to the vertices from the input bmesh object
        v1 = bmesh_object.verts[v1_index]
        v2 = bmesh_object.verts[v2_index]
        v3 = bmesh_object.verts[v3_index]

        # Add the new face in the bmesh object
        bmesh_object.faces.new((v1, v2, v3))


####################################################################################################
# @create_bmesh_object_from_spheres_list_using_icospheres
####################################################################################################
def create_bmesh_object_from_spheres_list_using_icospheres(spheres_list,
                                                           subdivisions=1):

    # Create the icosphere template object
    # icosphere_template = create_icosphere_template(subdivisions=subdivisions,
    #                                                center=Vector((0, 0, 0)), radius=1)

    icosphere_template = vmv.mesh.get_remeshed_icosphere_data(subdivisions=subdivisions)

    # Create the new bmesh object
    bmesh_object = bmesh.new()

    # Adding the vertices
    for sphere in spheres_list:
        append_icosphere_vertices_to_bmesh(bmesh_object=bmesh_object,
                                           center=sphere[0], radius=sphere[1],
                                           icosphere_template=icosphere_template)

    # Update the look-up table before making the queries
    bmesh_object.verts.ensure_lookup_table()

    # Adding the faces
    for i, sphere in enumerate(spheres_list):
        append_icosphere_faces_to_bmesh(bmesh_object=bmesh_object, i=i,
                                        icosphere_template=icosphere_template)

    # Return a reference to the bmesh object
    return bmesh_object


####################################################################################################
# @create_uv_sphere_template
####################################################################################################
def create_uv_sphere_template(subdivisions=8,
                              center=Vector((0, 0, 0)),
                              radius=1):
    # Create the icosphere bmesh
    uv_sphere_bmesh = create_uv_sphere(radius=radius, location=center, subdivisions=subdivisions)

    # Triangulate it
    vmv.bmeshi.triangulate_faces(bmesh_object=uv_sphere_bmesh)

    # Update the look-up tables before making the queries
    uv_sphere_bmesh.verts.ensure_lookup_table()
    uv_sphere_bmesh.faces.ensure_lookup_table()

    # Fill-up the vertices list
    vertices = list()
    for v in uv_sphere_bmesh.verts:
        vertices.append(v.co)

    # Fill-up the faces list
    faces = list()
    for f in uv_sphere_bmesh.faces:
        faces.append([f.verts[0].index, f.verts[1].index, f.verts[2].index])

    # Return the vertices and faces list
    return [vertices, faces]


####################################################################################################
# @create_bmesh_object_from_spheres_list_using_uv_spheres
####################################################################################################
def create_bmesh_object_from_spheres_list_using_uv_spheres(spheres_list,
                                                           subdivisions=16):
    """Creates a bmesh object composed of a list of given spheres using UV spheres.

    :param spheres_list:
        A list of spheres, where each item in the list is a list of center and radius.
        The first element is the center and the second item is the radius.
    :param subdivisions:
        The number of sphere subdivisions.
    :return:
        A reference to the created bmesh object.
    """

    # Create the icosphere template object
    uv_sphere_template = create_uv_sphere_template(subdivisions=subdivisions,
                                                   center=Vector((0, 0, 0)), radius=1)

    # Create the new bmesh object
    bmesh_object = bmesh.new()

    # Adding the vertices to the vertex object
    for sphere in spheres_list:
        append_icosphere_vertices_to_bmesh(bmesh_object=bmesh_object,
                                           center=sphere[0], radius=sphere[1],
                                           icosphere_template=uv_sphere_template)

    # Update the look-up table before making the queries
    bmesh_object.verts.ensure_lookup_table()

    # Adding the faces
    for i, sphere in enumerate(spheres_list):
        append_icosphere_faces_to_bmesh(bmesh_object=bmesh_object, i=i,
                                        icosphere_template=uv_sphere_template)

    # Return a reference to the bmesh object
    return bmesh_object
