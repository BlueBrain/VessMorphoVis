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


####################################################################################################
# @Simulation
####################################################################################################
class Simulation:
    """Simulation enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @Dynamics
    ################################################################################################
    class Dynamics:
        """Simulation dynamics
        """

        # Simulating radius variations
        RADIUS = 'VMV_SIMULATION_RADIUS'
        RADIUS_UI_ITEM = (RADIUS, 'Radius', 'Visualize radii variations over time')

        # Simulating flow variations
        FLOW = 'VMV_SIMULATION_FLOW'
        FLOW_UI_ITEM = (FLOW, 'Flow', 'Visualize flow variations over time')

        # Simulating pressure variations
        PRESSURE = 'VMV_SIMULATION_PRESSURE'
        PRESSURE_UI_ITEM = (PRESSURE, 'Pressure', 'Visualize pressure variations over time')

        # All items in a single list
        ALL_UI_ITEMS = [RADIUS_UI_ITEM, FLOW_UI_ITEM, PRESSURE_UI_ITEM]

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Radius
            if argument == 'radius':
                return Simulation.Dynamics.RADIUS

            # Flow
            elif argument == 'flow':
                return Simulation.Dynamics.FLOW

            # Pressure
            elif argument == 'pressure':
                return Simulation.Dynamics.PRESSURE

            # By default use the radius simulations, if available
            else:
                return Simulation.Dynamics.RADIUS
