####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import time
import copy

# Blender imports
import bpy

# Internal imports
import vmv
import vmv.bbox
import vmv.builders
import vmv.consts
import vmv.enums
import vmv.file
import vmv.skeleton
import vmv.interface
import vmv.utilities
import vmv.rendering


####################################################################################################
# @VMVMeshingPanel
####################################################################################################
class VMVMeshingPanel(bpy.types.Panel):
    """The meshing panel of VMV"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_label = 'Meshing'
    bl_idname = "OBJECT_PT_Meshing"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'VessMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw_mesh_reconstruction_options
    ################################################################################################
    def draw_mesh_reconstruction_options(self,
                                         context):
        """Draws the mesh reconstruction options on the meshing panel.

        :param context:
            Context.
        """
        # Skeleton meshing options
        skeleton_meshing_options_row = self.layout.row()
        skeleton_meshing_options_row.label(text='Meshing Options:', icon='SURFACE_DATA')

        # Which meshing technique to use
        meshing_method_row = self.layout.row()
        meshing_method_row.prop(context.scene, 'MeshingTechnique', icon='OUTLINER_OB_EMPTY')

        # Auto meta-ball resolution
        meta_auto_resolution_row = self.layout.row()
        meta_auto_resolution_row.prop(context.scene, 'MetaBallAutoResolution',
                                      icon='OUTLINER_OB_EMPTY')
        vmv.ui_options.mesh.meta_auto_resolution = context.scene.MetaBallAutoResolution

        # Meta-ball resolution
        meta_resolution_row = self.layout.row()
        meta_resolution_row.prop(context.scene, 'MetaBallResolution', icon='OUTLINER_OB_EMPTY')
        vmv.ui_options.mesh.meta_resolution = context.scene.MetaBallResolution

        # Tessellation parameters
        tess_level_row = self.layout.row()
        tess_level_row.prop(context.scene, 'TessellateMesh')
        tess_level_column = tess_level_row.column()
        tess_level_column.prop(context.scene, 'MeshTessellationLevel')

        if not context.scene.TessellateMesh:
            # Use 1.0 to disable the tessellation
            vmv.interface.ui_options.mesh.tessellate_mesh = False
            vmv.interface.ui_options.mesh.tessellation_level = 1.0
            tess_level_column.enabled = False
        else:
            vmv.interface.ui_options.mesh.tessellate_mesh = context.scene.TessellateMesh
            vmv.interface.ui_options.mesh.tessellation_level = context.scene.MeshTessellationLevel

        # Disable the resolution box if the auto resolution is set on
        if context.scene.MetaBallAutoResolution:
            meta_resolution_row.enabled = False
        else:
            meta_resolution_row.enabled = True

    ################################################################################################
    # @draw_mesh_color_options
    ################################################################################################
    def draw_mesh_color_options(self, context):
        """Draw the coloring options on the meshing panel.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Coloring parameters
        colors_row = layout.row()
        colors_row.label(text='Colors & Materials:', icon='COLOR')

        # Mesh material
        mesh_material_row = layout.row()
        mesh_material_row.prop(context.scene, 'MeshMaterial')
        vmv.ui_options.mesh.material = context.scene.MeshMaterial

        # Homogeneous mesh coloring
        homogeneous_color_row = layout.row()
        homogeneous_color_row.prop(context.scene, 'MeshColor')
        vmv.ui_options.mesh.color = context.scene.MeshColor

    ################################################################################################
    # @draw_mesh_reconstruction_button
    ################################################################################################
    def draw_mesh_reconstruction_button(self,
                                        context):
        """Draw the mesh reconstruction button on the meshing panel.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Mesh quick reconstruction options
        quick_reconstruction_row = layout.row()
        quick_reconstruction_row.label(text='Mesh Reconstruction:', icon='PARTICLE_POINT')

        # Mesh reconstruction options
        mesh_reconstruction_row = layout.row()
        mesh_reconstruction_row.operator('reconstruct.mesh', icon='MESH_DATA')

        # If the morphology is loaded only, print the performance stats.
        if vmv.interface.ui_morphology_loaded:

            # Stats
            meshing_stats_row = layout.row()
            meshing_stats_row.label(text='Stats:', icon='RECOVER_LAST')

            reconstruction_time_row = layout.row()
            reconstruction_time_row.prop(context.scene, 'MeshReconstructionTime')
            reconstruction_time_row.enabled = False

    ################################################################################################
    # @draw_mesh_rendering_options
    ################################################################################################
    def draw_mesh_rendering_options(self,
                                    context):
        """Draw the rendering options.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Rendering options
        rendering_row = layout.row()
        rendering_row.label(text='Rendering Options:', icon='RENDER_STILL')

        # Rendering resolution
        rendering_resolution_row = layout.row()
        rendering_resolution_row.label(text='Resolution:')
        rendering_resolution_row.prop(context.scene, 'MeshRenderingResolution', expand=True)

        # Add the frame resolution option
        if context.scene.MeshRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Frame resolution option (only for the close up mode)
            frame_resolution_row = layout.row()
            frame_resolution_row.label(text='Frame Resolution:')
            frame_resolution_row.prop(context.scene, 'MeshFrameResolution')
            frame_resolution_row.enabled = True

        # Otherwise, add the scale factor option
        else:

            # Scale factor option
            scale_factor_row = layout.row()
            scale_factor_row.label(text='Resolution Scale:')
            scale_factor_row.prop(context.scene, 'MeshFrameScaleFactor')
            scale_factor_row.enabled = True

        # Rendering view column
        view_row = layout.column()
        view_row.prop(context.scene, 'MeshRenderingView', icon='AXIS_FRONT')
        vmv.ui_options.mesh.camera_view = context.scene.MeshRenderingView

        # Rendering projection column only for a fixed resolution
        if context.scene.MeshRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Due to a bug in the workbench renderer in Blender, we will allow the
            # perspective projection for all the materials that use cycles and have high number of
            # samples per pixel, mainly the artistic rendering.
            if vmv.ui_options.mesh.material in vmv.enums.Shading.ARTISTIC_MATERIALS:

                # Add the projection option
                projection_row = self.layout.column()
                projection_row.prop(context.scene, 'MeshCameraProjection', icon='AXIS_FRONT')
                vmv.ui_options.mesh.camera_projection = \
                    context.scene.MeshCameraProjection

            # Set it by default to ORTHOGRAPHIC
            else:
                vmv.ui_options.mesh.camera_projection = \
                    vmv.enums.Rendering.Projection.ORTHOGRAPHIC

        # Set it by default to ORTHOGRAPHIC
        else:
            vmv.ui_options.mesh.camera_projection = \
                vmv.enums.Rendering.Projection.ORTHOGRAPHIC

        # Render still images button
        mesh_still_image_rendering = layout.row()
        mesh_still_image_rendering.operator('render_mesh.image', icon='MESH_DATA')

        # Render animation row
        render_animation_row = layout.row()
        render_animation_row.label(text='Render Animation:', icon='CAMERA_DATA')
        render_animations_buttons_row = layout.row(align=True)
        render_animations_buttons_row.operator('render_mesh.360', icon='FORCE_MAGNETIC')
        render_animations_buttons_row.enabled = True

        # Rendering progress bar
        neuron_mesh_rendering_progress_row = layout.row()
        neuron_mesh_rendering_progress_row.prop(context.scene, 'MeshRenderingProgress')
        neuron_mesh_rendering_progress_row.enabled = False

    ################################################################################################
    # @draw_mesh_export_options
    ################################################################################################
    def draw_mesh_export_options(self,
                                 context):
        """Draw the mesh export button.

        :param context:
            Context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Saving meshes parameters
        save_mesh_row = layout.row()
        save_mesh_row.label(text='Export Mesh As:', icon='MESH_UVSPHERE')

        # Exported format column
        format_column = layout.column()
        format_column.prop(context.scene, 'ExportedMeshFormat', icon='GROUP_VERTEX')
        format_column.operator('export.mesh', icon='MESH_DATA')

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # Get a reference to the layout of the panel
        layout = self.layout

        # Draw the mesh reconstruction options
        self.draw_mesh_reconstruction_options(context=context)

        # Draw the mesh coloring options
        self.draw_mesh_color_options(context=context)

        # Draw the mesh reconstruction button
        self.draw_mesh_reconstruction_button(context=context)

        # Draw the mesh rendering options
        self.draw_mesh_rendering_options(context=context)

        # Draw the mesh export options
        self.draw_mesh_export_options(context=context)

        # If the morphology is loaded, enable the layout, otherwise make it disabled by default
        if vmv.interface.ui_morphology_loaded:
            self.layout.enabled = True
        else:
            self.layout.enabled = False


####################################################################################################
# @VMVReconstructMesh
####################################################################################################
class VMVReconstructMesh(bpy.types.Operator):
    """Reconstructs the mesh of the vasculature"""

    # Operator parameters
    bl_idname = "reconstruct.mesh"
    bl_label = "Reconstruct Mesh"

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
        vmv.scene.clear_scene()

        # Starting timer
        start_reconstruction = time.time()

        # Meta builder
        if context.scene.MeshingTechnique == vmv.enums.Meshing.Technique.META_BALLS:
            builder = vmv.builders.MetaBuilder(morphology=vmv.interface.ui.ui_morphology,
                                               options=vmv.interface.ui.ui_options)

        # Skinning
        elif context.scene.MeshingTechnique == vmv.enums.Meshing.Technique.SKINNING:
            builder = vmv.builders.SkinningBuilder(morphology=vmv.interface.ui.ui_morphology,
                                                   options=vmv.interface.ui.ui_options)

        # Using the piece-wise
        else:
            builder = vmv.builders.PiecewiseWatertightBuilder(
                morphology=vmv.interface.ui.ui_morphology, options=vmv.interface.ui.ui_options)

        # Build the vasculature mesh
        builder.build()

        # Update the interface with some parameters
        context.scene.MetaBallResolution = vmv.interface.ui_options.mesh.meta_resolution

        # Reconstruction done
        reconstruction_done = time.time()
        context.scene.MeshReconstructionTime = reconstruction_done - start_reconstruction

        # Done
        return {'FINISHED'}


####################################################################################################
# @VMVRenderMeshImage
####################################################################################################
class VMVRenderMeshImage(bpy.types.Operator):
    """Renders the mesh of the vasculature"""

    # Operator parameters
    bl_idname = "render_mesh.image"
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

        # Ensure that there is a valid directory where the images will be written to
        if vmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.ui_options.io.images_directory):
            vmv.file.ops.clean_and_create_directory(vmv.interface.ui_options.io.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Rendering Mesh ... Wait Please')

        # Compute the bounding box for the available meshes only
        bounding_box = vmv.bbox.compute_scene_bounding_box_for_meshes()

        # Image name
        image_name = 'MESH_%s_%s' % (vmv.interface.ui_options.morphology.label,
                                     vmv.ui_options.mesh.camera_view)

        # Stretch the bounding box by few microns
        rendering_bbox = copy.deepcopy(bounding_box)
        rendering_bbox.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Adding the illumination
        vmv.shading.create_material_specific_illumination(
            vmv.interface.ui_options.mesh.material)

        # Render at a specific resolution
        if context.scene.MeshRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the morphology
            vmv.rendering.render(
                bounding_box=rendering_bbox,
                camera_view=vmv.ui_options.mesh.camera_view,
                camera_projection=vmv.ui_options.mesh.camera_projection,
                image_resolution=context.scene.MeshFrameResolution,
                image_name=image_name,
                image_directory=vmv.interface.ui_options.io.images_directory)

        # Render at a specific scale factor
        else:

            # Render the morphology
            vmv.rendering.render_to_scale(
                bounding_box=rendering_bbox,
                camera_view=vmv.ui_options.mesh.camera_view,
                image_scale_factor=context.scene.MeshFrameScaleFactor,
                image_name=image_name,
                image_directory=vmv.interface.ui_options.io.images_directory)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Morphology Done')

        # Done
        return {'FINISHED'}


####################################################################################################
# @VMVRenderMesh360
####################################################################################################
class VMVRenderMesh360(bpy.types.Operator):
    """Render a 360 view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "render_mesh.360"
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

        :param context: Panel context.
        :param event: A given event for the panel.
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
            if context.scene.MeshRenderingResolution == \
                    vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

                # Render the image
                vmv.rendering.render_at_angle(
                    scene_objects=vmv.get_list_of_meshes_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_resolution=context.scene.MeshFrameResolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                vmv.rendering.render_at_angle_to_scale(
                    scene_objects=vmv.get_list_of_meshes_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_scale_factor=context.scene.MeshFrameScaleFactor,
                    image_name=image_name)

            # Update the progress shell
            vmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.MeshRenderingProgress = int(100 * self.timer_limits / 360.0)

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
        if vmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.ui_options.io.sequences_directory):
            vmv.file.ops.clean_and_create_directory(
                vmv.interface.ui_options.io.sequences_directory)

        # A reference to the bounding box that will be used for the rendering
        rendering_bbox = vmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute a 360 bounding box to fit the arbors
        self.bounding_box_360 = vmv.bbox.compute_360_bounding_box(
            rendering_bbox, rendering_bbox.center)

        # Stretch the bounding box by few microns
        self.bounding_box_360.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_mesh_360' % (
            vmv.interface.ui_options.io.sequences_directory,
            vmv.interface.ui.ui_morphology.name)
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
        """Cancel the panel processing and return to the interaction mode.

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
class VMVExportMesh(bpy.types.Operator):
    """Export the reconstructed mesh to a file"""

    # Operator parameters
    bl_idname = "export.mesh"
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

        # Ensure that there is a valid directory where the images will be written to
        if vmv.interface.ui_options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.ui_options.io.meshes_directory):
            vmv.file.ops.clean_and_create_directory(
                vmv.interface.ui_options.io.meshes_directory)

        # Select the mesh object to be exported
        mesh_object = vmv.scene.select_object_containing_string(vmv.consts.Meshing.MESH_SUFFIX)

        # Export the mesh
        vmv.file.export_mesh_object(mesh_object=mesh_object,
                                    output_directory=vmv.interface.ui_options.io.meshes_directory,
                                    file_name='Test',
                                    file_format=context.scene.ExportedMeshFormat)

        # Done
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(VMVMeshingPanel)

    # Mesh reconstruction button
    bpy.utils.register_class(VMVReconstructMesh)

    # Mesh rendering buttons
    bpy.utils.register_class(VMVRenderMeshImage)
    bpy.utils.register_class(VMVRenderMesh360)

    # Mesh export button
    bpy.utils.register_class(VMVExportMesh)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(VMVMeshingPanel)

    # Mesh reconstruction button
    bpy.utils.unregister_class(VMVReconstructMesh)

    # Mesh rendering buttons
    bpy.utils.unregister_class(VMVRenderMeshImage)
    bpy.utils.unregister_class(VMVRenderMesh360)

    # Mesh export button
    bpy.utils.unregister_class(VMVExportMesh)
