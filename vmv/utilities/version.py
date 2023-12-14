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
import os


####################################################################################################
# @get_blender_version
####################################################################################################
def get_blender_version():
    """Gets the version of the running Blender application."""

    import bpy
    return bpy.app.version


####################################################################################################
# @get_blender_version_string
####################################################################################################
def get_blender_version_string():
    """Gets the version of the running Blender application as a string."""

    # Return the version as a string
    version = get_blender_version()
    return '%s_%s_%s' % (str(version[0]), str(version[1]), str(version[2]))


####################################################################################################
# @is_blender
####################################################################################################
def is_blender(major,
               minor,
               patch):
    """Verifies if the given Blender version has at least the version indicated by the
        (major, minor, patch) combination.

    :param major:
        The major revision.
    :param minor:
        The minor revision.
    :param patch:
        The patch revision.
    :return:
        True if the running Blender has at least the version indicated by the
        (major, minor, patch), False otherwise.
    """

    if get_blender_version() >= (major, minor, patch):
        return True
    return False


####################################################################################################
# @is_blender_279
####################################################################################################
def is_blender_279():
    return is_blender(2, 79, 0)


####################################################################################################
# @is_blender_280
####################################################################################################
def is_blender_280():
    return is_blender(2, 80, 0)


####################################################################################################
# @is_blender_281
####################################################################################################
def is_blender_281():
    return is_blender(2, 81, 0)


####################################################################################################
# @is_blender_282
####################################################################################################
def is_blender_282():
    return is_blender(2, 82, 0)


####################################################################################################
# @is_blender_283
####################################################################################################
def is_blender_283():
    return is_blender(2, 83, 0)


####################################################################################################
# @is_blender_290
####################################################################################################
def is_blender_290():
    return is_blender(2, 90, 0)


####################################################################################################
# @is_blender_291
####################################################################################################
def is_blender_291():
    return is_blender(2, 91, 0)


####################################################################################################
# @is_blender_292
####################################################################################################
def is_blender_292():
    return is_blender(2, 92, 0)


####################################################################################################
# @is_blender_293
####################################################################################################
def is_blender_293():
    return is_blender(2, 93, 0)


####################################################################################################
# @is_blender_30
####################################################################################################
def is_blender_3():
    return is_blender(3, 0, 0)


####################################################################################################
# @is_blender_31
####################################################################################################
def is_blender_31():
    return is_blender(3, 1, 0)


####################################################################################################
# @is_blender_32
####################################################################################################
def is_blender_32():
    return is_blender(3, 2, 0)


####################################################################################################
# @is_blender_33
####################################################################################################
def is_blender_33():
    return is_blender(3, 3, 0)


####################################################################################################
# @is_blender_34
####################################################################################################
def is_blender_34():
    return is_blender(3, 4, 0)


####################################################################################################
# @is_blender_35
####################################################################################################
def is_blender_35():
    return is_blender(3, 5, 0)


####################################################################################################
# @is_blender_36
####################################################################################################
def is_blender_36():
    return is_blender(3, 6, 0)


####################################################################################################
# @is_blender_36
####################################################################################################
def is_blender_40():
    return is_blender(4, 0, 0)


####################################################################################################
# @get_vmv_version
####################################################################################################
def get_vmv_version():
    """Gets the current VessMorphoVis version.

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

