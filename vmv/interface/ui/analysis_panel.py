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

        # Counts
        results_area.label(text='Structure')
        results_area.prop(scene, 'NumberUniqueSamples')
        results_area.prop(scene, 'NumberSamples')
        results_area.prop(scene, 'NumberSegments')
        results_area.prop(scene, 'NumberSections')
        results_area.prop(scene, 'NumberSectionsWithOneSegment')
        results_area.prop(scene, 'MinimumNumberSamplerPerSection')
        results_area.prop(scene, 'MaximumNumberSamplerPerSection')
        results_area.prop(scene, 'MeanNumberSamplerPerSection')
        results_area.prop(scene, 'NumberShortSections')


        # Radius analysis
        results_area.label(text='Radius Analysis')
        results_area.prop(scene, 'MinimumSampleRadius')
        results_area.prop(scene, 'MinimumNonZeroSampleRadius')
        results_area.prop(scene, 'MaximumSampleRadius')
        results_area.prop(scene, 'MeanSampleRadius')
        results_area.prop(scene, 'GlobalSampleRadiusRatio')
        results_area.prop(scene, 'GlobalSampleRadiusRatioFactor')
        results_area.prop(scene, 'NumberZeroRadiusSamples')

        # Length analysis
        results_area.label(text='Length Analysis')
        results_area.prop(scene, 'TotalLength')
        results_area.prop(scene, 'MinimumSegmentLength')
        results_area.prop(scene, 'SmallestSegmentLength')
        results_area.prop(scene, 'MaximumSegmentLength')
        results_area.prop(scene, 'MeanSegmentLength')
        results_area.prop(scene, 'GlobalSegmentLengthRatio')
        results_area.prop(scene, 'GlobalSegmentLengthRatioFactor')
        results_area.prop(scene, 'NumberZeroLengthSegments')

        results_area.prop(scene, 'MinimumSectionLength')
        results_area.prop(scene, 'SmallestSectionLength')
        results_area.prop(scene, 'MaximumSectionLength')
        results_area.prop(scene, 'MeanSectionLength')
        results_area.prop(scene, 'GlobalSectionLengthRatio')
        results_area.prop(scene, 'GlobalSectionLengthRatioFactor')
        results_area.prop(scene, 'NumberZeroLengthSections')

        # Segment length in X
        results_area.label(text='Segments Orientation Analysis')
        results_area.prop(scene, 'SegmentLengthX')
        results_area.prop(scene, 'SegmentLengthY')
        results_area.prop(scene, 'SegmentLengthZ')

        # Surface Area analysis
        results_area.label(text='Surface Area Analysis')
        results_area.prop(scene, 'TotalSurfaceArea')
        results_area.prop(scene, 'MinimumSegmentSurfaceArea')
        results_area.prop(scene, 'SmallestSegmentSurfaceArea')
        results_area.prop(scene, 'MaximumSegmentSurfaceArea')
        results_area.prop(scene, 'MeanSegmentSurfaceArea')
        results_area.prop(scene, 'GlobalSegmentSurfaceAreaRatio')
        results_area.prop(scene, 'GlobalSegmentSurfaceAreaRatioFactor')
        results_area.prop(scene, 'NumberZeroSurfaceAreaSegments')

        results_area.prop(scene, 'MinimumSectionSurfaceArea')
        results_area.prop(scene, 'SmallestSectionSurfaceArea')
        results_area.prop(scene, 'MaximumSectionSurfaceArea')
        results_area.prop(scene, 'MeanSectionSurfaceArea')
        results_area.prop(scene, 'GlobalSectionSurfaceAreaRatio')
        results_area.prop(scene, 'GlobalSectionSurfaceAreaRatioFactor')
        results_area.prop(scene, 'NumberZeroSurfaceAreaSections')

        # Volume analysis
        results_area.label(text='Volume Analysis')
        results_area.prop(scene, 'TotalVolume')
        results_area.prop(scene, 'MinimumSegmentVolume')
        results_area.prop(scene, 'SmallestSegmentVolume')
        results_area.prop(scene, 'MaximumSegmentVolume')
        results_area.prop(scene, 'MeanSegmentVolume')
        results_area.prop(scene, 'GlobalSegmentVolumeRatio')
        results_area.prop(scene, 'GlobalSegmentVolumeRatioFactor')
        results_area.prop(scene, 'NumberZeroVolumeSegments')

        results_area.prop(scene, 'MinimumSectionVolume')
        results_area.prop(scene, 'SmallestSectionVolume')
        results_area.prop(scene, 'MaximumSectionVolume')
        results_area.prop(scene, 'MeanSectionVolume')
        results_area.prop(scene, 'GlobalSectionVolumeRatio')
        results_area.prop(scene, 'GlobalSectionVolumeRatioFactor')
        results_area.prop(scene, 'NumberZeroVolumeSections')

        # Number of loops
        results_area.prop(scene, 'NumberLoops')

        # Number of components in the morphology
        results_area.prop(scene, 'NumberComponents')


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

        row.operator('vmv.export_analysis_results')

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

        # Just to make the line shorter
        scene = context.scene

        # Counts ###################################################################################
        vmv.logger.info('Structure')


        structure_items = vmv.analysis.compute_structure_analysis_items(
            vmv.interface.MorphologyObject)

        scene.NumberUniqueSamples = structure_items.number_unique_samples
        scene.NumberSamples = structure_items.number_samples
        scene.NumberSegments = structure_items.number_segments
        scene.NumberSections = structure_items.number_sections
        scene.NumberSectionsWithOneSegment = structure_items.number_sections_with_one_segment

        scene.MinimumNumberSamplerPerSection = structure_items.minimum_number_samples_per_section
        scene.MaximumNumberSamplerPerSection = structure_items.maximum_number_samples_per_section
        scene.MeanNumberSamplerPerSection = structure_items.mean_number_samples_per_section
        scene.NumberShortSections = structure_items.number_short_sections

        # Radius ###################################################################################
        r_items = vmv.analysis.compute_radius_analysis_items(
            sections=vmv.interface.MorphologyObject.sections_list)

        # Sample
        scene.MinimumSampleRadius = r_items.minimum_sample_radius
        scene.MinimumNonZeroSampleRadius = r_items.minimum_non_zero_sample_radius
        scene.MaximumSampleRadius = r_items.maximum_sample_radius
        scene.MeanSampleRadius = r_items.mean_sample_radius
        print(scene.MeanSampleRadius)
        scene.GlobalSampleRadiusRatio = r_items.global_sample_radius_ratio
        scene.GlobalSampleRadiusRatioFactor = r_items.global_sample_radius_ratio_factor
        scene.NumberZeroRadiusSamples = r_items.number_samples_with_zero_radius


        # Length ###################################################################################
        l_items = vmv.analysis.compute_length_analysis_items(
            sections=vmv.interface.MorphologyObject.sections_list)

        # Total
        scene.TotalLength = l_items.total_morphology_length

        # Segment
        scene.MinimumSegmentLength = l_items.minimum_segment_length
        scene.SmallestSegmentLength = l_items.minimum_non_zero_segment_length
        scene.MaximumSegmentLength = l_items.maximum_segment_length
        scene.MeanSegmentLength = l_items.mean_segment_length
        scene.GlobalSegmentLengthRatio = l_items.global_segment_length_ratio
        scene.GlobalSegmentLengthRatioFactor = l_items.global_segment_length_ratio_factor
        scene.NumberZeroLengthSegments = l_items.number_segments_with_zero_length

        # Section
        scene.MinimumSectionLength = l_items.minimum_section_length
        scene.SmallestSectionLength = l_items.minimum_non_zero_section_length
        scene.MaximumSectionLength = l_items.maximum_section_length
        scene.MeanSectionLength = l_items.mean_section_length
        scene.GlobalSectionLengthRatio = l_items.global_section_length_ratio
        scene.GlobalSectionLengthRatioFactor = l_items.global_section_length_ratio_factor
        scene.NumberZeroLengthSections = l_items.number_sections_with_zero_length

        # Surface Area #############################################################################
        sa_items = vmv.analysis.compute_surface_area_analysis_items(
            sections=vmv.interface.MorphologyObject.sections_list)

        # Total
        scene.TotalSurfaceArea = sa_items.total_morphology_surface_area

        # Segment
        scene.MinimumSegmentSurfaceArea = sa_items.minimum_segment_surface_area
        scene.SmallestSegmentSurfaceArea = sa_items.minimum_non_zero_segment_surface_area
        scene.MaximumSegmentSurfaceArea = sa_items.maximum_segment_surface_area
        scene.MeanSegmentSurfaceArea = sa_items.mean_segment_surface_area
        scene.GlobalSegmentSurfaceAreaRatio = sa_items.global_segment_surface_area_ratio
        scene.GlobalSegmentSurfaceAreaRatioFactor = sa_items.global_segment_surface_area_ratio_factor
        scene.NumberZeroSurfaceAreaSegments = sa_items.number_segments_with_zero_surface_area

        # Section
        scene.MinimumSectionSurfaceArea = sa_items.minimum_section_surface_area
        scene.SmallestSectionSurfaceArea = sa_items.minimum_non_zero_section_surface_area
        scene.MaximumSectionSurfaceArea = sa_items.maximum_section_surface_area
        scene.MeanSectionSurfaceArea = sa_items.mean_section_surface_area
        scene.GlobalSectionSurfaceAreaRatio = sa_items.global_section_surface_area_ratio
        scene.GlobalSectionSurfaceAreaRatioFactor = sa_items.global_section_surface_area_ratio_factor
        scene.NumberZeroSurfaceAreaSections = sa_items.number_sections_with_zero_surface_area

        # Volume ###################################################################################
        v_items = vmv.analysis.compute_volume_analysis_items(
            sections=vmv.interface.MorphologyObject.sections_list)

        # Total
        scene.TotalVolume = v_items.total_morphology_volume

        # Segment
        scene.MinimumSegmentVolume = v_items.minimum_segment_volume
        scene.SmallestSegmentVolume = v_items.minimum_non_zero_segment_volume
        scene.MaximumSegmentVolume = v_items.maximum_segment_volume
        scene.MeanSegmentVolume = v_items.mean_segment_volume
        scene.GlobalSegmentVolumeRatio = v_items.global_segment_volume_ratio
        scene.GlobalSegmentVolumeRatioFactor = \
            v_items.global_segment_volume_ratio_factor
        scene.NumberZeroVolumeSegments = v_items.number_segments_with_zero_volume

        # Section
        scene.MinimumSectionVolume = v_items.minimum_section_volume
        scene.SmallestSectionVolume = v_items.minimum_non_zero_section_volume
        scene.MaximumSectionVolume = v_items.maximum_section_volume
        scene.MeanSectionVolume = v_items.mean_section_volume
        scene.GlobalSectionVolumeRatio = v_items.global_section_volume_ratio
        scene.GlobalSectionVolumeRatioFactor = v_items.global_section_volume_ratio_factor
        scene.NumberZeroVolumeSections = v_items.number_sections_with_zero_volume




        # Alignment stats.
        vmv.logger.info('Alignment')
        x_segment_length, y_segment_length, z_segment_length = \
            vmv.analysis.analyze_segments_alignment_length(
                vmv.interface.MorphologyObject.sections_list)
        scene.SegmentLengthX = x_segment_length
        scene.SegmentLengthY = y_segment_length
        scene.SegmentLengthZ = z_segment_length

        vmv.logger.info('Loops')
        number_loops = vmv.analysis.compute_number_of_loops(
            vmv.interface.MorphologyObject.sections_list)
        scene.NumberLoops = number_loops

        vmv.logger.info('Components')
        number_components = vmv.analysis.compute_number_of_components(
            vmv.interface.MorphologyObject.sections_list)
        scene.NumberComponents = number_components

        # Bounding box data
        vmv.logger.info('Bounding box')
        if vmv.interface.MorphologyObject.bounding_box is None:
            vmv.interface.MorphologyObject.bounding_box = \
                vmv.interface.MorphologyObject.compute_bounding_box()
        scene.BBoxCenterX = vmv.interface.MorphologyObject.bounding_box.center[0]
        scene.BBoxCenterY = vmv.interface.MorphologyObject.bounding_box.center[1]
        scene.BBoxCenterZ = vmv.interface.MorphologyObject.bounding_box.center[2]
        scene.BoundsX = vmv.interface.MorphologyObject.bounding_box.bounds[0]
        scene.BoundsY = vmv.interface.MorphologyObject.bounding_box.bounds[1]
        scene.BoundsZ = vmv.interface.MorphologyObject.bounding_box.bounds[2]
        scene.BBoxPMinX = vmv.interface.MorphologyObject.bounding_box.p_min[0]
        scene.BBoxPMinY = vmv.interface.MorphologyObject.bounding_box.p_min[1]
        scene.BBoxPMinZ = vmv.interface.MorphologyObject.bounding_box.p_min[2]
        scene.BBoxPMaxX = vmv.interface.MorphologyObject.bounding_box.p_max[0]
        scene.BBoxPMaxY = vmv.interface.MorphologyObject.bounding_box.p_max[1]
        scene.BBoxPMaxZ = vmv.interface.MorphologyObject.bounding_box.p_max[2]

        # Update the analysis stats.
        analysis_done = time.time()
        scene.MorphologyAnalysisTime = analysis_done - analysis_stated

        # Done
        return {'FINISHED'}


