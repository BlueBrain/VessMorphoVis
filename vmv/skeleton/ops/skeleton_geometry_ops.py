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

# System imports
import random
import math
from mathutils import Vector

# Internal imports
import vmv
import vmv.consts
import vmv.shading


####################################################################################################
# @set_skeleton_radii_to_fixed_value
####################################################################################################
def set_skeleton_radii_to_fixed_value(morphology,
                                      fixed_radius_value):
    """Sets the radii of the morphology to a fixed value.

    :param morphology:
        Given morphology skeleton.
    :param fixed_radius_value:
        The value of the radius.
    """

    for section in morphology.sections_list:
        for sample in section.samples:
            sample.radius = fixed_radius_value


####################################################################################################
# @set_skeleton_radii_to_scaled_value
####################################################################################################
def set_skeleton_radii_to_scaled_value(morphology,
                                       scale_factor):
    """Sets the radii of the morphology to a scaled value.
    
    :param morphology:
        Given morphology skeleton.
    :param scale_factor:
        The scale factor used to the scale the radius of each sample
    """

    for section in morphology.sections_list:
        for sample in section.samples:
            sample.radius = sample.radius * scale_factor


####################################################################################################
# @update_skeleton_radii
####################################################################################################
def update_skeleton_radii(morphology,
                          options):
    """Update the radii of the arbors of a given morphology skeleton.

    :param morphology:
        A given morphology skeleton.
    :param options:
        Morphology options as set by the user.
    """

    if options.morphology.radii == vmv.enums.Morphology.Radii.FIXED:
        set_skeleton_radii_to_fixed_value(
            morphology=morphology, fixed_radius_value=options.morphology.sections_fixed_radii_value)

    elif options.morphology.radii == vmv.enums.Morphology.Radii.SCALED:
        set_skeleton_radii_to_scaled_value(
            morphology=morphology, scale_factor=options.morphology.sections_radii_scale)
    else:
        pass


####################################################################################################
# @set_poly_line_radii_to_fixed_value
####################################################################################################
def set_poly_line_radii_to_fixed_value(poly_line,
                                       fixed_radius_value):
    """

    :param polyline:
    :param fixed_radius_value:
    :return:
    """

    # Update the radii of all the samples. Note that [0] is the coordinate and [1] is the radius
    for sample in poly_line.samples:
        sample[1] = fixed_radius_value


####################################################################################################
# @set_poly_line_radii_to_fixed_value
####################################################################################################
def set_poly_line_radii_to_scaled_value(poly_line,
                                       scale_factor):
    """

    :param poly_line:
    :param fixed_radius_value:
    :return:
    """

    # Update the radii of all the samples. Note that [0] is the coordinate and [1] is the radius
    for sample in poly_line.samples:
        sample[1] *= scale_factor


####################################################################################################
# @update_poly_line_radii
####################################################################################################
def update_poly_line_radii(poly_line,
                           options):
    """

    :param poly_line:
    :param options:
    :return:
    """

    if options.morphology.radii == vmv.enums.Morphology.Radii.FIXED:
        set_poly_line_radii_to_fixed_value(
            poly_line=poly_line, fixed_radius_value=options.morphology.sections_fixed_radii_value)

    elif options.morphology.radii == vmv.enums.Morphology.Radii.SCALED:
        set_poly_line_radii_to_scaled_value(
            poly_line=poly_line, scale_factor=options.morphology.sections_radii_scale)
    else:
        pass


####################################################################################################
# @compute_segment_surface_area
####################################################################################################
def compute_segment_surface_area(sample_1, sample_2):

    # Retrieve the data of the samples along each segment on the section
    p0 = sample_1.point
    p1 = sample_2.point
    r0 = sample_1.radius
    r1 = sample_2.radius

    # Compute the segment lateral area
    segment_length = (p0 - p1).length
    r_sum = r0 + r1
    r_diff = r0 - r1
    segment_lateral_area = math.pi * r_sum * math.sqrt((r_diff * r_diff) + segment_length)

    return segment_lateral_area


####################################################################################################
# @compute_section_length
####################################################################################################
def compute_section_average_radius(section):
    
    # If the section has no samples, then return 0
    if len(section.samples) == 0:
        return 0.0

    # Initially, set to zero
    section_average_radius = 0.0

    # Add the radii  
    for sample in section.samples:
        section_average_radius += sample.radius
    
    # Average 
    section_average_radius /= len(section.samples)

    # Return the section average radius 
    return section_average_radius


