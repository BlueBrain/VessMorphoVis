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


def add_background_plane_for_front_camera(bounding_box):
    """

    :param bounding_box:
    :return:
    """

    # Front face
    front_face_v1 = copy.deepcopy(bounding_box.p_max)
    front_face_v2 = copy.deepcopy(front_face_v1)
    front_face_v2[1] = bounding_box.p_min[1]
    front_face_v3 = copy.deepcopy(front_face_v2)
    front_face_v3[0] = bounding_box.p_min[0]
    front_face_v4 = copy.deepcopy(front_face_v3)
    front_face_v4[1] = bounding_box.p_max[1]

    # Back face
    back_face_v1 = copy.deepcopy(front_face_v1)
    back_face_v1[2] = bounding_box.p_min[2]
    back_face_v2 = copy.deepcopy(front_face_v2)
    back_face_v2[2] = bounding_box.p_min[2]
    back_face_v3 = copy.deepcopy(front_face_v3)
    back_face_v3[2] = bounding_box.p_min[2]
    back_face_v4 = copy.deepcopy(front_face_v4)
    back_face_v4[2] = bounding_box.p_min[2]

    # Center points
    front_bottom_center = (front_face_v2 + front_face_v3) * 0.5
    back_bottom_center = (back_face_v2 + back_face_v3) * 0.5
    back_top_center = (back_face_v1 + back_face_v4) * 0.5

    FRONT_FACE_DELTA = 1000
    BACK_FACE_DELTA = 1000
    BOTTOM_FACE_DELTA = bounding_box.bounds[1] * 0.1

    # Point 1
    point_1 = copy.deepcopy(front_face_v2)
    point_1[1] -= BOTTOM_FACE_DELTA
    point_1[2] += FRONT_FACE_DELTA

    point_2 = copy.deepcopy(front_face_v3)
    point_2[1] -= BOTTOM_FACE_DELTA
    point_2[2] += FRONT_FACE_DELTA

    front_bottom_center = (point_1 + point_2) * 0.5


    point_3 = copy.deepcopy(back_face_v2)
    point_3[1] -= BOTTOM_FACE_DELTA
    point_3[2] -= BACK_FACE_DELTA

    point_4 = copy.deepcopy(back_face_v3)
    point_4[1] -= BOTTOM_FACE_DELTA
    point_4[2] -= BACK_FACE_DELTA

    back_bottom_center = (point_3 + point_4) * 0.5

    # Create a plane mesh, starting with a vertex
    plane_mesh = vmv.mesh.create_vertex(location=point_1, name='plane_mesh')

    # Extrude the plane mesh (that is so far a vertex) to @v3
    vmv.mesh.extrude_selected_vertices_on_mesh(plane_mesh, [0], point_1, point_2)

    # Select all the vertices and extrude towards p_max z
    vmv.mesh.extrude_selected_vertices_on_mesh(
        plane_mesh, [0, 1], front_bottom_center, back_bottom_center)

    point_5 = copy.deepcopy(back_face_v1)
    point_5[1] += 1000
    point_5[2] -= BACK_FACE_DELTA

    point_6 = copy.deepcopy(back_face_v4)
    point_6[1] += 1000
    point_6[2] -= BACK_FACE_DELTA

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
    plane_mesh.scale[0] = 1000

    # Smooth the surface for the shading
    vmv.mesh.shade_smooth_object(mesh_object=plane_mesh)

    # Return a reference to the final plane
    return plane_mesh




def add_background_plane(bounding_box):

    plane_mesh = vmv.mesh.create_plane()

    vmv.scene.set_active_object(plane_mesh)

    # Deselect all the vertices in the edit mode
    vmv.mesh.deselect_all_vertices(plane_mesh)

    # select the vertices
    vmv.mesh.select_vertices(plane_mesh, [0, 1])

    bpy.ops.object.mode_set(mode='EDIT')

    bpy.ops.mesh.extrude_region_move(
        MESH_OT_extrude_region={"use_normal_flip": False, "mirror": False},
        TRANSFORM_OT_translate={"value": (-3.84998, 1.53531, 8.31745), "orient_type": 'GLOBAL',
                                "orient_matrix": ((1, 0, 0), (0, 1, 0), (0, 0, 1)),
                                "orient_matrix_type": 'GLOBAL',
                                "constraint_axis": (False, False, False), "mirror": False,
                                "use_proportional_edit": False,
                                "proportional_edit_falloff": 'SMOOTH', "proportional_size": 1,
                                "use_proportional_connected": False,
                                "use_proportional_projected": False, "snap": False,
                                "snap_target": 'CLOSEST', "snap_point": (0, 0, 0),
                                "snap_align": False, "snap_normal": (0, 0, 0),
                                "gpencil_strokes": False, "cursor_transform": False,
                                "texture_space": False, "remove_on_cancel": False,
                                "release_confirm": False, "use_accurate": False})

    # Switch back to the object mode
    bpy.ops.object.mode_set(mode='OBJECT')


####################################################################################################
# @view_all_from_projection
####################################################################################################
def view_all_from_projection(projection='TOP'):
    """Shows the viewport along a specific axis or projection.

    :param projection:
        The projection view: TOP, BOTTOM, LEFT, RIGHT, FRONT, BACK
    :return:
    """

    # Switch to the top view
    bpy.ops.view3d.view_axis(type=projection)

    # View all the objects in the scene
    bpy.ops.view3d.view_all()


####################################################################################################
# @update_view_port_shading_to_solid
####################################################################################################
def update_view_port_shading_to_solid():
    """Updates the view port shading to solid.
    """

    # Switch to viewport shading
    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    space = next(space for space in area.spaces if space.type == 'VIEW_3D')
    space.shading.type = 'SOLID'


####################################################################################################
# @update_view_port_shading_to_material
####################################################################################################
def update_view_port_shading_to_material():
    """Updates the view port shading to material.
    """

    # Switch to viewport shading
    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    space = next(space for space in area.spaces if space.type == 'VIEW_3D')
    space.shading.type = 'MATERIAL'


####################################################################################################
# @update_view_port_shading_to_material
####################################################################################################
def update_view_port_shading_to_rendered():
    """Updates the view port shading to rendered.
    """

    # Switch to viewport shading
    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    space = next(space for space in area.spaces if space.type == 'VIEW_3D')
    space.shading.type = 'RENDERED'



