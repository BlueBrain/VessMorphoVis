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
import numpy as np


def get_section_poly_line_(section):
    #points_4d = np.hstack((section.points, np.ones((len(section.points), 1))))

    #print(points_4d)
    #print('-')
    #print(points_4d.tolist())

    poly_list = list(map(list, zip(map(tuple, np.hstack((section.points, np.ones((len(section.points), 1))))), 0.5 * section.diameters)))

    #print(poly_list)
    return  poly_list


####################################################################################################
# @get_section_poly_line
####################################################################################################
def get_section_poly_line(section):
    """Get the poly-line list or a series of points that reflect the skeleton of a single section.

    :param section:
        The geometry of a section.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_line = list()

    # Construct the section from all the samples
    for sample in section.samples:

        # Get the coordinates of the sample
        point = sample.point

        # Get the radius of the sample
        radius = sample.radius

        # TODO: Add an option to set the radii at the terminal or branching points to zero
        """
        if not section.is_root():
            if i == 0:
                radius = 0

        if not section.is_leaf():
            if i == len(section.samples) - 1:
                radius = 0
        """

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_connected_sections_poly_line
####################################################################################################
def get_connected_sections_poly_lines(section):
    """Get the poly-line list or a series of points that reflect the skeleton of a single section.

    :param section:
        The geometry of a section.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_lines = list()

    # If the section has any parents and any children
    if len(section.parents) > 0 and len(section.children) > 0:

        # Make a connected section between each parent and this section
        for parent in section.parents:

            # Extend the connectivity from the section to each child
            for child in section.children:

                # Get the section data
                samples = vmv.skeleton.ops.get_connectivity_poly_line_from_parent_to_child(
                    section=section, parent=parent, child=child)

                # Add the data to the list
                poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=0))

    # If the section has no parents but has some children
    if len(section.parents) == 0 and len(section.children) > 0:

        # Make a connected section between this section and each child
        for child in section.children:

            # Get the section data
            samples = vmv.skeleton.ops.get_connectivity_poly_line_from_section_to_child(
                section=section, child=child)

            # Add the data to the list
            poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=0))

    # If the section has some parent and no children
    if len(section.parents) > 0 and len(section.children) == 0:

        # Make a connected section between each parent and this section
        for parent in section.parents:

            # Get the section data
            samples = vmv.skeleton.ops.get_connectivity_poly_line_from_parent_to_section(
                section=section, parent=parent)

            # Add the data to the list
            poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=0))

    # If the section is an orphan, or has no parents and no children
    if len(section.parents) == 0 and len(section.children) == 0:

        # Get the section data of this section only
        samples = vmv.skeleton.ops.get_section_poly_line(section=section)

        # Add the data to the list
        poly_lines.append(vmv.skeleton.PolyLine(samples=samples, color_index=0))

    # Return the poly-line list
    return poly_lines


####################################################################################################
# @get_connected_sections_from_root_to_leaf
####################################################################################################
def get_connected_sections_from_root_to_leaf(section,
                                             poly_line,
                                             poly_lines):

    # If the section has been traversed, then simply return
    if section.traversed:
        return

    # Get the section samples
    poly_line.extend(get_section_poly_line(section))

    # If this is the last section (a leaf node) or all the children sections have been traversed
    if section.is_leaf() or section.all_children_traversed():

        # Copy the single poly-line to the poly-lines list
        poly_lines.append([copy.deepcopy(poly_line), 0])

        # Clear the poly line
        poly_line.clear()

        # Terminate the loop
        return

    # Arrange the children based on a specific criteria

    # Iterate over the children
    for child in section.children:

        get_connected_sections_from_root_to_leaf(child, poly_line, poly_lines)








