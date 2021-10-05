####################################################################################################
# Copyright (c) 2019 - 2021, EPFL / Blue Brain Project
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

# System import
import time
import math
import copy

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.bbox
import vmv.enums
import vmv.consts
import vmv.file
import vmv.builders
import vmv.skeleton
import vmv.interface
import vmv.utilities
import vmv.rendering
import vmv.mesh
import vmv.shading
from .morphology_panel_ops import *


####################################################################################################
# @VMV_MorphologyPanel
####################################################################################################
class VMV_MorphologyPanel(bpy.types.Panel):
    """Morphology visualization panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_label = 'Morphology Visualization'
    bl_idname = 'OBJECT_PT_VMV_MorphologyVisualization'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'VessMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @update_morphology_material
    ################################################################################################
    def update_morphology_material(self,
                                   context):
        """Updates the shading and materials assigned to the morphology on-the-fly.

        :param context:
            Blender context.
        """

        # Make sure that the morphology is loaded and drawn in the scene
        if vmv.interface.is_vascular_morphology_in_scene():

            # Detect how many material slots the morphology has
            slots = vmv.interface.MorphologyPolylineObject.material_slots

            # Single material
            if len(slots) == 1:
                color_map = [context.scene.VMV_MorphologyColor]

            # Alternating or short sections
            elif len(slots) == 2:
                color_map = [context.scene.VMV_MorphologyColor1,
                             context.scene.VMV_MorphologyColor2]

            # Alignment colors
            elif len(slots) == 125:
                color_map = vmv.utilities.create_xyz_color_list()

            # Full scale color-map
            else:
                color_map = vmv.utilities.create_color_map_from_color_list(
                    vmv.interface.Options.morphology.color_map_colors,
                    number_colors=vmv.interface.Options.morphology.color_map_resolution)

            # Keep a list of the morphology materials by name
            morphology_materials_names = list()
            for material in vmv.interface.MorphologyPolylineObject.data.materials:
                morphology_materials_names.append(material.name)

            # Create the new materials and assign them to the morphology
            for i in range(len(color_map)):

                # Create the material
                material = vmv.shading.create_material(
                    name='%s_%d_%s' % (vmv.interface.MorphologyObject.name, i,
                                       vmv.utilities.get_random_string(6)),
                    color=color_map[i],
                    material_type=context.scene.VMV_MorphologyMaterial)

                # Update the material with the new one
                vmv.interface.MorphologyPolylineObject.data.materials[i] = material

            # Clear the old materials, to avoid any memory explosion
            for material_name in morphology_materials_names:
                vmv.scene.clear_material_with_name(name=material_name)

    ################################################################################################
    # @update_time_frame
    ################################################################################################
    def update_time_frame(self,
                          context):
        """Updates the time frame and the corresponding text box for a given time step.

        :param context:
            Blender context.
        """

        # The value that is set by the user
        input_value = context.scene.VMV_CurrentSimulationFrame

        # If the input value is less than the first frame, set it to the first frame
        if input_value < context.scene.VMV_FirstSimulationFrame:
            context.scene.VMV_CurrentSimulationFrame = context.scene.VMV_FirstSimulationFrame

        # If the input value is greater than the last frame, set it to the last frame
        if input_value > context.scene.VMV_LastSimulationFrame:
            context.scene.VMV_CurrentSimulationFrame = context.scene.VMV_LastSimulationFrame

        # Otherwise, update the UI
        bpy.context.scene.frame_set(input_value)

        # Update the progress bar
        context.scene.VMV_SimulationProgressBar = math.ceil(int(
            100.0 * input_value / context.scene.VMV_LastSimulationFrame))

    ################################################################################################
    # @update_morphology_color
    ################################################################################################
    def update_morphology_color(self,
                                context):
        """Updates the morphology color on-the-fly once the color is changed from the palette.

        :param context:
            Blender context.
        """

        # Make sure that the morphology is loaded and drawn in the scene
        if vmv.interface.is_vascular_morphology_in_scene():

            # No materials, return
            if len(vmv.interface.MorphologyPolylineObject.data.materials) == 0:
                return

            # Just a single material
            elif len(vmv.interface.MorphologyPolylineObject.data.materials) == 1:

                # Update the active material
                vmv.interface.MorphologyPolylineObject.active_material.diffuse_color = \
                    Vector((context.scene.VMV_MorphologyColor[0],
                            context.scene.VMV_MorphologyColor[1],
                            context.scene.VMV_MorphologyColor[2],
                            1.0))
            # Make sure that the morphology has two materials
            elif len(vmv.interface.MorphologyPolylineObject.data.materials) == 2:
                # Update material 1
                vmv.interface.MorphologyPolylineObject.data.materials[0].diffuse_color = \
                    Vector((context.scene.VMV_MorphologyColor1[0],
                            context.scene.VMV_MorphologyColor1[1],
                            context.scene.VMV_MorphologyColor1[2],
                            1.0))

                # Update material 2
                vmv.interface.MorphologyPolylineObject.data.materials[1].diffuse_color = \
                    Vector((context.scene.VMV_MorphologyColor2[0],
                            context.scene.VMV_MorphologyColor2[1],
                            context.scene.VMV_MorphologyColor2[2],
                            1.0))
            # Color mapping
            else:

                # Interpolate
                colors = vmv.utilities.create_color_map_from_color_list(
                    vmv.interface.Options.morphology.color_map_colors,
                    number_colors=vmv.interface.Options.morphology.color_map_resolution)

                for i in range(len(vmv.interface.MorphologyPolylineObject.material_slots)):
                    vmv.interface.MorphologyPolylineObject.active_material_index = i

                    if bpy.context.scene.render.engine == 'CYCLES':
                        material_nodes = vmv.interface.MorphologyPolylineObject.active_material.node_tree
                        color_1 = material_nodes.nodes['ColorRamp'].color_ramp.elements[0].color
                        color_2 = material_nodes.nodes['ColorRamp'].color_ramp.elements[1].color

                        for j in range(3):
                            color_1[j] = colors[i][j]
                            color_2[j] = 0.5 * colors[i][j]
                    else:
                        vmv.interface.MorphologyPolylineObject.active_material.diffuse_color = \
                            Vector((colors[i][0], colors[i][1], colors[i][2], 1.0))

    ################################################################################################
    # @update_ui_colors
    ################################################################################################
    def update_ui_colors(self,
                         context):
        """Updates the UI colors once a different color-map is selected on-the-fly and accordingly
        check if the morphology object is present in the scene or not and update its colors as well.

        :param context:
            Blender context.
        """

        # Get a list of initial colors from the selected colormap
        colors = vmv.utilities.create_colormap_from_hex_list(
            vmv.enums.ColorMaps.get_hex_color_list(context.scene.VMV_ColorMap),
            vmv.consts.Color.COLORMAP_RESOLUTION)

        # Invert the colormap
        if context.scene.VMV_InvertColorMap:
            colors.reverse()

        # Update the colormap in the UI
        for color_index in range(vmv.consts.Color.COLORMAP_RESOLUTION):
            setattr(context.scene, 'VMV_Color%d' % color_index, colors[color_index])

        # Make sure that the morphology is already in the scene
        if vmv.interface.is_vascular_morphology_in_scene():

            # Interpolate
            colors = vmv.utilities.create_color_map_from_color_list(
                vmv.interface.Options.morphology.color_map_colors,
                number_colors=vmv.interface.Options.morphology.color_map_resolution)

            for i in range(len(vmv.interface.MorphologyPolylineObject.material_slots)):
                vmv.interface.MorphologyPolylineObject.active_material_index = i

                if bpy.context.scene.render.engine == 'CYCLES':
                    material_nodes = vmv.interface.MorphologyPolylineObject.active_material.node_tree
                    color_1 = material_nodes.nodes['ColorRamp'].color_ramp.elements[0].color
                    color_2 = material_nodes.nodes['ColorRamp'].color_ramp.elements[1].color

                    for j in range(3):
                        color_1[j] = colors[i][j]
                        color_2[j] = 0.5 * colors[i][j]
                else:
                    vmv.interface.MorphologyPolylineObject.active_material.diffuse_color = \
                        Vector((colors[i][0], colors[i][1], colors[i][2], 1.0))

    ################################################################################################
    # @update_bevel_object
    ################################################################################################
    def update_bevel_object(self,
                            context):
        """Updates the number of sides of the bevel object in the scene.

        :param context:
            Blender context.
        """

        # Make sure that the morphology is in the scene
        if vmv.interface.is_vascular_morphology_in_scene():

            # Get the bevel object
            bevel_object = vmv.scene.get_object_by_name(
                vmv.interface.MorphologyPolylineObject.data.bevel_object.name)

            # Make sure that this bevel object is not None
            if bevel_object is not None:

                # Delete the old bevel object
                vmv.scene.delete_object_in_scene(bevel_object)

                # Create a new bevel object
                bevel_object = vmv.mesh.create_bezier_circle(
                    radius=1.0, vertices=context.scene.VMV_BevelSides, name='bevel')
                vmv.interface.MorphologyPolylineObject.data.bevel_object = bevel_object
                vmv.scene.hide_object(scene_object=bevel_object)

    ################################################################################################
    # Tube quality
    bpy.types.Scene.VMV_BevelSides = bpy.props.IntProperty(
        name='Sides',
        description='Number of sides of the cross-section of each segment along the drawn tube.'
                    'The minimum is 4, maximum 128 and default is 8. High value is required for '
                    'closeups and low value is sufficient for far-away visualizations.',
        default=8, min=4, max=128,
        update=update_bevel_object)

    # Options that require an @update function #####################################################
    # The base color that will be used for all the components in the morphology
    bpy.types.Scene.VMV_MorphologyColor = bpy.props.FloatVectorProperty(
        name='Color',
        subtype='COLOR', default=vmv.consts.Color.LIGHT_RED_COLOR, min=0.0, max=1.0,
        description='The base color of the morphology.',
        update=update_morphology_color)

    # The alternative color used to color every second object in the morphology
    bpy.types.Scene.VMV_MorphologyColor1 = bpy.props.FloatVectorProperty(
        name='',
        description='The first alternating color of the morphology',
        subtype='COLOR', default=vmv.consts.Color.VERY_WHITE, min=0.0, max=1.0,
        update=update_morphology_color)

    # The alternative color used to color every second object in the morphology
    bpy.types.Scene.VMV_MorphologyColor2 = bpy.props.FloatVectorProperty(
        name='',
        subtype='COLOR', default=vmv.consts.Color.LIGHT_RED_COLOR, min=0.0, max=1.0,
        description='The second alternating color of the morphology',
        update=update_morphology_color)

    # A list of all the color maps available in VMV
    # Note that once a new colormap is selected, the corresponding colors will be set in the UI
    bpy.types.Scene.VMV_ColorMap = bpy.props.EnumProperty(
        items=vmv.enums.ColorMaps.COLOR_MAPS,
        name='',
        default=vmv.enums.ColorMaps.GNU_PLOT,
        update=update_ui_colors)

    # Inversion for the color-map
    bpy.types.Scene.VMV_InvertColorMap = bpy.props.BoolProperty(
        name='Invert',
        description='Invert the selected colormap.',
        default=False,
        update=update_ui_colors)

    # Red color for X alignment
    bpy.types.Scene.VMV_RedColor = bpy.props.FloatVectorProperty(
        name='',
        description='The red color corresponds to the X-axis',
        subtype='COLOR', default=vmv.consts.Color.RED, min=0.0, max=1.0)

    # Green color for Y alignment
    bpy.types.Scene.VMV_GreenColor = bpy.props.FloatVectorProperty(
        name='',
        description='The green color corresponds to the Y-axis',
        subtype='COLOR', default=vmv.consts.Color.GREEN, min=0.0, max=1.0)

    # Blue color for Z alignment
    bpy.types.Scene.VMV_BlueColor = bpy.props.FloatVectorProperty(
        name='',
        description='The blue color corresponds to the Z-axis',
        subtype='COLOR', default=vmv.consts.Color.BLUE, min=0.0, max=1.0)

    # Create a list of colors from the selected colormap
    colors = vmv.utilities.create_colormap_from_hex_list(
        vmv.enums.ColorMaps.get_hex_color_list(bpy.types.Scene.VMV_ColorMap),
        vmv.consts.Color.COLORMAP_RESOLUTION)

    # Update the UI color elements from the color map list
    for index in range(vmv.consts.Color.COLORMAP_RESOLUTION):
        setattr(bpy.types.Scene, 'VMV_Color%d' % index, bpy.props.FloatVectorProperty(
            name='', subtype='COLOR', default=colors[index], min=0.0, max=1.0, description='',
            update=update_morphology_color))

    # The current time frame of the simulation
    bpy.types.Scene.VMV_CurrentSimulationFrame = bpy.props.IntProperty(
        name='',
        default=0, min=0, max=1000000,
        update=update_time_frame)

    # Material
    bpy.types.Scene.VMV_MorphologyMaterial = bpy.props.EnumProperty(
        items=vmv.enums.Shader.SHADER_ITEMS,
        name='',
        default=vmv.enums.Shader.LAMBERT_WARD,
        update=update_morphology_material)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draws the panel.

        :param context:
            Panel context.
        """

        # Visualization type options
        add_visualization_type_options(
            layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # Static structure options
        visualization_type = vmv.interface.Options.morphology.visualization_type
        if visualization_type == vmv.enums.Morphology.Visualization.STRUCTURE:
            add_static_morphology_visualization_options(
                layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # Dynamic structure
        elif visualization_type == vmv.enums.Morphology.Visualization.RADII_STRUCTURAL_DYNAMICS:
            add_structural_dynamics_visualization_options(
                layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # Dynamic function (with colormap)
        else:
            add_colormap_dynamics_visualization_options(
                layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # Draw the morphology rendering options
        add_morphology_rendering_options(
            layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # If the morphology is loaded, enable the layout, otherwise make it disabled by default
        if vmv.interface.MorphologyLoaded:
            self.layout.enabled = True
        else:
            self.layout.enabled = False


####################################################################################################
# @VMV_ReconstructMorphology
####################################################################################################
class VMV_ReconstructMorphology(bpy.types.Operator):
    """Reconstructs the mesh of the vasculature"""

    # Operator parameters
    bl_idname = 'reconstruct.morphology'
    bl_label = 'Reconstruct Morphology'
    bl_options = {'REGISTER'}

    # The builder that will be used to build the morphology
    morphology_builder = None

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Executes the operator

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Clear the scene
        vmv.scene.ops.clear_scene()

        # Starting the reconstruction timer
        start_reconstruction = time.time()

        # Make sure that the morphology isn loaded and valid in memory
        if not vmv.interface.MorphologyLoaded:
            print('ERROR: Morphology is not loaded')

        # Construct the skeleton builder
        if vmv.interface.Options.morphology.builder == vmv.enums.Morphology.Builder.SEGMENTS:
            self.morphology_builder = vmv.builders.SegmentsBuilder(
                morphology=vmv.interface.MorphologyObject, options=vmv.interface.Options)

        # Disconnected sections builder
        elif vmv.interface.Options.morphology.builder == vmv.enums.Morphology.Builder.SECTIONS:

            self.morphology_builder = vmv.builders.SectionsBuilder(
                morphology=vmv.interface.MorphologyObject,
                options=vmv.interface.Options)

        # Samples builder
        elif vmv.interface.Options.morphology.builder == vmv.enums.Morphology.Builder.SAMPLES:

            self.morphology_builder = vmv.builders.SamplesBuilder(
                morphology=vmv.interface.MorphologyObject,
                options=vmv.interface.Options)

        else:
            return {'FINISHED'}

        # Build the morphology skeleton directly
        # NOTE: each builder must have this function @build_skeleton() implemented in it
        vmv.interface.MorphologyPolylineObject = self.morphology_builder.build_skeleton(
            context=context)

        # Interpolations
        scale = float(context.scene.VMV_MaximumValue) - float(context.scene.VMV_MinimumValue)
        delta = scale / float(vmv.consts.Color.COLORMAP_RESOLUTION)

        # Fill the list of colors
        for color_index in range(vmv.consts.Color.COLORMAP_RESOLUTION):
            r0_value = float(context.scene.VMV_MinimumValue) + (color_index * delta)
            r1_value = float(context.scene.VMV_MinimumValue) + ((color_index + 1) * delta)
            setattr(context.scene, 'VMV_R0_Value%d' % color_index, r0_value)
            setattr(context.scene, 'VMV_R1_Value%d' % color_index, r1_value)

        # Reconstruction timer
        reconstruction_done = time.time()
        context.scene.VMV_MorphologyReconstructionTime = reconstruction_done - start_reconstruction

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_ReconstructMesh
####################################################################################################
class VMV_ExportMorphology(bpy.types.Operator):
    """Export the reconstructed morphology to a file"""

    # Operator parameters
    bl_idname = 'export.morphology'
    bl_label = 'Export'

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Executes the operator

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(VMV_MorphologyPanel)

    # Morphology reconstruction button
    bpy.utils.register_class(VMV_ReconstructMorphology)

    # Simulation buttons
    bpy.utils.register_class(vmv.interface.VMV_LoadSimulation)
    bpy.utils.register_class(vmv.interface.VMV_PlaySimulation)
    bpy.utils.register_class(vmv.interface.VMV_SimulationPreviousFrame)
    bpy.utils.register_class(vmv.interface.VMV_SimulationNextFrame)
    bpy.utils.register_class(vmv.interface.VMV_SimulationFirstFrame)
    bpy.utils.register_class(vmv.interface.VMV_SimulationLastFrame)

    # Morphology rendering buttons
    bpy.utils.register_class(vmv.interface.VMV_RenderMorphologyImage)
    bpy.utils.register_class(vmv.interface.VMV_RenderMorphology360)
    bpy.utils.register_class(vmv.interface.VMV_RenderSimulation)

    # Morphology export button
    bpy.utils.register_class(VMV_ExportMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(VMV_MorphologyPanel)

    # Morphology reconstruction button
    bpy.utils.unregister_class(VMV_ReconstructMorphology)

    # Simulation buttons
    bpy.utils.unregister_class(vmv.interface.VMV_LoadSimulation)
    bpy.utils.unregister_class(vmv.interface.VMV_PlaySimulation)
    bpy.utils.unregister_class(vmv.interface.VMV_SimulationPreviousFrame)
    bpy.utils.unregister_class(vmv.interface.VMV_SimulationNextFrame)
    bpy.utils.unregister_class(vmv.interface.VMV_SimulationFirstFrame)
    bpy.utils.unregister_class(vmv.interface.VMV_SimulationLastFrame)

    # Morphology rendering buttons
    bpy.utils.unregister_class(vmv.interface.VMV_RenderMorphologyImage)
    bpy.utils.unregister_class(vmv.interface.VMV_RenderMorphology360)
    bpy.utils.unregister_class(vmv.interface.VMV_RenderSimulation)

    # Morphology export button
    bpy.utils.unregister_class(VMV_ExportMorphology)
