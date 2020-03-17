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
import random, copy, time

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.mesh
import vmv.bmeshi
import vmv.consts
import vmv.geometry
import vmv.mesh
import vmv.scene
import vmv.skeleton
import vmv.builders


####################################################################################################
# @SimplifiedSkeletonBuilder
####################################################################################################
class SimplifiedSkeletonBuilder:
    """Reconstructs a simplified skeleton that reflect the connectivity of the vasculature
    morphology without taking into considerations the actual radii of the samples and the geometry
    of the branches.
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

        # All the reconstructed objects of the morphology, for example, tubes, spheres, etc...
        self.morphology_objects = []

    ################################################################################################
    # @build_skeleton_as_connected_set_of_lines
    ################################################################################################
    def build_simplified_skeleton(self):
        """Draws simplified skeleton of the vasculature morphology.
        """

        import vmv
        import vmv.geometry


        bevel_object = vmv.mesh.create_bezier_circle(radius=0.1, vertices=8, name='bevel')
        poly_lines = list()

        start = time.time()

        for j in range(1):

            # Get the poly-line format of the section
            for i, section in enumerate(self.morphology.sections_list):
                section_data = vmv.skeleton.ops.get_section_poly_line(section=section)
                poly_lines.append(section_data)

        p_done = time.time()

        print(len(poly_lines))
        strips = vmv.geometry.create_x(poly_lines, name='line', material=None, bevel_object=bevel_object)

        # for s in strips:
        vmv.geometry.link_poly_line_to_scene(strips)

        d_done = time.time()

        print('p %f, d %f' % (p_done - start, d_done - p_done))

        # Since we only have a single object, just append it to the morphology objects
        #self.morphology_objects.append(morphology_mesh_object)

    ################################################################################################
    # @build
    ################################################################################################
    def build(self):
        """Draws the morphology skeleton using fast reconstruction and drawing methods.
        """

        # Clear the scene
        vmv.scene.ops.clear_scene()

        # Build a simplified skeleton of the morphology
        self.build_simplified_skeleton()



