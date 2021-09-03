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

# Blender imports
import bpy


####################################################################################################
# @VMV_LoadSimulation
####################################################################################################
class VMV_LoadSimulation(bpy.types.Operator):
    """Loads the simulation data and apply them on the morphology skeleton"""

    # Operator parameters
    bl_idname = 'load.simulation'
    bl_label = 'Load Simulation'

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

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_PlaySimulation(bpy.types.Operator):
    """Runs, pauses and stops the simulation"""

    # Operator parameters
    bl_idname = 'play.simulation'
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

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_SimulationNextFrame(bpy.types.Operator):
    """Runs, pauses and stops the simulation"""

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

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_SimulationPreviousFrame(bpy.types.Operator):
    """Runs, pauses and stops the simulation"""

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

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_SimulationFirstFrame(bpy.types.Operator):
    """Runs, pauses and stops the simulation"""

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

        # Done, return {'FINISHED'}
        return {'FINISHED'}


####################################################################################################
# @VMV_PlaySimulation
####################################################################################################
class VMV_SimulationLastFrame(bpy.types.Operator):
    """Runs, pauses and stops the simulation"""

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

        # Done, return {'FINISHED'}
        return {'FINISHED'}
