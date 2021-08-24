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

# Internal imports
import vmv
import vmv.bbox
import vmv.enums
import vmv.file
import vmv.builders
import vmv.skeleton
import vmv.interface
import vmv.utilities
import vmv.rendering
import vmv.shading


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
    color_map_row.label(text='Color Map:')
    color_map_row.prop(scene, 'VMV_ColorMap')
    color_map_row.prop(scene, 'VMV_InvertColorMap')

    # Clear the color map passed to VMV if it is full
    if len(vmv.interface.ui.options.morphology.color_map_colors) > 0:
        vmv.interface.ui.options.morphology.color_map_colors.clear()

    # Fill the list of colors
    for i in range(vmv.consts.Color.COLORMAP_RESOLUTION):

        # Add the colormap element to the UI
        colors = layout.row()
        colormap_element = colors.column()
        colormap_element.prop(scene, 'VMV_Color%d' % i)

        # Colormap range values
        values = colors.row()
        values.prop(scene, 'VMV_R0_Value%d' % i)
        values.prop(scene, 'VMV_R1_Value%d' % i)
        values.enabled = False

        # Get the color value from the panel
        color = getattr(scene, 'VMV_Color%d' % i)
        vmv.interface.ui.options.morphology.color_map_colors.append(color)


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
    color_1_row = layout.row()
    color_1_row.prop(scene, 'VMV_MorphologyColor1')
    options.morphology.color = scene.VMV_MorphologyColor1

    # Color 2
    color_2_row = layout.row()
    color_2_row.prop(scene, 'VMV_MorphologyColor2')
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
    vmv.interface.ui.options.morphology.color_coding = scene.VMV_PerSectionColorCodingBasis

    # Default coloring scheme
    if scene.VMV_PerSectionColorCodingBasis == vmv.enums.ColorCoding.DEFAULT:
        add_default_coloring_option(layout=layout, scene=scene, options=options)

    # Alternating colors
    elif scene.VMV_PerSectionColorCodingBasis == vmv.enums.ColorCoding.ALTERNATING_COLORS:
        add_alternating_colors_option(layout=layout, scene=scene, options=options)

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
    vmv.interface.ui.options.morphology.color_coding = scene.VMV_PerSegmentColorCodingBasis

    # Single arbor color
    if scene.VMV_PerSegmentColorCodingBasis == vmv.enums.ColorCoding.DEFAULT:
        add_default_coloring_option(layout=layout, scene=scene, options=options)

    # Alternating colors
    elif scene.VMV_PerSegmentColorCodingBasis == vmv.enums.ColorCoding.ALTERNATING_COLORS:
        add_alternating_colors_option(layout=layout, scene=scene, options=options)

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
    arbors_colors_row.label(text='Morphology Colors:', icon='COLOR')

    # Morphology material
    morphology_material_row = layout.row()
    morphology_material_row.label(text='Shading:')
    morphology_material_row.prop(scene, 'VMV_MorphologyMaterial')
    options.morphology_material = scene.VMV_MorphologyMaterial

    # Per-section color coding
    color_coding_row = layout.row()

    # Sections
    if options.morphology.builder == vmv.enums.Morphology.Builder.SECTIONS:
        color_coding_row.label(text='Color Coding:')
        color_coding_row.prop(scene, 'VMV_PerSectionColorCodingBasis')
        add_per_section_color_coding_options(layout, scene, options)

    # Segments
    elif options.morphology.builder == vmv.enums.Morphology.Builder.SEGMENTS:
        color_coding_row.label(text='Color Coding:')
        color_coding_row.prop(scene, 'VMV_PerSegmentColorCodingBasis')
        add_per_segment_color_coding_options(layout, scene, options)

    # Otherwise, use the default coloring scheme
    else:
        add_default_coloring_option(layout=layout, scene=scene, options=options)