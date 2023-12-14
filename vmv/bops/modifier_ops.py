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
# @apply_voxelization_remeshing_modifier
####################################################################################################
def apply_voxelization_remeshing_modifier(voxel_size: float):
    """Apply the voxelization re-meshing modifier to an-already selected mesh.

    :param voxel_size:
        The voxelization resolution.
    """

    bpy.ops.object.modifier_add(type='REMESH')
    bpy.context.object.modifiers["Remesh"].voxel_size = voxel_size
    bpy.ops.object.modifier_apply(modifier="Remesh")


####################################################################################################
# @triangulate_mesh_in_object_mode
####################################################################################################
def triangulate_mesh_in_object_mode():
    """Triangulates an-already selected mesh using the Triangulate modifier in the object mode."""

    bpy.ops.object.modifier_add(type='TRIANGULATE')
    bpy.ops.object.modifier_apply(modifier="Triangulate")


####################################################################################################
# @decimate_mesh
####################################################################################################
def decimate_mesh(decimation_ratio):
    """Decimates an already-selected mesh object.

    :param decimation_ratio:
        The decimation ratio.
    """

    bpy.ops.object.modifier_add(type='DECIMATE')
    bpy.context.object.modifiers["Decimate"].ratio = decimation_ratio

    if vmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Decimate")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Decimate")


####################################################################################################
# @surface_subdivision
####################################################################################################
def surface_subdivision(levels=1):
    """Applies a surface subdivision operation.

    :param levels:
        Subdivision levels, by default 1.
    :return:
    """

    bpy.ops.object.modifier_add(type='SUBSURF')
    bpy.context.object.modifiers["Subdivision"].levels = levels

    if vmv.utilities.is_blender_280():
        bpy.context.object.modifiers["Subdivision"].levels = levels
    else:
        bpy.context.object.modifiers["Subsurf"].levels = levels

    if vmv.utilities.is_blender_290():
        bpy.ops.object.modifier_apply(modifier="Subdivision")
    else:
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Subdivision")


####################################################################################################
# @create_skin_modifier
####################################################################################################
def create_skin_modifier(mesh_object):
    """Creates a skin modifier for a given mesh object.

    :param mesh_object:
        A given mesh object with which a skin modifier will be created.
    """

    mesh_object.modifiers.new(name="Skin", type='SKIN')


####################################################################################################
# @apply_skin_modifier
####################################################################################################
def apply_skin_modifier():
    """Applies the skin modifier for an already-selected mesh."""

    bpy.ops.object.modifier_apply(modifier="Skin")