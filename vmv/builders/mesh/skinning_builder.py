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
from .base import MeshBuilder


####################################################################################################
# @SkinningBuilder
####################################################################################################
class SkinningBuilder(MeshBuilder):

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
            Loaded options from VessMorphoVis.
        """

        # Base
        MeshBuilder.__init__(self, morphology=morphology, options=options)

        # Final mesh center
        self.center = Vector((0.0, 0.0, 0.0))

        # Create the skeleton materials during the initialization
        self.create_skeleton_materials()




        self.indexed_samples_list = list()

    ################################################################################################
    # @build
    ################################################################################################
    def build_mesh(self):
        """Reconstructs the neuronal mesh using meta objects.
        """

        print('building meshes')
        import vmv.bmeshi
        # Verify and repair the morphology
        # self.verify_and_repair_morphology()

        # Update the center of the mesh to the center of the bounding box of the morphology
        self.center = self.morphology.bounding_box.center

        # Create the bmesh object
        bmeshi_object = vmv.bmeshi.create_bmesh_object()

        vertex_index = 0

        # Iterate over the sections, and then the samples, and then build the bmesh
        for i_section in self.morphology.sections_list:

            # TODO: Make sure that the section has more than one sample

            # Create the first sample (or corresponding vertex)
            vmv.bmeshi.add_new_vertex_to_bmesh(bmeshi_object, vertex_index,
                                               i_section.samples[0].point)
            self.indexed_samples_list.append(i_section.samples[0].radius)
            vertex_index += 1

            for j in range(1, len(i_section.samples)):
                vmv.bmeshi.extrude_vertex_towards_point(bmeshi_object, vertex_index - 1,
                                                        i_section.samples[j].point)
                self.indexed_samples_list.append(i_section.samples[j].radius)
                vertex_index += 1

        # Convert the bmesh to a mesh
        self.mesh = vmv.bmeshi.convert_bmesh_to_mesh(bmeshi_object, 'Sample')

        # Activate the arbor mesh
        vmv.scene.set_active_object(self.mesh)

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.mesh.select_all(action='DESELECT')
        bpy.ops.object.editmode_toggle()

        self.mesh.modifiers.new(name="Skin", type='SKIN')

        # Activate the arbor mesh
        vmv.scene.set_active_object(self.mesh)

        # Iterate over the sections, and then the samples, and then build the bmesh

        for j in range(0, int(len(self.indexed_samples_list) / 2)):
            # Get a reference to the vertex
            vertex = self.mesh.data.skin_vertices[0].data[j]
            vertex.radius = self.indexed_samples_list[j], self.indexed_samples_list[j]



        bpy.ops.object.modifier_apply(modifier="Skin")

        # Catmul-clark subdivision




        # Update the radii of the mesh


        # Build the connectivity

        # Build the centerline skeleton

        # Inflate the skeleton

        # Apply the skinning modifier

        # Apply the materials

        # Return a reference to the resulting mesh

        # Create an instance of the SectionBuilder to build the morphology in advance
        #morphology_builder = vmv.builders.SectionsBuilder(self.morphology, self.options)

        # Build the skeleton and return a reference to it
        #morphology_skeleton = morphology_builder.build_skeleton()

        # Convert it to a mesh
        #self.mesh = vmv.scene.convert_object_to_mesh(morphology_skeleton)

        # Update its name with the mesh suffix to be able to locate it
        #self.mesh.name = self.mesh.name + vmv.consts.Suffix.MESH_SUFFIX

        # Assign the material to the mesh
        #self.assign_material_to_mesh()

        # Mission done
        #vmv.logger.header('Done!')

        # Return a reference to the created mesh
        return self.mesh
