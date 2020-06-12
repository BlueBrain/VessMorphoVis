####################################################################################################
# Copyright (c) 2018 - 2019, EPFL / Blue Brain Project
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
import vmv.bmeshi
import vmv.scene
import vmv.skeleton


####################################################################################################
# @SamplesBuilder
####################################################################################################
class SamplesBuilder:
    """Morphology builder with samples, where each sample is drawn as an independent object.
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

        # All the reconstructed objects of the morphology, for example, tubes, spheres, etc...
        self.morphology_objects = []

        # A list of the colors/materials of the skeleton
        self.materials = None

    ################################################################################################
    # @draw_section_samples_as_spheres
    ################################################################################################
    @staticmethod
    def draw_section_samples_as_spheres(section):
        """Draw the section samples as a set of spheres.

        :param section:
            A given section to draw.
        :return:
            List of spheres of the section.
        """
        output = list()
        for sample in section.samples:
            sphere = vmv.bmeshi.create_ico_sphere(
                radius=sample.radius, location=sample.point, subdivisions=1)
            output.append(sphere)
        return output

    ################################################################################################
    # @link_and_shade_spheres
    ################################################################################################
    def link_and_shade_spheres(self,
                               sphere_list,
                               materials_list,
                               prefix):
        """Links the added sphere to the scene.

        :param sphere_list:
            A list of sphere to be linked to the scene and shaded with the corresponding materials.
        :param materials_list:
            A list of materials to be applied to the spheres after being linked to the scene.
        :param prefix:
            Prefix to name each sphere object after linking it to the scene.
        """

        joint_bmesh = vmv.bmeshi.join_bmeshes_list(bmeshes_list=sphere_list)

        # Link the bmesh spheres to the scene
        sphere_mesh = vmv.bmeshi.ops.link_to_new_object_in_scene(joint_bmesh, prefix)

        # Smooth shading
        vmv.mesh.shade_smooth_object(sphere_mesh)

        # Assign the material
        vmv.shading.set_material_to_object(sphere_mesh, materials_list[0])

        # Append the sphere mesh to the morphology objects
        self.morphology_objects.append(sphere_mesh)

    ################################################################################################
    # @get_sections_poly_lines_data
    ################################################################################################
    def get_sections_poly_lines_data(self):
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
        for i, section in enumerate(self.morphology.sections_list):

            # Poly-line samples
            poly_line_samples = vmv.skeleton.ops.get_section_poly_line(section=section)

            # Poly-line material index (we use two colors to highlight the sections)
            poly_line_material_index = i % 2

            # Add the poly-line to the aggregate list
            poly_lines_data.append([poly_line_samples, poly_line_material_index])

        # Return the poly-lines list
        return poly_lines_data

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self):
        """Draws the morphology skeleton using fast reconstruction and drawing method.
        """

        vmv.logger.header('Building skeleton: SamplesBuilder')

        # Clear the scene
        vmv.logger.info('Clearing scene')
        vmv.scene.ops.clear_scene()

        # Clear the materials
        vmv.scene.ops.clear_scene_materials()

        self.materials = vmv.skeleton.ops.create_skeleton_materials(
            name='axon_skeleton', material_type=self.options.morphology.material,
            color=self.options.morphology.color)

        # Pre-process the radii
        vmv.logger.info('Adjusting radii')
        vmv.skeleton.update_skeleton_radii(morphology=self.morphology, options=self.options)

        # Construct the final object and add it to the morphology
        vmv.logger.info('Constructing object')

        spheres = list()
        for section in self.morphology.sections_list:
            spheres.extend(self.draw_section_samples_as_spheres(section))

        # Construct the final object and add it to the morphology
        vmv.logger.info('Linking spheres')

        self.link_and_shade_spheres(sphere_list=spheres,
                                    materials_list=self.materials,
                                    prefix='samples')
