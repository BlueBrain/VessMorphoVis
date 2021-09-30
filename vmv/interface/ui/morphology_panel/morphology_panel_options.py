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

# Blender imports
import bpy

# Internal imports
import vmv.enums


####################################################################################################
# @define_visualization_methods_menus
####################################################################################################
def define_visualization_methods_menus():

    # Morphology builders available when visualizing STATIC structure only
    bpy.types.Scene.VMV_StaticStructureBuilders = bpy.props.EnumProperty(
        items=[vmv.enums.Morphology.Builder.SECTIONS_UI_ITEM,
               vmv.enums.Morphology.Builder.SEGMENTS_UI_ITEM,
               vmv.enums.Morphology.Builder.SAMPLES_UI_ITEM],
        name='Method',
        default=vmv.enums.Morphology.Builder.SECTIONS)

    # Morphology builders available when visualizing DYNAMIC structure only
    bpy.types.Scene.VMV_DynamicStructureBuilders = bpy.props.EnumProperty(
        items=[vmv.enums.Morphology.Builder.SECTIONS_UI_ITEM],
        name='Method',
        default=vmv.enums.Morphology.Builder.SECTIONS)

    # Morphology builders available when visualizing DYNAMIC function with colormap
    bpy.types.Scene.VMV_DynamicFunctionBuilders = bpy.props.EnumProperty(
        items=[vmv.enums.Morphology.Builder.SEGMENTS_UI_ITEM],
        name='Method',
        default=vmv.enums.Morphology.Builder.SEGMENTS)


####################################################################################################
# @define_visualization_methods_menus
####################################################################################################
def define_color_mapping_values():

    # Colormap minimum and maximum values
    for i in range(vmv.consts.Color.COLORMAP_RESOLUTION):
        delta = 100.0 / float(vmv.consts.Color.COLORMAP_RESOLUTION)
        setattr(bpy.types.Scene, 'VMV_R0_Value%d' % i, bpy.props.FloatProperty(
            name='', default=i * delta, precision=5,
            min=-1e10, max=1e10, description=''))
        setattr(bpy.types.Scene, 'VMV_R1_Value%d' % i, bpy.props.FloatProperty(
            name='', default=(i + 1) * delta, precision=5,
            min=-1e10, max=1e10, description=''))


# Morphology visualization #########################################################################
# Visualization methods
define_visualization_methods_menus()

# Section radius
bpy.types.Scene.VMV_SectionsRadii = bpy.props.EnumProperty(
    items=vmv.enums.Morphology.Radii.RADII_UI_ITEMS,
    name='Radii',
    default=vmv.enums.Morphology.Radii.AS_SPECIFIED)

# Fixed section radius value
bpy.types.Scene.VMV_FixedRadiusValue = bpy.props.FloatProperty(
    name='Value (micron)',
    description='The value of the fixed radius in microns between (0.05 and 5.0).',
    default=1.0, min=0.05, max=5.0)

# Tubes radius scale value
bpy.types.Scene.VMV_RadiusScaleValue = bpy.props.FloatProperty(
    name='Scale',
    description='A scale factor for scaling the radii of the tubes between (0.01 and 5.0).',
    default=1.0, min=0.01, max=5.0)


# Shading parameters ###############################################################################
# Segments color-coding
bpy.types.Scene.VMV_PerSegmentColorCodingBasis = bpy.props.EnumProperty(
    items=vmv.enums.ColorCoding.SEGMENTS_COLOR_CODING_ITEMS,
    name='',
    description='The color-coding schemes for segment-based visualization.',
    default=vmv.enums.ColorCoding.DEFAULT)

# Sections color-coding
bpy.types.Scene.VMV_PerSectionColorCodingBasis = bpy.props.EnumProperty(
    items=vmv.enums.ColorCoding.SECTIONS_COLOR_CODING_ITEMS,
    name='',
    description='The color-coding schemes for section-based visualization.',
    default=vmv.enums.ColorCoding.DEFAULT)

