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
# @ColorMaps
####################################################################################################
class ColorMaps:
    """ColorMaps enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Default RGB color-map
    RGB = 'RGB_COLOR_MAP'

    # HSV color-map
    HSV = 'HSV_COLOR_MAP'

    # Viridis
    VIRIDIS = 'VIRIDIS_COLOR_MAP'

    # Plasma
    PLASMA = 'PLASMA_COLOR_MAP'

    ################################################################################################
    # get_enum
    ################################################################################################
    @staticmethod
    def get_enum(color_map_name):
        """Return the color-map enumerator from the name

        :param color_map_name:
            The name of the color map.
        :return:
            The color-map enumerator.
        """
        if color_map_name == 'rgb':
            return ColorMaps.RGB
        elif color_map_name == 'hsv':
            return ColorMaps.HSV
        else:
            return ColorMaps.RGB

    def get_hex_color_list(color_map_enum):

        if color_map_enum == ColorMaps.VIRIDIS:
            return ['430652', '308C8B', 'F7E545'] 
        elif color_map_enum == ColorMaps.PLASMA:
            return ['1B0D85', 'CA4F75', 'EEF447']
        else:
            
            return ['1B0D85', 'CA4F75', 'EEF447']

    ################################################################################################
    # A list of all the available color-maps in VessMorphoVis
    ################################################################################################
    COLOR_MAPS = [

        # HSV
        (VIRIDIS, 'VIRIDIS', 'Viridis color map'),

        # Plasma
        (PLASMA, 'PLASMA', 'Plasma color map'),

    ]


#'viridis', 'plasma', 'inferno', 'magma', 'cividis'