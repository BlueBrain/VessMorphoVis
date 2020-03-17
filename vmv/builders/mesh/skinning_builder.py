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

# Blender imports
import bpy

# Internal imports
import vmv
import vmv.bmeshi
import vmv.consts
import vmv.geometry
import vmv.mesh
import vmv.scene
import vmv.skeleton
import vmv.builders


####################################################################################################
# @CenterLineSkeletonBuilder
####################################################################################################
class SkinningBuilder:
    """A simple skeleton builder that draws the skeleton as a list of connected center-lines to show
    the structure of the morphology.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor.

        :param morphology:
            A given morphology.
        """

        # Morphology
        self.morphology = morphology

        # All the options of the project
        self.options = options

        # A reference to the reconstructed mesh
        self.reconstructed_mesh = None

        # A list of all the materials that will be assigned to the reconstructed mesh
        self.materials = list()

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

        # Create the
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
        bpy.context.view_layer.objects.active = self.reconstructed_mesh

        # Adjusting the texture space, before assigning the material
        bpy.context.object.data.use_auto_texspace = False
        bpy.context.object.data.texspace_size[0] = 5
        bpy.context.object.data.texspace_size[1] = 5
        bpy.context.object.data.texspace_size[2] = 5

        # Assign the material to the selected mesh
        vmv.shading.set_material_to_object(self.reconstructed_mesh, self.materials[0])

        # Activate the mesh object
        self.reconstructed_mesh.select_set(True)
        bpy.context.view_layer.objects.active = self.reconstructed_mesh

    ################################################################################################
    # @build_skeleton_as_connected_set_of_lines
    ################################################################################################
    def build_skeleton_as_connected_set_of_lines(self,
                                                 remove_duplicate_samples=True):
        """This method draws the skeleton almost instantaneously.

        :param remove_duplicate_samples:
            If this flag is set to True, it remove the duplicate points in the morphology.
        """

        # Construct a bmesh object that will be used to build the morphology
        morphology_bmesh_object = vmv.bmeshi.create_bmesh_object()

        radius_identifier = morphology_bmesh_object.verts.layers.float.new('radius')

        # For every section in the, add a new poly-line to the bmesh object
        index = 0
        for section in self.morphology.sections_list:

            # For every two-connected samples in the morphology, add a line segment to the bmesh
            for i in range(len(section.samples) - 1):

                # Sample points
                p0 = section.samples[i].point
                p1 = section.samples[i + 1].point

                # Construct the line segment and add it to the bmesh
                vmv.bmeshi.add_line_segment_to_bmesh(morphology_bmesh_object, p0, p1)

                morphology_bmesh_object.verts.ensure_lookup_table()
                morphology_bmesh_object.verts[index][radius_identifier] = section.samples[i].radius
                index += 1

                morphology_bmesh_object.verts.ensure_lookup_table()
                morphology_bmesh_object.verts[index][radius_identifier] = section.samples[i + 1].radius
                index += 1

        import bmesh

        bmesh.ops.remove_doubles(
            morphology_bmesh_object, verts=morphology_bmesh_object.verts[:], dist=0.001)

        # Convert the bmesh object into a mesh object that can be linked to the scene
        morphology_mesh_object = vmv.bmeshi.convert_bmesh_to_mesh(
            morphology_bmesh_object, self.morphology.name)


        # Apply the skin modifier
        morphology_mesh_object.modifiers.new(name="Skin", type='SKIN')
        vmv.scene.set_active_object(morphology_mesh_object)

        for i in range(len(morphology_bmesh_object.verts[:])):
            morphology_bmesh_object.verts.ensure_lookup_table()
            radius = morphology_bmesh_object.verts[i][radius_identifier]
            vertex = morphology_mesh_object.data.skin_vertices[0].data[i]
            vertex.radius = radius, radius
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")




        # Since we only have a single object, just append it to the morphology objects
        self.reconstructed_mesh = morphology_mesh_object

    ################################################################################################
    # @build
    ################################################################################################
    def build(self):
        """Draws the morphology skeleton using fast reconstruction and drawing methods.
        """

        # Clear the scene
        vmv.scene.ops.clear_scene()

        # Build the skeleton as a set of connected lines (or center-lines)
        self.build_skeleton_as_connected_set_of_lines()

        # Finalize the meta object and construct a solid object
        # We can here create the materials at the end to avoid any issues
        vmv.logger.info('Assigning material')
        self.create_skeleton_materials()

        # Assign the material to the mesh
        self.assign_material_to_mesh()

        # Mission done
        vmv.logger.header('Done!')



