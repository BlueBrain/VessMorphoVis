####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# System imports
import copy

# Blender imports
import bpy

# Internal imports
import vmv
import vmv.consts
import vmv.utilities
import vmv.mesh
import vmv.geometry
import vmv.scene


####################################################################################################
# add_background_plane_for_front_camera
####################################################################################################
def add_background_plane_for_front_camera(bounding_box):
    """Add a stylish plane that would reveal the shadow of the object and make the rendering
    stand out.

    :param bounding_box:
        Morphology or mesh bounding box.
    :return:
        A reference to the constructed plane.
    """

    # Bounding box front face
    front_face_v1 = copy.deepcopy(bounding_box.p_max)
    front_face_v2 = copy.deepcopy(front_face_v1)
    front_face_v2[1] = bounding_box.p_min[1]
    front_face_v3 = copy.deepcopy(front_face_v2)
    front_face_v3[0] = bounding_box.p_min[0]
    front_face_v4 = copy.deepcopy(front_face_v3)
    front_face_v4[1] = bounding_box.p_max[1]

    # Bounding box back face
    back_face_v1 = copy.deepcopy(front_face_v1)
    back_face_v1[2] = bounding_box.p_min[2]
    back_face_v2 = copy.deepcopy(front_face_v2)
    back_face_v2[2] = bounding_box.p_min[2]
    back_face_v3 = copy.deepcopy(front_face_v3)
    back_face_v3[2] = bounding_box.p_min[2]
    back_face_v4 = copy.deepcopy(front_face_v4)
    back_face_v4[2] = bounding_box.p_min[2]

    # Point 1
    point_1 = copy.deepcopy(front_face_v2)
    point_1[1] -= bounding_box.bounds[1] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_1[2] += vmv.consts.RenderingPlanes.FRONT_FACE_DELTA

    # Point 2
    point_2 = copy.deepcopy(front_face_v3)
    point_2[1] -= bounding_box.bounds[1] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_2[2] += vmv.consts.RenderingPlanes.FRONT_FACE_DELTA

    # Center
    front_bottom_center = (point_1 + point_2) * 0.5

    # Point 3
    point_3 = copy.deepcopy(back_face_v2)
    point_3[1] -= bounding_box.bounds[1] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_3[2] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Point 4
    point_4 = copy.deepcopy(back_face_v3)
    point_4[1] -= bounding_box.bounds[1] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_4[2] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Center
    back_bottom_center = (point_3 + point_4) * 0.5

    # Create a plane mesh, starting with a vertex
    plane_mesh = vmv.mesh.create_vertex(location=point_1, name='plane_mesh')

    # Extrude the plane mesh (that is so far a vertex) to @v3
    vmv.mesh.extrude_selected_vertices_on_mesh(plane_mesh, [0], point_1, point_2)

    # Select all the vertices and extrude towards p_max z
    vmv.mesh.extrude_selected_vertices_on_mesh(
        plane_mesh, [0, 1], front_bottom_center, back_bottom_center)

    # Point 5
    point_5 = copy.deepcopy(back_face_v1)
    point_5[1] += vmv.consts.RenderingPlanes.TOP_FACE_DELTA
    point_5[2] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Point 6
    point_6 = copy.deepcopy(back_face_v4)
    point_6[1] += vmv.consts.RenderingPlanes.TOP_FACE_DELTA
    point_6[2] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Center
    back_top_center = (point_5 + point_6) * 0.5

    # Select all the vertices and extrude towards p_max z
    vmv.mesh.extrude_selected_vertices_on_mesh(
        plane_mesh, [2, 3], back_bottom_center, back_top_center)

    # Select this plane
    vmv.scene.set_active_object(plane_mesh)

    # Set the pivot to the origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Subdivide the faces to make a smooth and easy transition
    vmv.mesh.subdivide_faces(mesh_object=plane_mesh, faces_indices=[], cuts=5, all_faces=True)

    # Smooth the plane
    vmv.mesh.smooth_object(mesh_object=plane_mesh, level=5)

    # Scale the final plane mesh to fill the view
    plane_mesh.scale[0] = vmv.consts.RenderingPlanes.HORIZON_SCALE

    # Smooth the surface for the shading
    vmv.mesh.shade_smooth_object(mesh_object=plane_mesh)

    # Return a reference to the final plane
    return plane_mesh


