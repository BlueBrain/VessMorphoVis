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
import vmv.enums
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

            # Interpolations
            scale = float(context.scene.VMV_MaximumValue) - float(context.scene.VMV_MinimumValue)
            delta = scale / float(vmv.consts.Color.COLORMAP_RESOLUTION)

            # Fill the list of colors
            for color_index in range(vmv.consts.Color.COLORMAP_RESOLUTION):
                r0_value = float(context.scene.VMV_MinimumValue) + (color_index * delta)
                r1_value = float(context.scene.VMV_MinimumValue) + ((color_index + 1) * delta)
                print(r0_value, r1_value)
                setattr(context.scene, 'VMV_R0_Value%d' % color_index, r0_value)
                setattr(context.scene, 'VMV_R1_Value%d' % color_index, r1_value)

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
            self.morphology_builder.load_radius_simulation_data_at_step(self.frame, context=context)

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

        # A simple reference
        visualization_type = vmv.interface.Options.morphology.visualization_type

        # Construct the morphology builder based on the simulation type
        if visualization_type == vmv.enums.Morphology.Visualization.RADII_STRUCTURAL_DYNAMICS:

            # A sections builder will be used to show variations in structure with respect to time
            self.morphology_builder = vmv.builders.SectionsBuilder(
                morphology=vmv.interface.MorphologyObject, options=vmv.interface.Options)
        else:

            # A segments builder will be used to show functional variations with color map
            self.morphology_builder = vmv.builders.SegmentsBuilder(
                morphology=vmv.interface.MorphologyObject, options=vmv.interface.Options)

        # Construct the polyline object with dynamic colormap

        if visualization_type == vmv.enums.Morphology.Visualization.RADII_COLORMAP or \
           visualization_type == vmv.enums.Morphology.Visualization.FLOW_COLORMAP or \
           visualization_type == vmv.enums.Morphology.Visualization.PRESSURE_COLORMAP:
            self.morphology_object_polyline = self.morphology_builder.build_skeleton(
                context=context, dynamic_colormap=True)
        else:
            self.morphology_object_polyline = self.morphology_builder.build_skeleton(
                context=context)

        # Simulation dynamic range
        if visualization_type == vmv.enums.Morphology.Visualization.RADII_STRUCTURAL_DYNAMICS:
            pass
        elif visualization_type == vmv.enums.Morphology.Visualization.RADII_COLORMAP:
            self.morphology_builder.identify_radius_simulation_dynamic_range()
        elif visualization_type == vmv.enums.Morphology.Visualization.FLOW_COLORMAP:
            self.morphology_builder.identify_flow_simulation_dynamic_range()
        elif visualization_type == vmv.enums.Morphology.Visualization.FLOW_COLORMAP:
            self.morphology_builder.identify_pressure_simulation_dynamic_range()
        else:
            pass

        # Update the last simulation frame
        # TODO: Depending on the simulation type
        if vmv.interface.MorphologyObject.has_radius_simulation:
            context.scene.VMV_LastSimulationFrame = \
                len(vmv.interface.MorphologyObject.radius_simulation_data[0]) - 1

        # NOTE: Make sure you pass the current polyline object to the global reference to be able
        # to control it while updating certain UI elements
        vmv.interface.MorphologyPolylineObject = self.morphology_object_polyline

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        self.event_timer = wm.event_timer_add(time_step=0.001, window=context.window)
        wm.modal_handler_add(self)

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
            if not vmv.interface.SimulationRunning:

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
        if not vmv.interface.SimulationRunning:

            # Use the event timer to update the UI during the soma building
            wm = context.window_manager
            self.event_timer = wm.event_timer_add(time_step=0.001, window=context.window)
            wm.modal_handler_add(self)

            # Switch the button to PAUSE
            bpy.types.Scene.VMV_PlayPauseButtonIcon = 'PAUSE'

            # The simulation should RUN
            vmv.interface.SimulationRunning = True

        # If the simulation is already running, i.e the button was PAUSE
        else:

            # The simulation should PAUSE
            vmv.interface.SimulationRunning = False

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
