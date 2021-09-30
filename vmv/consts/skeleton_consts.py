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
# @Skeleton
####################################################################################################
class Skeleton:
    """Skeleton constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Maximum branching order
    MAX_BRANCHING_ORDER = 1000

    # The index of the sample index in an SWC file
    SWC_SAMPLE_INDEX_IDX = 0

    # The index of the type of a sample in an SWC file
    SWC_SAMPLE_TYPE_IDX = 1

    # The index of the x-coordinates of a sample in an SWC file
    SWC_SAMPLE_X_COORDINATES_IDX = 2

    # The index of the y-coordinates of a sample in an SWC file
    SWC_SAMPLE_Y_COORDINATES_IDX = 3

    # The index of the z-coordinates of a sample in an SWC file
    SWC_SAMPLE_Z_COORDINATES_IDX = 4

    # The index of the radius of a sample in an SWC file
    SWC_SAMPLE_RADIUS_IDX = 5

    # The index of the parent index of a sample in an SWC file
    SWC_SAMPLE_PARENT_INDEX_IDX = 6

    # The index of a sample that has no parent in an SWC file
    SWC_NO_PARENT_SAMPLE_TYPE = -1

    # The index of an undefined samples in an SWC file
    SWC_UNDEFINED_SAMPLE_TYPE = 0

    # The index of a soma sample in an SWC file
    SWC_SOMA_SAMPLE_TYPE = 1

    # the index of an axon sample in an SWC file
    SWC_AXON_SAMPLE_TYPE = 2

    # The index of a basal dendrite sample in an SWC file
    SWC_BASAL_DENDRITE_SAMPLE_TYPE = 3

    # The index of an apical dendrite sample in an SWC file
    SWC_APICAL_DENDRITE_SAMPLE_TYPE = 4

    # The index of a fork point sample (bi- or trifurcation)
    SWC_FORK_POINT_SAMPLE_TYPE = 5

    # The index of an end point sample in an SWC file
    SWC_END_POINT_SAMPLE_TYPE = 6

    # The index of a custom sample in an SWC file
    SWC_CUSTOM_SAMPLE_TYPE = 7
