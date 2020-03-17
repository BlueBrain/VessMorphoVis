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
import vmv
import vmv.analysis


####################################################################################################
# @VMVAnalysisPanel
####################################################################################################
class VMVAnalysisPanel(bpy.types.Panel):
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
    # Analysis items
    ################################################################################################
    # Total morphology length
    bpy.types.Scene.MorphologyTotalLength = bpy.props.FloatProperty(
        name="Total Length",
        description="The total length of the morphology skeleton",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Number of samples
    bpy.types.Scene.NumberSamples = bpy.props.IntProperty(
        name="Total # Samples",
        description="The total number of samples in the morphology skeleton",
        default=0, subtype='FACTOR')

    # Number of segments
    bpy.types.Scene.NumberSegments = bpy.props.IntProperty(
        name="Total # Segments",
        description="The total number of segments in the morphology skeleton",
        default=0,  subtype='FACTOR')

    # Number of sections
    bpy.types.Scene.NumberSections = bpy.props.IntProperty(
        name="Total # Sections",
        description="The total number of sections in the morphology skeleton",
        default=0, subtype='FACTOR')

    # Number of sections with two samples only
    bpy.types.Scene.NumberSectionsWithTwoSamples = bpy.props.IntProperty(
        name="# Sections with 2 Samples",
        description="The number of sections that have only two samples",
        default=0, subtype='FACTOR')

    # Number of loops
    bpy.types.Scene.NumberLoops = bpy.props.IntProperty(
        name="Total # Loops",
        description="The total number of loops in the morphology skeleton",
        default=0, subtype='FACTOR')

    # Number of components
    bpy.types.Scene.NumberComponents = bpy.props.IntProperty(
        name="# Components",
        description="The number of components of separate structures in the morphology skeleton",
        default=0, subtype='FACTOR')

    # Minimum sample radius
    bpy.types.Scene.MinimumSampleRadius = bpy.props.FloatProperty(
        name="Min. Sample Radius",
        description="The minimum radius of the samples for the whole morphology",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Maximum sample radius
    bpy.types.Scene.MaximumSampleRadius = bpy.props.FloatProperty(
        name="Max. Sample Radius",
        description="The maximum radius of the samples for the whole morphology",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Average sample radius
    bpy.types.Scene.AverageSampleRadius = bpy.props.FloatProperty(
        name="Avg. Sample Radius",
        description="The average radius of the samples for the whole morphology",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Minimum segment length
    bpy.types.Scene.MinimumSegmentLength = bpy.props.FloatProperty(
        name="Min. Segment Length",
        description="The minimum length of the segments along the entire morphology skeleton",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Maximum segment length
    bpy.types.Scene.MaximumSegmentLength = bpy.props.FloatProperty(
        name="Max. Segment Length",
        description="The maximum length of the segments along the entire morphology skeleton",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Average segment length
    bpy.types.Scene.AverageSegmentLength = bpy.props.FloatProperty(
        name="Avg. Segment Length",
        description="The average length of the segments along the entire morphology skeleton",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Minimum section length
    bpy.types.Scene.MinimumSectionLength = bpy.props.FloatProperty(
        name="Min. Section Length",
        description="The minimum length of the section along the entire morphology skeleton",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Maximum section length
    bpy.types.Scene.MaximumSectionLength = bpy.props.FloatProperty(
        name="Max. Section Length",
        description="The maximum length of the section along the entire morphology skeleton",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Average section length
    bpy.types.Scene.AverageSectionLength = bpy.props.FloatProperty(
        name="Avg. Section Length",
        description="The average length of the section along the entire morphology skeleton",
        subtype='FACTOR', min=0, max=1e32, precision=5)

    # Number short sections
    bpy.types.Scene.NumberShortSections = bpy.props.IntProperty(
        name="# Short Sections",
        description="The total number of short sections along the morphology, where the sum of the "
                    "radii of the first and last samples is smaller than the section length",
        default=0, subtype='FACTOR')

    # Number zero-radius samples
    bpy.types.Scene.NumberZeroRadiusSamples = bpy.props.IntProperty(
        name="# Zero-radius Samples",
        description="The total number of the sample with zero radius in the morphology skeleton",
        default=0, subtype='FACTOR')

    # Number of duplicated sections
    bpy.types.Scene.NumberDuplicatedSamples = bpy.props.IntProperty(
        name="# Duplicated Samples",
        description="The total number of duplicated samples in the morphology skeleton that "
                    "are almost in the same position",
        default=0, subtype='FACTOR')

    # Bounding box
    bpy.types.Scene.BBoxPMinX = bpy.props.FloatProperty(
        name="X",
        description="X-coordinate of PMin",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMinY = bpy.props.FloatProperty(
        name="Y",
        description="Y-coordinate of PMin",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMinZ = bpy.props.FloatProperty(
        name="Z",
        description="Z-coordinate of PMin",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMaxX = bpy.props.FloatProperty(
        name="X",
        description="X-coordinate of PMax",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMaxY = bpy.props.FloatProperty(
        name="Y",
        description="Y-coordinate of PMax",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxPMaxZ = bpy.props.FloatProperty(
        name="Z",
        description="Z-coordinate of PMax",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxCenterX = bpy.props.FloatProperty(
        name="X",
        description="X-coordinate of center of the morphology",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxCenterY = bpy.props.FloatProperty(
        name="Y",
        description="Y-coordinate of center of the morphology",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BBoxCenterZ = bpy.props.FloatProperty(
        name="Z",
        description="Z-coordinate of center of the morphology",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BoundsX = bpy.props.FloatProperty(
        name="X",
        description="Morphology width",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BoundsY = bpy.props.FloatProperty(
        name="Y",
        description="Morphology height",
        min=-1e10, max=1e10, subtype='FACTOR')
    bpy.types.Scene.BoundsZ = bpy.props.FloatProperty(
        name="Z",
        description="Morphology depth",
        min=-1e10, max=1e10, subtype='FACTOR')

    # Analysis time
    bpy.types.Scene.MorphologyAnalysisTime = bpy.props.FloatProperty(
        name="Analysis Time (Sec)",
        default=0, min=0, max=1000000)

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
        if vmv.interface.ui_morphology_loaded:
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
# @VMVAnalyzeMorphology
####################################################################################################
class VMVAnalyzeMorphology(bpy.types.Operator):
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
            vmv.interface.ui.ui_morphology.sections_list)
        context.scene.MorphologyTotalLength = morphology_total_length

        # Total number of samples
        vmv.logger.info('Samples')
        total_number_samples = vmv.analysis.compute_total_number_samples_from_sections_list(
            vmv.interface.ui.ui_morphology.sections_list)
        context.scene.NumberSamples = total_number_samples

        # Total number of segments
        vmv.logger.info('Segments')
        context.scene.NumberSegments = total_number_samples - 1

        # Total number of sections
        vmv.logger.info('Sections')
        total_number_sections = vmv.analysis.compute_total_number_sections(
            vmv.interface.ui.ui_morphology.sections_list)
        context.scene.NumberSections = total_number_sections

        # Sections with two samples
        vmv.logger.info('Sections with two samples')
        number_section_with_two_samples = vmv.analysis.compute_number_of_sections_with_two_samples(
            vmv.interface.ui.ui_morphology.sections_list)
        context.scene.NumberSectionsWithTwoSamples = number_section_with_two_samples

        # Number of short sections
        vmv.logger.info('Short sections')
        number_short_sections = vmv.analysis.compute_number_of_short_sections(
            vmv.interface.ui.ui_morphology.sections_list)
        context.scene.NumberShortSections = number_short_sections

        # Samples radius stats.
        vmv.logger.info('Radii')
        minimum_sample_radius, maximum_sample_radius, average_sample_radius = \
            vmv.analysis.analyze_samples_radii(vmv.interface.ui.ui_morphology.points_list)
        context.scene.MinimumSampleRadius = minimum_sample_radius
        context.scene.MaximumSampleRadius = maximum_sample_radius
        context.scene.AverageSampleRadius = average_sample_radius

        vmv.logger.info('Zero-radii')
        context.scene.NumberZeroRadiusSamples = vmv.analysis.analyze_samples_with_zero_radii(
            vmv.interface.ui.ui_morphology.points_list)

        vmv.logger.info('Repair Zero-radii')
        vmv.analysis.correct_samples_with_zero_radii(vmv.interface.ui.ui_morphology.sections_list)

        # Segments length stats.
        vmv.logger.info('Segments lengths')
        minimum_segment_length, maximum_segment_length, average_segment_length = \
            vmv.analysis.analyze_segments_length(vmv.interface.ui.ui_morphology.sections_list)
        context.scene.MinimumSegmentLength = minimum_segment_length
        context.scene.MaximumSegmentLength = maximum_segment_length
        context.scene.AverageSegmentLength = average_segment_length

        # Section length stats.
        vmv.logger.info('Sections lengths')
        minimum_section_length, maximum_section_length, average_section_length = \
            vmv.analysis.analyze_sections_length(vmv.interface.ui.ui_morphology.sections_list)
        context.scene.MinimumSectionLength = minimum_section_length
        context.scene.MaximumSectionLength = maximum_section_length
        context.scene.AverageSectionLength = average_section_length

        vmv.logger.info('Loops')
        number_loops = vmv.analysis.compute_number_of_loops(
            vmv.interface.ui.ui_morphology.sections_list)
        context.scene.NumberLoops = number_loops

        vmv.logger.info('Components')
        number_components = vmv.analysis.compute_number_of_components(
            vmv.interface.ui.ui_morphology.sections_list)
        context.scene.NumberComponents = number_components

        # Bounding box data
        vmv.logger.info('Bounding box')
        context.scene.BBoxCenterX = vmv.interface.ui.ui_morphology.bounding_box.center[0]
        context.scene.BBoxCenterY = vmv.interface.ui.ui_morphology.bounding_box.center[1]
        context.scene.BBoxCenterZ = vmv.interface.ui.ui_morphology.bounding_box.center[2]
        context.scene.BoundsX = vmv.interface.ui.ui_morphology.bounding_box.bounds[0]
        context.scene.BoundsY = vmv.interface.ui.ui_morphology.bounding_box.bounds[1]
        context.scene.BoundsZ = vmv.interface.ui.ui_morphology.bounding_box.bounds[2]
        context.scene.BBoxPMinX = vmv.interface.ui.ui_morphology.bounding_box.p_min[0]
        context.scene.BBoxPMinY = vmv.interface.ui.ui_morphology.bounding_box.p_min[1]
        context.scene.BBoxPMinZ = vmv.interface.ui.ui_morphology.bounding_box.p_min[2]
        context.scene.BBoxPMaxX = vmv.interface.ui.ui_morphology.bounding_box.p_max[0]
        context.scene.BBoxPMaxY = vmv.interface.ui.ui_morphology.bounding_box.p_max[1]
        context.scene.BBoxPMaxZ = vmv.interface.ui.ui_morphology.bounding_box.p_max[2]

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
    bpy.utils.register_class(VMVAnalysisPanel)

    # Analysis button
    bpy.utils.register_class(VMVAnalyzeMorphology)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # InputOutput data
    bpy.utils.unregister_class(VMVAnalysisPanel)

    # Analysis button
    bpy.utils.unregister_class(VMVAnalyzeMorphology)
