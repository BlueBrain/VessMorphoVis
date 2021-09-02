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
import vmv.utilities

# Meshing parameters ###############################################################################
# Meshing technique
bpy.types.Scene.VMV_MeshingTechnique = bpy.props.EnumProperty(
    items=vmv.enums.Meshing.Technique.MESHING_TECHNIQUES_ITEMS,
    name='Technique',
    default=vmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT)

# Mesh tessellation flag
bpy.types.Scene.VMV_TessellateMesh = bpy.props.BoolProperty(
    name='Tessellation',
    description='Tessellate the reconstructed mesh to reduce the geometry complexity',
    default=False)

# Mesh tessellation level
bpy.types.Scene.VMV_MeshTessellationRatio = bpy.props.FloatProperty(
    name='Ratio',
    description='Mesh tessellation ratio (between 0.01 and 1.0)',
    default=1.0, min=0.01, max=1.0)

# Auto-detected meta balls resolution
bpy.types.Scene.VMV_MetaBallAutoResolution = bpy.props.BoolProperty(
    name='Auto',
    description='Detects the resolution of the meta balls object based on the radius of the '
                'smallest sample in the morphology. You can disable this option and set a '
                'user-specific resolution below',
    default=True)

# Mesh color
bpy.types.Scene.VMV_MetaBallResolution = bpy.props.FloatProperty(
    name='',
    default=vmv.consts.Meshing.META_RESOLUTION,
    min=vmv.consts.Meshing.MIN_META_BALL_RESOLUTION,
    max=vmv.consts.Meshing.MAX_META_BALL_RESOLUTION,
    description='The resolution of the meta object')

# Color parameters #################################################################################
# Mesh material
bpy.types.Scene.VMV_MeshShader = bpy.props.EnumProperty(
    items=vmv.enums.Shader.SHADER_ITEMS,
    name='Shader',
    default=vmv.enums.Shader.LAMBERT_WARD)

# Mesh color
bpy.types.Scene.VMV_MeshColor = bpy.props.FloatVectorProperty(
    name='Mesh Color', subtype='COLOR',
    default=vmv.consts.Color.LIGHT_RED_COLOR, min=0.0, max=1.0,
    description='The color of the reconstructed mesh surface')

# Rendering parameters #############################################################################
# Rendering resolution
bpy.types.Scene.VMV_MeshRenderingResolution = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Resolution.RESOLUTION_ITEMS,
    name='Type',
    default=vmv.enums.Rendering.Resolution.FIXED_RESOLUTION)

# Image resolution
bpy.types.Scene.VMV_MeshFrameResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the mesh',
    default=vmv.consts.Image.DEFAULT_RESOLUTION,
    min=vmv.consts.Image.MIN_RESOLUTION,
    max=vmv.consts.Image.MAX_RESOLUTION)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.VMV_MeshFrameScaleFactor = bpy.props.FloatProperty(
    name='Scale',
    default=vmv.consts.Image.DEFAULT_IMAGE_SCALE_FACTOR,
    min=vmv.consts.Image.MIN_IMAGE_SCALE_FACTOR,
    max=vmv.consts.Image.MAX_IMAGE_SCALE_FACTOR,
    description='The scale factor for rendering a mesh to scale')

# Rendering views
bpy.types.Scene.VMV_MeshRenderingView = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.View.VIEW_ITEMS,
    name='View', default=vmv.enums.Rendering.View.FRONT)

# Projection
bpy.types.Scene.VMV_MeshCameraProjection = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Projection.PROJECTION_ITEMS,
    name='Projection', default=vmv.enums.Rendering.Projection.ORTHOGRAPHIC)

# Render the corresponding scale bar on the resulting image
bpy.types.Scene.VMV_RenderMeshScaleBar = bpy.props.BoolProperty(
    name='Add Scale Bar',
    description='Add a scale bar overlaid on the resulting image automatically',
    default=False)

# Exported mesh file formats
bpy.types.Scene.VMV_ExportedMeshFormat = bpy.props.EnumProperty(
    items=vmv.enums.Meshing.ExportFormat.FILE_FORMATS_ITEMS,
    name='Format', default=vmv.enums.Meshing.ExportFormat.PLY)

# Stats. parameters ################################################################################
# 360 rendering progress bar
bpy.types.Scene.VMV_MeshRenderingProgress = bpy.props.IntProperty(
    name='Rendering Progress',
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Reconstruction time
bpy.types.Scene.VMV_MeshReconstructionTime = bpy.props.FloatProperty(
    name='Reconstruction Time (Sec)',
    description='The time it takes to reconstruct the vasculature mesh',
    default=0, min=0, max=1000000)
