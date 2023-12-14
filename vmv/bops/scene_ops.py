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
# @get_active_object
####################################################################################################
def get_active_object():
    """Returns a reference to the active object in the scene.

    :return:
        A reference to the active object in the scene.
    """

    if vmv.utilities.is_blender_280():
        return bpy.context.active_object
    else:
        return bpy.context.scene.objects.active


####################################################################################################
# @view_axis
####################################################################################################
def view_axis(axis='TOP'):
    """Views the given axis (or projection) in the 3D viewport.

    :param axis:
        An enum in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP', 'FRONT', 'BACK'].
    """

    if vmv.utilities.is_blender_280():
        bpy.ops.view3d.view_axis(type=axis)
    else:
        bpy.ops.view3d.viewnumpad(type=axis)


####################################################################################################
# @shade_smooth
####################################################################################################
def shade_smooth():
    """Shades a given object to be smooth."""

    bpy.ops.object.shade_smooth()
