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

# Internal imports
from .analysis import *
from .consts import *
from .enums import *
from .options import *
from .interface import *
from .scene import *
from .shading import *
from .skeleton import *

# System imports
import sys

# Internal imports
import vmv.file

# Create the logger
logger = vmv.file.Logger()


####################################################################################################
# @kill
####################################################################################################
def kill(option=0):
    """ Kill VessMorphoVis.

    :param option:
        Optional arguments for handling the killing operation to avoid Blender crashes.
    """

    sys.exit(option)
