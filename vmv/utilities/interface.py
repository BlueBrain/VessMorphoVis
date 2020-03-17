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

# System imports
import copy

# Blender imports
import bpy


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



