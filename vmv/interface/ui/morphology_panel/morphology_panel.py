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

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.bbox
import vmv.enums
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
    # @update_time_frame
    ################################################################################################
    def update_time_frame(self,
                          context):
        """Updates the time frame and the corresponding text box for a given time step

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

        # TODO: Verify if the morphology is deleted or exists in the scene, using its name!
        if vmv.interface.MorphologyPolylineObject is not None:
            color = context.scene.VMV_MorphologyColor

            vmv.interface.MorphologyPolylineObject.active_material.diffuse_color = \
                Vector((color[0], color[1], color[2], 1.0))

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

        if vmv.interface.MorphologyPolylineObject is not None:

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

        # TODO: Verify if the morphology is deleted or exists in the scene, using its name!
        if vmv.interface.MorphologyPolylineObject is not None:
            bevel_sides = context.scene.VMV_TubeQuality

            # Get the bevel object
            bevel_object = vmv.scene.get_object_by_name('bevel')
            if bevel_object is not None:

                # Delete the old bevel object
                vmv.scene.delete_object_in_scene(bevel_object)

                # Create a new bevel object
                bevel_object = vmv.mesh.create_bezier_circle(
                    radius=1.0, vertices=bevel_sides, name='bevel')
                vmv.interface.MorphologyPolylineObject.data.bevel_object = bevel_object

    # Tube quality
    bpy.types.Scene.VMV_TubeQuality = bpy.props.IntProperty(
        name='Sides',
        description='Number of sides of the cross-section of each segment along the drawn tube.'
                    'The minimum is 4, maximum 128 and default is 8. High value is required for '
                    'closeups and low value is sufficient for far-away visualizations',
        default=8, min=4, max=128,
        update=update_bevel_object)

    # Options that require an @update function #####################################################
    # The base color that will be used for all the components in the morphology
    bpy.types.Scene.VMV_MorphologyColor = bpy.props.FloatVectorProperty(
        name='Color',
        subtype='COLOR', default=vmv.consts.Color.LIGHT_RED_COLOR, min=0.0, max=1.0,
        description='The base color of the morphology',
        update=update_morphology_color)

    # A list of all the color maps available in VMV
    # Note that once a new colormap is selected, the corresponding colors will be set in the UI
    bpy.types.Scene.VMV_ColorMap = bpy.props.EnumProperty(
        items=vmv.enums.ColorMaps.COLOR_MAPS,
        name='',
        default=vmv.enums.ColorMaps.GNU_PLOT,
        update=update_ui_colors)

    bpy.types.Scene.VMV_InvertColorMap = bpy.props.BoolProperty(
        name='Invert',
        description='Invert the selected colormap',
        default=False,
        update=update_ui_colors)

    # Create a list of colors from the selected colormap
    colors = vmv.utilities.create_colormap_from_hex_list(
        vmv.enums.ColorMaps.get_hex_color_list(bpy.types.Scene.VMV_ColorMap),
        vmv.consts.Color.COLORMAP_RESOLUTION)

    # Update the UI color elements from the color map list
    for index in range(vmv.consts.Color.COLORMAP_RESOLUTION):
        setattr(bpy.types.Scene, 'VMV_Color%d' % index, bpy.props.FloatVectorProperty(
            name='', subtype='COLOR', default=colors[index], min=0.0, max=1.0, description=''))

    # The current time frame of the simulation
    bpy.types.Scene.VMV_CurrentSimulationFrame = bpy.props.IntProperty(
        name='',
        default=0, min=0, max=1000000,
        update=update_time_frame)

    ################################################################################################
    # @draw_morphology_color_options
    ################################################################################################
    def draw_morphology_color_options(self, context):
        """Draw the coloring options.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene

        # Reference to morphology options
        morphology_options = vmv.interface.Options.morphology

        # Coloring parameters
        colors_row = self.layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Morphology material
        morphology_material_row = self.layout.row()
        morphology_material_row.prop(scene, 'VMV_MorphologyMaterial')
        morphology_options.material = scene.VMV_MorphologyMateria

    ################################################################################################
    # @draw_morphology_rendering_options
    ################################################################################################
    def draw_morphology_rendering_options(self,
                                          context):
        """Draw the rendering options.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Rendering options
        rendering_row = self.layout.row()
        rendering_row.label(text='Rendering Options:', icon='RENDER_STILL')

        # Rendering resolution
        rendering_resolution_row = self.layout.row()
        rendering_resolution_row.label(text='Resolution:')
        rendering_resolution_row.prop(context.scene, 'VMV_MorphologyRenderingResolution', expand=True)

        # Add the frame resolution option
        if context.scene.VMV_MorphologyRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Frame resolution option (only for the close up mode)
            frame_resolution_row = self.layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(context.scene, 'VMV_MorphologyImageResolution')
            vmv.interface.Options.morphology.resolution_basis = \
                context.scene.VMV_MorphologyRenderingResolution

        # Otherwise, add the scale factor option
        else:

            # Scale factor option
            scale_factor_row = self.layout.row()
            scale_factor_row.label(text='Resolution Scale:')
            scale_factor_row.prop(context.scene, 'VMV_MorphologyImageScaleFactor')
            vmv.interface.Options.morphology.resolution_scale_factor = \
                context.scene.VMV_MorphologyImageScaleFactor

        # Rendering view column
        view_row = self.layout.column()
        view_row.prop(context.scene, 'VMV_MorphologyRenderingViews', icon='AXIS_FRONT')
        vmv.Options.morphology.camera_view = context.scene.VMV_MorphologyRenderingViews

        # Rendering projection column only for a fixed resolution
        if context.scene.VMV_MorphologyRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Due to a bug in the workbench renderer in Blender, we will allow the
            # perspective projection for all the materials that use cycles and have high number of
            # samples per pixel, mainly the artistic rendering.
            if vmv.Options.morphology.material in vmv.enums.Shader.SUB_SURFACE_SCATTERING:

                # Add the projection option
                projection_row = self.layout.column()
                projection_row.prop(context.scene, 'VMV_MorphologyCameraProjection', icon='AXIS_FRONT')
                vmv.Options.morphology.camera_projection = \
                    context.scene.VMV_MorphologyCameraProjection

            # Set it by default to ORTHOGRAPHIC
            else:
                vmv.Options.morphology.camera_projection = \
                    vmv.enums.Rendering.Projection.ORTHOGRAPHIC

                # Scale bar
                scale_bar_row = layout.row()
                scale_bar_row.prop(context.scene, 'VMV_RenderMorphologyScaleBar')
                vmv.interface.Options.morphology.render_scale_bar = context.scene.VMV_RenderMorphologyScaleBar

        # Set it by default to ORTHOGRAPHIC
        else:
            vmv.Options.morphology.camera_projection = \
                vmv.enums.Rendering.Projection.ORTHOGRAPHIC

            # Scale bar
            scale_bar_row = layout.row()
            scale_bar_row.prop(context.scene, 'VMV_RenderMorphologyScaleBar')
            vmv.interface.Options.morphology.render_scale_bar = context.scene.VMV_RenderMorphologyScaleBar

        # Rendering button
        rendering_button_row = self.layout.column()
        rendering_button_row.operator('render_morphology.image', icon='MESH_DATA')

        # Render animation row
        render_animation_row = self.layout.row()
        render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
        render_animations_buttons_row = self.layout.row(align=True)
        render_animations_buttons_row.operator('render_morphology.360', icon='FORCE_MAGNETIC')

        # Render simulation
        if vmv.interface.SimulationLoaded:
            rendering_simulation_button_row = self.layout.column()
            rendering_simulation_button_row.operator('render.simulation', icon='MESH_DATA')

        # Rendering progress bar
        rendering_progress_row = self.layout.row()
        rendering_progress_row.prop(context.scene, 'VMV_MorphologyRenderingProgress')
        rendering_progress_row.enabled = False

    ################################################################################################
    # @draw_morphology_export_options
    ################################################################################################
    def draw_morphology_export_options(self,
                                       context):
        """Draw the morphology export button.

        :param context:
            Context.
        """

        # Saving meshes parameters
        save_mesh_row = self.layout.row()
        save_mesh_row.label(text='Export Morphology As:', icon='MESH_UVSPHERE')

        # Exported format column
        format_column = self.layout.column()
        format_column.prop(context.scene, 'ExportedMorphologyFormat', icon='GROUP_VERTEX')
        format_column.operator('export.morphology', icon='MESH_DATA')

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draw the panel.

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
        self.draw_morphology_rendering_options(context=context)

        # Draw the morphology export options
        # self.draw_morphology_export_options(context=context)

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
        # Disconnected segments builder
        if vmv.interface.Options.morphology.builder == \
                vmv.enums.Morphology.Builder.SEGMENTS:
            self.morphology_builder = vmv.builders.SegmentsBuilder(
                morphology=vmv.interface.MorphologyObject, options=vmv.interface.Options)

        # Disconnected sections builder
        elif vmv.interface.Options.morphology.builder == \
                vmv.enums.Morphology.Builder.SECTIONS:

            self.morphology_builder = vmv.builders.SectionsBuilder(
                morphology=vmv.interface.MorphologyObject,
                options=vmv.interface.Options)

        # Samples builder
        elif vmv.interface.Options.morphology.builder == \
                vmv.enums.Morphology.Builder.SAMPLES:

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


        """
        # Load the morphology file
        loading_result = vmv.interface.ui.load_morphology(self, context.scene)

        # If the result is None, report the issue
        if loading_result is None:
            self.report({'ERROR'}, 'Please select a morphology file')
            return {'FINISHED'}

        # Meshing technique
        meshing_technique = vmv.interface.Options.mesh.meshing_technique

        # Piece-wise watertight meshing
        if meshing_technique == vmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:

            # Create the mesh builder
            mesh_builder = vmv.builders.PiecewiseBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.Options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Bridging
        elif meshing_technique == vmv.enums.Meshing.Technique.BRIDGING:

            # Create the mesh builder
            mesh_builder = vmv.builders.BridgingBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.Options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Union
        elif meshing_technique == vmv.enums.Meshing.Technique.UNION:

            # Create the mesh builder
            mesh_builder = vmv.builders.UnionBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.Options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Extrusion
        elif meshing_technique == vmv.enums.Meshing.Technique.EXTRUSION:

            # Create the mesh builder
            mesh_builder = vmv.builders.ExtrusionBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.Options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        elif meshing_technique == vmv.enums.Meshing.Technique.SKINNING:

            # Create the mesh builder
            mesh_builder = vmv.builders.SkinningBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.Options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        elif meshing_technique == vmv.enums.Meshing.Technique.META_OBJECTS:

            # Create the mesh builder
            mesh_builder = vmv.builders.MetaBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.Options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        else:

            # Invalid method
            self.report({'ERROR'}, 'Invalid Meshing Technique')
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
