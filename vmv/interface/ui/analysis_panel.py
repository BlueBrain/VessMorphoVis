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
import vmv.analysis


####################################################################################################
# @VMV_AnalysisPanel
####################################################################################################
class VMV_AnalysisPanel(bpy.types.Panel):
    """Analysis panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_label = 'Analysis'
    bl_idname = "OBJECT_PT_VMV_Analysis"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'VessMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self, context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Get a reference to the scene
        scene = context.scene

        # Analyze button
        row = layout.row()
        row.operator('analyze.morphology')

        # Input data options
        input_data_options_row = layout.row()
        input_data_options_row.label(text='Analysis Results:', icon='LIBRARY_DATA_DIRECT')

        # The area where the results will be shown
        results_area = layout.column()

        # Number of samples
        results_area.prop(scene, 'NumberSamples')

        # Minimum sample radius
        results_area.prop(scene, 'MinimumSampleRadius')

        # Maximum sample radius
        results_area.prop(scene, 'MaximumSampleRadius')

        # Average sample radius
        results_area.prop(scene, 'AverageSampleRadius')

        # Number of zero-radius samples
        results_area.prop(scene, 'NumberZeroRadiusSamples')

        # Number of duplicated samples
        results_area.prop(scene, 'NumberDuplicatedSamples')

        # Number of segments
        results_area.prop(scene, 'NumberSegments')

        # Minimum segment length
        results_area.prop(scene, 'MinimumSegmentLength')

        # Maximum segment length
        results_area.prop(scene, 'MaximumSegmentLength')

        # Average segment length
        results_area.prop(scene, 'AverageSegmentLength')

        # Number of sections
        results_area.prop(scene, 'NumberSections')

        # Number of short sections
        results_area.prop(scene, 'NumberShortSections')

        # Number of short sections with two samples
        results_area.prop(scene, 'NumberSectionsWithTwoSamples')

        # Minimum section length
        results_area.prop(scene, 'MinimumSectionLength')

        # Maximum section length
        results_area.prop(scene, 'MaximumSectionLength')

        # Average section length
        results_area.prop(scene, 'AverageSectionLength')

        # Minimum segment length
        results_area.prop(scene, 'MinimumSegmentLength')

        # Maximum segment length
        results_area.prop(scene, 'MaximumSegmentLength')

        # Average segment length
        results_area.prop(scene, 'AverageSegmentLength')

        # Number of loops
        results_area.prop(scene, 'NumberLoops')

        # Number of components in the morphology
        results_area.prop(scene, 'NumberComponents')

        # Morphology total length
        results_area.prop(scene, 'MorphologyTotalLength')

        # Draw the bounding Box
        bounding_box_p_row = layout.row()
        bounding_box_p_min_row = bounding_box_p_row.column(align=True)
        bounding_box_p_min_row.label(text='BBox PMin:')
        bounding_box_p_min_row.prop(scene, 'BBoxPMinX')
        bounding_box_p_min_row.prop(scene, 'BBoxPMinY')
        bounding_box_p_min_row.prop(scene, 'BBoxPMinZ')
        bounding_box_p_min_row.enabled = False

        bounding_box_p_max_row = bounding_box_p_row.column(align=True)
        bounding_box_p_max_row.label(text='BBox PMax:')
        bounding_box_p_max_row.prop(scene, 'BBoxPMaxX')
        bounding_box_p_max_row.prop(scene, 'BBoxPMaxY')
        bounding_box_p_max_row.prop(scene, 'BBoxPMaxZ')
        bounding_box_p_max_row.enabled = False

        bounding_box_data_row = layout.row()
        bounding_box_center_row = bounding_box_data_row.column(align=True)
        bounding_box_center_row.label(text='BBox Center:')
        bounding_box_center_row.prop(scene, 'BBoxCenterX')
        bounding_box_center_row.prop(scene, 'BBoxCenterY')
        bounding_box_center_row.prop(scene, 'BBoxCenterZ')
        bounding_box_center_row.enabled = False

        bounding_box_bounds_row = bounding_box_data_row.column(align=True)
        bounding_box_bounds_row.label(text='BBox Bounds:')
        bounding_box_bounds_row.prop(scene, 'BoundsX')
        bounding_box_bounds_row.prop(scene, 'BoundsY')
        bounding_box_bounds_row.prop(scene, 'BoundsZ')
        bounding_box_bounds_row.enabled = False

        # Disable the editing of the results area since it will be used only for display
        results_area.enabled = False

        # If the morphology is loaded, enable the layout, otherwise make it disabled by default
        if vmv.interface.MorphologyLoaded:
            self.layout.enabled = True

            # Stats
            analysis_stats_row = layout.row()
            analysis_stats_row.label(text='Stats:', icon='RECOVER_LAST')

            loading_time_row = layout.row()
            loading_time_row.prop(scene, 'MorphologyAnalysisTime')
            loading_time_row.enabled = False

        else:
            self.layout.enabled = False


####################################################################################################
# @VMV_AnalyzeMorphology
####################################################################################################
class VMV_AnalyzeMorphology(bpy.types.Operator):
    """Analyze the morphology skeleton"""

    # Operator parameters
    bl_idname = "analyze.morphology"
    bl_label = "Analyze"

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

        vmv.logger.header('Analyzing morphology')
        analysis_stated = time.time()

        # Morphology total length
        vmv.logger.info('Total length')
        morphology_total_length = vmv.analysis.compute_total_morphology_length(
            vmv.interface.MorphologyObject.sections_list)
        context.scene.MorphologyTotalLength = morphology_total_length

        # Total number of samples
        vmv.logger.info('Samples')
        total_number_samples = vmv.analysis.compute_total_number_samples_from_sections_list(
            vmv.interface.MorphologyObject.sections_list)
        context.scene.NumberSamples = total_number_samples

        # Total number of segments
        vmv.logger.info('Segments')
        context.scene.NumberSegments = total_number_samples - 1

        # Total number of sections
        vmv.logger.info('Sections')
        total_number_sections = vmv.analysis.compute_total_number_sections(
            vmv.interface.MorphologyObject.sections_list)
        context.scene.NumberSections = total_number_sections

        # Sections with two samples
        vmv.logger.info('Sections with two samples')
        number_section_with_two_samples = vmv.analysis.compute_number_of_sections_with_two_samples(
            vmv.interface.MorphologyObject.sections_list)
        context.scene.NumberSectionsWithTwoSamples = number_section_with_two_samples

        # Number of short sections
        vmv.logger.info('Short sections')
        number_short_sections = vmv.analysis.compute_number_of_short_sections(
            vmv.interface.MorphologyObject.sections_list)
        context.scene.NumberShortSections = number_short_sections

        # Samples radius stats.
        vmv.logger.info('Radii')
        minimum_sample_radius, maximum_sample_radius, average_sample_radius, zero_radii_sample = \
            vmv.analysis.analyze_samples_radii(vmv.interface.MorphologyObject.sections_list)
        context.scene.MinimumSampleRadius = minimum_sample_radius
        context.scene.MaximumSampleRadius = maximum_sample_radius
        context.scene.AverageSampleRadius = average_sample_radius
        context.scene.NumberZeroRadiusSamples = zero_radii_sample

        vmv.logger.info('Repair Zero-radii')
        vmv.analysis.correct_samples_with_zero_radii(vmv.interface.MorphologyObject.sections_list)

        # Segments length stats.
        vmv.logger.info('Segments lengths')
        minimum_segment_length, maximum_segment_length, average_segment_length = \
            vmv.analysis.analyze_segments_length(vmv.interface.MorphologyObject.sections_list)
        context.scene.MinimumSegmentLength = minimum_segment_length
        context.scene.MaximumSegmentLength = maximum_segment_length
        context.scene.AverageSegmentLength = average_segment_length

        # Section length stats.
        vmv.logger.info('Sections lengths')
        minimum_section_length, maximum_section_length, average_section_length = \
            vmv.analysis.analyze_sections_length(vmv.interface.MorphologyObject.sections_list)
        context.scene.MinimumSectionLength = minimum_section_length
        context.scene.MaximumSectionLength = maximum_section_length
        context.scene.AverageSectionLength = average_section_length

        vmv.logger.info('Loops')
        number_loops = vmv.analysis.compute_number_of_loops(
            vmv.interface.MorphologyObject.sections_list)
        context.scene.NumberLoops = number_loops

        vmv.logger.info('Components')
        number_components = vmv.analysis.compute_number_of_components(
            vmv.interface.MorphologyObject.sections_list)
        context.scene.NumberComponents = number_components

        # Bounding box data
        vmv.logger.info('Bounding box')
        if vmv.interface.MorphologyObject.bounding_box is None:
            vmv.interface.MorphologyObject.bounding_box = \
                vmv.interface.MorphologyObject.compute_bounding_box()
        context.scene.BBoxCenterX = vmv.interface.MorphologyObject.bounding_box.center[0]
        context.scene.BBoxCenterY = vmv.interface.MorphologyObject.bounding_box.center[1]
        context.scene.BBoxCenterZ = vmv.interface.MorphologyObject.bounding_box.center[2]
        context.scene.BoundsX = vmv.interface.MorphologyObject.bounding_box.bounds[0]
        context.scene.BoundsY = vmv.interface.MorphologyObject.bounding_box.bounds[1]
        context.scene.BoundsZ = vmv.interface.MorphologyObject.bounding_box.bounds[2]
        context.scene.BBoxPMinX = vmv.interface.MorphologyObject.bounding_box.p_min[0]
        context.scene.BBoxPMinY = vmv.interface.MorphologyObject.bounding_box.p_min[1]
        context.scene.BBoxPMinZ = vmv.interface.MorphologyObject.bounding_box.p_min[2]
        context.scene.BBoxPMaxX = vmv.interface.MorphologyObject.bounding_box.p_max[0]
        context.scene.BBoxPMaxY = vmv.interface.MorphologyObject.bounding_box.p_max[1]
        context.scene.BBoxPMaxZ = vmv.interface.MorphologyObject.bounding_box.p_max[2]

        # Update the analysis stats.
        analysis_done = time.time()
        context.scene.MorphologyAnalysisTime = analysis_done - analysis_stated

        # Done
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # InputOutput data
    bpy.utils.register_class(VMV_AnalysisPanel)

    # Analysis button
    bpy.utils.register_class(VMV_AnalyzeMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # InputOutput data
    bpy.utils.unregister_class(VMV_AnalysisPanel)

    # Analysis button
    bpy.utils.unregister_class(VMV_AnalyzeMorphology)
