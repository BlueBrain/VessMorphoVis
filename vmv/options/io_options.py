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


####################################################################################################
# @IOOptions
####################################################################################################
class IOOptions:
    """Input / Output options.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # INPUT OPTIONS ############################################################################
        # The path to the morphology file
        self.file_path = None

        # OUTPUT OPTIONS ###########################################################################
        # The root output directory where the results will be generated
        self.output_directory = None

        # Images directory, where the images will be rendered
        self.images_directory = None

        # Sequences directory, where the movies will be rendered
        self.sequences_directory = None

        # Meshes directory, where the reconstructed meshes will be saved
        self.meshes_directory = None

        # Morphologies directory, where the repaired morphologies will be saved
        self.morphologies_directory = None

        # Analysis directory, where the analysis reports will be saved
        self.analysis_directory = None

        # Center the loaded morphology from the file at the origin upon loading it
        self.center_morphology_at_origin = False

        # Re-sampling the input morphology
        self.resample_morphology = False
