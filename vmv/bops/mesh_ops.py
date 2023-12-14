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
import bpy

# Internal imports
import vmv.utilities


####################################################################################################
# @select_all_vertices
####################################################################################################
def select_all_vertices():
    """Selects all the vertices of already-selected mesh objects that are in edit mode."""

    bpy.ops.mesh.select_all(action='SELECT')


####################################################################################################
# @deselect_all_vertices
####################################################################################################
def deselect_all_vertices():
    """Deselects all the vertices of already-selected mesh objects that are in edit mode."""

    bpy.ops.mesh.select_all(action='DESELECT')


####################################################################################################
# @remove_doubles
####################################################################################################
def remove_doubles(distance=0.001):
    """Removes duplicate vertices that lie within the given distance along the surface of selected
    meshes. This function only works when the vertices of a selected mesh are already selected,
    otherwise it will have no effect.

    :param distance:
        The threshold distance used to remove the vertices, by default 0.001.
    """

    vmv.utilities.disable_std_output()
    bpy.ops.mesh.remove_doubles(threshold=distance)
    vmv.utilities.enable_std_output()


####################################################################################################
# @separate_mesh_partitions
####################################################################################################
def separate_mesh_partitions():
    """Separates a given mesh into multiple partitions, if any. The mesh must be already selected before
    calling this function."""

    bpy.ops.mesh.separate(type='LOOSE')


####################################################################################################
# @merge_at_center
####################################################################################################
def merge_at_center():
    """Merges the selected vertices of an already selected mesh to the center."""

    bpy.ops.mesh.merge(type='CENTER')


####################################################################################################
# @add_plane
####################################################################################################
def add_plane(size=1,
              location=(0.0, 0.0, 0.0)):
    """Adds a new plane to the scene.

    :param size:
        The size of the plane, by default 1.0.
    :param location:
        The location of the plane (center), by default the origin.
    """

    bpy.ops.mesh.primitive_plane_add(size=size, location=location)


####################################################################################################
# @add_icosphere
####################################################################################################
def add_icosphere(radius,
                  location,
                  subdivisions):
    """Blender call that adds an icosphere to the scene.

    :param radius:
        The radius of the sphere.
    :param location:
        The location of the sphere.
    :param subdivisions:
        The number of subdivisions of the sphere, ideally from 3 to 6.
    """

    bpy.ops.mesh.primitive_ico_sphere_add(
        subdivisions=subdivisions, radius=radius, location=location)


####################################################################################################
# @add_uv_sphere
####################################################################################################
def add_uv_sphere(radius,
                  location,
                  segments,
                  sections):
    """Blender call that adds a UV sphere to the scene.

    :param radius:
        The radius of the sphere.
    :param location:
        The location of the sphere.
    :param segments:
        The number of segments of the sphere.
    :param sections:
        The number of sections of the sphere.
    """

    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=segments, ring_count=sections, size=radius, location=location)


####################################################################################################
# @add_circle
####################################################################################################
def add_circle(radius,
               location,
               number_sides,
               fill):
    """Blender call that adds a mesh circle to the scene.

    :param radius:
        The radius of the circle.
    :param location:
        The location of the circle.
    :param number_sides:
        The number of sides composing the circle, for example if 4 is used a square will be added.
    :param fill:
        If this parameter is set, the circle surface area is filled, or closed.
    """

    bpy.ops.mesh.primitive_circle_add(
        vertices=number_sides, radius=radius, location=location, fill_type=fill)


####################################################################################################
# @add_bezier_circle
####################################################################################################
def add_bezier_circle(radius,
                      location):
    """Blender call that adds a Bezier circle to the scene.

    :param radius:
        THe radius of the circle.
    :param location:
        The location (center) of the circle.
    """

    bpy.ops.curve.primitive_bezier_circle_add(radius=radius, location=location)


####################################################################################################
# @add_cube
####################################################################################################
def add_cube(side_length,
             location):
    """Blender call that adds a cube to the scene.

    :param side_length:
        The side length of the cube, commonly known by the radius in the Blender context.
    :param location:
        The location of the cube.
    """

    bpy.ops.mesh.primitive_cube_add(radius=side_length, location=location)


####################################################################################################
# @convert_to_mesh
####################################################################################################
def convert_to_mesh():
    """Converts an already selected non-mesh object into a mesh."""

    bpy.ops.object.convert(target='MESH')


####################################################################################################
# @convert_quads_to_tris
####################################################################################################
def convert_quads_to_tris():
    """Converts all the quads in the mesh into triangles."""

    bpy.ops.mesh.quads_convert_to_tris(quad_method='BEAUTY', ngon_method='BEAUTY')