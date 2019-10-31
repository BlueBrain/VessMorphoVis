####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
# Image
####################################################################################################
class Image:
    """Image constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Minimum image resolution (for sliders)
    MIN_RESOLUTION = 256

    # Maximum image resolution (for sliders)
    MAX_RESOLUTION = 10240

    # Default resolution
    DEFAULT_RESOLUTION = 1024

    # Default number of samples per pixels
    DEFAULT_SAMPLES_PER_PIXELS = 32

    # Samples per pixel in case of emission shader
    SAMPLES_PER_PIXELS_EMISSION_SHADER = 2

    # Default image scale factor
    DEFAULT_IMAGE_SCALE_FACTOR = 1.0

    # Minimum image scale factor
    MIN_IMAGE_SCALE_FACTOR = 0.1

    # Maximum image scale factor
    MAX_IMAGE_SCALE_FACTOR = 25.0

    # Default full view resolution
    FULL_VIEW_RESOLUTION = 1024

    # Default close up view resolution
    CLOSE_UP_RESOLUTION = 512

    # Default close up dimensions (in microns)
    CLOSE_UP_DIMENSIONS = 20

    # The bounding box increment that will clean the edges around the images
    GAP_DELTA = 5.0
