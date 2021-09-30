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

# Internal imports
import vmv.options

# The options parsed from the user interface
Options = vmv.options.VessMorphoVisOptions()

# A reference to the morphology skeleton in a cyclic graph
MorphologyObject = None

# A reference to the reconstructed morphology polyline object
MorphologyPolylineObject = None

# A flag that is used to track if the morphology is loaded or not
MorphologyLoaded = False

# A flag that is used to track the simulation loading
SimulationLoaded = False

# A flag that captures the state of the simulation, whether it is running or not
SimulationRunning = False

# Current visualization type, to update the UI once the visualization type is changed
CurrentVisualizationType = None

# A flag that is used to track if VMV is initialized or not
SystemInitialized = False

# A reference to the reconstructed mesh object
MeshObject = None

# UI Icons
Icons = None
