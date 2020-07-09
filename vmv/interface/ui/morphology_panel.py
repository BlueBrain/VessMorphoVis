####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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
import copy

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
import vmv.shading


####################################################################################################
# @VMVColorMapOperator
####################################################################################################
class VMVColorMapOperator(bpy.types.Operator):
    """Color-map operator for interactively changing the color-map in the UI"""

    ################################################################################################
    # Operator parameters
    ################################################################################################
    bl_idname = "operator.pick_colormap"
    bl_label = "Select ColorMap"
    bl_options = {'REGISTER', 'INTERNAL'}

    ################################################################################################
    # @update_ui_colors
    ################################################################################################
    def update_ui_colors(self, context):
        colors = vmv.utilities.create_color_map_from_hex_list(
        vmv.enums.ColorMaps.get_hex_color_list(context.scene.ColorMap),
        vmv.consts.Color.NUMBER_COLORS_UI)

        for i in range(vmv.consts.Color.NUMBER_COLORS_UI):
            setattr(context.scene, 'Color%d' % i, colors[i])

        if vmv.interface.ui.morphology_skeleton is not None:

            # Interpolate
            colors = vmv.utilities.create_color_map_from_color_list(
                vmv.interface.ui.options.morphology.color_map_colors,
                number_colors=vmv.interface.ui.options.morphology.color_map_resolution)

            for i in range(len(vmv.interface.ui.morphology_skeleton.material_slots)):
                vmv.interface.ui.morphology_skeleton.active_material_index = i

                if bpy.context.scene.render.engine == 'CYCLES':
                    material_nodes = vmv.interface.ui.morphology_skeleton.active_material.node_tree
                    color_1 = material_nodes.nodes['ColorRamp'].color_ramp.elements[0].color
                    color_2 = material_nodes.nodes['ColorRamp'].color_ramp.elements[1].color
                    for j in range(3):
                        color_1[j] = colors[i][j]
                        color_2[j] = 0.5 * colors[i][j]
                else:
                    vmv.interface.ui.morphology_skeleton.active_material.diffuse_color = \
                        Vector((colors[i][0], colors[i][1], colors[i][2], 1.0))

    # A list of all the color maps available in VessMorphoVis
    # Note that once a new colormap is selected, the corresponding colors will be set in the UI
    bpy.types.Scene.ColorMap = bpy.props.EnumProperty(
        items=vmv.ColorMaps.COLOR_MAPS,
        name="ColorMap",
        default=vmv.enums.ColorMaps.VIRIDIS,
        update=update_ui_colors)

    # Create a list of colors from the selected colormap
    colors = vmv.utilities.create_color_map_from_hex_list(
        vmv.enums.ColorMaps.get_hex_color_list(bpy.types.Scene.ColorMap), 
        vmv.consts.Color.NUMBER_COLORS_UI)

    # UI color elements for the color map
    for i in range(vmv.consts.Color.NUMBER_COLORS_UI):
        setattr(bpy.types.Scene, 'Color%d' % i, bpy.props.FloatVectorProperty(
                name='', subtype='COLOR', default=colors[i], min=0.0, max=1.0, description=''))

    ################################################################################################
    # @poll
    ################################################################################################
    @classmethod
    def poll(cls, context):
        return True

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        return {'FINISHED'}

    ################################################################################################
    # @invoke
    ################################################################################################
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):

        # A reference to the layout 
        layout = self.layout

        # Color map 
        color_map = layout.row()
        color_map.prop(context.scene, 'ColorMap')
        
        # Its resolution 
        color_map_resolution = layout.row()
        color_map_resolution.prop(context.scene, 'ColorMapResolution')
        vmv.interface.ui.options.morphology.color_map_resolution = \
            context.scene.ColorMapResolution - 1
        
        # Clear the color map passed to VMV if it is full 
        if len(vmv.interface.ui.options.morphology.color_map_colors) > 0:
            vmv.interface.ui.options.morphology.color_map_colors.clear()
        
        # UI color elements 
        colors = layout.row()
        for i in range(vmv.consts.Color.NUMBER_COLORS_UI):
            
            # Add the color to the interface 
            colors.prop(context.scene, 'Color%d' % i)

            # Get the color value 
            color = getattr(context.scene, 'Color%d' % i)

            # Send it to VMV parameters 
            vmv.interface.ui.options.morphology.color_map_colors.append(color)