####################################################################################################
# @cExportAnalysisResults
####################################################################################################
class VMV_ExportAnalysisResults(bpy.types.Operator):
    """Export the analysis results into a file"""

    # Operator parameters
    bl_idname = "vmv.export_analysis_results"
    bl_label = "Export Results"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        # Ensure that there is a valid directory where the images will be written to
        if vmv.interface.Options.io.output_directory is None:
            self.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
            return {'FINISHED'}

        if not vmv.file.ops.path_exists(context.scene.VMV_OutputDirectory):
            self.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
            return {'FINISHED'}

        # Verify the output directory
        vmv.interface.validate_output_directory(self)

        # Create the analysis directory if it does not exist
        if not vmv.file.ops.path_exists(vmv.interface.Options.io.analysis_directory):
            vmv.file.ops.clean_and_create_directory(
                vmv.interface.Options.io.analysis_directory)

        # Export the analysis results
        vmv.analysis.export_analysis_results(
            morphology=vmv.interface.MorphologyObject,
            output_directory=vmv.interface.Options.io.analysis_directory)

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

    # Export analysis results button
    bpy.utils.register_class(VMV_ExportAnalysisResults)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # InputOutput data
    bpy.utils.unregister_class(VMV_AnalysisPanel)

    # Analysis button
    bpy.utils.unregister_class(VMV_AnalyzeMorphology)

    # Export analysis results button
    bpy.utils.unregister_class(VMV_ExportAnalysisResults)

