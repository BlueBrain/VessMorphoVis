####################################################################################################
# Copyright (c) 2023, EPFL / Blue Brain Project
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

import vmv.bmeshi
import vmv.geometry
import vmv.shading
import vmv.scene

import random
from mathutils import Vector

def slice_morphology_based_on_sample_radius(morphology,
                                            number_slices=5,
                                            smallest_sample_radius=None,
                                            largest_sample_radius=None):

    # If the smallest and largest radii are not given by default, calculate them please
    if smallest_sample_radius is None or largest_sample_radius is None:
        smallest_sample_radius = 1e32
        largest_sample_radius = -1e32
        for i_section in morphology.sections_list:
            for i_sample in i_section.samples:
                if i_sample.radius < smallest_sample_radius:
                    smallest_sample_radius = i_sample.radius
                if i_sample.radius > largest_sample_radius:
                    largest_sample_radius = i_sample.radius

    # Construct the range lists
    ranges_lists = list()
    step = ((largest_sample_radius - smallest_sample_radius) / number_slices)
    for i in range(number_slices):
        ranges_lists.append(smallest_sample_radius + (i * step))

    # Construct the slicing lists
    samples_lists = list()
    for i in range(number_slices):
        samples_lists.append(list())

    for i in range(number_slices):
        min_value = ranges_lists[i]
        max_value = min_value + step

        for i_section in morphology.sections_list:
            for i_sample in i_section.samples:
                if min_value <= i_sample.radius < max_value:
                    samples_lists[i].append(i_sample)

    return samples_lists


def create_vertex_based_mesh_objects(morphology,
                                     number_slices=5,
                                     smallest_sample_radius=None,
                                     largest_sample_radius=None):

    # If the smallest and largest radii are not given by default, calculate them please
    if smallest_sample_radius is None or largest_sample_radius is None:
        smallest_sample_radius = 1e32
        largest_sample_radius = -1e32
        for i_section in morphology.sections_list:
            for i_sample in i_section.samples:
                if i_sample.radius < smallest_sample_radius:
                    smallest_sample_radius = i_sample.radius
                if i_sample.radius > largest_sample_radius:
                    largest_sample_radius = i_sample.radius

    # Construct the range lists
    ranges_lists = list()
    step = ((largest_sample_radius - smallest_sample_radius) / number_slices)
    for i in range(number_slices):
        ranges_lists.append(smallest_sample_radius + (i * step))
    ranges_lists.append(largest_sample_radius)

    # Construct the slicing lists
    samples_lists = list()
    for i in range(number_slices):
        samples_lists.append(list())

    for i in range(number_slices):
        min_value = ranges_lists[i]
        max_value = min_value + step

        for i_section in morphology.sections_list:
            for i_sample in i_section.samples:
                if min_value <= i_sample.radius < max_value:
                    samples_lists[i].append(i_sample.point)

    for i in range(number_slices):

        name = 'Group_%d_PS' % i
        samples_positions = samples_lists[i]
        vertices_mesh = vmv.bmeshi.convert_bmesh_to_mesh(
            bmesh_object=vmv.bmeshi.create_vertices(locations=samples_positions),
            name=name)

        # Create the material
        rgb = Vector((random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1)))
        material = vmv.shading.create_material(
            name=name, color=rgb, material_type=vmv.enums.Shader.LAMBERT_WARD)

        vertex_radius = 0.5 * (ranges_lists[i] + ranges_lists[i + 1])
        particle_system = vmv.geometry.create_particle_system_for_vertices(
            mesh_object=vertices_mesh, name=name, vertex_radius=vertex_radius, material=material)
