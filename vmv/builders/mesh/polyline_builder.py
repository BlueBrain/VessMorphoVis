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
from .base import MeshBuilder


####################################################################################################
# @PolylineBuilder
####################################################################################################
class PolylineBuilder(MeshBuilder):
    """Mesh builder that creates piecewise watertight meshes for the different sections in the
    morphology."""

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

    ################################################################################################
    # @build
    ################################################################################################
    def build_mesh(self):
        """Reconstructs the neuronal mesh using meta objects.
        """

        # Verify and repair the morphology
        # self.verify_and_repair_morphology()

        # Update the center of the mesh to the center of the bounding box of the morphology
        self.center = self.morphology.bounding_box.center

        # Create an instance of the SectionBuilder to build the morphology in advance
        morphology_builder = vmv.builders.SectionsBuilder(self.morphology, self.options)

        # Build the skeleton and return a reference to it
        morphology_skeleton = morphology_builder.build_skeleton()

        # Convert it to a mesh
        self.mesh = vmv.scene.convert_object_to_mesh(morphology_skeleton)

        # Update its name with the mesh suffix to be able to locate it
        self.mesh.name = self.mesh.name + vmv.consts.Suffix.MESH_SUFFIX

        # Assign the material to the mesh
        #self.assign_material_to_mesh()

        # Mission done
        vmv.logger.header('Done!')

        # Return a reference to the created mesh
        return self.mesh