# Color-mapping values
define_color_mapping_values()

# Rendering parameters #############################################################################
# Rendering resolution
bpy.types.Scene.VMV_MorphologyRenderingResolution = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Resolution.RESOLUTION_ITEMS,
    name='Type',
    default=vmv.enums.Rendering.Resolution.FIXED_RESOLUTION)

# Rendering views
bpy.types.Scene.VMV_MorphologyRenderingViews = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.View.VIEW_ITEMS,
    name='View', default=vmv.enums.Rendering.View.FRONT)

# Camera projection (ORTHO is the standard)
bpy.types.Scene.VMV_MorphologyCameraProjection = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Projection.PROJECTION_ITEMS,
    name='Projection', default=vmv.enums.Rendering.Projection.ORTHOGRAPHIC)

# Image resolution
bpy.types.Scene.VMV_MorphologyImageResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the morphology.',
    default=vmv.consts.Image.DEFAULT_RESOLUTION,
    min=vmv.consts.Image.MIN_RESOLUTION,
    max=vmv.consts.Image.MAX_RESOLUTION)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.VMV_MorphologyImageScaleFactor = bpy.props.FloatProperty(
    name='Scale', default=1.0, min=1.0, max=100.0,
    description='The scale factor for rendering a morphology to scale.')

# Render the corresponding scale bar on the resulting image
bpy.types.Scene.VMV_RenderMorphologyScaleBar = bpy.props.BoolProperty(
    name='Add Scale Bar',
    description='Add a scale bar overlaid on the resulting image automatically.',
    default=False)

# Add background to the final image or set it transparent
bpy.types.Scene.VMV_TransparentMorphologyBackground = bpy.props.BoolProperty(
    name='TransparentBackground',
    description='Set transparent background for the rendered image.',
    default=True)

# 360 rendering progress bar
bpy.types.Scene.VMV_MorphologyRenderingProgress = bpy.props.IntProperty(
    name='Rendering Progress',
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Simulation options ###############################################################################
# The first time frame of the simulation as loaded from the file
bpy.types.Scene.VMV_FirstSimulationFrame = bpy.props.IntProperty(
    name='',
    description='The first time frame of the simulation as loaded from the morphology file'
                'This is the typical initial time-step with which the simulation will start from.',
    default=0, min=0, max=1000000)

# The last time frame of the simulation as loaded from the file
bpy.types.Scene.VMV_LastSimulationFrame = bpy.props.IntProperty(
    name='',
    description='The last time frame of the simulation as loaded from the morphology file'
                'This is the typical last time-step with which the simulation will end at.',
    default=0, min=0, max=1000000)

# Simulation progress bar
bpy.types.Scene.VMV_SimulationProgressBar = bpy.props.IntProperty(
    name='',
    description='The time it takes to reconstruct the vasculature mesh.',
    default=0, min=0, max=100, subtype='PERCENTAGE')

# The icon that will be displayed on the Play/Pause button
bpy.types.Scene.VMV_PlayPauseButtonIcon = 'PLAY'

# Other parameters #################################################################################
# The minimum value associated with the color map
bpy.types.Scene.VMV_MinimumValue = bpy.props.StringProperty(
    name='', description='', default='0', maxlen=10)

# The maximum value associated with the color map
bpy.types.Scene.VMV_MaximumValue = bpy.props.StringProperty(
    name='', description='', default='100', maxlen=10)

# Reconstruction time
bpy.types.Scene.VMV_MorphologyReconstructionTime = bpy.props.FloatProperty(
    name='Reconstruction Time (Sec)',
    description='The time it takes to reconstruct the vasculature morphology.',
    default=0, min=0, max=1000000)

# Rendering time
bpy.types.Scene.VMV_MorphologyRenderingTime = bpy.props.FloatProperty(
    name='Rendering (Sec)',
    description='The time it takes to render the morphology into an image',
    default=0, min=0, max=1000000)
