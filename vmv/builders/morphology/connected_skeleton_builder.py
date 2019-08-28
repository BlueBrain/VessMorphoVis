####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
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
import random, copy

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.bmeshi
import vmv.geometry
import vmv.mesh
import vmv.scene

import vmv
import vmv.skeleton


####################################################################################################
# @ConnectedSkeletonBuilder
####################################################################################################
class ConnectedSkeletonBuilder:
    """Reconstructs the vasculature morphology as a single object,
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
        :parm options
            System options.
        """

        # Morphology
        self.morphology = morphology

        # All the options of the project
        self.options = options

        # All the reconstructed objects of the morphology, for example, tubes, spheres, etc... .
        self.morphology_objects = []

        # A list of the colors/materials of the morphology
        self.morphology_materials = None

        self.skeleton_mesh = None

        self.sections_meshes = list()

        self.center = Vector((0, 0, 0))

        # A magic scaling factor for accurate adjustments of the radius of the branches
        # Note that the 1.4 is sqrt(2) for the smoothing factor
        self.radius_scaling_factor = 3 * 1.41421356237

    ################################################################################################
    # @extend_section_along_skeleton
    ################################################################################################
    def extend_section_along_skeleton(self,
                                      section,
                                      section_mesh):

        for i in range(len(section.samples) - 1):
            print('\t\tExtrusion Section [%d]' % section.samples[i].index)#, end='\r')
            vmv.bmeshi.ops.extrude_vertex_towards_point(
                section_mesh, i, section.samples[i + 1].point - self.center)

    ################################################################################################
    # @extrude_morphology_skeleton
    ################################################################################################
    def extrude_morphology_skeleton(self):
        # For each section in the morphology, draw the section as a series of disconnected segments
        for section in self.morphology.sections_list:
            self.extend_section_along_skeleton(section)

    def merge_duplicated_samples(self,
                                 sample_1_index,
                                 sample_2_index):

        # Select vertex
        vmv.mesh.ops.select_vertices(self.skeleton_mesh, [sample_1_index, sample_2_index])
        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.object.editmode_toggle()

    def build_section(self, section):

        section_mesh = vmv.bmeshi.create_vertex(section.samples[0].point - self.center)
        self.extend_section_along_skeleton(section, section_mesh)

        # Convert the skeleton to a mesh
        self.sections_meshes.append(vmv.bmeshi.convert_bmesh_to_mesh(section_mesh, 'Skeleton'))

    def extend_section(self,
                       section):

        # create a new vertex in the mesh
        vmv.bmeshi.add_new_vertex_to_bmesh(self.skeleton_mesh, section.samples[0].index,
                                           location=section.samples[0].point - self.center)

        # extend from this point then
        for i in range(0, len(section.samples) - 1):
            print('\t\tExtrusion Section [%d]' % section.samples[i].index)  # , end='\r')
            vmv.bmeshi.ops.extrude_vertex_towards_point(
                self.skeleton_mesh, section.samples[i].index,
                section.samples[i + 1].point - self.center)

    def connect_to_parent(self,
                          section):

        if len(section.parents) == 0:
            return

        indices = list()
        indices.append(section.samples[0].index)

        for parent in section.parents:
            indices.append(parent.samples[-1].index)

        # select vertices
        vmv.mesh.select_vertices(self.skeleton_mesh, indices)

        # merge
        bpy.ops.object.editmode_toggle()
        #bpy.ops.mesh.merge(type='CENTER')
        bpy.ops.mesh.edge_face_add()

        bpy.ops.object.editmode_toggle()

    ################################################################################################
    # @select_vertex
    ################################################################################################
    @staticmethod
    def select_vertex(vertex_idx):
        """Selects a vertex along a morphology path using its index during the skinning process.

        :param vertex_idx:
            The index of the vertex that needs to be selected.
        """

        # Set the current mode to the object mode
        # bpy.ops.object.mode_set(mode='OBJECT')

        # Select the active object (that is supposed to be the arbor being created)
        obj = bpy.context.active_object

        # Switch to the edit mode
        # bpy.ops.object.mode_set(mode='EDIT')

        # Switch to the vertex mode
        bpy.ops.mesh.select_mode(type="VERT")

        # Deselect all the vertices
        bpy.ops.mesh.select_all(action='DESELECT')

        # Switch back to the object mode
        bpy.ops.object.mode_set(mode='OBJECT')

        # Select the vertex
        obj.data.vertices[vertex_idx].select = True

        # Switch to the edit mode
        bpy.ops.object.mode_set(mode='EDIT')

    ################################################################################################
    # @select_vertex
    ################################################################################################
    def update_section_samples_radii(self,
                                     section):
        """Update the radii of the samples along a given section.

        :param section:
            A given section to update the radii of its samples.
        """

        # Make sure to include the first sample of the root section

        # Sample by sample along the section
        for i in range(0, len(section.samples)):
            print('\t\tUpdating Radii [%d]' % section.samples[i].index, end='\r')

            # Select the vertex at the given sample
            self.select_vertex(section.samples[i].index)

            # Radius scale factor
            radius = section.samples[i].radius * self.radius_scaling_factor
            print(radius)

            # Resize the radius of the selected vertex
            bpy.ops.transform.skin_resize(value=(radius, radius, radius),
                                          constraint_axis=(False, False, False),
                                          constraint_orientation='GLOBAL',
                                          mirror=False,
                                          proportional='DISABLED',
                                          proportional_edit_falloff='SMOOTH',
                                          proportional_size=1)

    ################################################################################################
    # @get_sections_poly_lines_data
    ################################################################################################
    def get_connected_sections_poly_lines_data(self):
        """Gets a list of the data of all the poly-lines that correspond to the sections in the
        morphology.

        NOTE: Each entry in the the poly-lines list has the following format:
            * poly_lines_data[0]: a list of all the samples (points and their radii)
            * poly_lines_data[0]: the material index

        :return:
            A list of all the poly-lines that correspond to the sections in the entire morphology.
        """

        # A list of all the poly-lines
        poly_lines_data = list()

        # Get the poly-line data of each section
        for i, root in enumerate(self.morphology.roots):

            poly_line = list()
            poly_lines = list()

            vmv.skeleton.ops.get_connected_sections_from_root_to_leaf(
                section=root, poly_line=poly_line, poly_lines=poly_lines)

            # Poly-line material index (we use two colors to highlight the sections)
            poly_line_material_index = i % 2

            # Add the poly-line to the aggregate list
            poly_lines_data.extend(poly_lines)

        # Return the poly-lines list
        return poly_lines_data

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self):
        """Draws the morphology skeleton using fast reconstruction and drawing method.
        """

        vmv.logger.header('Building skeleton: ConnectedSkeletonBuilder')

        # Clear the scene
        vmv.logger.detail('Clearing scene')
        vmv.scene.ops.clear_scene()

        # Clear the materials
        vmv.scene.ops.clear_scene_materials()

        # Create a static bevel object that you can use to scale the samples
        bevel_object = vmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Construct sections poly-lines
        vmv.logger.detail('Constructing poly-lines')
        poly_lines_data = self.get_connected_sections_poly_lines_data()

        # Pre-process the radii
        vmv.logger.detail('Adjusting radii')
        vmv.skeleton.update_poly_lines_radii(poly_lines=poly_lines_data, options=self.options)

        # Construct the final object and add it to the morphology
        vmv.logger.detail('Drawing object')
        self.morphology_objects.append(
            vmv.geometry.create_poly_lines_object_from_poly_lines_data(
                poly_lines_data, color=self.options.morphology.color,
                material=self.options.morphology.material, name=self.morphology.name,
                bevel_object=bevel_object))

    ################################################################################################
    # @build
    ################################################################################################
    def build_skeletoxxxn(self):
        """Draws the morphology skeleton using fast reconstruction and drawing methods.
        """

        # Clear the scene
        vmv.scene.ops.clear_scene()

        self.center = self.morphology.bounding_box.center

        # Create an initial proxy mesh at the origin (reflecting the soma)
        #self.skeleton_mesh = nmv.geometry.create_vertex_mesh(name=self.morphology.label)
        #self.skeleton_mesh = vmv.bmeshi.create_vertex(
        #    self.morphology.sections_list[0].samples[0].point)

        for section in self.morphology.sections_list:
            print('section')
            for sample in section.samples:
                print(sample.index)

        #for section in self.morphology.sections_list:
        #    for sample in section.samples:
        #        vmv.geometry.create_uv_sphere(location=sample.point-self.center, radius=sample.radius)
        #    break

        import bmesh
        self.skeleton_mesh = bmesh.new()

        for section in self.morphology.sections_list:
            print('new section')
            self.extend_section(section)


        #self.extend_section(self.morphology.sections_list[0])
        #self.extend_section(self.morphology.sections_list[1])
        #self.extend_section(self.morphology.sections_list[2])

        """
        for vertex in self.skeleton_mesh.verts:

            indices = list()
            indices.append(vertex.index)


            for other_vertex in self.skeleton_mesh.vertex:

                if vertex.index == other_vertex.index:
                    continue

                if (vertex.co - other_vertex.co).length < 0.00001:
                    indices.append(other_vertex.co)
        """






        # Convert the skeleton to a mesh
        self.skeleton_mesh = vmv.bmeshi.convert_bmesh_to_mesh(self.skeleton_mesh, 'Skeleton')

        # Select the skeleton mesh and make it active
        vmv.scene.set_active_object(self.skeleton_mesh)

        #for section in self.morphology.sections_list:
        #    print('new section')
        #    self.connect_to_parent(section)






        # now we have a skeleton mesh, we need to use skinning

        # Apply the skinning modifier
        skin = self.skeleton_mesh.modifiers.new(name="Skin", type='SKIN')

        # adjust radii
        bpy.ops.object.editmode_toggle()
        for section in self.morphology.sections_list:
            print('new section')
            self.update_section_samples_radii(section)

        #self.update_section_samples_radii(self.morphology.sections_list[1])
        #self.update_section_samples_radii(self.morphology.sections_list[2])


        #bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Skin")





        #for section in self.morphology.sections_list:
        #    print("*")
        #    self.build_section(section)



        # connections
        #for section in self.morphology.sections_list:

        #    self.connect_to_parent(section)





        # Extrude the morphology skeleton
        #self.extrude_morphology_skeleton()

        # Convert the skeleton to a mesh
        #self.skeleton_mesh = vmv.bmeshi.convert_bmesh_to_mesh(self.skeleton_mesh, 'Skeleton')

        return


        # Switch to edit mode
        #bpy.ops.object.editmode_toggle()

        # For the merge
        for connection in self.morphology.connectivity_list:

            # The index of the parent section
            parent_section_index = connection[0]

            # The index of the child section
            child_section_index = connection[1]

            # Parent section
            parent_section = self.morphology.sections_list[parent_section_index]

            # Child section
            child_section = self.morphology.sections_list[child_section_index]

            sample_0_index = parent_section.samples[-1].index
            sample_1_index = child_section.samples[0].index

            self.merge_duplicated_samples(sample_0_index, sample_1_index)

        # Switch to back to object mode
        #bpy.ops.object.editmode_toggle()

        # Select the skeleton mesh for the edit
        vmv.scene.set_active_object(self.skeleton_mesh)




