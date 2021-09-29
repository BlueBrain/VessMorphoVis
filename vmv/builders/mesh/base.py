####################################################################################################
# Copyright (c) 2018 - 2021, EPFL / Blue Brain Project
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
import sys
import copy

# Blender imports
import bpy

# Internal imports
import vmv
import vmv.geometry
import vmv.mesh
import vmv.scene
import vmv.skeleton
import vmv.utilities


####################################################################################################
# @MeshBuilder
####################################################################################################
class MeshBuilder:
    """Base class, where all the mesh builders will inherit from.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology to reconstruct its skeleton as a series of disconnected sections.
        :param options:
            System options.
        """

        # Clone the original morphology to morphology before the pre=processing
        self.morphology = morphology

        # All the options of the project
        self.options = options

        # Skeleton materials
        self.materials = None

        # The reconstructed mesh object
        self.mesh = None

    ################################################################################################
    # @create_materials
    ################################################################################################
    def create_materials(self,
                         name,
                         color):
        """Creates just two materials of the mesh on the input parameters of the user.

        :param name:
            The name of the material/color.
        :param color:
            The code of the given colors.
        :return:
            A list of two elements (different or same colors) where we can apply later to the drawn
            sections or segments.
        """

        # A list of the created materials
        materials_list = list()

        # Create a couple of materials for consistency
        for i in range(2):
            material = vmv.shading.create_material(
                name='%s_color_%d' % (name, i), color=color,
                material_type=self.options.mesh.material)

            # Append the material to the materials list
            materials_list.append(material)

        # Return the list
        return materials_list

    ################################################################################################
    # @create_skeleton_materials
    ################################################################################################
    def create_skeleton_materials(self):
        """Create the materials of the skeleton.
        """

        for material in bpy.data.materials:
            if 'mesh_material' in material.name:
                material.user_clear()
                bpy.data.materials.remove(material)

        # Create the materials
        self.materials = self.create_materials(name='mesh_material', color=self.options.mesh.color)

        # Create an illumination specific for the given material
        vmv.shading.create_material_specific_illumination(
            material_type=self.options.mesh.material, camera_view=self.options.mesh.camera_view)

    ################################################################################################
    # @assign_material_to_mesh
    ################################################################################################
    def assign_material_to_mesh(self):

        # Deselect all objects
        vmv.scene.ops.deselect_all()

        # Adjusting the texture space, before assigning the material
        vmv.shading.adjust_material_uv(mesh_object=self.mesh)

        # Assign the material to the selected mesh
        vmv.shading.set_material_to_object(self.mesh, self.materials[0])

        # Activate the mesh object
        vmv.scene.set_active_object(self.mesh)
