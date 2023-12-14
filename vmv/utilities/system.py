####################################################################################################
# Copyright (c) 2016 - 2023, EPFL / Blue Brain Project
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
import subprocess
import importlib


####################################################################################################
# @command_exists
####################################################################################################
def command_exists(name):
    """Checks if a given command exists or not.

    :param name:
        Command.
    :return:
        True of False.
    """

    try:
        devnull = open(os.devnull)
        subprocess.Popen([name], stdout=devnull, stderr=devnull).communicate()
    except OSError as e:
        return False
    return True


####################################################################################################
# @import_module
####################################################################################################
def import_module(module_name: str,
                  warn_me_if_unavailable=False):
    """Imports a "non-standard" module into the code. It checks if the module is available in the
    running Python environment or not and then returns a reference to the module if it is installed,
    otherwise it returns None to allow the user to know that this module is not installed on the
    system. A warning messages is optional if the module is unavailable.

    Parameters
    ----------
    module_name :
        The name of the module given as a string.
    warn_me_if_unavailable :
        If this flag is set to True, a warning message will be printed.

    Returns
    -------
        This function returns a reference to the module if it is installed, None otherwise.
    """

    try:
        return importlib.import_module(module_name)
    except ImportError:
        if warn_me_if_unavailable:
            print('The module [ %s ] is not installed in this python environment' % module_name)
        return None
