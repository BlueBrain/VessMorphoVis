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
import time

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.builders
import vmv.enums
import vmv.utilities
import vmv.scene


####################################################################################################
# @VMVIOPanel
####################################################################################################
class VMVIOPanel(bpy.types.Panel):
    """Input and output data panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_category = 'VessMorphoVis'
    bl_label = 'Input / Output'
    bl_idname = "OBJECT_PT_VMV_IO"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # A list of layout rows/columns to show and hide based on the status of the morphology
        show_hide_elements = list()

        # Get a reference to the panel layout
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene

        # Input data options
        input_data_options_row = layout.row()
        input_data_options_row.label(text='Input Data:', icon='LIBRARY_DATA_DIRECT')

        # Input morphology file
        morphology_file_row = layout.row()
        morphology_file_row.prop(scene, 'MorphologyFile')
        vmv.interface.options.io.morphology_file_path = scene.MorphologyFile

        # Get the morphology file path, name and label from the given morphology file
        vmv.interface.options.morphology.morphology_file_path = scene.MorphologyFile
        vmv.interface.options.morphology.morphology_file_name = \
            vmv.file.get_file_name_from_path(scene.MorphologyFile)
        vmv.interface.options.morphology.label = \
            vmv.file.get_file_name_from_path(scene.MorphologyFile)

        # Center the morphology at the origin
        morphology_centering_check_box = layout.row()
        morphology_centering_check_box.prop(scene, 'CenterMorphologyAtOrigin')
        vmv.interface.options.io.center_morphology_at_origin = scene.CenterMorphologyAtOrigin

        # Center the morphology at the origin
        morphology_resampling_check_box = layout.row()
        morphology_resampling_check_box.prop(scene, 'ResampleMorphology')
        vmv.interface.options.io.resample_morphology = scene.ResampleMorphology

        loading_button_row = layout.row()
        loading_button_row .operator('load.morphology', icon='LIBRARY_DATA_DIRECT')

        # Output options
        output_data_options_row = layout.row()
        output_data_options_row.label(text='Output Options:', icon='NEWFOLDER')
        show_hide_elements.append(output_data_options_row)

        # Output directory
        output_directory_row = layout.row()
        output_directory_row.prop(scene, 'OutputDirectory')
        vmv.interface.options.io.output_directory = scene.OutputDirectory
        show_hide_elements.append(output_directory_row)

        # Default paths
        default_paths_row = layout.row()
        default_paths_row.prop(scene, 'DefaultArtifactsRelativePath')
        show_hide_elements.append(default_paths_row)

        # Output directories
        output_paths_column = layout.column()
        show_hide_elements.append(output_paths_column)

        # Images path
        output_paths_column.prop(scene, 'ImagesPath')
        vmv.interface.options.io.images_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.ImagesPath)

        # Sequences path
        output_paths_column.prop(scene, 'SequencesPath')
        vmv.interface.options.io.sequences_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.SequencesPath)

        # Meshes path
        output_paths_column.prop(scene, 'MeshesPath')
        vmv.interface.options.io.meshes_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.MeshesPath)

        # Morphologies path
        output_paths_column.prop(scene, 'MorphologiesPath')
        vmv.interface.options.io.morphologies_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.MorphologiesPath)

        # Analysis path
        output_paths_column.prop(scene, 'AnalysisPath')
        vmv.interface.options.io.analysis_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.AnalysisPath)

        if vmv.interface.ui_morphology_loaded:
            for element in show_hide_elements:
                element.enabled = True
        else:
            for element in show_hide_elements:
                element.enabled = False

        # Disable the default paths selection if the use default paths flag is set
        if scene.DefaultArtifactsRelativePath:
            output_paths_column.enabled = False

        # If the morphology is loaded only, print the performance stats.
        if vmv.interface.ui_morphology_loaded:

            # Stats
            morphology_stats_row = layout.row()
            morphology_stats_row.label(text='Stats:', icon='RECOVER_LAST')

            loading_time_row = layout.row()
            loading_time_row.prop(scene, 'MorphologyLoadingTime')
            loading_time_row.enabled = False

            drawing_time_row = layout.row()
            drawing_time_row.prop(scene, 'MorphologyDrawingTime')
            drawing_time_row.enabled = False


####################################################################################################
# @VMVLoadMorphology
####################################################################################################
class VMVLoadMorphology(bpy.types.Operator):
    """Load the morphology"""

    # Operator parameters
    bl_idname = "load.morphology"
    bl_label = "Load"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Executes the operator

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Clear the scene from any existing data
        import vmv
        vmv.logger.header('Loading morphology')
        vmv.scene.clear_scene()

        # Initialize all the operations that needs to run once and for all
        import vmv.interface
        #if not vmv.interface.ui.Globals.nmv_initialized:
        vmv.interface.load_fonts()

        # Extend the clipping planes to be able to visualize larger data sets
        vmv.scene.extend_clipping_planes()

        # Create a morphology reader object
        morphology_reader = vmv.file.create_morphology_reader(
            vmv.interface.options.io.morphology_file_path)

        # Construct a morphology object to be used later by the entire application
        loading_start = time.time()

        vmv.interface.ui.ui_morphology = morphology_reader.construct_morphology_object(
            center_at_origin=vmv.interface.options.io.center_morphology_at_origin,
            resample_morphology=vmv.interface.options.io.resample_morphology)

        # Update the interface
        loading_done = time.time()
        context.scene.MorphologyLoadingTime = loading_done - loading_start
        vmv.logger.info('Morphology loaded in [%f] seconds' % (loading_done - loading_start))

        # Just draw the skeleton as a sign of complete morphology loading
        try:

            # Construct a builder object
            builder = vmv.builders.DisconnectedSectionsBuilder(
                 morphology=vmv.interface.ui.ui_morphology, options=vmv.interface.ui.options)
            builder.build_skeleton()

            # Switch to full view along some axis
            vmv.utilities.view_all_from_projection()

            # Update the viewport shading
            vmv.utilities.update_view_port_shading_to_solid()

            # Show the loading time
            drawing_done = time.time()
            context.scene.MorphologyDrawingTime = drawing_done - loading_done
            vmv.logger.info('Morphology drawn in [%f] seconds' % (drawing_done - loading_done))

            # The morphology is loaded
            vmv.interface.ui_morphology_loaded = True

            # Set back the radii of the morphology to that as specified in the loaded file
            vmv.interface.ui.options.morphology.radii = \
                vmv.enums.Morphology.Radii.AS_SPECIFIED

            # Configure the output directory
            vmv.interface.configure_output_directory(options=vmv.interface.ui.options,
                                                     context=context)

        # Unable to load the morphology
        except ValueError:
            vmv.logger.log('ERROR: Unable to load the morphology file')

            # The morphology is not loaded
            vmv.interface.ui_morphology_loaded = False

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Load the icons
    vmv.interface.load_icons()

    # InputOutput data
    bpy.utils.register_class(VMVIOPanel)
    bpy.utils.register_class(VMVLoadMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # InputOutput data
    bpy.utils.unregister_class(VMVIOPanel)
    bpy.utils.unregister_class(VMVLoadMorphology)

