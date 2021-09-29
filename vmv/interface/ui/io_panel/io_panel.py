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

# Internal imports
import vmv.builders
import vmv.enums
import vmv.scene
import vmv.utilities
from .io_panel_ops import *


####################################################################################################
# @VMV_IOPanel
####################################################################################################
class VMV_IOPanel(bpy.types.Panel):
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

        # Add input data options to the panel
        add_input_options(layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # Add the output options to the panel
        add_output_options(layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # Only, if the morphology is loaded
        if vmv.interface.MorphologyLoaded:

            # Add file content summary data to the panel
            add_file_content_summary(layout=self.layout, scene=context.scene)

            # Add loading statistics
            add_statistics(layout=self.layout, scene=context.scene)


####################################################################################################
# @VMV_LoadMorphology
####################################################################################################
class VMV_LoadMorphology(bpy.types.Operator):
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
        if not vmv.interface.SystemInitialized:

            # Load the fonts
            vmv.interface.load_fonts()

            # Extend the clipping planes to be able to visualize larger data sets
            vmv.scene.extend_clipping_planes()

            # VMV is initialized
            vmv.interface.SystemInitialized = True

        # Create a morphology reader object
        morphology_reader = vmv.file.create_morphology_reader(vmv.interface.Options.io.file_path)

        # Construct a morphology object to be used later by the entire application
        loading_start = time.time()

        vmv.interface.MorphologyObject = morphology_reader.construct_morphology_object(
            center_at_origin=vmv.interface.Options.io.center_morphology_at_origin,
            resample_morphology=vmv.interface.Options.io.resample_morphology)

        # Update the interface, morphology name
        context.scene.VMV_MorphologyName = vmv.interface.MorphologyObject.name

        # Update the interface, number of samples
        context.scene.VMV_NumberMorphologySamples = vmv.interface.MorphologyObject.number_samples

        # Update the interface, number of sections
        context.scene.VMV_NumberMorphologySections = vmv.interface.MorphologyObject.number_sections

        # Update the interface
        loading_done = time.time()
        context.scene.VMV_MorphologyLoadingTime = loading_done - loading_start
        vmv.logger.info('Morphology loaded in [%f] seconds' % (loading_done - loading_start))

        # Just draw the skeleton as a sign of complete morphology loading
        try:

            # Construct a builder object
            builder = vmv.builders.SectionsBuilder(morphology=vmv.interface.MorphologyObject,
                                                   options=vmv.interface.Options)
            vmv.interface.MorphologyPolylineObject = builder.build_skeleton()

            # Switch to full view along some axis
            vmv.utilities.view_all_from_projection()

            # Show the loading time
            drawing_done = time.time()
            context.scene.VMV_MorphologyDrawingTime = drawing_done - loading_done
            vmv.logger.info('Morphology drawn in [%f] seconds' % (drawing_done - loading_done))

            # The morphology is loaded
            vmv.interface.MorphologyLoaded = True

            # Set back the radii of the morphology to that as specified in the loaded file
            vmv.interface.Options.morphology.radii = vmv.enums.Morphology.Radii.AS_SPECIFIED

            # Configure the output directory
            vmv.interface.configure_output_directory(options=vmv.interface.Options,
                                                     context=context)

        # Unable to load the morphology
        except ValueError:
            vmv.logger.log('ERROR: Unable to load the morphology file')

            # The morphology is not loaded
            vmv.interface.MorphologyLoaded = False

        # Once loaded, define the options based on the content of the morphology file
        vmv.interface.define_morphology_visualization_type_items()

        # Resetting the simulation loaded flag
        vmv.interface.SimulationLoaded = False

        # Done
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Load the icons
    vmv.interface.load_icons()

    # InputOutput data
    bpy.utils.register_class(VMV_IOPanel)
    bpy.utils.register_class(VMV_LoadMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # InputOutput data
    bpy.utils.unregister_class(VMV_IOPanel)
    bpy.utils.unregister_class(VMV_LoadMorphology)

