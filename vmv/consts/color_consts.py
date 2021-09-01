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
from mathutils import Vector


####################################################################################################
# Math
####################################################################################################
class Color:
    """Color constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Red
    RED = Vector((1.0, 0.0, 0.0))

    # Green
    GREEN = Vector((0.0, 1.0, 0.0))

    # Blue
    BLUE = Vector((0.0, 0.0, 1.0))

    # White
    WHITE = Vector((1.0, 1.0, 1.0))

    # Very White
    VERY_WHITE = Vector((10.0, 10.0, 10.0))

    # Gray
    GRAY = Vector((0.5, 0.5, 0.5))

    # Matt black
    MATT_BLACK = Vector((0.1, 0.1, 0.1))

    # Black
    BLACK = Vector((0.0, 0.0, 0.0))

    # Default color for blood
    DEFAULT_BLOOD_COLOR = Vector((172.0 / 256.0, 4.0 / 256.0, 4.0 / 256.0))

    # Light red color
    LIGHT_RED_COLOR = Vector((0.9, 0.1, 0.075))

    # NUmber of colors in the colormap
    COLORMAP_RESOLUTION = 16
