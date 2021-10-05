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

# Blender imports
import copy

import bpy

# Internal imports
import vmv.bbox
import vmv.enums
import vmv.file
import vmv.builders
import vmv.skeleton
import vmv.interface
import vmv.utilities
import vmv.rendering
import vmv.shading
from .morphology_panel_options import *


####################################################################################################
# @define_morphology_visualization_type_items
####################################################################################################
def define_morphology_visualization_type_items():

    # If the morphology object is None, or not loaded, simply use the structure
    if vmv.interface.MorphologyObject is None:
        bpy.types.Scene.VMV_VisualizationType = bpy.props.EnumProperty(
            items=[vmv.enums.Morphology.Visualization.STRUCTURE_UI_ITEM],
            name='Visualization',
            default=vmv.enums.Morphology.Visualization.STRUCTURE)

    # Otherwise, define the items based on the content of the morphology file
    else:

        # A list of items that is dependent on the input morphology contents
        items = list()

        # Basically, add the structure
        items.append(vmv.enums.Morphology.Visualization.STRUCTURE_UI_ITEM)

        # Radius variations
        if vmv.interface.MorphologyObject.has_radius_simulation:
            items.append(
                vmv.enums.Morphology.Visualization.RADII_STRUCTURAL_DYNAMICS_UI_ITEM)
            items.append(vmv.enums.Morphology.Visualization.RADII_COLORMAP_DYNAMICS_UI_ITEM)

        # Flow variations
        if vmv.interface.MorphologyObject.has_flow_simulation:
            items.append(vmv.enums.Morphology.Visualization.FLOW_COLORMAP_DYNAMICS_UI_ITEM)

        # Pressure variations
        if vmv.interface.MorphologyObject.has_pressure_simulation:
            items.append(
                vmv.enums.Morphology.Visualization.PRESSURE_COLORMAP_DYNAMICS_UI_ITEM)

        # Visualization type, only the structure, when the morphology does not have simulation data
        bpy.types.Scene.VMV_VisualizationType = bpy.props.EnumProperty(
            items=items,
            name='Visualization',
            default=vmv.enums.Morphology.Visualization.STRUCTURE)


####################################################################################################
# @add_visualization_type_options
####################################################################################################
def add_visualization_type_options(layout,
                                   scene,
                                   options):

    # Make sure that the morphology is loaded
    if vmv.interface.MorphologyObject is not None:

        # Visualization type
        visualization_type_row = layout.row()
        vmv.interface.CurrentVisualizationType = copy.deepcopy(options.morphology.visualization_type)
        visualization_type_row.prop(scene, 'VMV_VisualizationType')
        options.morphology.visualization_type = scene.VMV_VisualizationType

        if scene.VMV_VisualizationType != vmv.interface.CurrentVisualizationType:
            vmv.interface.SimulationLoaded = False
        vmv.interface.CurrentVisualizationType = copy.deepcopy(scene.VMV_VisualizationType)


####################################################################################################
# @add_colormap_options
####################################################################################################
def add_colormap_options(layout,
                         scene,
                         options):
    """Adds the coloring options that gives extra components to assign a colormap to the morphology.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Color map
    color_map_row = layout.row()
    color_map_row.label(text='Color Map')
    color_map_row.prop(scene, 'VMV_ColorMap')
    color_map_row.prop(scene, 'VMV_InvertColorMap')

    # Clear the color map passed to VMV if it is full
    if len(options.morphology.color_map_colors) > 0:
        options.morphology.color_map_colors.clear()

    # Fill the list of colors
    for i_color in range(vmv.consts.Color.COLORMAP_RESOLUTION):

        # Add the colormap element to the UI
        colors = layout.row()
        colormap_element = colors.column()
        colormap_element.prop(scene, 'VMV_Color%d' % i_color)

        # Colormap range values
        values = colors.row()
        values.prop(scene, 'VMV_R0_Value%d' % i_color)
        values.prop(scene, 'VMV_R1_Value%d' % i_color)
        values.enabled = False

        # Get the color value from the panel
        color = getattr(scene, 'VMV_Color%d' % i_color)
        options.morphology.color_map_colors.append(color)


####################################################################################################
# @add_default_coloring_option
####################################################################################################
def add_default_coloring_option(layout,
                                scene,
                                options):
    """Adds to the UI the single arbor color elements.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    row = layout.row()
    row.prop(scene, 'VMV_MorphologyColor')
    options.morphology.color = scene.VMV_MorphologyColor


