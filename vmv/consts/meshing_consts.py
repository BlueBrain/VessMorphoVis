####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
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
# Meshing
####################################################################################################
class Meshing:
    """Meshing constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Minimum tessellation level
    MIN_TESSELLATION_LEVEL = 0.1

    # Maximum tessellation level
    MAX_TESSELLATION_LEVEL = 1.0

    # Default sides of a bevel object
    BEVEL_OBJECT_SIDES = 16

    # Meta-ball default resolution
    META_RESOLUTION = 1.0

    # Minimum meta ball resolution
    MIN_META_BALL_RESOLUTION = 0.01

    # Minimum meta ball resolution
    MAX_META_BALL_RESOLUTION = 10.0
