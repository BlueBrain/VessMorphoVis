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

# System imports
import copy
import math 

# Blender imports
from mathutils import Vector

import vmv
import vmv.geometry
import vmv.skeleton
import numpy as np


####################################################################################################
# @get_color_coded_section_poly_line_with_single_color
####################################################################################################
def get_color_coded_section_poly_line_with_single_color(section):

    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius] 
        for sample in section.samples]

    # Return the constructed poly-line 
    return vmv.skeleton.PolyLine(samples=samples, color_index=0)    


####################################################################################################
# @get_color_coded_section_poly_line_with_alternating_colors
####################################################################################################
def get_color_coded_section_poly_line_with_alternating_colors(section):

    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius] 
        for sample in section.samples]
    

    # Return the constructed poly-line 
    return vmv.skeleton.PolyLine(samples=samples, color_index=section.index % 2)     


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_radius
####################################################################################################
def get_color_coded_section_poly_line_based_on_radius(section,
                                                      minimum, 
                                                      maximum,
    color_map_resolution=vmv.consts.Color.COLOR_MAP_RESOLUTION):

    
    # Compute the average radius of the section 
    section_average_radius = vmv.skeleton.compute_section_average_radius(section)

    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius] 
        for sample in section.samples]
        
    # Poly-line color index (we use two colors to highlight the segment)
    color_index = math.ceil(color_map_resolution * section_average_radius / (maximum - minimum)) - 1
    

    # Return the constructed poly-line 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_radius
####################################################################################################
def get_color_coded_section_poly_line_based_on_length(section,
                                                      minimum, 
                                                      maximum,
    color_map_resolution=vmv.consts.Color.COLOR_MAP_RESOLUTION):

    
    # Compute the average radius of the section 
    section_length = vmv.skeleton.compute_section_length(section)

    # Poly-line samples 
    samples = list()
    
    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius] 
        for sample in section.samples]

        
    # Poly-line color index (we use two colors to highlight the segment)
    color_index = math.ceil(color_map_resolution * section_length / (maximum - minimum)) - 1

    # Return the constructed poly-lines 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_surface_area
####################################################################################################
def get_color_coded_section_poly_line_based_on_surface_area(section,
                                                            minimum, 
                                                            maximum,
    color_map_resolution=vmv.consts.Color.COLOR_MAP_RESOLUTION):

    # Compute the average radius of the section 
    section_surface_area = vmv.skeleton.compute_section_surface_area(section)

    # Poly-line samples 
    samples = list()
    
    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius] 
        for sample in section.samples]

    # Poly-line color index (we use two colors to highlight the segment)
    color_index = math.ceil(color_map_resolution * section_surface_area / (maximum - minimum)) - 1

    # Return the constructed poly-lines 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_volume
####################################################################################################
def get_color_coded_section_poly_line_based_on_volume(section,
                                                      minimum, 
                                                      maximum,
    color_map_resolution=vmv.consts.Color.COLOR_MAP_RESOLUTION):

    # Compute the average radius of the section 
    section_volume = vmv.skeleton.compute_section_volume(section)

    # Poly-line samples 
    samples = list()
    
    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius] 
        for sample in section.samples]

        
    # Poly-line color index (we use two colors to highlight the segment)
    color_index = math.ceil(color_map_resolution * section_volume / (maximum - minimum)) - 1

    # Return the constructed poly-lines 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_volume
####################################################################################################
def get_color_coded_section_poly_line_based_on_number_samples(section,
                                                              minimum, 
                                                              maximum,
    color_map_resolution=vmv.consts.Color.COLOR_MAP_RESOLUTION):

    # Poly-line samples 
    samples = list()
    
    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius] 
        for sample in section.samples]
        
    # Poly-line color index (we use two colors to highlight the segment)
    color_index = math.ceil(color_map_resolution * len(section.samples) / (maximum - minimum)) - 1

    # Return the constructed poly-lines 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)