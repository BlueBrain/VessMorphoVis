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

# Internal imports
import vmv.consts
import vmv.enums


####################################################################################################
# @update_section_parenting
####################################################################################################
def update_section_parenting(section,
                             sections_list):
    """Updates the section parents' and children references.

    :param section:
        A given section to update.
    :param sections_list:
        A list of all the sections in the morphology.
    """

    # Detect if the section has no parent, then set it as a root
    # Use the first sample to identify if this section is a root or not
    if str(section.samples[0].parent_index) == str(-1):

        # This section is a root
        section.parent = None
        section.parent_index = None

    for i_section in sections_list:

        # If this is the same section
        if i_section.index == section.index:

            # Next section
            continue

        # If the last sample along the section has the same index of the first sample of the
        # auxiliary section, then the auxiliary section is a child
        if section.samples[-1].index == i_section.samples[0].index:

            # Add the auxiliary section as a child to the parent section
            section.children.append(i_section)

        # If the first sample along the section has the same index of the last sample of the
        # auxiliary section, then the auxiliary section is a parent
        if section.samples[0].index == i_section.samples[-1].index:

            # Set the auxiliary section to be a parent to this child section
            section.parent = i_section
            section.parent_index = i_section.index


####################################################################################################
# @build_arbors_from_sections
####################################################################################################
def build_arbors_from_sections(sections_list):
    """Returns a list of nodes where we can access the different sections of a single arbor as a
    tree.

    :param sections_list:
        A linear list of sections.
    :return:
        A list containing references to the root nodes of the different arbors in the sections list.
    """

    # If the sections list is None
    if sections_list is None:

        # This is an issue
        vmv.logger.log('ERROR: Invalid sections list')

        # Return None
        return None

    # If the sections list is empty
    if len(sections_list) == 0:

        # Then return None
        return None

    # A list of roots
    roots = list()

    # Iterate over the sections and get the root ones
    for section in sections_list:

        # If the section has no parent, it is a root then
        if section.parent is None:

            # Append this root to the list
            roots.append(section)

    # If the list does not contain any roots, then return None, otherwise return the entire list
    if len(roots) == 0:

        # This might be an issue
        vmv.logger.log('WARNING: No roots found in the sections list')

        # Return None
        return None

    else:

        # Return the root list
        return roots
