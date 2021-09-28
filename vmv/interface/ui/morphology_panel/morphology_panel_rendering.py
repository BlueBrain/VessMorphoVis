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

# System imports
import math

# Blender imports
import bpy
import copy

# Internal imports
import vmv.bbox
import vmv.builders
import vmv.interface
import vmv.rendering
import vmv.utilities


####################################################################################################
# @VMV_RenderMorphologyImage
####################################################################################################
class VMV_RenderMorphologyImage(bpy.types.Operator):
    """Renders an image of the morphology of the vasculature"""

    # Operator parameters
    bl_idname = 'render_morphology.image'
    bl_label = 'Render Image'

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
        if vmv.interface.Options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.VMV_OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the images directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.Options.io.images_directory):
            vmv.file.ops.clean_and_create_directory(vmv.interface.Options.io.images_directory)

        # Report the process starting in the UI
        self.report({'INFO'}, 'Rendering Morphology ... Wait Please')

        # Compute the bounding box for the available meshes only
        bounding_box = vmv.bbox.compute_scene_bounding_box_for_curves()

        # Image name
        image_name = 'MORPHOLOGY_%s_%s' % (vmv.interface.Options.morphology.label,
                                           vmv.Options.morphology.camera_view)

        # Stretch the bounding box by few microns
        rendering_bbox = copy.deepcopy(bounding_box)
        rendering_bbox.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Adding the illumination
        vmv.shading.create_material_specific_illumination(
            vmv.interface.Options.morphology.material)

        # Draw the morphology scale bar
        if context.scene.VMV_RenderMorphologyScaleBar:
            scale_bar = vmv.interface.draw_scale_bar(
                bounding_box=bounding_box,
                material_type=vmv.interface.Options.morphology.material,
                view=vmv.Options.morphology.camera_view)

        # Render at a specific resolution
        if context.scene.VMV_MorphologyRenderingResolution == \
                vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

            # Render the morphology
            vmv.rendering.render(
                bounding_box=rendering_bbox,
                camera_view=vmv.Options.morphology.camera_view,
                camera_projection=vmv.Options.morphology.camera_projection,
                image_resolution=context.scene.VMV_MorphologyImageResolution,
                image_name=image_name,
                image_directory=vmv.interface.Options.io.images_directory,
                add_background_plane=not vmv.Options.morphology.transparent_background)

        # Render at a specific scale factor
        else:

            # Render the morphology
            vmv.rendering.render_to_scale(
                bounding_box=rendering_bbox,
                camera_view=vmv.Options.morphology.camera_view,
                image_scale_factor=context.scene.VMV_MorphologyImageScaleFactor,
                image_name=image_name,
                image_directory=vmv.interface.Options.io.images_directory,
                add_background_plane=not vmv.Options.morphology.transparent_background)

        # Delete the morphology scale bar, if rendered
        if context.scene.VMV_RenderMorphologyScaleBar:
            vmv.scene.delete_object_in_scene(scene_object=scale_bar)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Morphology Done')

        return {'FINISHED'}


