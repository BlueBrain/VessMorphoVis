####################################################################################################
# Copyright (c) 2020, EPFL / Blue Brain Project
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

# Blender Imports
from mathutils import Vector


####################################################################################################
# @interpolate_list
####################################################################################################
def interpolate_list(input_list, fi):
    
    # Split floating-point index into whole & fractional parts
    i, f = int(fi // 1), fi % 1  
    
    # Avoid index error
    j = i + 1 if f > 0 else i  
    
    # Return the value 
    return (1 - f) * input_list[i] + f * input_list[j]


####################################################################################################
# @hex_to_rgb
####################################################################################################
def hex_to_rgb(hex_color):
    
    # Create an RGB tuple with 256 
    rgb = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

    # Return the Vector for mathutil compatability 
    return Vector((rgb[0] / 256.0, rgb[1] / 256.0, rgb[2] / 256.0)) 


####################################################################################################
# @ create_color_map_from_color_list
####################################################################################################
def create_color_map_from_color_list(color_list, number_colors):

    # RGB lists 
    r_list = list()
    g_list = list()
    b_list = list()
    
    # Color list 
    for color in color_list:
        r_list.append(color[0])
        g_list.append(color[1])
        b_list.append(color[2])
    
    # Delta 
    delta = (len(color_list) - 1) / (number_colors - 1)
        
    # Interpolated lists 
    interpolated_r_list = [interpolate_list(r_list, i * delta) for i in range(number_colors)]
    interpolated_g_list = [interpolate_list(g_list, i * delta) for i in range(number_colors)]
    interpolated_b_list = [interpolate_list(b_list, i * delta) for i in range(number_colors)]
    
    # Interpolated colors 
    interpolated_colors = list()
    for i in range(len(interpolated_r_list)):
        interpolated_colors.append(
            Vector((interpolated_r_list[i], interpolated_g_list[i], interpolated_b_list[i])))
                
    return interpolated_colors


####################################################################################################
# @ create_color_map_from_hex_list
####################################################################################################
def create_color_map_from_hex_list(hex_list, 
                                   number_colors):

    # A list of the RGB colors
    rgb_color_list = list()

    # Convert the HEX colors to RGB 
    for color in hex_list:
        rgb_color_list.append(hex_to_rgb(color))

    # Create the RGB color list
    return create_color_map_from_color_list(rgb_color_list, number_colors)


####################################################################################################
# @sample_range
####################################################################################################
def sample_range(start,
                 end,
                 steps):

    # Delta
    delta = 1. * (end - start) / (steps - 1)

    # Data
    data = list()
    for i in range(steps):
        value = start + i * delta
        data.append(value)

    return data


####################################################################################################
# @equal
####################################################################################################
def equal(arg1, arg2, epsilon=1e-5):

    if math.fabs(arg1 - arg2) < epsilon:
        return True
    return False


####################################################################################################
# @mean
####################################################################################################
def mean(input_list):

    sum_value = 0.
    for i in input_list:
        if math.isnan(i):
            continue
        else:
            sum_value += i

    return sum_value / (1. * len(input_list))


####################################################################################################
# @get_non_zero_minimum_value
####################################################################################################
def get_non_zero_minimum_value(input_list):

    # Initially, a large value
    value = 1e32

    # Check every item in the list
    for item in input_list:

        # The value in the list must be greater than zero
        if item > 0:

            # The item must be smaller than the current value
            if item < value:
                value = item

    # If the value has not changed, return zero as a flag
    if value == 1e32:
        return 0

    # Otherwise, return the actual value found in the list
    return value


####################################################################################################
# @get_non_zero_minimum_value
####################################################################################################
def compute_zero_elements_count(input_list,
                                epsilon=1e-10):

    count = 0
    for item in input_list:
        if item < epsilon:
            count += 1

    return count
