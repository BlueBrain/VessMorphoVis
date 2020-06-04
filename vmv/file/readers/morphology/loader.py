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

# System imports
import sys, os

# Internal imports
import vmv


####################################################################################################
# @read_h5_morphology
####################################################################################################
def read_h5_morphology(h5_file):
    """Verifies if the given path is valid or not and then loads a .h5 morphology file according
    to the common standard specified by the BBP team.

    If the path is not valid, this function returns None.

    :param h5_file:
        Path to the H5 morphology file.
    :return:
        A morphology object or None if the path is not valid.
    """

    # If the path is valid
    if os.path.isfile(h5_file):

        # Load the .h5 morphology
        reader = vmv.file.readers.H5Reader(h5_file=h5_file)
        morphology_object = reader.construct_morphology_object()

        # Return a reference to this morphology object
        return morphology_object

    # Issue an error
    vmv.logger.log('ERROR: The morphology path [%s] is invalid' % h5_file)

    # Otherwise, return None
    return None


####################################################################################################
# @read_mat_morphology
####################################################################################################
def read_mat_morphology(mat_file):
    """Verifies if the given path is valid or not and then loads a .mat morphology file according
    to the common standard specified by the BBP team.

    If the path is not valid, this function returns None.

    :param mat_file:
        Path to the .mat morphology file.
    :return:
        A morphology object or None if the path is not valid.
    """

    # If the path is valid
    if os.path.isfile(mat_file):

        # Load the .h5 morphology
        reader = vmv.file.readers.MATReader(mat_file=mat_file)
        morphology_object = reader.construct_morphology_object()

        # Return a reference to this morphology object
        return morphology_object

    # Issue an error
    vmv.logger.log('ERROR: The morphology path [%s] is invalid' % mat_file)

    # Otherwise, return None
    return None


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

    # If it is a .mat file, use the Matlab loader
    elif '.mat' in morphology_extension:
        return vmv.file.readers.MATReader(mat_file=morphology_file_path)

    # If it is a .vmv file, use the VMVReader
    elif '.vmv' in morphology_extension:
        return vmv.file.readers.VMVReader(vmv_file=morphology_file_path)

    else:
        # Issue an error, wrong extension
        vmv.logger.log('ERROR: The morphology extension [%s] is NOT SUPPORTED' %
                       morphology_extension)
        return None


####################################################################################################
# @read_morphology_from_file
####################################################################################################
def read_morphology_from_file(options):
    """Loads a morphology object from file. This loader mainly supports .h5 file format.

    :param options:
        A reference to the system options.
    :return:
        Morphology object and True (if the morphology is loaded) or False (if the something is
        wrong).
    """

    # The morphology file path is available from the system options
    morphology_file_path = options.morphology.morphology_file_path

    # Get the extension from the file path
    morphology_prefix, morphology_extension = os.path.splitext(morphology_file_path)

    # If it is a .h5 file, use the h5 loader
    if '.h5' in morphology_extension:

        # Load the .h5 file
        try:
            morphology_object = read_h5_morphology(morphology_file_path)

        # Cannot read the file for some reason
        except ValueError:
            vmv.logger.log('ERROR: The morphology file [%s] could NOT be read' %
                           morphology_file_path)
            return False, None

    # If it is a .mat file, use the Matlab loader
    elif '.mat' in morphology_extension:

        # Load the .mat file
        try:
            morphology_object = read_mat_morphology(morphology_file_path)

        # Cannot read the file for some reason
        except ValueError:
            vmv.logger.log('ERROR: The morphology file [%s] could NOT be read' %
                           morphology_file_path)
            return False, None
    else:

        # Issue an error, wrong extension
        vmv.logger.log('ERROR: The morphology extension [%s] is NOT SUPPORTED' %
                       morphology_extension)
        return False

    # If the morphology object is None, return False
    if morphology_object is None:
        return False, None

    # The morphology file was loaded successfully
    return True, morphology_object
