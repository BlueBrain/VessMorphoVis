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
from mathutils import Vector

# Internal modules
import vmv
import vmv.builders
import vmv.enums
import vmv.mesh
import vmv.skeleton
import vmv.utilities
import vmv.scene


####################################################################################################
# @MetaBuilder
####################################################################################################
class PolylineBuilder:
    """Mesh builder that creates piecewise watertight sub-meshes for the connected sections."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology skeleton to create the mesh for.
        :param options:
            Loaded options from NeuroMorphoVis.
        """

        # Morphology
        self.morphology = morphology

        # Loaded options from VessMorphoVis
        self.options = options

        # A list of the colors/materials of the mesh
        self.materials = None

        # Meta object skeleton, used to build the skeleton of the morphology
        self.meta_skeleton = None

        # Meta object mesh, used to build the mesh of the morphology
        self.mesh = None

        # Final mesh center
        self.center = Vector((0.0, 0.0, 0.0))

        # Create the skeleton materials during the initialization
        self.create_skeleton_materials()

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
        materials_list = []

        for i in range(2):

            # Create the material
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

        # Soma
        self.materials = self.create_materials(
            name='mesh_material', color=self.options.mesh.color)

        # Create an illumination specific for the given material
        # vmv.shading.create_material_specific_illumination(self.options.morphology.material)

    ################################################################################################
    # @assign_material_to_mesh
    ################################################################################################
    def assign_material_to_mesh(self):

        # Deselect all objects
        vmv.scene.ops.deselect_all()

        # Activate the mesh object
        bpy.context.view_layer.objects.active = self.mesh

        # Adjusting the texture space, before assigning the material
        bpy.context.object.data.use_auto_texspace = False
        bpy.context.object.data.texspace_size[0] = 5
        bpy.context.object.data.texspace_size[1] = 5
        bpy.context.object.data.texspace_size[2] = 5

        # Assign the material to the selected mesh
        vmv.shading.set_material_to_object(self.mesh, self.materials[0])

        # Activate the mesh object
        vmv.scene.select_objects([self.mesh])
        bpy.context.view_layer.objects.active = self.mesh

    ################################################################################################
    # @build
    ################################################################################################
    def build_mesh(self):
        """Reconstructs the neuronal mesh using meta objects.
        """

        # Verify and repair the morphology
        # self.verify_and_repair_morphology()

        self.center = self.morphology.bounding_box.center

        morphology_builder = vmv.builders. ConnectedSectionsBuilder(self.morphology, self.options)
        morphology_skeleton_objects = morphology_builder.build()

        # group the morphology
        if len(morphology_skeleton_objects) > 1:
            morphology_object = vmv.scene.join_objects(morphology_skeleton_objects, 'obj')
        else:
            morphology_object = morphology_skeleton_objects[0]

        self.mesh = vmv.scene.convert_object_to_mesh(morphology_object)

        # We can here create the materials at the end to avoid any issues
        self.create_skeleton_materials()

        # Assign the material to the mesh
        self.assign_material_to_mesh()

        # Mission done
        vmv.logger.header('Done!')

        # Return a reference to the created mesh
        return self.mesh