####################################################################################################
# @VMVMorphologyPanel
####################################################################################################
class VMVMorphologyPanel(bpy.types.Panel):
    """Morphology reconstruction panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_label = 'Morphology Reconstruction'
    bl_idname = "OBJECT_PT_VMV_MorphologyReconstruction"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'VessMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # Panel options
    ################################################################################################



    ################################################################################################
    # @draw_mesh_reconstruction_options
    ################################################################################################
    def draw_morphology_reconstruction_options(self,
                                               context):
        """Draws the morphology reconstruction options.

        :param context:
            Context.
        """

        # Skeleton meshing options
        skeleton_meshing_options_row = self.layout.row()
        skeleton_meshing_options_row.label(
            text='Morphology Reconstruction Options:', icon='SURFACE_DATA')

        # Morphology reconstruction techniques option
        morphology_reconstruction_row = self.layout.row()
        morphology_reconstruction_row.prop(
            context.scene, 'ReconstructionMethod', icon='FORCE_CURVE')
        vmv.interface.ui.options.morphology.reconstruction_method = \
            context.scene.ReconstructionMethod

        # Sections radii option
        sections_radii_row = self.layout.row()
        sections_radii_row.prop(context.scene, 'SectionsRadii', icon='SURFACE_NCURVE')

        # Radii as specified in the morphology file
        if context.scene.SectionsRadii == vmv.enums.Morphology.Radii.AS_SPECIFIED:

            # Pass options from UI to system
            vmv.interface.ui.options.morphology.radii = \
                vmv.enums.Morphology.Radii.AS_SPECIFIED
            vmv.interface.ui.options.morphology.scale_sections_radii = False
            vmv.interface.ui.options.morphology.unify_sections_radii = False
            vmv.interface.ui.options.morphology.sections_radii_scale = 1.0

        # Fixed diameter
        elif context.scene.SectionsRadii == vmv.enums.Morphology.Radii.FIXED:

            fixed_diameter_row = self.layout.row()
            fixed_diameter_row.label(text='Fixed Radius Value:')
            fixed_diameter_row.prop(context.scene, 'FixedRadiusValue')

            # Pass options from UI to system
            vmv.interface.ui.options.morphology.radii = vmv.enums.Morphology.Radii.FIXED
            vmv.interface.ui.options.morphology.scale_sections_radii = False
            vmv.interface.ui.options.morphology.unify_sections_radii = True
            vmv.interface.ui.options.morphology.sections_fixed_radii_value = \
                context.scene.FixedRadiusValue

        # Scaled diameter
        elif context.scene.SectionsRadii == vmv.enums.Morphology.Radii.SCALED:

            scaled_diameter_row = self.layout.row()
            scaled_diameter_row.label(text='Radius Scale Factor:')
            scaled_diameter_row.prop(context.scene, 'RadiusScaleValue')

            # Pass options from UI to system
            vmv.interface.ui.options.morphology.radii = vmv.enums.Morphology.Radii.SCALED
            vmv.interface.ui.options.morphology.unify_sections_radii = False
            vmv.interface.ui.options.morphology.scale_sections_radii = True
            vmv.interface.ui.options.morphology.sections_radii_scale = \
                context.scene.RadiusScaleValue

        else:
            vmv.logger.log('ERROR')

        # Tube quality
        tube_quality_row = self.layout.row()
        tube_quality_row.label(text='Tube Quality:')
        tube_quality_row.prop(context.scene, 'TubeQuality')
        vmv.interface.ui.options.morphology.bevel_object_sides = context.scene.TubeQuality

        # Morphology reconstruction techniques option
        # skeleton_style_row = self.layout.row()
        # skeleton_style_row.prop(context.scene, 'ArborsStyle', icon='WPAINT_HLT')


        # Morphology branching
        #branching_row = self.layout.row()
        #branching_row.label(text='Branching:')
        #branching_row.prop(context.scene, 'MorphologyBranching', expand=True)
        #vmv.interface.ui.options.morphology.branching = context.scene.MorphologyBranching

        # Arbor quality option
        #arbor_quality_row = self.layout.row()
        #arbor_quality_row.label(text='Arbor Quality:')
        #arbor_quality_row.prop(context.scene, 'ArborQuality')


        # Sections diameters option
        #sections_radii_row = self.layout.row()
        #sections_radii_row.prop(context.scene, 'SectionsRadii', icon='SURFACE_NCURVE')

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
        morphology_options = vmv.interface.ui.options.morphology

        # Coloring parameters
        colors_row = self.layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Morphology material
        morphology_material_row = self.layout.row()
        morphology_material_row.prop(scene, 'MorphologyMaterial')
        morphology_options.material = scene.MorphologyMaterial
    
        # If the disconnected segments is selected
        if morphology_options.reconstruction_method == \
            vmv.enums.Morphology.ReconstructionMethod.DISCONNECTED_SEGMENTS:

            # Per-segment color coding 
            color_coding_row = layout.row()
            color_coding_row.prop(scene, 'PerSegmentColorCodingBasis')
            morphology_options.color_coding = scene.PerSegmentColorCodingBasis

            # Single color 
            if scene.PerSegmentColorCodingBasis == vmv.enums.ColorCoding.SINGLE_COLOR:

                # Base morphology color
                color_row = self.layout.row()
                color_row.prop(scene, 'MorphologyColor')
                morphology_options.color = scene.MorphologyColor
                
            elif scene.PerSegmentColorCodingBasis == vmv.enums.ColorCoding.ALTERNATING_COLORS:

                # Base morphology color
                color_row = self.layout.row()
                color_row.prop(scene, 'MorphologyColor')
                morphology_options.color = scene.MorphologyColor

                # Alternating morphology color
                color_row = self.layout.row()
                color_row.prop(scene, 'MorphologyAlternatingColor')
                morphology_options.alternating_color = scene.MorphologyAlternatingColor

            else:

                # Color-mapping 
                layout = self.layout
                layout.operator(VMVColorMapOperator.bl_idname, icon='COLOR')
                
                # Clear the color map passed to VMV if it is full 
                if len(vmv.interface.ui.options.morphology.color_map_colors) > 0:
                    vmv.interface.ui.options.morphology.color_map_colors.clear()

                    # Fill the list of colors
                    for i in range(vmv.consts.Color.NUMBER_COLORS_UI):
                        colors = layout.row()
                        cmap = colors.column()
                        cmap.prop(scene, 'Color%d' % i)
                        cmap.enabled = False
                        values = colors.column()
                        values.prop(scene, 'Value%d' % i)
                        values.enabled = False
                        # Get the color value
                        color = getattr(context.scene, 'Color%d' % i)
                        vmv.interface.ui.options.morphology.color_map_colors.append(color)
        
        # Disconnected sections builder
        elif morphology_options.reconstruction_method == \
                vmv.enums.Morphology.ReconstructionMethod.DISCONNECTED_SECTIONS:

            # Per-section color coding 
            color_coding_row = layout.row()
            color_coding_row.prop(context.scene, 'PerSectionColorCodingBasis')
            morphology_options.color_coding = scene.PerSectionColorCodingBasis

            # Single color 
            if scene.PerSectionColorCodingBasis == vmv.enums.ColorCoding.SINGLE_COLOR:

                # Base morphology color
                color_row = self.layout.row()
                color_row.prop(scene, 'MorphologyColor')
                morphology_options.color = scene.MorphologyColor
                
            elif scene.PerSectionColorCodingBasis == vmv.enums.ColorCoding.ALTERNATING_COLORS:

                # Base morphology color
                color_row = self.layout.row()
                color_row.prop(scene, 'MorphologyColor')
                morphology_options.color = scene.MorphologyColor

                # Alternating morphology color
                color_row = self.layout.row()
                color_row.prop(scene, 'MorphologyAlternatingColor')
                morphology_options.alternating_color = scene.MorphologyAlternatingColor

            else:

                # Color-mapping 
                layout = self.layout
                layout.operator(VMVColorMapOperator.bl_idname, icon='COLOR')
                
                # Clear the color map passed to VMV if it is full 
                if len(vmv.interface.ui.options.morphology.color_map_colors) > 0:
                    vmv.interface.ui.options.morphology.color_map_colors.clear()

                # Fill the list of colors
                for i in range(vmv.consts.Color.NUMBER_COLORS_UI):
                    colors = layout.row()
                    cmap = colors.column()
                    cmap.prop(scene, 'Color%d' % i)
                    cmap.enabled = False
                    values = colors.column()
                    values.prop(scene, 'Value%d' % i)
                    values.enabled = False
                    # Get the color value 
                    color = getattr(context.scene, 'Color%d' % i)
                    vmv.interface.ui.options.morphology.color_map_colors.append(color)
        else:
            pass

    ################################################################################################
    # @draw_morphology_reconstruction_button
    ################################################################################################
    def draw_morphology_reconstruction_button(self,
                                              context):
        """Draw the morphology reconstruction button.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Mesh quick reconstruction options
        reconstruction_row = self.layout.row()
        reconstruction_row.label(text='Morphology Reconstruction:', icon='PARTICLE_POINT')

        # Morphology reconstruction options
        morphology_reconstruction_row = self.layout.row()
        morphology_reconstruction_row.operator('reconstruct.morphology', icon='MESH_DATA')

        # If the morphology is loaded only, print the performance stats.
        if vmv.interface.ui_morphology_loaded:

            # Stats
            morphology_stats_row = layout.row()
            morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')

            loading_time_row = layout.row()
            loading_time_row.prop(context.scene, 'MorphologyReconstructionTime')
            loading_time_row.enabled = False

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
        rendering_resolution_row.prop(context.scene, 'MorphologyRenderingResolution', expand=True)

        # Add the frame resolution option
        if context.scene.MorphologyRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Frame resolution option (only for the close up mode)
            frame_resolution_row = self.layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(context.scene, 'MorphologyFrameResolution')
            vmv.interface.ui.options.morphology.resolution_basis = \
                context.scene.MorphologyRenderingResolution

        # Otherwise, add the scale factor option
        else:

            # Scale factor option
            scale_factor_row = self.layout.row()
            scale_factor_row.label(text='Resolution Scale:')
            scale_factor_row.prop(context.scene, 'MorphologyFrameScaleFactor')
            vmv.interface.ui.options.morphology.resolution_scale_factor = \
                context.scene.MorphologyFrameScaleFactor

        # Rendering view column
        view_row = self.layout.column()
        view_row.prop(context.scene, 'MorphologyRenderingViews', icon='AXIS_FRONT')
        vmv.options.morphology.camera_view = context.scene.MorphologyRenderingViews

        # Rendering projection column only for a fixed resolution
        if context.scene.MorphologyRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Due to a bug in the workbench renderer in Blender, we will allow the
            # perspective projection for all the materials that use cycles and have high number of
            # samples per pixel, mainly the artistic rendering.
            if vmv.options.morphology.material in vmv.enums.Shader.SUB_SURFACE_SCATTERING:

                # Add the projection option
                projection_row = self.layout.column()
                projection_row.prop(context.scene, 'MorphologyCameraProjection', icon='AXIS_FRONT')
                vmv.options.morphology.camera_projection = \
                    context.scene.MorphologyCameraProjection

            # Set it by default to ORTHOGRAPHIC
            else:
                vmv.options.morphology.camera_projection = \
                    vmv.enums.Rendering.Projection.ORTHOGRAPHIC

        # Set it by default to ORTHOGRAPHIC
        else:
            vmv.options.morphology.camera_projection = \
                vmv.enums.Rendering.Projection.ORTHOGRAPHIC

        # Rendering button
        rendering_button_row = self.layout.column()
        rendering_button_row.operator('render_morphology.image', icon='MESH_DATA')

        # Render animation row
        render_animation_row = self.layout.row()
        render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
        render_animations_buttons_row = self.layout.row(align=True)
        render_animations_buttons_row.operator('render_morphology.360', icon='FORCE_MAGNETIC')

        # Rendering progress bar
        rendering_progress_row = self.layout.row()
        rendering_progress_row.prop(context.scene, 'MorphologyRenderingProgress')
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
        format_column.prop(context.scene, 'ExportedMeshFormat', icon='GROUP_VERTEX')
        format_column.operator('export.morphology', icon='MESH_DATA')

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # Draw the morphology reconstruction options
        self.draw_morphology_reconstruction_options(context=context)

        # Draw the morphology color options
        self.draw_morphology_color_options(context=context)

        # Draw the morphology reconstruction button
        self.draw_morphology_reconstruction_button(context=context)

        # Draw the morphology rendering options
        self.draw_morphology_rendering_options(context=context)

        # Draw the morphology export options
        self.draw_morphology_export_options(context=context)

        # If the morphology is loaded, enable the layout, otherwise make it disabled by default
        if vmv.interface.ui_morphology_loaded:
            self.layout.enabled = True
        else:
            self.layout.enabled = False


