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