####################################################################################################
# add_background_plane_for_top_camera
####################################################################################################
def add_background_plane_for_top_camera(bounding_box):
    """Add a stylish plane that would reveal the shadow of the object and make the rendering
    stand out.

    :param bounding_box:
        Morphology or mesh bounding box.
    :return:
        A reference to the constructed plane.
    """

    # Bounding box front face
    front_face_v1 = copy.deepcopy(bounding_box.p_max)
    front_face_v1[0] = bounding_box.p_min[0]
    front_face_v2 = copy.deepcopy(front_face_v1)
    front_face_v2[2] = -bounding_box.p_max[2]
    front_face_v3 = copy.deepcopy(front_face_v2)
    front_face_v3[0] = bounding_box.p_max[0]
    front_face_v4 = copy.deepcopy(bounding_box.p_max)

    # Bounding box back face
    back_face_v1 = copy.deepcopy(front_face_v1)
    back_face_v1[1] = bounding_box.p_min[1]
    back_face_v2 = copy.deepcopy(front_face_v2)
    back_face_v2[1] = bounding_box.p_min[1]
    back_face_v3 = copy.deepcopy(front_face_v3)
    back_face_v3[1] = bounding_box.p_min[1]
    back_face_v4 = copy.deepcopy(front_face_v4)
    back_face_v4[1] = bounding_box.p_min[1]

    # Point 1
    point_1 = copy.deepcopy(front_face_v2)
    point_1[2] -= bounding_box.bounds[2] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_1[1] += vmv.consts.RenderingPlanes.FRONT_FACE_DELTA

    # Point 2
    point_2 = copy.deepcopy(front_face_v3)
    point_2[2] -= bounding_box.bounds[2] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_2[1] += vmv.consts.RenderingPlanes.FRONT_FACE_DELTA

    # Center
    front_bottom_center = (point_1 + point_2) * 0.5

    # Point 3
    point_3 = copy.deepcopy(back_face_v2)
    point_3[2] -= bounding_box.bounds[2] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_3[1] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Point 4
    point_4 = copy.deepcopy(back_face_v3)
    point_4[2] -= bounding_box.bounds[2] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_4[1] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Center
    back_bottom_center = (point_3 + point_4) * 0.5

    # Create a plane mesh, starting with a vertex
    plane_mesh = vmv.mesh.create_vertex(location=point_1, name='plane_mesh')

    # Extrude the plane mesh (that is so far a vertex) to @v3
    vmv.mesh.extrude_selected_vertices_on_mesh(plane_mesh, [0], point_1, point_2)

    # Select all the vertices and extrude towards p_max z
    vmv.mesh.extrude_selected_vertices_on_mesh(
        plane_mesh, [0, 1], front_bottom_center, back_bottom_center)

    # Point 5
    point_5 = copy.deepcopy(back_face_v1)
    point_5[2] += vmv.consts.RenderingPlanes.TOP_FACE_DELTA
    point_5[1] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Point 6
    point_6 = copy.deepcopy(back_face_v4)
    point_6[2] += vmv.consts.RenderingPlanes.TOP_FACE_DELTA
    point_6[1] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Center
    back_top_center = (point_5 + point_6) * 0.5

    # Select all the vertices and extrude towards p_max z
    vmv.mesh.extrude_selected_vertices_on_mesh(
        plane_mesh, [2, 3], back_bottom_center, back_top_center)

    # Select this plane
    vmv.scene.set_active_object(plane_mesh)

    # Set the pivot to the origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Subdivide the faces to make a smooth and easy transition
    vmv.mesh.subdivide_faces(mesh_object=plane_mesh, faces_indices=[], cuts=5, all_faces=True)

    # Smooth the plane
    vmv.mesh.smooth_object(mesh_object=plane_mesh, level=5)

    # Scale the final plane mesh to fill the view
    plane_mesh.scale[0] = vmv.consts.RenderingPlanes.HORIZON_SCALE

    # Smooth the surface for the shading
    vmv.mesh.shade_smooth_object(mesh_object=plane_mesh)

    # Return a reference to the final plane
    return plane_mesh