####################################################################################################
# @VMVReconstructMorphology
####################################################################################################
class VMVReconstructMorphology(bpy.types.Operator):
    """Reconstructs the mesh of the vasculature"""

    # Operator parameters
    bl_idname = "reconstruct.morphology"
    bl_label = "Reconstruct Morphology"
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
        if not vmv.interface.ui_morphology_loaded:
            print('ERROR: Morphology is not loaded')

        # Construct the skeleton builder
        # Disconnected segments builder
        if vmv.interface.ui.options.morphology.reconstruction_method == \
                vmv.enums.Morphology.ReconstructionMethod.DISCONNECTED_SEGMENTS:
            self.morphology_builder = vmv.builders.DisconnectedSegmentsBuilder(
                morphology=vmv.interface.ui.ui_morphology, options=vmv.interface.ui.options)

        # Disconnected sections builder
        elif vmv.interface.ui.options.morphology.reconstruction_method == \
                vmv.enums.Morphology.ReconstructionMethod.DISCONNECTED_SECTIONS:

            self.morphology_builder = vmv.builders.DisconnectedSectionsBuilder(
                morphology=vmv.interface.ui.ui_morphology,
                options=vmv.interface.ui.options)

        # Samples builder
        elif vmv.interface.ui.options.morphology.reconstruction_method == \
                vmv.enums.Morphology.ReconstructionMethod.SAMPLES:

            self.morphology_builder = vmv.builders.SamplesBuilder(
                morphology=vmv.interface.ui.ui_morphology,
                options=vmv.interface.ui.options)

        # Connected sections builder
        elif vmv.interface.ui.options.morphology.reconstruction_method == \
                vmv.enums.Morphology.ReconstructionMethod.CONNECTED_SECTIONS:
            self.morphology_builder = vmv.builders.ConnectedSectionsBuilder(
                morphology=vmv.interface.ui.ui_morphology, options=vmv.interface.ui.options)

        else:
            return {'FINISHED'}

        # Build the morphology skeleton directly
        # NOTE: each builder must have this function @build_skeleton() implemented in it
        vmv.interface.ui.morphology_skeleton = self.morphology_builder.build_skeleton(context=context)

        # Interpolations
        color_map_range = \
            float(context.scene.MaximumValue) - float(context.scene.MinimumValue)
        delta = color_map_range / float(vmv.consts.Color.NUMBER_COLORS_UI - 1)

        # Fill the list of colors
        for i in range(vmv.consts.Color.NUMBER_COLORS_UI):
            value = float(context.scene.MinimumValue) + (i * delta)
            setattr(context.scene, 'Value%d' % i, value)

        # Reconstruction timer
        reconstruction_done = time.time()
        context.scene.MorphologyReconstructionTime = reconstruction_done - start_reconstruction

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMVRenderMorphologyImage
####################################################################################################
class VMVRenderMorphologyImage(bpy.types.Operator):
    """Renders an image of the morphology of the vasculature"""

    # Operator parameters
    bl_idname = "render_morphology.image"
    bl_label = "Render Image"

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
        import vmv

        # Ensure that there is a valid directory where the images will be written to
        if vmv.interface.ui.options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.options.io.images_directory):
            vmv.file.ops.clean_and_create_directory(vmv.interface.options.io.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Rendering Morphology ... Wait Please')

        # Compute the bounding box for the available meshes only
        bounding_box = vmv.bbox.compute_scene_bounding_box_for_curves()

        # Image name
        image_name = 'MORPHOLOGY_%s_%s' % (vmv.interface.options.morphology.label,
                                           vmv.options.morphology.camera_view)

        # Stretch the bounding box by few microns
        rendering_bbox = copy.deepcopy(bounding_box)
        rendering_bbox.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Adding the illumination
        vmv.shading.create_material_specific_illumination(
            vmv.interface.options.morphology.material)

        # Render at a specific resolution
        if context.scene.MorphologyRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the morphology
            vmv.rendering.render(
                bounding_box=rendering_bbox,
                camera_view=vmv.options.morphology.camera_view,
                camera_projection=vmv.options.morphology.camera_projection,
                image_resolution=context.scene.MorphologyFrameResolution,
                image_name=image_name,
                image_directory=vmv.interface.options.io.images_directory)

        # Render at a specific scale factor
        else:

            # Render the morphology
            vmv.rendering.render_to_scale(
                bounding_box=rendering_bbox,
                camera_view=vmv.options.morphology.camera_view,
                image_scale_factor=context.scene.MorphologyFrameScaleFactor,
                image_name=image_name,
                image_directory=vmv.interface.options.io.images_directory)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Morphology Done')

        return {'FINISHED'}


####################################################################################################
# @VMVRenderMesh360
####################################################################################################
class VMVRenderMorphology360(bpy.types.Operator):
    """Render a 360 view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "render_morphology.360"
    bl_label = "Render 360"

    # Timer parameters
    event_timer = None
    timer_limits = 0

    # 360 bounding box
    bounding_box_360 = None

    # Output data
    output_directory = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):
        """
        Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

        # Get a reference to the scene
        scene = context.scene

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > 360:

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Set the frame name
            image_name = '%s/%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render at a specific resolution
            if context.scene.MorphologyRenderingResolution == \
                    vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

                # Render the image
                vmv.rendering.render_at_angle(
                    scene_objects=vmv.get_list_of_curves_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_resolution=context.scene.MorphologyFrameResolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                vmv.rendering.render_at_angle_to_scale(
                    scene_objects=vmv.get_list_of_curves_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_scale_factor=context.scene.MorphologyFrameResolution,
                    image_name=image_name)

            # Update the progress shell
            vmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.MorphologyRenderingProgress = int(100 * self.timer_limits / 360.0)

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self, context):
        """Execute the operator

        :param context:
            Panel context.
        """

        # Ensure that there is a valid directory where the images will be written to
        if vmv.interface.options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.options.io.sequences_directory):
            vmv.file.ops.clean_and_create_directory(
                vmv.interface.options.io.sequences_directory)

        # A reference to the bounding box that will be used for the rendering
        rendering_bbox = vmv.bbox.compute_scene_bounding_box_for_curves()

        # Compute a 360 bounding box to fit the arbors
        self.bounding_box_360 = vmv.bbox.compute_360_bounding_box(
            rendering_bbox, rendering_bbox.center)

        # Stretch the bounding box by few microns
        self.bounding_box_360.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_mesh_360' % (
            vmv.interface.options.io.sequences_directory,
            vmv.interface.options.morphology.label)
        vmv.file.ops.clean_and_create_directory(self.output_directory)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
        wm.modal_handler_add(self)

        # Done
        return {'RUNNING_MODAL'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self, context):
        """
        Cancel the panel processing and return to the interaction mode.

        :param context: Panel context.
        """

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Morphology Rendering Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @VMVReconstructMesh
####################################################################################################
class VMVExportMorphology(bpy.types.Operator):
    """Export the reconstructed mesh to a file"""

    # Operator parameters
    bl_idname = "export.morphology"
    bl_label = "Export"

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
        meshing_technique = vmv.interface.options.mesh.meshing_technique

        # Piece-wise watertight meshing
        if meshing_technique == vmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT:

            # Create the mesh builder
            mesh_builder = vmv.builders.PiecewiseBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Bridging
        elif meshing_technique == vmv.enums.Meshing.Technique.BRIDGING:

            # Create the mesh builder
            mesh_builder = vmv.builders.BridgingBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Union
        elif meshing_technique == vmv.enums.Meshing.Technique.UNION:

            # Create the mesh builder
            mesh_builder = vmv.builders.UnionBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        # Extrusion
        elif meshing_technique == vmv.enums.Meshing.Technique.EXTRUSION:

            # Create the mesh builder
            mesh_builder = vmv.builders.ExtrusionBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        elif meshing_technique == vmv.enums.Meshing.Technique.SKINNING:

            # Create the mesh builder
            mesh_builder = vmv.builders.SkinningBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.options)

            # Reconstruct the mesh
            vmv.interface.ui_reconstructed_mesh = mesh_builder.reconstruct_mesh()

        elif meshing_technique == vmv.enums.Meshing.Technique.META_OBJECTS:

            # Create the mesh builder
            mesh_builder = vmv.builders.MetaBuilder(
                morphology=vmv.interface.ui_morphology, options=vmv.interface.options)

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

    # ColorMap 
    bpy.utils.register_class(VMVColorMapOperator)

    # Panel
    bpy.utils.register_class(VMVMorphologyPanel)

    # Mesh reconstruction button
    bpy.utils.register_class(VMVReconstructMorphology)

    # Mesh rendering buttons
    bpy.utils.register_class(VMVRenderMorphologyImage)
    bpy.utils.register_class(VMVRenderMorphology360)

    # Mesh export button
    bpy.utils.register_class(VMVExportMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # ColorMap 
    bpy.utils.unregister_class(VMVColorMapOperator)

    # Panel
    bpy.utils.unregister_class(VMVMorphologyPanel)

    # Mesh reconstruction button
    bpy.utils.unregister_class(VMVReconstructMorphology)

    # Mesh rendering buttons
    bpy.utils.unregister_class(VMVRenderMorphologyImage)
    bpy.utils.unregister_class(VMVRenderMorphology360)

    # Mesh export button
    bpy.utils.unregister_class(VMVExportMorphology)
