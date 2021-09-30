####################################################################################################
# Copyright (c) 2019 - 2021, EPFL / Blue Brain Project
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
import sys, os

# Internal imports
import vmv


####################################################################################################
# @create_morphology_reader
####################################################################################################
def create_morphology_reader(morphology_file_path):
    """Creates a morphology reader based on the extension.

    :param morphology_file_path:
        Morphology file path.
    :return:
        A reader object. 
    """

    # Get the extension from the file path
    morphology_prefix, morphology_extension = os.path.splitext(morphology_file_path)

    # If it is a .h5 file, use the MorphIO loader
    if '.h5' in morphology_extension:
        return vmv.file.readers.MorphIOLoader(morphology_file=morphology_file_path)

    # If it is a .h5 file, use the MorphIO loader
    elif '.swc' in morphology_extension:
        return vmv.file.readers.SWCLoader(morphology_file=morphology_file_path)

    # If it is a .vmv file, use the VMVReader
    elif '.vmv' in morphology_extension:
        return vmv.file.readers.VMVReader(vmv_file=morphology_file_path)

    else:
        # Issue an error, wrong extension
        vmv.logger.log('ERROR: The morphology extension [%s] is NOT SUPPORTED' %
                       morphology_extension)
        return None