####################################################################################################
# add_background_plane_for_side_camera
####################################################################################################
def add_background_plane_for_side_camera(bounding_box):
    """Add a stylish plane that would reveal the shadow of the object and make the rendering
    stand out.

    :param bounding_box:
        Morphology or mesh bounding box.
    :return:
        A reference to the constructed plane.
    """

    # Bounding box front face
    front_face_v1 = copy.deepcopy(bounding_box.p_max)
    front_face_v1[2] = bounding_box.p_min[2]
    front_face_v2 = copy.deepcopy(front_face_v1)
    front_face_v2[1] = bounding_box.p_min[1]
    front_face_v3 = copy.deepcopy(front_face_v2)
    front_face_v3[2] = bounding_box.p_max[2]
    front_face_v4 = copy.deepcopy(bounding_box.p_max)

    # Bounding box back face
    back_face_v1 = copy.deepcopy(front_face_v1)
    back_face_v1[0] = bounding_box.p_min[0]
    back_face_v2 = copy.deepcopy(front_face_v2)
    back_face_v2[0] = bounding_box.p_min[0]
    back_face_v3 = copy.deepcopy(front_face_v3)
    back_face_v3[0] = bounding_box.p_min[0]
    back_face_v4 = copy.deepcopy(front_face_v4)
    back_face_v4[0] = bounding_box.p_min[0]

    # Point 1
    point_1 = copy.deepcopy(front_face_v2)
    point_1[1] -= bounding_box.bounds[1] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_1[0] += vmv.consts.RenderingPlanes.FRONT_FACE_DELTA

    # Point 2
    point_2 = copy.deepcopy(front_face_v3)
    point_2[1] -= bounding_box.bounds[1] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_2[0] += vmv.consts.RenderingPlanes.FRONT_FACE_DELTA

    # Center
    front_bottom_center = (point_1 + point_2) * 0.5

    # Point 3
    point_3 = copy.deepcopy(back_face_v2)
    point_3[1] -= bounding_box.bounds[1] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_3[0] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Point 4
    point_4 = copy.deepcopy(back_face_v3)
    point_4[1] -= bounding_box.bounds[1] * vmv.consts.RenderingPlanes.BOTTOM_FACE_DELTA
    point_4[0] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Center
    back_bottom_center = (point_3 + point_4) * 0.5

    # Create a plane mesh, starting with a vertex
    plane_mesh = vmv.mesh.create_vertex(location=point_1, name='plane_mesh')

    # Extrude the plane mesh (that is so far a vertex) to @v3
    vmv.mesh.extrude_selected_vertices_on_mesh(plane_mesh, [0], point_1, point_2)

    # Select all the vertices and extrude towards p_max z
    vmv.mesh.extrude_selected_vertices_on_mesh(
        plane_mesh, [0, 1], front_bottom_center, back_bottom_center)

    # Point 5
    point_5 = copy.deepcopy(back_face_v1)
    point_5[1] += 1000
    point_5[0] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Point 6
    point_6 = copy.deepcopy(back_face_v4)
    point_6[1] += 1000
    point_6[0] -= vmv.consts.RenderingPlanes.BACK_FACE_DELTA

    # Center
    back_top_center = (point_5 + point_6) * 0.5

    # Select all the vertices and extrude towards p_max z
    vmv.mesh.extrude_selected_vertices_on_mesh(plane_mesh, [2, 3], back_bottom_center,
                                               back_top_center)

    # Select this plane
    vmv.scene.set_active_object(plane_mesh)

    # Set the pivot to the origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Subdivide the faces to make a smooth and easy transition
    vmv.mesh.subdivide_faces(mesh_object=plane_mesh, faces_indices=[], cuts=5, all_faces=True)

    # Smooth the plane
    vmv.mesh.smooth_object(mesh_object=plane_mesh, level=5)

    # Scale the final plane mesh to fill the view
    plane_mesh.scale[2] = vmv.consts.RenderingPlanes.HORIZON_SCALE

    # Smooth the surface for the shading
    vmv.mesh.shade_smooth_object(mesh_object=plane_mesh)

    # Return a reference to the final plane
    return plane_mesh


