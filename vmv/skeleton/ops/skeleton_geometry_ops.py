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
    """

    :param morphology:
    :param fixed_radius_value:
    :return:
    """

    for section in morphology.sections_list:
        for sample in section.samples:
            sample.radius = fixed_radius_value


####################################################################################################
# @set_skeleton_radii_to_scaled_value
####################################################################################################
def set_skeleton_radii_to_scaled_value(morphology,
                                       scale_factor):
    """

    :param morphology:
    :param scale_factor:
    :return:
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

    :param poly_line:
    :param fixed_radius_value:
    :return:
    """

    # Poly-line samples
    poly_line_samples = poly_line[0]

    # Update the radii of all the samples. Note that [0] is the coordinate and [1] is the radius
    for poly_line_sample in poly_line_samples:
        poly_line_sample[1] = fixed_radius_value


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

    # Poly-line samples
    poly_line_samples = poly_line[0]

    # Update the radii of all the samples. Note that [0] is the coordinate and [1] is the radius
    for poly_line_sample in poly_line_samples:
        poly_line_sample[1] *= scale_factor


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