####################################################################################################
# @add_alternating_colors_option
####################################################################################################
def add_alternating_colors_option(layout,
                                  scene,
                                  options):
    """Adds alternating coloring options, simply two colors where we can see different patterns in
    the morphology.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Color 1
    row = layout.row()
    row.label(text='Color 1')
    row.prop(scene, 'VMV_MorphologyColor1')
    options.morphology.color = scene.VMV_MorphologyColor1

    # Color 2
    row = layout.row()
    row.label(text='Color 2')
    row.prop(scene, 'VMV_MorphologyColor2')
    options.morphology.alternating_color = scene.VMV_MorphologyColor2


####################################################################################################
# @add_alignment_colors_option
####################################################################################################
def add_alignment_colors_option(layout,
                                scene):

    # Red Color
    row = layout.row()
    row.label(text='X')
    column = row.column()
    column.prop(scene, 'VMV_RedColor')
    column.enabled = False

    # Green Color
    row = layout.row()
    row.label(text='Y')
    column = row.column()
    column.prop(scene, 'VMV_GreenColor')
    column.enabled = False

    # Blue Color
    row = layout.row()
    row.label(text='Z')
    column = row.column()
    column.prop(scene, 'VMV_BlueColor')
    column.enabled = False


####################################################################################################
# @add_short_sections_colors_option
####################################################################################################
def add_short_sections_colors_option(layout,
                                     scene,
                                     options):
    """Adds alternating coloring options, simply two colors where we can see different patterns in
    the morphology to visualize the short sections.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Color 1
    row = layout.row()
    row.label(text='Normal Section')
    row.prop(scene, 'VMV_MorphologyColor1')
    options.morphology.color = scene.VMV_MorphologyColor1

    # Color 2
    row = layout.row()
    row.label(text='Short Section')
    row.prop(scene, 'VMV_MorphologyColor2')
    options.morphology.alternating_color = scene.VMV_MorphologyColor2


####################################################################################################
# @add_per_section_color_coding_options
####################################################################################################
def add_per_section_color_coding_options(layout,
                                         scene,
                                         options):
    """Adds the coloring options of the per-section coloring scheme.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Set the color coding scheme
    options.morphology.color_coding = scene.VMV_PerSectionColorCodingBasis

    # Default coloring scheme
    if scene.VMV_PerSectionColorCodingBasis == vmv.enums.ColorCoding.DEFAULT:
        add_default_coloring_option(layout=layout, scene=scene, options=options)

    # Alternating colors
    elif scene.VMV_PerSectionColorCodingBasis == vmv.enums.ColorCoding.ALTERNATING_COLORS:
        add_alternating_colors_option(layout=layout, scene=scene, options=options)

    # Short sections
    elif scene.VMV_PerSectionColorCodingBasis == vmv.enums.ColorCoding.SHORT_SECTIONS:
        add_short_sections_colors_option(layout=layout, scene=scene, options=options)

    # Using a colormap
    else:
        add_colormap_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @add_per_segment_color_coding_options
####################################################################################################
def add_per_segment_color_coding_options(layout,
                                         scene,
                                         options):
    """Adds the coloring options of the per-segment coloring scheme.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Color coding scheme
    options.morphology.color_coding = scene.VMV_PerSegmentColorCodingBasis

    # Single arbor color
    if scene.VMV_PerSegmentColorCodingBasis == vmv.enums.ColorCoding.DEFAULT:
        add_default_coloring_option(layout=layout, scene=scene, options=options)

    # Alternating colors
    elif scene.VMV_PerSegmentColorCodingBasis == vmv.enums.ColorCoding.ALTERNATING_COLORS:
        add_alternating_colors_option(layout=layout, scene=scene, options=options)

    # Alignment colors
    elif scene.VMV_PerSegmentColorCodingBasis == vmv.enums.ColorCoding.BY_SEGMENT_ALIGNMENT:
        add_alignment_colors_option(layout=layout, scene=scene)

    # Using a colormap
    else:
        add_colormap_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @add_color_options
