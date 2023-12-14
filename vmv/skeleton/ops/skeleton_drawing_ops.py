####################################################################################################
# Copyright (c) 2019 - 2023, EPFL / Blue Brain Project
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

# Blender imports
from mathutils import Vector

# Internal imports
import vmv.geometry


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
                                                    center=(0.0, 0.0, 0.0)):
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
                                                    center=(0.0, 0.0, 0.0)):
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
                                                          center=(0.0, 0.0, 0.0)):

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
                                                      center=(0.0, 0.0, 0.0)):
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

    # Append a '_section' keyword after the section name to be able to recognize it later
    section_name = '%s_section' % name

    # Draw the section from the given data in poly-line format
    section_object = vmv.geometry.draw_poly_line(
        poly_line_data=data, name=section_name, material=material, color=color,
        bevel_object=bevel_object, caps=caps)

    # Return a reference to the drawn section object
    return section_object


