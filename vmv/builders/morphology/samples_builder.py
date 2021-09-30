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

# Internal imports
import vmv.geometry
import vmv.mesh
import vmv.bmeshi
import vmv.scene
import vmv.skeleton
from .base import MorphologyBuilder


####################################################################################################
# @SamplesBuilder
####################################################################################################
class SamplesBuilder(MorphologyBuilder):
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

        # Base
        MorphologyBuilder.__init__(self, morphology=morphology, options=options)

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
                               prefix):
        """Links the added sphere to the scene.

        :param sphere_list:
            A list of sphere to be linked to the scene and shaded with the corresponding materials.
        :param prefix:
            Prefix to name each sphere object after linking it to the scene.
        """

        joint_bmesh = vmv.bmeshi.join_bmeshes_list(bmeshes_list=sphere_list)

        # Link the bmesh spheres to the scene
        self.morphology_skeleton = vmv.bmeshi.ops.link_to_new_object_in_scene(joint_bmesh, prefix)

        # Smooth shading
        vmv.mesh.shade_smooth_object(self.morphology_skeleton)

        # Create a simple material
        material = vmv.shading.create_material(
            name='morphology_skeleton', material_type=self.options.morphology.material,
            color=self.options.morphology.color)

        # Assign the material
        vmv.shading.set_material_to_object(self.morphology_skeleton, material)

        # Create the corresponding illumination
        vmv.shading.create_material_specific_illumination(
            material_type=self.options.morphology.material)

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self, 
                       context=None,
                       dynamic_colormap=False):
        """Draws the morphology skeleton using fast reconstruction and drawing method.
        """

        vmv.logger.header('Building Skeleton: SamplesBuilder')

        # Call the base function
        super(SamplesBuilder, self).build_skeleton(context=context)

        # Get the context 
        self.context = context 

        # Clear the scene
        vmv.logger.info('Clearing Scene')
        vmv.scene.ops.clear_scene()

        # Clear the materials
        vmv.scene.ops.clear_scene_materials()

        # Pre-process the radii
        vmv.logger.info('Adjusting Radii')
        vmv.skeleton.update_skeleton_radii(morphology=self.morphology, options=self.options)

        # Construct the final object and add it to the morphology
        vmv.logger.info('Constructing Object')

        spheres = list()
        for section in self.morphology.sections_list:
            spheres.extend(self.draw_section_samples_as_spheres(section))

        # Construct the final object and add it to the morphology
        vmv.logger.info('Linking spheres')

        # Link the sphere together into a single object and shade it
        self.link_and_shade_spheres(sphere_list=spheres, prefix=self.morphology_name)

        # Return a reference to the morphology
        return self.morphology_skeleton
