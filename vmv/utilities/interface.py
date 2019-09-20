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
import sys

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

    # Get the points from the bounding box
    point_1 = bounding_box.p_min
    point_2 = bounding_box.p_max

    # Adjust the two points along the same plane
    point_2[1] = point_1[1]
    point_2[2] = point_1[2]

    # Reflect the Z-axis to be near to the camera
    point_1[2] *= -1
    point_2[2] *= -1

    # Create a plane mesh, starting with a vertex
    plane_mesh = vmv.mesh.create_vertex(location=point_1)

    # Extrude the plane mesh (that is so far a vertex) to @point_2
    vmv.mesh.extrude_point_to_point_on_mesh(plane_mesh, 0, point_1, point_2)

    # Select all the vertices and extrude towards p_max z

    center_1 = (point_1 + point_2) * 0.5
    center_2 = bounding_box.p_min

    print(center_1)
    print(center_2)

    vmv.mesh.extrude_all_vertices_on_mesh(plane_mesh, center_1, center_2)

    return

    # Add plane 1, located at the origin at the XY plane
    plane_1_mesh = vmv.mesh.create_plane(name='plane_1')

    # Add plane 2, located at the origin at the XY plane
    plane_2_mesh = vmv.mesh.create_plane(name='plane_2')

    # Scale plane 1
    plane_1_mesh.scale[0] = bounding_box.bounds[0]
    plane_1_mesh.scale[1] = bounding_box.bounds[1]

    # Scale plane 2
    plane_2_mesh.scale[0] = bounding_box.bounds[0]
    plane_2_mesh.scale[1] = bounding_box.bounds[2]

    # Rotate plane 2 around the X-axis
    plane_2_mesh.rotation_euler[0] = 1.5708

    # Translate plane 1
    plane_1_mesh.location[2] = bounding_box.p_min[2]

    # Translate plane 2
    plane_2_mesh.location[1] = bounding_box.p_min[1]

    return

    # Join the two plane
    plane_mesh = vmv.mesh.ops.join_mesh_objects(mesh_list=[plane_1_mesh, plane_2_mesh],
                                                name='plane_mesh')

    plane_mesh.scale[0] *= 2
    plane_mesh.scale[1] *= 2
    plane_mesh.scale[2] *= 2

    # Remove the doubles to have a continuous surface
    vmv.mesh.remove_double_points(mesh_object=plane_mesh, threshold=0.1)

    # Smooth the plane
    vmv.mesh.smooth_object(mesh_object=plane_mesh, level=5)

    # Smooth the surface for the shading
    vmv.mesh.shade_smooth_object(mesh_object=plane_mesh)

    # Scale the final plane mesh to fill the view
    plane_mesh.scale[0] = 1000

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



