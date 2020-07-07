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


####################################################################################################
# PolyLine
####################################################################################################
class PolyLine:
    """Blender poly-lines that are used to represent a section with some parameters.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 samples,
                 color_index):

        # Poly-line samples arranged in the format [(X, Y, Z, 1), R]
        self.samples = samples

        # Poly-line color index to be able to diffrentiate it in other poly-lines in 
        # the same dataset
        self.color_index = color_index


