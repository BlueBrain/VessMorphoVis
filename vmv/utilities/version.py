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
import sys
import os

# Blender imports
import bpy


####################################################################################################
# @get_blender_version
####################################################################################################
def get_blender_version():
    """Get Blender version.

    :return:
        A list of the version of the running Blender.
    """

    import bpy
    return bpy.app.version


####################################################################################################
# @get_blender_version_string
####################################################################################################
def get_blender_version_string():
    """Gets Blender version as a string.

    :return:
        A string of the version of the running Blender.
    """

    # Get the version list
    version = get_blender_version()

    # Return the version as a string
    return '%s_%s_%s' % (str(version[0]), str(version[1]), str(version[2]))


####################################################################################################
# @is_blender_280
####################################################################################################
def is_blender_280():
    """Checks if the used version of Blender is greater than 2.8 or not.

    :return:
        True if this version of Blender is 2.8 or greater to work with the new API, otherwise False.
    """

    if get_blender_version() >= (2, 80, 0):
        return True
    return False


####################################################################################################
# @get_vmv_version
####################################################################################################
def get_vmv_version():
    """Get VessMorphoVis version.

    :return:
        VessMorphoVis version tuple.
    """

    # Load the version from the version file
    version_file_path = '%s/../../.version' % os.path.dirname(os.path.realpath(__file__))
    version_file = open(version_file_path, 'r')
    version_string = ''
    for line in version_file:
        version_string = line
        break
    version_file.close()

    version = version_string.split(' ')
    return [int(version[0]), int(version[1]), int(version[2])]