####################################################################################################
def add_color_options(layout,
                      scene,
                      options):
    """Morphology coloring options.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Color parameters
    arbors_colors_row = layout.row()
    arbors_colors_row.label(text='Morphology Colors', icon='COLOR')

    # Per-section color coding
    color_coding_row = layout.row()

    # Sections
    if options.morphology.builder == vmv.enums.Morphology.Builder.SECTIONS:
        color_coding_row.label(text='Color Coding')
        color_coding_row.prop(scene, 'VMV_PerSectionColorCodingBasis')
        add_per_section_color_coding_options(layout, scene, options)

    # Segments
    elif options.morphology.builder == vmv.enums.Morphology.Builder.SEGMENTS:
        color_coding_row.label(text='Color Coding')
        color_coding_row.prop(scene, 'VMV_PerSegmentColorCodingBasis')
        add_per_segment_color_coding_options(layout, scene, options)

    # Otherwise, use the default coloring scheme
    else:
        add_default_coloring_option(layout=layout, scene=scene, options=options)

    # Morphology material
    morphology_material_row = layout.row()
    morphology_material_row.label(text='Shading')
    morphology_material_row.prop(scene, 'VMV_MorphologyMaterial')
    options.morphology.material = scene.VMV_MorphologyMaterial


####################################################################################################
# @add_radii_options
####################################################################################################
def add_radii_options(layout,
                      scene,
                      options):

    # Sections radii option
    sections_radii_row = layout.row()
    sections_radii_row.prop(scene, 'VMV_SectionsRadii', icon='SURFACE_NCURVE')

    # Radii as specified in the morphology file
    if scene.VMV_SectionsRadii == vmv.enums.Morphology.Radii.AS_SPECIFIED:
        options.morphology.radii = vmv.enums.Morphology.Radii.AS_SPECIFIED
        options.morphology.scale_sections_radii = False
        options.morphology.unify_sections_radii = False
        options.morphology.sections_radii_scale = 1.0

    # Fixed radius
    elif scene.VMV_SectionsRadii == vmv.enums.Morphology.Radii.FIXED:
        fixed_diameter_row = layout.row()
        fixed_diameter_row.label(text='Fixed Radius Value')
        fixed_diameter_row.prop(scene, 'VMV_FixedRadiusValue')

        # Pass options from UI to system
        options.morphology.radii = vmv.enums.Morphology.Radii.FIXED
        options.morphology.scale_sections_radii = False
        options.morphology.unify_sections_radii = True
        options.morphology.sections_fixed_radii_value = scene.VMV_FixedRadiusValue

    # Scaled diameter
    elif scene.VMV_SectionsRadii == vmv.enums.Morphology.Radii.SCALED:
        scaled_diameter_row = layout.row()
        scaled_diameter_row.label(text='Radius Scale Factor')
        scaled_diameter_row.prop(scene, 'VMV_RadiusScaleValue')

        # Pass options from UI to system
        options.morphology.radii = vmv.enums.Morphology.Radii.SCALED
        options.morphology.scale_sections_radii = True
        options.morphology.unify_sections_radii = False
        options.morphology.sections_radii_scale = scene.VMV_RadiusScaleValue

    else:
        vmv.logger.log('ERROR')


####################################################################################################
# @add_radii_options
####################################################################################################
def add_tube_quality_options(layout,
                             scene,
                             options):
    # Tube quality
    tube_quality_row = layout.row()
    tube_quality_row.label(text='Tube Quality')
    tube_quality_row.prop(scene, 'VMV_BevelSides')
    options.morphology.bevel_object_sides = scene.VMV_BevelSides


####################################################################################################
# @add_static_morphology_visualization_options
####################################################################################################
def add_static_morphology_visualization_options(layout,
                                                scene,
                                                options):
    """Draws the morphology reconstruction options.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Skeleton meshing options
    skeleton_meshing_options_row = layout.row()
    skeleton_meshing_options_row.label(
        text='Morphology Options', icon='SURFACE_DATA')

    # Builder
    builder_row = layout.row()
    builder_row.prop(scene, 'VMV_StaticStructureBuilders', icon='FORCE_CURVE')
    options.morphology.builder = scene.VMV_StaticStructureBuilders

    # Radii options are common
    add_radii_options(layout=layout, scene=scene, options=options)

    # The samples builder does not have any specific options for the moment
    if options.morphology.builder == vmv.enums.Morphology.Builder.SAMPLES:
        pass
    else:
        # Tube quality only for the sections and segments, to improve the performance
        add_tube_quality_options(layout=layout, scene=scene, options=options)

    # Color options
    add_color_options(layout=layout, scene=scene, options=options)

    # Add the morphology reconstruction button
    add_morphology_reconstruction_button(layout=layout, scene=scene)


