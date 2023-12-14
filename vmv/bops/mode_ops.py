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


####################################################################################################
# @switch_to_edit_mode
####################################################################################################
def switch_to_edit_mode():
    """Switches the selected object into the edit mode (vertices, edges or faces)."""

    bpy.ops.object.mode_set(mode='EDIT')


####################################################################################################
# @switch_to_object_mode
####################################################################################################
def switch_to_object_mode():
    """Switches the selected object to the object mode."""

    bpy.ops.object.mode_set(mode='OBJECT')


####################################################################################################
# @select_vertex_mode
####################################################################################################
def select_vertex_mode():
    """Switch to the vertex mode."""

    bpy.ops.mesh.select_mode(type="VERT")
