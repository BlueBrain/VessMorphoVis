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

# Blender imports
import bpy

# Internal imports
import vmv
import vmv.shading
import vmv.consts
import vmv.skeleton


####################################################################################################
# @create_skeleton_materials
####################################################################################################
def create_skeleton_materials(builder):
    """Creates the materials of the skeleton.

    :param builder:
        A reference to the builder that is used to create the skeleton.

    NOTE: The created materials are stored in private variables.
    """

    # Clear all the materials that are already present in the scene
    for material in bpy.data.materials:
        if 'morphology_skeleton' in material.name:
            material.user_clear()
            bpy.data.materials.remove(material)

    # Skeleton materials
    builder.materials = vmv.skeleton.ops.create_skeleton_materials(
        name='morphology_skeleton', material_type=builder.options.morphology.material,
        color=builder.options.morphology.color)