####################################################################################################
# @get_minimum_and_maximum_sections_average_radii
####################################################################################################
def get_minimum_and_maximum_sections_average_radii(morphology):

    # Get a list of radii 
    radii = [compute_section_average_radius(section=section) 
        for section in morphology.sections_list]

    # Return the minimum and maximum 
    return min(radii), max(radii)


####################################################################################################
# @get_minimum_and_maximum_sections_lengths
####################################################################################################
def get_minimum_and_maximum_sections_lengths(morphology):

    # Get a list of lengths 
    sections_lengths = [compute_section_length(section=section) 
        for section in morphology.sections_list]

    # Return the minimum and maximum
    return min(sections_lengths), max(sections_lengths)


####################################################################################################
# @get_minimum_and_maximum_samples_radii
####################################################################################################
def get_minimum_and_maximum_samples_radii(morphology):

    minimum = vmv.consts.Math.INFINITY  
    maximum = -vmv.consts.Math.INFINITY

    for section in morphology.sections_list:

        for sample in section.samples:
            if sample.radius < minimum:
                minimum = sample.radius
            if sample.radius > maximum:
                maximum = sample.radius
    
    return minimum, maximum


###################################################################################################
# @get_minimum_and_maximum_segments_length
####################################################################################################
def get_minimum_and_maximum_segments_length(morphology):


    minimum = vmv.consts.Math.INFINITY  
    maximum = -vmv.consts.Math.INFINITY

    for section in morphology.sections_list:

        for i in range(len(section.samples) - 1):

            segment_length = (section.samples[i + 1].point - section.samples[i].point).length
            if segment_length < minimum:
                minimum = segment_length
            if segment_length > maximum:
                maximum = segment_length
    
    return minimum, maximum



####################################################################################################
# @compute_section_length
####################################################################################################
def compute_section_length(section):
    
    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return 0.0

    # Initially, set to zero
    section_length = 0.0

    # Compute the length from the segments 
    for i in range(len(section.samples) - 1):
        section_length += (section.samples[i + 1].point - section.samples[i].point).length
    
    # Return the section length 
    return section_length


####################################################################################################
# @compute_segments_surface_areas_in_section
####################################################################################################
def compute_segments_surface_areas_in_section(section,
                                              segments_surface_areas):
    """Computes a list of the surface areas of all the segments in the section.

    :param section:
        A given section to compute the surface area of its segments.
    :param segments_surface_areas:
        A list to collect the resulting data.
    """

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return

    # Integrate the surface area between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment lateral area
        segment_length = (p0 - p1).length
        r_sum = r0 + r1
        r_diff = r0 - r1
        segment_lateral_area = math.pi * r_sum * math.sqrt((r_diff * r_diff) + segment_length)

        # Compute the segment surface area and append it list
        segments_surface_areas.append(segment_lateral_area + math.pi * ((r0 * r0) + (r1 * r1)))


####################################################################################################
# @compute_section_surface_area
####################################################################################################
def compute_section_surface_area(section):
    
    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return 0.0

    # Initially, set to zero
    segments_surface_areas = list()

    # Compute the surface areas from the segments
    compute_segments_surface_areas_in_section(
        section=section, segments_surface_areas=segments_surface_areas)
    
    # Sum 
    section_surface_area = sum(segments_surface_areas)

    # Return the section surface area 
    return section_surface_area



####################################################################################################
# @compute_segment_volume
####################################################################################################
def compute_segment_volume(sample_1, sample_2):

    # Retrieve the data of the samples along each segment on the section
    p0 = sample_1.point
    p1 = sample_2.point
    r0 = sample_1.radius
    r1 = sample_2.radius

    # Compute the segment volume and append to the total section volume
    segment_volume = (1.0 / 3.0) * math.pi * (p0 - p1).length * (r0 * r0 + r0 * r1 + r1 * r1)

    return segment_volume

