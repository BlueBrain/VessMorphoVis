####################################################################################################
# Copyright (c) 2021, EPFL / Blue Brain Project
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

# Internal imports
import vmv.builders
import vmv.interface


####################################################################################################
# @VMV_LoadSimulation
####################################################################################################
class VMV_LoadSimulation(bpy.types.Operator):
    """Loads the simulation data and apply them on the morphology skeleton"""

    # Operator parameters
    bl_idname = 'load.simulation'
    bl_label = 'Load Simulation'

    # Timer parameters
    event_timer = None
    frame = 0

    # The simulation cannot be displayed without re-building the morphology polyline object
    morphology_builder = None

    # The reconstructed morphology polyline object that will be used to display the simulation data
    morphology_object_polyline = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'ESC'} or self.frame > context.scene.VMV_LastSimulationFrame:

            # Reset the frame to the first one
            self.frame = 0

            # Update the time line frame to the first one
            bpy.context.scene.frame_set(0)

            # Update the current simulation frame to the first one
            context.scene.VMV_CurrentSimulationFrame = 0

            # Refresh the panel context
            self.cancel(context)

            # Update the SimulationLoaded flag to update the UI
            vmv.interface.SimulationLoaded = True

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Update the frame in the time line
            bpy.context.scene.frame_current = self.frame

            # Load the simulation data on a per-frame basis
            self.morphology_builder.load_radius_simulation_data_at_step(self.frame)

            # Update the progress bar
            context.scene.VMV_SimulationProgressBar = \
                math.ceil(int(100.0 * self.frame / context.scene.VMV_LastSimulationFrame))

            # Update the current simulation frame
            context.scene.VMV_CurrentSimulationFrame = self.frame

            # Upgrade the time step
            self.frame += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Executes the operator.

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Construct the morphology builder
        # TODO: Depending on the simulation type
        self.morphology_builder = vmv.builders.SectionsBuilder(
            morphology=vmv.interface.MorphologyObject, options=vmv.interface.Options)

        # Construct the polyline object
        self.morphology_object_polyline = self.morphology_builder.build_skeleton(context=context)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        self.event_timer = wm.event_timer_add(time_step=0.001, window=context.window)
        wm.modal_handler_add(self)

        # Update the last simulation frame
        # TODO: Depending on the simulation type
        if vmv.interface.MorphologyObject.has_radius_simulation:
            context.scene.VMV_LastSimulationFrame = \
                len(vmv.interface.MorphologyObject.radius_simulation_data[0]) - 1

        # Done
        return {'RUNNING_MODAL'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self,
               context):
        """
        Cancel the panel processing and return to the interaction mode.

        :param context:
            Panel context.
        """

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Simulation Loading Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_PlaySimulation(bpy.types.Operator):
    """Runs, pauses and stops the simulation"""

    # Operator parameters
    bl_idname = 'play.simulation'
    bl_label = ''

    # Timer parameters
    event_timer = None
    frame = 0

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self, context, event):
        """Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

        # Cancelling event, if the ESC button is pressed
        if event.type in {'ESC'}:

            # Reset the frame to the first one
            self.frame = 0

            # Update the time line frame to the first one
            bpy.context.scene.frame_set(0)

            # Update the current simulation frame to the first one
            context.scene.VMV_CurrentSimulationFrame = 0

            # Cancel the context to update the panel
            self.cancel(context)

            # Switch the button to PLAY
            bpy.types.Scene.VMV_PlayPauseButtonIcon = 'PLAY'

            # Done
            return {'FINISHED'}

        # Restart
        if context.scene.VMV_CurrentSimulationFrame >= context.scene.VMV_LastSimulationFrame:

            # Reset the frame to the first one
            self.frame = 0

            # Update the time line frame to the first one
            bpy.context.scene.frame_set(0)

            # Update the current simulation frame to the first one
            context.scene.VMV_CurrentSimulationFrame = 0

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # If the simulation is not running
            if not bpy.types.Scene.VMV_IsSimulationRunning:

                # Update the current frame in the time line
                bpy.context.scene.frame_current = context.scene.VMV_CurrentSimulationFrame

                # Switch the button to PLAY
                bpy.types.Scene.VMV_PlayPauseButtonIcon = 'PLAY'

                # Cancel the context
                self.cancel(context)
                wm = context.window_manager
                wm.event_timer_remove(self.event_timer)

                # Return
                return {'FINISHED'}

            # Update the current frame
            bpy.context.scene.frame_current = context.scene.VMV_CurrentSimulationFrame

            # Update the progress bar
            context.scene.VMV_SimulationProgressBar = \
                math.ceil(int(100.0 * self.frame / context.scene.VMV_LastSimulationFrame))

            # Update the frame
            self.frame = context.scene.VMV_CurrentSimulationFrame

            # Next frame
            context.scene.VMV_CurrentSimulationFrame += 1

        # Next frame
        return {'PASS_THROUGH'}

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

        # If the simulation is not running, i.e. the button was still PLAY
        if not bpy.types.Scene.VMV_IsSimulationRunning:

            # Use the event timer to update the UI during the soma building
            wm = context.window_manager
            self.event_timer = wm.event_timer_add(time_step=0.001, window=context.window)
            wm.modal_handler_add(self)

            # Switch the button to PAUSE
            bpy.types.Scene.VMV_PlayPauseButtonIcon = 'PAUSE'

            # The simulation should RUN
            bpy.types.Scene.VMV_IsSimulationRunning = True

        # If the simulation is already running, i.e the button was PAUSE
        else:

            # The simulation should PAUSE
            bpy.types.Scene.VMV_IsSimulationRunning = False

        # Go into the MODAL mode
        return {'RUNNING_MODAL'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self, context):
        """
        Cancel the panel processing and return to the interaction mode.

        :param context:
            Panel context.
        """

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_SimulationNextFrame(bpy.types.Operator):
    """Plays the next frame of the simulation"""

    # Operator parameters
    bl_idname = 'play_next_frame.simulation'
    bl_label = ''

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

        # Set the timeline to the initial frame
        if bpy.context.scene.frame_current < context.scene.VMV_LastSimulationFrame:

            # Update the frame
            bpy.context.scene.frame_set(bpy.context.scene.frame_current + 1)

            # Update the text box
            context.scene.VMV_CurrentSimulationFrame = bpy.context.scene.frame_current

            # Update the progress bar
            context.scene.VMV_SimulationProgressBar = math.ceil(int(
                100.0 * context.scene.VMV_CurrentSimulationFrame /
                context.scene.VMV_LastSimulationFrame))

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_SimulationPreviousFrame(bpy.types.Operator):
    """Plays the previous frame of the simulation"""

    # Operator parameters
    bl_idname = 'play_previous_frame.simulation'
    bl_label = ''

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

        # Set the timeline to the initial frame
        if bpy.context.scene.frame_current > 0:

            # Update the frame
            bpy.context.scene.frame_set(bpy.context.scene.frame_current - 1)

            # Update the text box
            context.scene.VMV_CurrentSimulationFrame = bpy.context.scene.frame_current

            # Update the progress bar
            context.scene.VMV_SimulationProgressBar = math.ceil(int(
                100.0 * context.scene.VMV_CurrentSimulationFrame /
                context.scene.VMV_LastSimulationFrame))

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_SimulationFirstFrame(bpy.types.Operator):
    """Plays the first frame of the simulation"""

    # Operator parameters
    bl_idname = 'play_first_frame.simulation'
    bl_label = ''

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

        # Set the timeline to the initial frame
        bpy.context.scene.frame_set(0)

        # Update the text box
        context.scene.VMV_CurrentSimulationFrame = 0

        # Update the progress bar
        context.scene.VMV_SimulationProgressBar = 0

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_SimulationLastFrame(bpy.types.Operator):
    """Plays the last frame of the simulation"""

    # Operator parameters
    bl_idname = 'play_last_frame.simulation'
    bl_label = ''

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

        # Set the timeline to the final frame
        bpy.context.scene.frame_set(context.scene.VMV_LastSimulationFrame)

        # Update the text box
        context.scene.VMV_CurrentSimulationFrame = context.scene.VMV_LastSimulationFrame

        # Update the progress bar
        context.scene.VMV_SimulationProgressBar = 100

        # Done, return {'FINISHED'}
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
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                vmv.rendering.render_at_angle_to_scale(
                    scene_objects=vmv.get_list_of_curves_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_scale_factor=context.scene.VMV_MorphologyImageResolution,
                    image_name=image_name)

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