####################################################################################################
# @add_static_morphology_visualization_options
####################################################################################################
def add_structural_dynamics_visualization_options(layout,
                                                  scene,
                                                  options):
    # Builder
    builder_row = layout.row()
    builder_row.prop(scene, 'VMV_DynamicStructureBuilders', icon='FORCE_CURVE')
    options.morphology.builder = scene.VMV_DynamicStructureBuilders

    # Tube quality only for the sections and segments, to improve the performance
    add_tube_quality_options(layout=layout, scene=scene, options=options)

    # Simulation visualization
    add_simulation_visualization_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @add_static_morphology_visualization_options
####################################################################################################
def add_colormap_dynamics_visualization_options(layout,
                                                scene,
                                                options):
    builder_row = layout.row()
    builder_row.prop(scene, 'VMV_DynamicFunctionBuilders', icon='FORCE_CURVE')
    options.morphology.builder = scene.VMV_DynamicFunctionBuilders

    # Add radius options
    add_radii_options(layout=layout, scene=scene, options=options)

    # Tube quality only for the sections and segments, to improve the performance
    add_tube_quality_options(layout=layout, scene=scene, options=options)

    # Simulation visualization
    add_simulation_visualization_options(layout=layout, scene=scene, options=options)

    # Color-coding (per-segment)
    add_colormap_options(layout=layout, scene=scene, options=options)


####################################################################################################
# @add_morphology_reconstruction_button
####################################################################################################
def add_morphology_reconstruction_button(layout,
                                         scene):
    """Adds the morphology reconstruction button to the panel.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    """

    # Title
    layout.row().label(text='Morphology Reconstruction', icon='PARTICLE_POINT')

    # Button
    layout.row().operator('reconstruct.morphology', icon='MESH_DATA')

    # If the morphology is loaded only, print the performance stats.
    if vmv.interface.MorphologyLoaded:

        # Stats
        layout.row().label(text='Stats', icon='RECOVER_LAST')

        row = layout.row()
        row.prop(scene, 'VMV_MorphologyReconstructionTime')
        row.enabled = False


####################################################################################################
# @add_morphology_reconstruction_button
####################################################################################################
def add_simulation_visualization_options(layout,
                                         scene,
                                         options):
    # Title
    layout.row().label(text='Simulation Visualization', icon='PARTICLE_POINT')

    # Adding the simulation loading button, if the simulation is not loaded
    layout.row().operator('load.simulation', icon='FORCE_TURBULENCE')

    # If the simulation is loaded add the simulation controls
    if vmv.interface.SimulationLoaded:

        # Simulation range as loaded from the morphology file
        row = layout.row()
        column = row.column()
        column.label(text='Range')
        column = row.column()
        row = column.row(align=True)
        row.prop(scene, 'VMV_FirstSimulationFrame')
        row.prop(scene, 'VMV_LastSimulationFrame')
        row.enabled = False

        # Simulation controls
        control = layout.row(align=True)
        first_frame_button = control.column()
        first_frame_button.operator('play_first_frame.simulation', icon='REW')
        previous_frame_button = control.column()
        previous_frame_button.operator('play_previous_frame.simulation', icon='PREV_KEYFRAME')
        play_pause_button = control.column()
        play_pause_button.operator('play.simulation', icon=bpy.types.Scene.VMV_PlayPauseButtonIcon)
        next_frame_button = control.column()
        next_frame_button.operator('play_next_frame.simulation', icon='NEXT_KEYFRAME')
        last_frame_button = control.column()
        last_frame_button.operator('play_last_frame.simulation', icon='FF')
        control.prop(scene, 'VMV_CurrentSimulationFrame')

        # If the simulation is running, disable all the other buttons to avoid conflicts
        if vmv.interface.SimulationRunning:
            first_frame_button.enabled = False
            previous_frame_button.enabled = False
            next_frame_button.enabled = False
            last_frame_button.enabled = False
        else:
            first_frame_button.enabled = True
            previous_frame_button.enabled = True
            next_frame_button.enabled = True
            last_frame_button.enabled = True

    # Simulation progress bar
    progress = layout.row()
    progress.prop(scene, 'VMV_SimulationProgressBar')
    progress.enabled = False