####################################################################################################
# @VMV_RenderMorphology360
####################################################################################################
class VMV_RenderMorphology360(bpy.types.Operator):
    """Render a 360 view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = 'render_morphology.360'
    bl_label = 'Render 360'

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
            if context.scene.VMV_MorphologyRenderingResolution == \
                    vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

                # Render the image
                vmv.rendering.render_at_angle(
                    scene_objects=vmv.get_list_of_curves_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_resolution=context.scene.VMV_MorphologyImageResolution,
                    image_name=image_name,
                    add_background_plane=not vmv.Options.morphology.transparent_background)

            # Render at a specific scale factor
            else:

                # Render the image
                vmv.rendering.render_at_angle_to_scale(
                    scene_objects=vmv.get_list_of_curves_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_scale_factor=context.scene.VMV_MorphologyImageResolution,
                    image_name=image_name,
                    add_background_plane=not vmv.Options.morphology.transparent_background)

            # Update the progress shell
            vmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.VMV_MorphologyRenderingProgress = int(100 * self.timer_limits / 360.0)

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
        if vmv.interface.Options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.VMV_OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.Options.io.sequences_directory):
            vmv.file.ops.clean_and_create_directory(
                vmv.interface.Options.io.sequences_directory)

        # A reference to the bounding box that will be used for the rendering
        rendering_bbox = vmv.bbox.compute_scene_bounding_box_for_curves()

        # Compute a 360 bounding box to fit the arbors
        self.bounding_box_360 = vmv.bbox.compute_360_bounding_box(
            rendering_bbox, rendering_bbox.center)

        # Stretch the bounding box by few microns
        self.bounding_box_360.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_mesh_360' % (
            vmv.interface.Options.io.sequences_directory,
            vmv.interface.Options.morphology.label)
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
# @VMV_RenderSimulation
####################################################################################################
class VMV_RenderSimulation(bpy.types.Operator):
    """Renders a sequence of the simulation data, frame by frame"""

    # Operator parameters
    bl_idname = 'render.simulation'
    bl_label = 'Render Simulation'

    # Timer parameters
    event_timer = None
    timer_limits = 0

    # 360 bounding box
    bounding_box = None

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
        if event.type in {'ESC'} or self.timer_limits > bpy.context.scene.VMV_LastSimulationFrame:

            # Reset the timer limits
            self.timer_limits = 0

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            bpy.context.scene.frame_current = self.timer_limits

            # Draw the morphology scale bar
            if context.scene.VMV_RenderMorphologyScaleBar:
                scale_bar = vmv.interface.draw_scale_bar(
                    bounding_box=self.bounding_box,
                    material_type=vmv.interface.Options.morphology.material,
                    view=vmv.Options.morphology.camera_view)

            # Render at a specific resolution
            if context.scene.VMV_MorphologyRenderingResolution == \
                    vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

                # Render the morphology
                vmv.rendering.render(
                    bounding_box=self.bounding_box,
                    camera_view=vmv.Options.morphology.camera_view,
                    camera_projection=vmv.Options.morphology.camera_projection,
                    image_resolution=context.scene.VMV_MorphologyImageResolution,
                    image_name='{0:05d}'.format(self.timer_limits),
                    image_directory=self.output_directory)

            # Render at a specific scale factor
            else:

                # Render the morphology
                vmv.rendering.render_to_scale(
                    bounding_box=self.bounding_box,
                    camera_view=vmv.Options.morphology.camera_view,
                    image_scale_factor=context.scene.VMV_MorphologyImageScaleFactor,
                    image_name='{0:05d}'.format(self.timer_limits),
                    image_directory=self.output_directory)

            # Delete the morphology scale bar, if rendered
            if context.scene.VMV_RenderMorphologyScaleBar:
                vmv.scene.delete_object_in_scene(scene_object=scale_bar)

            # Update the progress shell
            vmv.utilities.show_progress('Rendering', self.timer_limits,
                                        context.scene.VMV_LastSimulationFrame)

            # Update the progress bar
            context.scene.VMV_MorphologyRenderingProgress = \
                math.ceil(int(100.0 * self.timer_limits / context.scene.VMV_LastSimulationFrame))

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
        if vmv.interface.Options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.VMV_OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Create the sequences directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.Options.io.sequences_directory):
            vmv.file.ops.clean_and_create_directory(
                vmv.interface.Options.io.sequences_directory)

        # A reference to the bounding box that will be used for the rendering
        self.bounding_box = vmv.bbox.compute_scene_bounding_box_for_curves()

        # Stretch the bounding box by few microns
        self.bounding_box.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_simulation' % (
            vmv.interface.Options.io.sequences_directory,
            vmv.interface.Options.morphology.label)
        vmv.file.ops.clean_and_create_directory(self.output_directory)

        # Use the event timer to update the UI
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