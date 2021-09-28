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
# Meshing
####################################################################################################
class RenderingPlanes:
    """Rendering planes constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Front face delta in blender units
    FRONT_FACE_DELTA = 1000

    # Back face delta in blender units
    BACK_FACE_DELTA = 1000

    # Top face delta in blender units
    TOP_FACE_DELTA = 1000

    # Bottom face delta in %
    BOTTOM_FACE_DELTA = 1

    # Horizon scale
    HORIZON_SCALE = 100

    # The distance of the background plane from the center
    BACKGROUND_PLANE_Z = 5e4
