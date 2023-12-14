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


####################################################################################################
# @EdgeSection
####################################################################################################
class EdgeSection:
    """The EdgeSection represents a simplified (or reduced) representation of the @Section. It
    represents the section as an edge with two "terminal" points only. It simplifies constructing
    the connectivity between the sections using edge-based operations."""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 index,
                 sample_1,
                 sample_2):
        """Constructor

        Parameters
        ----------
        index :
            The index of the edge section. It MUST be similar to that of the original section.
        sample_1 :
            The first sample of the edge (first terminal sample of the section @.samples[0].
        sample_2 :
            The second sample of the edge (last terminal sample of the section @.samples[-1].
        """

        # The index of the section
        self.index = index

        # The first sample of the edge (first terminal sample of the section @.samples[0]
        self.sample_1 = sample_1

        # The second sample of the edge (last terminal sample of the section @.samples[-1]
        self.sample_2 = sample_2
