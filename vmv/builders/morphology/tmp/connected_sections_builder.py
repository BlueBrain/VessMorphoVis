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
import random, copy

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.consts
import vmv.geometry
import vmv.mesh
import vmv.scene
import vmv.skeleton
import vmv.builders


####################################################################################################
# @ConnectedSectionsBuilder
####################################################################################################
class ConnectedSectionsBuilder:
    """Connected sections builder
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

        # All the reconstructed objects of the morphology, for example, tubes, spheres, etc... .
        self.morphology_objects = []

        # A list of the colors/materials of the morphology
        self.morphology_materials = None

        self.bevel_object = None

        # A list of the colors/materials of the skeleton
        self.materials = None

        # Morphology center
        self.center = vmv.consts.Math.ORIGIN

        # Morphology center
        self.center = vmv.consts.Math.ORIGIN

        # A list of the colors/materials of the skeleton
        self.materials = None

        self.object = None

        self.components = list()

        # Build the materials
        #vmv.builders.create_skeleton_materials(builder=self)

        # Create a static bevel object that you can use to scale the samples along the arbors
        # of the morphology
        self.bevel_object = vmv.mesh.create_bezier_circle(radius=1.0, vertices=16, name='bevel')

        # UI context 
        self.context = None

    def get_number_components(self):
        return  len(self.components)


    def build_component(self, component_index):
        """Builds each component and reflect the change to the UI.

        :return:
        """
        # Draw the poly-line from the data
        poly_line = vmv.geometry.ops.draw_poly_line(
            poly_line_data=self.components[component_index], name='line', material=None,
            bevel_object=self.bevel_object)

        if self.object is None:
            self.object = poly_line
        else:
            self.object = vmv.scene.join_objects([self.object, poly_line])



    ################################################################################################
    # @build_section
    ################################################################################################
    def build_section(self,
                      section):
        """Build section, connected with one of the parent and one of the children to make a smooth
        continuation between the sections.

        :param section:
            A given section to build.
        :return:
            Returns a reference to the created sections, just in case if we need to use them to
            reconstruct the mesh.
        """
        '''
        # A list to keep the connectivity data to draw the poly-lines of the connected sections
        sections_data = list()

        # If the section has any parents and any children
        if len(section.parents) > 0 and len(section.children) > 0:

            # Make a connected section between each parent and this section
            for parent in section.parents:

                # Extend the connectivity from the section to each child
                for child in section.children:

                    # Get the section data
                    section_data = vmv.skeleton.ops.get_connectivity_poly_line_from_parent_to_child(
                        section=section, parent=parent, child=child, center=self.center)

                    # Add the data to the list
                    sections_data.append(section_data)

        # If the section has no parents but has some children
        if len(section.parents) == 0 and len(section.children) > 0:

            # Make a connected section between this section and each child
            for child in section.children:

                # Get the section data
                section_data = vmv.skeleton.ops.get_connectivity_poly_line_from_section_to_child(
                        section=section, child=child, center=self.center)

                # Add the data to the list
                sections_data.append(section_data)

        # If the section has some parent and no children
        if len(section.parents) > 0 and len(section.children) == 0:

            # Make a connected section between each parent and this section
            for parent in section.parents:

                # Get the section data
                section_data = vmv.skeleton.ops.get_connectivity_poly_line_from_parent_to_section(
                    section=section, parent=parent, center=self.center)

                # Add the data to the list
                sections_data.append(section_data)

        # If the section is an orphan, or has no parents and no children
        if len(section.parents) == 0 and len(section.children) == 0:

            # Get the section data of this section only
            section_data = vmv.skeleton.ops.get_section_poly_line(
                section=section, center=self.center)

            # Add the data to the list
            sections_data.append(section_data)

        # A list that will keep references to the drawn poly-lines
        drawn_poly_lines = list()

        # Draw the poly-lines
        for section_data in sections_data:

            # Draw the poly-line from the data
            poly_line = vmv.geometry.ops.draw_poly_line(
                poly_line_data=section_data, name='line', material=self.materials[0],
                bevel_object=self.bevel_object)

            # Add the poly-line to the list
            drawn_poly_lines.append(poly_line)
    '''
    '''
    ################################################################################################
    # @build_section
    ################################################################################################
    def build_section(self,
                      section):
        """Build section, connected with one of the parent and one of the children to make a smooth
        continuation between the sections.

        :param section:
            A given section to build.
        :return:
            Returns a reference to the created sections, just in case if we need to use them to
            reconstruct the mesh.
        """
        
        # A list to keep the connectivity data to draw the poly-lines of the connected sections
        sections_data = list()

        # If the section has any parents and any children
        if len(section.parents) > 0 and len(section.children) > 0:

            # Make a connected section between each parent and this section
            for parent in section.parents:

                # Extend the connectivity from the section to each child
                for child in section.children:

                    # Get the section data
                    section_data = vmv.skeleton.ops.get_connectivity_poly_line_from_parent_to_child(
                        section=section, parent=parent, child=child, center=self.center)

                    # Add the data to the list
                    sections_data.append(section_data)

        # If the section has no parents but has some children
        if len(section.parents) == 0 and len(section.children) > 0:

            # Make a connected section between this section and each child
            for child in section.children:

                # Get the section data
                section_data = vmv.skeleton.ops.get_connectivity_poly_line_from_section_to_child(
                        section=section, child=child, center=self.center)

                # Add the data to the list
                sections_data.append(section_data)

        # If the section has some parent and no children
        if len(section.parents) > 0 and len(section.children) == 0:

            # Make a connected section between each parent and this section
            for parent in section.parents:

                # Get the section data
                section_data = vmv.skeleton.ops.get_connectivity_poly_line_from_parent_to_section(
                    section=section, parent=parent, center=self.center)

                # Add the data to the list
                sections_data.append(section_data)

        # If the section is an orphan, or has no parents and no children
        if len(section.parents) == 0 and len(section.children) == 0:

            # Get the section data of this section only
            section_data = vmv.skeleton.ops.get_section_poly_line(
                section=section, center=self.center)

            # Add the data to the list
            sections_data.append(section_data)

        # A list that will keep references to the drawn poly-lines
        drawn_poly_lines = list()

        # Draw the poly-lines
        for section_data in sections_data:

            # Draw the poly-line from the data
            poly_line = vmv.geometry.ops.draw_poly_line(
                poly_line_data=section_data, name='line', material=self.materials[0],
                bevel_object=self.bevel_object)

            # Add the poly-line to the list
            drawn_poly_lines.append(poly_line)
    '''

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
        for section in self.morphology.sections_list:

            # Poly-line samples
            poly_lines = vmv.skeleton.ops.get_connected_sections_poly_lines(section=section)

            # Poly-line material index (we use two colors to highlight the sections)
            poly_lines_data.extend(poly_lines)

        # Return the poly-lines list
        return poly_lines_data

    ################################################################################################
    # @build_skeleton
    ################################################################################################
    def build_skeleton(self, 
                       context=None):
        """Draws the morphology skeleton using fast reconstruction and drawing method.
        """

        vmv.logger.header('Building skeleton: ConnectedSectionsBuilder')

        # Get the context 
        self.context = context 
        
        # Clear the scene
        vmv.logger.detail('Clearing scene')
        vmv.scene.ops.clear_scene()

        # Clear the materials
        vmv.logger.info('Clearing assets')
        vmv.scene.ops.clear_scene_materials()

        # Create assets and color - maps
        vmv.logger.info('Creating assets')
        color_map = [self.options.mesh.color]

        # Create a static bevel object that you can use to scale the samples
        bevel_object = vmv.mesh.create_bezier_circle(
            radius=1.0, vertices=self.options.morphology.bevel_object_sides, name='bevel')

        # Construct sections poly-lines
        vmv.logger.log('Constructing poly-lines')
        poly_lines_data = self.get_connected_sections_poly_lines_data()

        # Pre-process the radii
        vmv.logger.detail('Adjusting radii')
        vmv.skeleton.update_poly_lines_radii(poly_lines=poly_lines_data, options=self.options)

        # Construct the final object and add it to the morphology
        vmv.logger.log('Drawing object')
        return vmv.geometry.create_poly_lines_object_from_poly_lines_data(
            poly_lines_data, material=self.options.morphology.material, color_map=color_map,
            name=self.morphology.name, bevel_object=bevel_object)


    def build_skeletonxx(self):
        """Builds a list of connected sections with only a single traversal per section

        :return:
            A list of connected sections.
        """

        # For every root in the morphology
        for root in self.morphology.roots:

            poly_line_data = list()
            poly_lines_data = list()

            # Get the section data
            vmv.skeleton.ops.get_connectivity_poly_lines_from_this_section_to_leaf(
                root, poly_line_data, poly_lines_data, center=self.morphology.bounding_box.center)

            self.components.extend(poly_lines_data)

            for i, poly_line in enumerate(poly_lines_data):

                # Draw the poly-line from the data
                p = vmv.geometry.ops.draw_poly_line(
                    poly_line_data=poly_line, name='line', material=None,
                    bevel_object=self.bevel_object)

        # Reset the traversal state
        self.morphology.reset_traversal_states()

    ################################################################################################
    # @build
    ################################################################################################
    def build(self, context=None):
        """Draws the morphology skeleton using fast reconstruction and drawing methods.
        """

        # Get the context 
        self.context = context 

        # Clear the scene
        vmv.scene.ops.clear_scene()


        # Get the center of the morphology
        self.center = self.morphology.bounding_box.center

        # For each section in the morphology, draw the section as a series of disconnected segments
        #for section in self.morphology.sections_list:
        #    self.build_section(section)

        # self.morphology.update_terminals_radii()

        self.build_skeleton()

        return self.morphology_objects
