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
import vmv.utilities


####################################################################################################
# @construct_section_polyline_samples
####################################################################################################
def construct_section_polyline_samples(section):
    """Constructs (or converts) a section with the format required to build a Blender polyline.

    @param section:
        A given vascular section.
    @return:
        A list containing all the samples of the section in the polyline format.
    """

    return [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius]
            for sample in section.samples]


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
# @get_color_coded_section_poly_line_for_short_sections
####################################################################################################
def get_color_coded_section_poly_line_for_short_sections(section):

    # Add the samples
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius]
               for sample in section.samples]

    # Return the constructed poly-line
    if vmv.is_short_section(section=section):
        return vmv.skeleton.PolyLine(samples=samples, color_index=1)
    else:
        return vmv.skeleton.PolyLine(samples=samples, color_index=0)


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_radius
####################################################################################################
def get_color_coded_section_poly_line_based_on_radius(
        section, minimum, maximum, color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):

    # Compute the average radius of the section 
    section_average_radius = vmv.skeleton.compute_section_average_radius(section)

    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius]
               for sample in section.samples]
        
    # Poly-line color index (we use two colors to highlight the segment)
    color_index = vmv.utilities.get_index(value=section_average_radius,
                                          minimum_value=minimum,
                                          maximum_value=maximum,
                                          number_steps=color_map_resolution)

    # Return the constructed poly-line 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_radius
####################################################################################################
def get_color_coded_section_poly_line_based_on_length(
        section, minimum, maximum, color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):

    # Compute the average radius of the section 
    section_length = vmv.skeleton.compute_section_length(section)

    # Poly-line samples
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius]
               for sample in section.samples]

    # Poly-line color index (we use two colors to highlight the segment)
    color_index = vmv.utilities.get_index(value=section_length,
                                          minimum_value=minimum,
                                          maximum_value=maximum,
                                          number_steps=color_map_resolution)

    # Return the constructed poly-lines
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_surface_area
####################################################################################################
def get_color_coded_section_poly_line_based_on_surface_area(
        section, minimum, maximum, color_map_resolution=vmv.consts.Color.COLORMAP_RESOLUTION):

    # Compute the average radius of the section 
    section_surface_area = vmv.skeleton.compute_section_surface_area(section)
    
    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius]
               for sample in section.samples]

    # Poly-line color index (we use two colors to highlight the segment)
    color_index = vmv.utilities.get_index(value=section_surface_area,
                                          minimum_value=minimum,
                                          maximum_value=maximum,
                                          number_steps=color_map_resolution)

    # Return the constructed poly-lines 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_section_poly_line_based_on_volume
####################################################################################################
def get_color_coded_section_poly_line_based_on_volume(section,
                                                      minimum,
                                                      maximum,
                                                      color_map_resolution):

    # Compute the average radius of the section 
    section_volume = vmv.skeleton.compute_section_volume(section)

    # Add the samples 
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius]
               for sample in section.samples]

    # Poly-line color index (we use two colors to highlight the segment)
    color_index = vmv.utilities.get_index(value=section_volume,
                                          minimum_value=minimum,
                                          maximum_value=maximum,
                                          number_steps=color_map_resolution)

    # Return the constructed poly-lines 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_section_poly_line_based_on_number_samples
####################################################################################################
def get_color_coded_section_poly_line_based_on_number_samples(
        section, minimum, maximum, color_map_resolution):

    # Add the samples
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius]
               for sample in section.samples]

    # Poly-line color index (we use two colors to highlight the segment)
    color_index = vmv.utilities.get_index(value=len(section.samples),
                                          minimum_value=minimum,
                                          maximum_value=maximum,
                                          number_steps=color_map_resolution)

    # Return the constructed poly-lines 
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)


####################################################################################################
# @get_color_coded_sections_poly_lines_based_on_section_index
####################################################################################################
def get_color_coded_sections_poly_lines_based_on_section_index(
        section, minimum, maximum, color_map_resolution):

    # Add the samples
    samples = [[(sample.point[0], sample.point[1], sample.point[2], 1), sample.radius]
               for sample in section.samples]

    # Poly-line color index (we use two colors to highlight the segment)
    color_index = vmv.utilities.get_index(value=section.index,
                                          minimum_value=minimum,
                                          maximum_value=maximum,
                                          number_steps=color_map_resolution)

    # Return the constructed poly-lines
    return vmv.skeleton.PolyLine(samples=samples, color_index=color_index)
