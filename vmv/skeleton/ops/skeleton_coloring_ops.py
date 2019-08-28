####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
import random
from mathutils import Vector

# Internal imports
import vmv
import vmv.consts
import vmv.shading


####################################################################################################
# @create_materials
####################################################################################################
def create_skeleton_materials(name,
                              material_type,
                              color):
    """Creates two materials for any component of the skeleton based on the input parameters
    of the user.

    :param name:
        The name of the material/color.
    :param material_type:
        The material type.
    :param color:
        The code of the given colors.
    :return:
        A list of two elements (different or even same colors) where we can apply later to the
        drawn sections or segments.
    """

    # A list of the created materials
    materials_list = list()

    # Random colors
    if color[0] == -1 and color[1] == 0 and color[2] == 0:

        # Initialize the color vector to black
        color_vector = vmv.consts.Color.BLACK

        # Generate random colors
        for i in range(2):
            color_vector.x = random.uniform(0.0, 1.0)
            color_vector.y = random.uniform(0.0, 1.0)
            color_vector.z = random.uniform(0.0, 1.0)

            # Create the material and append it to the list
            material = vmv.shading.create_material(
                name='%s_random_%d' % (name, i), color=color_vector, material_type=material_type)
            materials_list.append(material)

    # If set to black / white
    elif color[0] == 0 and color[1] == -1 and color[2] == 0:

        # Create the material and append it to the list
        material = vmv.shading.create_material(
            name='%s_bw_0' % name, color=vmv.consts.Color.MATT_BLACK, material_type=material_type)
        materials_list.append(material)

        # Create the material and append it to the list
        material = vmv.shading.create_material(
            name='%s_bw_1' % name, color=vmv.consts.Color.WHITE, material_type=material_type)
        materials_list.append(material)

    # Specified colors
    else:
        for i in range(2):

            # Create the material and append it to the list
            material = vmv.shading.create_material(
                name='%s_color_%d' % (name, i), color=color, material_type=material_type)
            materials_list.append(material)

    # Return the list
    return materials_list


####################################################################################################
# @get_colors_list_from_color_index
####################################################################################################
def get_colors_list_from_color_index(color_index):
    """Returns a list of colors from a given single color index that is defined by the user from
    the interface.

    :param color_index:
        A given color index to create two colors list.
    :return:
        Returns a list of colors from a given single color index that is defined by the user from
        the interface.
    """

    # A list of the created materials
    colors_list = list()

    # Random colors
    if color_index[0] == -1 and color_index[1] == 0 and color_index[2] == 0:

        # Initialize the color vector to black
        color_vector = vmv.consts.Color.BLACK

        # Generate random colors
        for i in range(2):
            color_vector.x = random.uniform(0.0, 1.0)
            color_vector.y = random.uniform(0.0, 1.0)
            color_vector.z = random.uniform(0.0, 1.0)
            colors_list.append(Vector((color_vector.x, color_vector.y, color_vector.z)))

    # If set to black / white
    elif color_index[0] == 0 and color_index[1] == -1 and color_index[2] == 0:

        # Black
        colors_list.append(Vector((0.0, 0.0, 0.0)))

        # White
        colors_list.append(Vector((1.0, 1.0, 1.0)))

    # Specific colors
    else:
        for i in range(2):
            colors_list.append(color_index)

    # Return the list
    return colors_list
