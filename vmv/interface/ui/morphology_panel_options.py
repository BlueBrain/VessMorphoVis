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

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.ColorMapResolution = bpy.props.IntProperty(
    name="Resolution", default=vmv.consts.Color.COLOR_MAP_RESOLUTION, min=4, max=128,
    description="The resolution of the color-map. Range [4 - 128] samples.")

# Center morphology at the origin
bpy.types.Scene.CenterMorphology = bpy.props.BoolProperty(
    name="Center Morphology at Origin",
    description="Center the loaded morphology skeleton at the origin to make it easy to "
                "navigate and visualize it",
    default=True)

# Progressive reconstruction
bpy.types.Scene.ProgressiveReconstruction = bpy.props.BoolProperty(
    name="Progressive Reconstruction",
    description="Show the sequence of reconstructing the morphology interactively. "
                "This option might be slow for large datasets that have more than 10000 "
                "morphological samples",
    default=False)

# Adaptive resampling
bpy.types.Scene.AdaptiveResampling = bpy.props.BoolProperty(
    name="Adaptive Resampling",
    description="Resample the morphology skeleton adaptively to reduce the number of drawn "
                "samples while preserving the structure of the morphology",
    default=False)

# Reconstruction method
bpy.types.Scene.ReconstructionMethod = bpy.props.EnumProperty(
    items=vmv.enums.Morphology.ReconstructionMethod.METHOD_ITEMS,
    name="Method",
    default=vmv.enums.Morphology.ReconstructionMethod.DISCONNECTED_SECTIONS)

# Rendering resolution
bpy.types.Scene.MorphologyRenderingResolution = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Resolution.RESOLUTION_ITEMS,
    name='Type',
    default=vmv.enums.Rendering.Resolution.FIXED_RESOLUTION)

# Rendering views
bpy.types.Scene.MorphologyRenderingViews = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.View.VIEW_ITEMS,
    name='View', default=vmv.enums.Rendering.View.FRONT)

# Projection
bpy.types.Scene.MorphologyCameraProjection = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Projection.PROJECTION_ITEMS,
    name='Projection', default=vmv.enums.Rendering.Projection.ORTHOGRAPHIC)

# Mesh materials
bpy.types.Scene.MorphologyMaterial = bpy.props.EnumProperty(
    items=vmv.enums.Shader.MATERIAL_ITEMS,
    name="Material",
    default=vmv.enums.Shader.LAMBERT_WARD)

# Mesh color
bpy.types.Scene.MorphologyColor = bpy.props.FloatVectorProperty(
    name="Morphology Color", subtype='COLOR',
    default=vmv.consts.Color.DEFAULT_BLOOD_COLOR, min=0.0, max=1.0,
    description="The color of the reconstructed morphology")

# 360 rendering progress bar
bpy.types.Scene.MorphologyRenderingProgress = bpy.props.IntProperty(
    name="Rendering Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Image resolution
bpy.types.Scene.MorphologyFrameResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the morphology',
    default=512, min=128, max=1024 * 10)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.MorphologyFrameScaleFactor = bpy.props.FloatProperty(
    name="Scale", default=1.0, min=1.0, max=100.0,
    description="The scale factor for rendering a morphology to scale")

