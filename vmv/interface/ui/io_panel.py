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


# System imports
import time

# Blender imports
import bpy

# Internal imports
import vmv
import vmv.scene


####################################################################################################
# @VMVIOPanel
####################################################################################################
class VMVIOPanel(bpy.types.Panel):
    """Input and output data panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_space_type = 'VIEW_3D'
    #bl_region_type = 'TOOLS'
    #bl_label = 'Input / Output'
    #bl_category = 'VMV'

    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    bl_label = 'Input / Output'
    bl_idname = "OBJECT_PT_IO"
    # bl_category = 'VessMorphoVis'

    bl_category = 'VessMorphoVis'
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    ################################################################################################
    # Panel options
    ################################################################################################
    # Morphology file
    bpy.types.Scene.MorphologyFile = bpy.props.StringProperty(
        name="Morphology File",
        description="Select a specific vasculature morphology to load",
        default='Select File', maxlen=2048,  subtype='FILE_PATH')

    # Morphology directory
    bpy.types.Scene.MorphologyDirectory = bpy.props.StringProperty(
        name="Morphology Directory",
        description="Select a directory to mesh all the morphologies in it",
        default="Select Directory", maxlen=2048, subtype='DIR_PATH')

    # Output directory
    bpy.types.Scene.OutputDirectory = bpy.props.StringProperty(
        name="Output Directory",
        description="Select a directory where the results will be generated",
        default="Select Directory", maxlen=5000, subtype='DIR_PATH')

    # Use default paths for the artifacts
    bpy.types.Scene.DefaultArtifactsRelativePath = bpy.props.BoolProperty(
        name="Use Default Output Paths",
        description="Use the default sub-paths for the artifacts",
        default=True)

    # Images relative path
    bpy.types.Scene.ImagesPath = bpy.props.StringProperty(
        name="Images",
        description="Relative path where the images will be generated",
        default="images", maxlen=1000)

    # Sequences relative path
    bpy.types.Scene.SequencesPath = bpy.props.StringProperty(
        name="Sequences",
        description="Relative path where the sequences will be generated",
        default="sequences", maxlen=1000)

    # Meshes relative path
    bpy.types.Scene.MeshesPath = bpy.props.StringProperty(
        name="Meshes",
        description="Relative path where the sequences will be generated",
        default="meshes", maxlen=1000)

    # Morphologies relative path
    bpy.types.Scene.MorphologiesPath = bpy.props.StringProperty(
        name="Morphologies",
        description="Relative path where the morphologies will be generated",
        default="morphologies", maxlen=1000)

    # Analysis relative path
    bpy.types.Scene.AnalysisPath = bpy.props.StringProperty(
        name="Analysis",
        description="Relative path where the analysis reports will be generated",
        default="analysis", maxlen=1000)

    # Center the loaded morphology at the origin
    bpy.types.Scene.CenterMorphologyAtOrigin = bpy.props.BoolProperty(
        name="Center At Origin",
        description="Center the loaded morphology at the origin",
        default=True)

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
        vmv.interface.ui_options.io.morphology_file_path = scene.MorphologyFile

        # Center the morphology at the origin
        morphology_centering_check_box = layout.row()
        morphology_centering_check_box.prop(scene, 'CenterMorphologyAtOrigin')
        vmv.interface.ui_options.io.center_morphology_at_origin = scene.CenterMorphologyAtOrigin

        loading_button_row = layout.row()
        loading_button_row .operator('load.morphology', icon='LIBRARY_DATA_DIRECT')

        # Output options
        output_data_options_row = layout.row()
        output_data_options_row.label(text='Output Options:', icon='SCRIPT')
        show_hide_elements.append(output_data_options_row)

        # Output directory
        output_directory_row = layout.row()
        output_directory_row.prop(scene, 'OutputDirectory')
        vmv.interface.ui_options.io.output_directory = scene.OutputDirectory
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
        vmv.interface.ui_options.io.images_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.ImagesPath)

        # Sequences path
        output_paths_column.prop(scene, 'SequencesPath')
        vmv.interface.ui_options.io.sequences_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.SequencesPath)

        # Meshes path
        output_paths_column.prop(scene, 'MeshesPath')
        vmv.interface.ui_options.io.meshes_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.MeshesPath)

        # Morphologies path
        output_paths_column.prop(scene, 'MorphologiesPath')
        vmv.interface.ui_options.io.morphologies_directory = \
            '%s/%s' % (scene.OutputDirectory, scene.MorphologiesPath)

        # Analysis path
        output_paths_column.prop(scene, 'AnalysisPath')
        vmv.interface.ui_options.io.analysis_directory = \
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

        # Extend the clipping planes to be able to visualize larger data sets
        vmv.scene.extend_clipping_planes()

        # Create a morphology reader object
        morphology_reader = vmv.file.H5Reader(vmv.interface.ui_options.io.morphology_file_path)

        # Construct a morphology object to be used later by the entire application
        loading_start = time.time()
        vmv.interface.ui.ui_morphology = morphology_reader.construct_morphology_object(
            center_at_origin=vmv.interface.ui_options.io.center_morphology_at_origin)
        loading_done = time.time()
        vmv.logger.info('Morphology loaded in [%f] seconds' % (loading_done - loading_start))

        # Just draw the skeleton as a sign of complete morphology loading
        try:

            import vmv.builders
            import vmv.enums
            # Initially, set the radius to FIXED to represent a center line
            vmv.interface.ui.ui_options.morphology.radii = vmv.enums.Skeletonization.Radii.FIXED
            vmv.interface.ui.ui_options.morphology.sections_fixed_radii_value = 1.0

            # Construct a builder object
            builder = vmv.builders.DisconnectedSectionsBuilder(
                 morphology=vmv.interface.ui.ui_morphology, options=vmv.interface.ui.ui_options)
            builder.build_skeleton()

            # Switch to the top view
            bpy.ops.view3d.view_axis(type='TOP')

            # View all the objects in the scene
            bpy.ops.view3d.view_all()

            # Switch to viewport shading
            area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
            space = next(space for space in area.spaces if space.type == 'VIEW_3D')
            space.shading.type = 'MATERIAL'

            drawing_done = time.time()
            vmv.logger.info('Morphology drawn in [%f] seconds' % (drawing_done - loading_done))

            # The morphology is loaded
            vmv.interface.ui_morphology_loaded = True

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

