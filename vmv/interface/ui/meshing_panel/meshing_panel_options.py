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

# Add background to the final image or set it transparent
bpy.types.Scene.VMV_TransparentMeshBackground = bpy.props.BoolProperty(
    name='TransparentBackground',
    description='Set transparent background for the rendered image.',
    default=True)

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

# Rendering time
bpy.types.Scene.VMV_MeshRenderingTime = bpy.props.FloatProperty(
    name='Rendering (Sec)',
    description='The time it takes to render the mesh into an image',
    default=0, min=0, max=1000000)
