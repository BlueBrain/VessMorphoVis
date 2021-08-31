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
import bpy

# Internal imports
import vmv.consts

# Simulation parameters ############################################################################
# This scene parameter is used to propagate if the loaded morphology has simulation data or not
bpy.types.Scene.VMV_MorphologyHasSimulationData = bpy.props.BoolProperty(
    name='', description='', default=False)

# Confirms if the loaded morphology has radius simulation data
bpy.types.Scene.VMV_MorphologyHasRadiusSimulation = bpy.props.BoolProperty(
    name='', description='', default=False)

# Confirms if the loaded morphology has pressure simulation data
bpy.types.Scene.VMV_MorphologyHasPressureSimulation = bpy.props.BoolProperty(
    name='', description='', default=False)

# Confirms if the loaded morphology has flow simulation data
bpy.types.Scene.VMV_MorphologyHasFlowSimulation = bpy.props.BoolProperty(
    name='', description='', default=False)

# Visualization type, static structure or dynamic simulation
bpy.types.Scene.VMV_VisualizationType = bpy.props.EnumProperty(
    items=[('Structure',
            'Structure',
            'Visualize static data showing only the structural aspects of the blood vessel'),
           ('Dynamics',
            'Dynamics',
            'Visualize simulation data with respect to time')],
    name='',
    default='Structure')

# Available simulations
bpy.types.Scene.VMV_AvailableSimulations = bpy.props.EnumProperty(
    items=[('Radius',
            'Radius',
            'Visualize the radius variations'),
           ('Flow',
            'Flow',
            'Visualize the flow variations'),
           ('Pressure',
            'Pressure',
            'Visualize the pressure variations')],
    name='',
    default='Radius')

# Simulation starting frame
bpy.types.Scene.VMV_TimeFrameStart = bpy.props.IntProperty(
    name='Start (t0)',
    default=0, min=0, max=100)

# Simulation end frame
bpy.types.Scene.VMV_TimeFrameEnd = bpy.props.IntProperty(
    name='End (t0)',
    default=0, min=0, max=100)

# Reconstruction parameters ########################################################################
# Morphology builder
bpy.types.Scene.VMV_Builder = bpy.props.EnumProperty(
    items=vmv.enums.Morphology.Builder.METHOD_ITEMS,
    name='Method',
    default=vmv.enums.Morphology.Builder.SECTIONS)

# Tube quality
bpy.types.Scene.VMV_TubeQuality = bpy.props.IntProperty(
    name='Sides',
    description='Number of sides of the cross-section of each segment along the drawn tube.'
                'The minimum is 4, maximum 128 and default is 8. High value is required for '
                'closeups and low value is sufficient for far-away visualizations',
    default=8, min=4, max=128)

# Section radius
bpy.types.Scene.VMV_SectionsRadii = bpy.props.EnumProperty(
    items=[(vmv.enums.Morphology.Radii.AS_SPECIFIED,
            'As Specified in Morphology',
            'Use the cross-sectional radii as reported in the morphology file'),
           (vmv.enums.Morphology.Radii.FIXED,
            'At a Fixed Radii',
            'Set all the tubes to a fixed radius'),
           (vmv.enums.Morphology.Radii.SCALED,
            'With Scale Factor',
            'Scale all the tubes using a specified scale factor')],
    name='Radii',
    default=vmv.enums.Morphology.Radii.AS_SPECIFIED)

# Fixed section radius value
bpy.types.Scene.VMV_FixedRadiusValue = bpy.props.FloatProperty(
    name='Value (micron)',
    description='The value of the fixed radius in microns between (0.05 and 5.0)',
    default=1.0, min=0.05, max=5.0)

# Tubes radius scale value
bpy.types.Scene.VMV_RadiusScaleValue = bpy.props.FloatProperty(
    name='Scale',
    description='A scale factor for scaling the radii of the tubes between (0.01 and 5.0)',
    default=1.0, min=0.01, max=5.0)

# Shading parameters ###############################################################################
# Material
bpy.types.Scene.VMV_MorphologyMaterial = bpy.props.EnumProperty(
    items=vmv.enums.Shader.MATERIAL_ITEMS,
    name='',
    default=vmv.enums.Shader.LAMBERT_WARD)

# Segments color-coding
bpy.types.Scene.VMV_PerSegmentColorCodingBasis = bpy.props.EnumProperty(
    items=vmv.enums.ColorCoding.SEGMENTS_COLOR_CODING_ITEMS,
    name='',
    default=vmv.enums.ColorCoding.DEFAULT)

# Sections color-coding
bpy.types.Scene.VMV_PerSectionColorCodingBasis = bpy.props.EnumProperty(
    items=vmv.enums.ColorCoding.SECTIONS_COLOR_CODING_ITEMS,
    name='',
    default=vmv.enums.ColorCoding.DEFAULT)

# The alternative color used to color every second object in the morphology
bpy.types.Scene.VMV_MorphologyColor1 = bpy.props.FloatVectorProperty(
    name='Color 1',
    subtype='COLOR', default=vmv.consts.Color.VERY_WHITE, min=0.0, max=1.0,
    description='The first alternating color of the morphology')

# The alternative color used to color every second object in the morphology
bpy.types.Scene.VMV_MorphologyColor2 = bpy.props.FloatVectorProperty(
    name='Color 2',
    subtype='COLOR', default=vmv.consts.Color.DEFAULT_BLOOD_COLOR, min=0.0, max=1.0,
    description='The second alternating color of the morphology')

# Colormap minimum and maximum values
for i in range(vmv.consts.Color.COLORMAP_RESOLUTION):
    delta = 100.0 / float(vmv.consts.Color.COLORMAP_RESOLUTION)
    setattr(bpy.types.Scene, 'VMV_R0_Value%d' % i, bpy.props.FloatProperty(
        name='', default=i * delta,
        min=0.0, max=1e10, description=''))
    setattr(bpy.types.Scene, 'VMV_R1_Value%d' % i, bpy.props.FloatProperty(
        name='', default=(i + 1) * delta,
        min=0.0, max=1e10, description=''))

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.VMV_ColorMapResolution = bpy.props.IntProperty(
    name='Resolution', default=vmv.consts.Color.COLORMAP_RESOLUTION, min=4, max=128,
    description='The resolution of the color-map. Range [4 - 128] samples.')

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

# Camera projection
bpy.types.Scene.VMV_MorphologyCameraProjection = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Projection.PROJECTION_ITEMS,
    name='Projection', default=vmv.enums.Rendering.Projection.ORTHOGRAPHIC)

# 360 rendering progress bar
bpy.types.Scene.VMV_MorphologyRenderingProgress = bpy.props.IntProperty(
    name='Rendering Progress',
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Image resolution
bpy.types.Scene.VMV_MorphologyImageResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the morphology',
    default=512, min=128, max=1024 * 10)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.VMV_MorphologyImageScaleFactor = bpy.props.FloatProperty(
    name='Scale', default=1.0, min=1.0, max=100.0,
    description='The scale factor for rendering a morphology to scale')

# Render the corresponding scale bar on the resulting image
bpy.types.Scene.VMV_RenderMorphologyScaleBar = bpy.props.BoolProperty(
    name='Add Scale Bar',
    description='Add a scale bar overlaid on the resulting image automatically',
    default=False)

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
    description='The time it takes to reconstruct the vasculature morphology',
    default=0, min=0, max=1000000)