####################################################################################################
# @get_section_poly_line_and_append_disconnections
####################################################################################################
def get_section_poly_line_and_append_disconnections(section,
                          center=Vector((0.0, 0.0, 0.0))):
    """Get the poly-line list or a series of points that reflect the skeleton of a single section.

    :param section:
        The geometry of a section.
    :param center:
        Center.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_line = []

    # If the section is root, then do not append sample at the beginning
    if not section.is_root():

        # Get the coordinates of the sample
        point = section.samples[0].point - center

        # Append the sample at the beginning
        poly_line.append(None)

    # Construct the section from all the samples
    for i in range(len(section.samples)):

        # Get the coordinates of the sample
        point = section.samples[i].point - center

        # Get the radius of the sample
        radius = section.samples[i].radius # * random.uniform(1.0, 5.0)

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # If the section is not leaf, add a sample at the end
    if not section.is_leaf():

        # Get the coordinates of the sample
        point = section.samples[-1].point - center

        # Append the sample at the beginning
        poly_line.append(None)

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_connectivity_poly_line_from_parent_to_child
####################################################################################################
def get_connectivity_poly_line_from_parent_to_child(section,
                                                    parent,
                                                    child,
                                                    center=Vector((0.0, 0.0, 0.0))):
    """Get the poly-line list or a series of points that reflect the skeleton of a single section.

    :param section:
        The geometry of a section.
    :param parent:
        One of the parents of the section.
    :param child:
        One of the children of the section.
    :param center:
        Center.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_line = []

    # Parent samples
    for i in range(len(parent.samples) - 1):

        # Get the coordinates of the sample
        point = parent.samples[i].point - center

        # Get the radius of the sample
        radius = parent.samples[i].radius

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Section samples
    for i in range(len(section.samples) - 1):

        # Get the coordinates of the sample
        point = section.samples[i].point - center

        # Get the radius of the sample
        radius = section.samples[i].radius

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Child samples
    for i in range(len(child.samples)):
        # Get the coordinates of the sample
        point = child.samples[i].point - center

        # Get the radius of the sample
        radius = child.samples[i].radius

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_connectivity_poly_line_from_section_to_child
####################################################################################################
def get_connectivity_poly_line_from_section_to_child(section,
                                                     child,
                                                     center=Vector((0.0, 0.0, 0.0))):
    """Get the poly-line list or a series of points that reflect the skeleton of a single section.

    :param section:
        The geometry of a section.
    :param child:
        One of the children of the section.
    :param center:
        Center.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_line = []

    # Section samples
    for i in range(len(section.samples) - 1):

        # Get the coordinates of the sample
        point = section.samples[i].point - center

        # Get the radius of the sample
        radius = section.samples[i].radius

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Child samples
    for i in range(len(child.samples)):
        # Get the coordinates of the sample
        point = child.samples[i].point - center

        # Get the radius of the sample
        radius = child.samples[i].radius

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @get_connectivity_poly_line_from_this_section_to_leaf
####################################################################################################
def get_connectivity_poly_lines_from_this_section_to_leaf(section,
                                                          poly_line_data=[],
                                                          poly_lines_data=[],
                                                          center=Vector((0.0, 0.0, 0.0))):

    # If the section is a root node, append its samples
    if section.is_root():

        # An array containing the data of the section arranged in blender poly-line format
        poly_line = list()

        # Section samples
        for i in range(len(section.samples) - 1):

            # Get the coordinates of the sample
            point = section.samples[i].point - center

            # Get the radius of the sample
            radius = section.samples[i].radius

            # Use the actual radius of the samples reported in the morphology file
            poly_line.append([(point[0], point[1], point[2], 1), radius])

        # Update the traversal state
        section.traversed = True

        # Append the data to the global polyline
        poly_line_data.extend(poly_line)

    # If the section is a leaf node
    elif section.is_leaf():

        # If the section was not traversed before
        if not section.traversed:

            # An array containing the data of the section arranged in blender poly-line format
            poly_line = list()

            # Section samples
            for i in range(len(section.samples) - 1):

                # Get the coordinates of the sample
                point = section.samples[i].point - center

                # Get the radius of the sample
                radius = section.samples[i].radius

                # Use the actual radius of the samples reported in the morphology file
                poly_line.append([(point[0], point[1], point[2], 1), radius])

            # Update the traversal state
            section.traversed = True

            # Append the data to the global polyline
            poly_line_data.extend(poly_line)

            # Append the poly-line data to the poly-lines data list
            poly_lines_data.append(copy.deepcopy(poly_line_data))

            # Clear all the items in the poly-line data
            poly_line_data.clear()

        else:

            # Append the poly-line data to the poly-lines data list
            poly_lines_data.append(copy.deepcopy(poly_line_data))

            # Clear all the items in the poly-line data
            poly_line_data.clear()

    # Stem section
    else:

        # If the section was not traversed before
        if not section.traversed:

            # An array containing the data of the section arranged in blender poly-line format
            poly_line = list()

            # Section samples
            for i in range(len(section.samples) - 1):

                # Get the coordinates of the sample
                point = section.samples[i].point - center

                # Get the radius of the sample
                radius = section.samples[i].radius

                # Use the actual radius of the samples reported in the morphology file
                poly_line.append([(point[0], point[1], point[2], 1), radius])

            # Update the traversal state
            section.traversed = True

            # Append the data to the global polyline
            poly_line_data.extend(poly_line)

        else:

            # Append the poly-line data to the poly-lines data list
            poly_lines_data.append(copy.deepcopy(poly_line_data))

            # Clear all the items in the poly-line data
            poly_line_data.clear()

    # Traverse the children
    for child in section.children:

        # Extend the poly-line and get the connectivity of the children
        get_connectivity_poly_lines_from_this_section_to_leaf(section=child,
                                                              poly_line_data=poly_line_data,
                                                              poly_lines_data=poly_lines_data,
                                                              center=center)


####################################################################################################
# @get_connectivity_poly_line_from_parent_to_child
####################################################################################################
def get_connectivity_poly_line_from_parent_to_section(section,
                                                      parent,
                                                      center=Vector((0.0, 0.0, 0.0))):
    """Get the poly-line list or a series of points that reflect the skeleton of a single section.

    :param section:
        The geometry of a section.
    :param parent:
        One of the parents of the section.
    :param center:
        Center.
    :return:
        Section data in poly-line format that is suitable for drawing by Blender.
    """

    # An array containing the data of the section arranged in blender poly-line format
    poly_line = []

    # Parent samples
    for i in range(len(parent.samples) - 1):

        # Get the coordinates of the sample
        point = parent.samples[i].point - center

        # Get the radius of the sample
        radius = parent.samples[i].radius

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Section samples
    for i in range(len(section.samples) - 1):

        # Get the coordinates of the sample
        point = section.samples[i].point - center

        # Get the radius of the sample
        radius = section.samples[i].radius

        # Use the actual radius of the samples reported in the morphology file
        poly_line.append([(point[0], point[1], point[2], 1), radius])

    # Return the poly-line list
    return poly_line


####################################################################################################
# @draw_section_from_poly_line_data
####################################################################################################
def draw_section_from_poly_line_data(data,
                                     name,
                                     material=None,
                                     color=None,
                                     bevel_object=None,
                                     caps=False):
    """Draw a morphological section as a poly-line (or tube) object and returns a reference to it.

    :param data:
        Section data in poly-line format.
    :param name:
        The name of the section object in the scene, for referencing.
    :param material:
        Section material.
    :param color:
        Section color.
    :param bevel_object:
        A given bevel object to scale the section.
    :param caps:
        A flag to close the caps of the section sides or keep them open.
    :return:
        A reference to the drawn section.
    """

    # If the data list has less than two samples, then report the error
    #if len(data) < 2:

    #    vmv.logger.log('\t\t* ERROR: Drawn section [%s] has less than two samples' % name)

    # Append a '_section' keyword after the section name to be able to recognize it later
    section_name = '%s_section' % name

    # Draw the section from the given data in poly-line format
    section_object = vmv.geometry.draw_poly_line(poly_line_data=data, name=section_name,
        material=material, color=color, bevel_object=bevel_object, caps=caps)

    # Return a reference to the drawn section object
    return section_object


####################################################################################################
# @draw_connected_sections
####################################################################################################
def draw_connected_sections(section, name='sample',
                            poly_line_data=[],
                            sections_objects=[],
                            secondary_sections=[],
                            branching_level=0,
                            bevel_object=None,
                            caps=False):
    """Draw a list of sections connected together as a poly-line.

    :param section:
        Section root.
    :param poly_line_data:
        A list of lists containing the data of the poly-line format.
    :param sections_objects:
        A list that should contain all the drawn section objects.
    :param secondary_sections:
        A list of the secondary sections along the arbor.
    :param branching_level:
        Current branching level.
    :param max_branching_level:
        Maximum branching level the section can grow up to, infinity.
    :param name:
        Section name.
    :param material_list:
        A list of materials for random coloring of the section.
    :param bevel_object:
        A given bevel object to scale the section.
    :param fixed_radius:
        A fixed radius for each sample in the section, or None.
    :param transform:
        Transform from local and circuit coordinates.
    :param repair_morphology:
        Apply some filters to repair the morphology during the poly-line construction.
    :param caps:
        A flag to close the section caps or not.
    :param render_frame:
        A flag to render a progressive frame.
    :param frame_destination:
        The directory where the frame will be dumped.
    :param camera:
        A given camera to render the frame.
    :param ignore_branching_samples:
        Ignore fetching the branching samples from the morphology skeleton.
    :param roots_connection:
        How the root sections are connected to the soma.
    """

    # Ignore the drawing if the section is None
    if section is None:
        return

    # Increment the branching level
    branching_level += 1

    # Verify if this is the last section along the arbor or not
    is_last_section = False
    if not section.has_children():
        is_last_section = True

    # Verify if this a continuous section or not
    is_continuous = True
    if len(poly_line_data) == 0:
        is_continuous = False
        secondary_sections.append(section)

    # Get a list of all the poly-line that corresponds to the given section
    section_data = get_section_poly_line(section=section)

    # Extend the polyline samples for final mesh building
    poly_line_data.extend(section_data)

    # If the section does not have any children, then draw the section and clean the
    # poly_line_data list
    if not section.has_children():

        # Section name
        section_name = '%s_%d' % (name, section.index)

        # Draw the section
        section_object = draw_section_from_poly_line_data(
            data=poly_line_data, name=section_name,
            bevel_object=bevel_object, caps=caps)

        # Add the section object to the sections_objects list
        sections_objects.append(section_object)

        # Clean the polyline samples list
        poly_line_data[:] = []

        # If no more branching is required, then exit the loop
        return

    # Iterate over the children sections and draw them, if any
    for child in section.children:

        # Draw the children sections
        draw_connected_sections(
            section=child, name=name, poly_line_data=poly_line_data,
            sections_objects=sections_objects, secondary_sections=secondary_sections,
            branching_level=branching_level, bevel_object=bevel_object, caps=caps)


####################################################################################################
# @resample_samples_list_adaptively
####################################################################################################
def resample_samples_list_adaptively(samples):

    """Re-samples a list of samples adaptively.

    :param samples:
        A list of samples to be re-sampled.
    """

    # If the section has no samples, ignore this filter and return
    if len(samples) < 4:
        return

    # The section has more than three samples, then it can be re-sampled, but never remove
    # the first or the last samples

    i = 0
    while True:

        # Just keep the last sample of the branch just in case
        if i < len(samples) - 2:

            sample_1 = samples[i]
            sample_2 = samples[i + 1]

            # Segment length
            segment_length = (sample_2.point - sample_1.point).length

            # If the distance between the two samples if less than the radius of the first
            # sample remove the second sample
            if segment_length < sample_1.radius + sample_2.radius:
                samples.remove(samples[i + 1])
                i = 0
            else:
                i += 1

        # No more samples to process, break please
        else:
            break


####################################################################################################
# @resample_section_adaptively
####################################################################################################
def resample_section_adaptively(section):
    """Re-samples the sections adaptively based on the radii of each sample and the distance between
    each two consecutive samples.

    :param section:
        A given section to resample.
    """

    return resample_samples_list_adaptively(section.samples)


def update_samples(section, index=0):

    # If this section is root
    if section.is_root():
        for sample in section.samples:
            sample.index = index
            index += 1

    # If this section is not root
    else:

        # If the section has a single parent, then the first sample of the section has the same
        # index of the last sample of that parent
        if section.has_single_parent():
            section.samples[0].index = section.parents[0].samples[-1].index

        # Otherwise, the section has more than a single parent (loop)
        else:
            pass




def update_samples_indices_globally(section,
                                    index=0):

    # reset the visiting state

    # if root
    if section.is_root():
        for sample in section.samples:
            sample.global_index = index
            index = index + 1

    # if not root
    else:

        # if the section is not root, then it might have one parent or more

        # the section has a single parent
        if section.has_single_parent():
            section.samples[0].global_index = section.parents[0].samples[-1].global_index

        else:
            pass




        section.samples[0].global_index = section.parents[0].samples[-1].global_index

        index = index + 1
        for i in range(1, len(section.samples)):
            pass



    # indexing
    for sample in section.samples:
        sample.global_index = index
        index = index + 1





