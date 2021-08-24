####################################################################################################
# Copyright (c) 2018 - 2020, EPFL / Blue Brain Project
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
# Paths
####################################################################################################
class Paths:
    """Paths constants
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # The folder where the data is stored
    DATA_FOLDER = 'data'

    # The folder where the images will be generated
    IMAGES_FOLDER = 'images'

    # The folder where the output morphologies will be generated
    MORPHOLOGIES_FOLDER = 'morphologies'

    # The folder where the meshes will be generated
    MESHES_FOLDER = 'meshes'

    # The folder where the sequences will be generated
    SEQUENCES_FOLDER = 'sequences'

    # The folder where the stats. will be generated
    STATS_FOLDER = 'stats'

    # The folder where the analysis files will be generated
    ANALYSIS_FOLDER = 'analysis'

    # The folder where SLURM files will be generated
    SLURM_FOLDER = 'slurm'

    # The folder where SLURM jobs will be generated
    SLURM_JOBS_FOLDER = '%s/jobs' % SLURM_FOLDER

    # The folder where SLURM log files will be generated
    SLURM_LOGS_FOLDER = '%s/logs' % SLURM_FOLDER

    # Keep a reference to the current directory
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # The directory where all the fonts will be loaded from
    FONTS_DIRECTORY = '%s/../../data/fonts' % current_directory

    # Images path
    IMAGES_PATH = '%s/../../data/images' % current_directory
