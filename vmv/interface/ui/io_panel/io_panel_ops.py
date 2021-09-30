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

# Internal imports
import vmv.file
from .io_panel_options import *


####################################################################################################
# @add_input_options
####################################################################################################
def add_input_options(layout,
                      scene,
                      options):
    """Adds the input options to the panel.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Input data options
    input_data_row = layout.row()
    input_data_row.label(text='Input Data', icon='LIBRARY_DATA_DIRECT')

    # Input morphology file
    morphology_file_row = layout.row()
    morphology_file_row.prop(scene, 'VMV_MorphologyFile')
    options.io.file_path = scene.VMV_MorphologyFile

    # Get the morphology file path, name and label from the given morphology file
    options.morphology.file_path = scene.VMV_MorphologyFile
    options.morphology.file_name = vmv.file.get_file_name_from_path(scene.VMV_MorphologyFile)
    options.morphology.label = options.morphology.file_name

    # Center the morphology at the origin
    centering_check_box = layout.row()
    centering_check_box.prop(scene, 'VMV_CenterMorphologyAtOrigin')
    options.io.center_morphology_at_origin = scene.VMV_CenterMorphologyAtOrigin

    # Center the morphology at the origin
    resampling_check_box = layout.row()
    resampling_check_box.prop(scene, 'VMV_ResampleMorphology')
    options.io.resample_morphology = scene.VMV_ResampleMorphology

    # Loading button
    loading_button_row = layout.row()
    loading_button_row.operator('load.morphology', icon='LIBRARY_DATA_DIRECT')


####################################################################################################
# @add_output_options
####################################################################################################
def add_output_options(layout,
                       scene,
                       options):
    """Adds the output options to the panel.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # A list that contains all the UI elements that are either shown or hidden
    show_hide_elements = list()

    # Output options
    output_data_options = layout.row()
    output_data_options.label(text='Output Options', icon='NEWFOLDER')
    show_hide_elements.append(output_data_options)

    # Output directory
    output_directory_row = layout.row()
    output_directory_row.prop(scene, 'VMV_OutputDirectory')
    options.io.output_directory = scene.VMV_OutputDirectory
    show_hide_elements.append(output_directory_row)

    # Default paths
    default_paths_row = layout.row()
    default_paths_row.prop(scene, 'VMV_DefaultArtifactsRelativePath')
    show_hide_elements.append(default_paths_row)

    # Output directories
    output_paths_column = layout.column()
    show_hide_elements.append(output_paths_column)

    # Images path
    output_paths_column.prop(scene, 'VMV_ImagesPath')
    options.io.images_directory = '%s/%s' % (scene.VMV_OutputDirectory, scene.VMV_ImagesPath)

    # Sequences path
    output_paths_column.prop(scene, 'VMV_SequencesPath')
    options.io.sequences_directory = '%s/%s' % (scene.VMV_OutputDirectory, scene.VMV_SequencesPath)

    # Meshes path
    output_paths_column.prop(scene, 'VMV_MeshesPath')
    options.io.meshes_directory = '%s/%s' % (scene.VMV_OutputDirectory, scene.VMV_MeshesPath)

    # Morphologies path
    output_paths_column.prop(scene, 'VMV_MorphologiesPath')
    options.io.morphologies_directory = '%s/%s' % (scene.VMV_OutputDirectory,
                                                   scene.VMV_MorphologiesPath)

    # Analysis path
    output_paths_column.prop(scene, 'VMV_AnalysisPath')
    options.io.analysis_directory = '%s/%s' % (scene.VMV_OutputDirectory, scene.VMV_AnalysisPath)

    # If the morphology is loaded, then show the elements, otherwise, hide them
    if vmv.interface.MorphologyLoaded:
        for element in show_hide_elements:
            element.enabled = True
    else:
        for element in show_hide_elements:
            element.enabled = False

    # Disable the default paths selection if the use default paths flag is set
    if scene.VMV_DefaultArtifactsRelativePath:
        output_paths_column.enabled = False


####################################################################################################
# @add_file_content_summary
####################################################################################################
def add_file_content_summary(layout,
                             scene):
    """Adds the file content summary to the panel.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    """

    # File summary
    row = layout.row()
    row.label(text='File Summary', icon='BORDERMOVE')

    # Just put them all in a single column
    column = layout.column()

    # File name
    column.prop(scene, 'VMV_MorphologyName')

    # Total number of samples
    column.prop(scene, 'VMV_NumberMorphologySamples')

    # Total number of sections
    column.prop(scene, 'VMV_NumberMorphologySections')

    # Number of steps for radius variations, if zero, the file doesn't have any variations
    column.prop(scene, 'VMV_RadiusVariationsSteps')

    # Number of steps for flow variations, if zero, the file doesn't have any variations
    column.prop(scene, 'VMV_FlowVariationsSteps')

    # Number of steps for pressure variations, if zero, the file doesn't have any variations
    column.prop(scene, 'VMV_PressureVariationsSteps')
    column.enabled = False


####################################################################################################
# @add_statistics
####################################################################################################
def add_statistics(layout,
                   scene):
    """Adds the morphology loading statistics to the panel.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    """

    # Stats
    morphology_stats_row = layout.row()
    morphology_stats_row.label(text='Stats', icon='RECOVER_LAST')

    # Loading time
    loading_time_row = layout.row()
    loading_time_row.prop(scene, 'VMV_MorphologyLoadingTime')
    loading_time_row.enabled = False

    # Drawing time
    drawing_time_row = layout.row()
    drawing_time_row.prop(scene, 'VMV_MorphologyDrawingTime')
    drawing_time_row.enabled = False