####################################################################################################
# @add_morphology_rendering_options
####################################################################################################
def add_morphology_rendering_options(layout,
                                      scene,
                                      options):
    """Draw the rendering options.

    :param context:
        Context.
    """

    # Rendering options
    rendering_row = layout.row()
    rendering_row.label(text='Rendering Options', icon='RENDER_STILL')

    # Rendering resolution
    rendering_resolution_row = layout.row()
    rendering_resolution_row.label(text='Resolution')
    rendering_resolution_row.prop(scene, 'VMV_MorphologyRenderingResolution', expand=True)

    # Add the frame resolution option
    if scene.VMV_MorphologyRenderingResolution == \
            vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

        # Frame resolution option (only for the close up mode)
        frame_resolution_row = layout.row()
        frame_resolution_row.label(text='Frame Resolution')
        frame_resolution_row.prop(scene, 'VMV_MorphologyImageResolution')
        options.morphology.resolution_basis = \
            scene.VMV_MorphologyRenderingResolution

    # Otherwise, add the scale factor option
    else:

        # Scale factor option
        scale_factor_row = layout.row()
        scale_factor_row.label(text='Resolution Scale')
        scale_factor_row.prop(scene, 'VMV_MorphologyImageScaleFactor')
        options.morphology.resolution_scale_factor = \
            scene.VMV_MorphologyImageScaleFactor

    # Rendering view column
    view_row = layout.column()
    view_row.prop(scene, 'VMV_MorphologyRenderingViews', icon='AXIS_FRONT')
    vmv.Options.morphology.camera_view = scene.VMV_MorphologyRenderingViews

    # Scale bar
    scale_bar_row = layout.row()
    scale_bar_row.prop(scene, 'VMV_RenderMorphologyScaleBar')
    options.morphology.render_scale_bar = scene.VMV_RenderMorphologyScaleBar

    # Background
    background_row = layout.row()
    background_row.prop(scene, 'VMV_TransparentMorphologyBackground')
    options.morphology.transparent_background = scene.VMV_TransparentMorphologyBackground

    # Rendering button
    rendering_button_row = layout.column()
    rendering_button_row.operator('render_morphology.image', icon='MESH_DATA')

    # Render animation row
    render_animation_row = layout.row()
    render_animation_row.label(text='Render Animation', icon='CAMERA_DATA')
    render_animations_buttons_row = layout.row(align=True)
    render_animations_buttons_row.operator('render_morphology.360', icon='FORCE_MAGNETIC')

    # Render simulation
    if vmv.interface.SimulationLoaded:
        rendering_simulation_button_row = layout.column()
        rendering_simulation_button_row.operator('render.simulation', icon='MESH_DATA')

    # Rendering progress bar
    rendering_progress_row = layout.row()
    rendering_progress_row.prop(scene, 'VMV_MorphologyRenderingProgress')
    rendering_progress_row.enabled = False

    # Rendering time
    rendering_time_row = layout.row()
    rendering_time_row.prop(scene, 'VMV_MorphologyRenderingTime')
    rendering_time_row.enabled = False


####################################################################################################
# @draw_morphology_export_options
####################################################################################################
def draw_morphology_export_options(layout,
                                   scene,
                                   options):
    """Draw the morphology export button.

    :param context:
        Context.
    """

    # Saving meshes parameters
    save_mesh_row = layout.row()
    save_mesh_row.label(text='Export Morphology As', icon='MESH_UVSPHERE')

    # Exported format column
    format_column = layout.column()
    format_column.prop(scene, 'ExportedMorphologyFormat', icon='GROUP_VERTEX')
    format_column.operator('export.morphology', icon='MESH_DATA')