####################################################################################################
# @compute_section_volume_from_segments
####################################################################################################
def compute_segments_volumes_in_section(section,
                                        segments_volumes):
    """Computes the volume of a section from its segments.

    This approach assumes that each segment is approximated by a tapered cylinder and uses the
    formula reported in this link: https://keisan.casio.com/exec/system/1223372110.

    :param section:
        A given section to compute its volume.
    :param segments_volumes:
        A list to collect the resulting data.
    """

    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return

    # Integrate the volume between each two successive samples
    for i in range(len(section.samples) - 1):

        # Retrieve the data of the samples along each segment on the section
        p0 = section.samples[i].point
        p1 = section.samples[i + 1].point
        r0 = section.samples[i].radius
        r1 = section.samples[i + 1].radius

        # Compute the segment volume and append to the total section volume
        segment_volume = (1.0 / 3.0) * math.pi * (p0 - p1).length * (r0 * r0 + r0 * r1 + r1 * r1)

        # Append to the list
        segments_volumes.append(segment_volume)


####################################################################################################
# @compute_section_volume
####################################################################################################
def compute_section_volume(section):
    
    # If the section has less than two samples, then report the error
    if len(section.samples) < 2:
        return 0.0

    # Initially, set to zero
    segments_volumes = list()

    # Compute the volumes from the segments
    compute_segments_volumes_in_section(section=section, segments_volumes=segments_volumes)
    
    # Sum 
    section_volume = sum(segments_volumes)

    # Return the section volume 
    return section_volume


####################################################################################################
# @compute_sections_surface_areas_from_segments
####################################################################################################
def compute_sections_surface_areas_from_segments(section,
                                                 sections_surface_areas):
    """Computes the surface areas of all the sections along a given arbor.

    :param section:
        A given section to compute its surface area.
    :param sections_surface_areas:
        A list to collect the resulting data.
    """

    # Compute section surface area
    section_surface_area = compute_section_surface_area_from_segments(section=section)

    # Append the computed surface area to the list
    sections_surface_areas.append(section_surface_area)

###################################################################################################
# @get_minimum_and_maximum_segments_surface_area
####################################################################################################
def get_minimum_and_maximum_segments_surface_area(morphology):

    
    segments_surface_areas = list()

    for section in morphology.sections_list:

        compute_segments_surface_areas_in_section(
            section=section, segments_surface_areas=segments_surface_areas)
            
    return min(segments_surface_areas), max(segments_surface_areas)


###################################################################################################
# @get_minimum_and_maximum_segments_volume
####################################################################################################
def get_minimum_and_maximum_segments_volume(morphology):

    segments_volumes = list()

    for section in morphology.sections_list:

        compute_segments_volumes_in_section(
            section=section, segments_volumes=segments_volumes)
            
    return min(segments_volumes), max(segments_volumes)



###################################################################################################
# @get_minimum_and_maximum_sections_surface_area
####################################################################################################
def get_minimum_and_maximum_sections_surface_areas(morphology):

    sections_surface_area = list()

    for section in morphology.sections_list:
        sections_surface_area.append(compute_section_surface_area(section=section))
            
    return min(sections_surface_area), max(sections_surface_area)


###################################################################################################
# @get_minimum_and_maximum_sections_volume
####################################################################################################
def get_minimum_and_maximum_sections_volumes(morphology):

    
    sections_volumes = list()

    for section in morphology.sections_list:

        sections_volumes.append(compute_section_volume(section=section))
            
    return min(sections_volumes), max(sections_volumes)


###################################################################################################
# @get_minimum_and_maximum_sections_number_samples
####################################################################################################
def get_minimum_and_maximum_sections_number_samples(morphology):

    
    sections_number_samples = list()

    for section in morphology.sections_list:

        sections_number_samples.append(len(section.samples))
            
    return min(sections_number_samples), max(sections_number_samples)


###################################################################################################
# @get_minimum_and_maximum_segments_index
####################################################################################################
def get_minimum_and_maximum_segments_index(morphology):

    # We compute the total number of segments in the morphology.
    total_number_segments = 0

    # For every section in the morphology, append the total number of segments in the section
    for section in morphology.sections_list:
        total_number_segments += len(section.samples)

    # Return the result
    return 0, total_number_segments


def update_poly_lines_radii(poly_lines,
                            options):
    """

    :param poly_lines:
    :param options:
    :return:
    """

    # Save the processing time
    if options.morphology.radii == vmv.enums.Morphology.Radii.FIXED or \
            options.morphology.radii == vmv.enums.Morphology.Radii.SCALED:

        for poly_line in poly_lines:
            update_poly_line_radii(poly_line=poly_line, options=options)





def resample_poly_line_adaptively(poly_line):



    pass

def resample_poly_lines_adaptively(poly_lines):
    """

    :param poly_lines:
    :return:
    """

    for poly_line in poly_lines:
        resample_poly_line_adaptively(poly_line=poly_line)