# Reconstruction progress bar
bpy.types.Scene.ReconstructionProgress = bpy.props.IntProperty(
    name="Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Tube quality
bpy.types.Scene.TubeQuality = bpy.props.IntProperty(
    name="Sides",
    description="Number of sides of the cross-section of each segment along the drawn tube."
                "The minimum is 4, maximum 128 and default is 8. High value is required for "
                "closeups and low value is sufficient for far-away visualizations",
    default=8, min=4, max=128)

# Section radius
bpy.types.Scene.SectionsRadii = bpy.props.EnumProperty(
    items=[(vmv.enums.Morphology.Radii.AS_SPECIFIED,
            'As Specified in Morphology',
            "Use the cross-sectional radii as reported in the morphology file"),
           (vmv.enums.Morphology.Radii.FIXED,
            'At a Fixed Radii',
            "Set all the tubes to a fixed radius"),
           (vmv.enums.Morphology.Radii.SCALED,
            'With Scale Factor',
            "Scale all the tubes using a specified scale factor")],
    name="Radii",
    default=vmv.enums.Morphology.Radii.AS_SPECIFIED)

# Fixed section radius value
bpy.types.Scene.FixedRadiusValue = bpy.props.FloatProperty(
    name="Value (micron)",
    description="The value of the fixed radius in microns between (0.05 and 5.0)",
    default=1.0, min=0.05, max=5.0)

# Tubes radius scale value
bpy.types.Scene.RadiusScaleValue = bpy.props.FloatProperty(
    name="Scale",
    description="A scale factor for scaling the radii of the tubes between (0.01 and 5.0)",
    default=1.0, min=0.01, max=5.0)

# Material
bpy.types.Scene.MorphologyMaterial = bpy.props.EnumProperty(
    items=vmv.enums.Shader.MATERIAL_ITEMS,
    name="Material",
    default=vmv.enums.Shader.LAMBERT_WARD)

# Color each component
bpy.types.Scene.ColorComponents = bpy.props.BoolProperty(
    name="Color Components",
    description="Each component of the morphology will be assigned a different random color",
    default=False)

# Color the components using black and white alternatives
bpy.types.Scene.ColorComponentsBlackAndWhite = bpy.props.BoolProperty(
    name="Black / White",
    description="Each component of the morphology will be assigned a either black or white",
    default=False)

# The base color used for all the objects of the morphology
bpy.types.Scene.MorphologyColor = bpy.props.FloatVectorProperty(
    name="Base Color",
    subtype='COLOR', default=vmv.consts.Color.DEFAULT_BLOOD_COLOR, min=0.0, max=1.0,
    description="The base color of the morphology")

# The alternative color used to color every second object in the morphology
bpy.types.Scene.MorphologyAlternatingColor = bpy.props.FloatVectorProperty(
    name="Alternating Color",
    subtype='COLOR', default=vmv.consts.Color.WHITE, min=0.0, max=1.0,
    description="The alternating color of the morphology")

# Reconstruction time
bpy.types.Scene.MorphologyReconstructionTime = bpy.props.FloatProperty(
    name="Reconstruction Time (Sec)",
    description="The time it takes to reconstruct the vasculature morphology",
    default=0, min=0, max=1000000)

# Segments color-coding
bpy.types.Scene.PerSegmentColorCodingBasis = bpy.props.EnumProperty(
    items=vmv.enums.ColorCoding.SEGMENTS_COLOR_CODING_ITEMS,
    name='Color Coding',
    default=vmv.enums.ColorCoding.SINGLE_COLOR)

# Sections color-coding
bpy.types.Scene.PerSectionColorCodingBasis = bpy.props.EnumProperty(
    items=vmv.enums.ColorCoding.SECTIONS_COLOR_CODING_ITEMS,
    name='Color Coding',
    default=vmv.enums.ColorCoding.SINGLE_COLOR)

# The minimum value associated with the color map
bpy.types.Scene.MinimumValue = bpy.props.StringProperty(
    name='', description='', default='0', maxlen=10)

# The maximum value associated with the color map
bpy.types.Scene.MaximumValue = bpy.props.StringProperty(
    name='', description='', default='100', maxlen=10)

# Reconstruction time
bpy.types.Scene.MorphologyReconstructionTime = bpy.props.FloatProperty(
    name="Reconstruction Time (Sec)",
    description="The time it takes to reconstruct the vasculature morphology",
    default=0, min=0, max=1000000)

# UI color elements for the color map
for i in range(vmv.consts.Color.NUMBER_COLORS_UI):
    setattr(bpy.types.Scene, 'Value%d' % i, bpy.props.FloatProperty(
        name='', default=0 + (i * 100.0 / float(vmv.consts.Color.NUMBER_COLORS_UI - 1)),
        min=0.0, max=1e10, description=''))
