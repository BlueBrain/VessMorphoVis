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
import vmv
import vmv.consts
import vmv.enums
import vmv.utilities

# Meshing technique
bpy.types.Scene.MeshingTechnique = bpy.props.EnumProperty(
    items=vmv.enums.Meshing.Technique.MESHING_TECHNIQUES_ITEMS,
    name='Method', default=vmv.enums.Meshing.Technique.META_BALLS)

# Mesh tessellation flag
bpy.types.Scene.TessellateMesh = bpy.props.BoolProperty(
    name='Tessellation',
    description='Tessellate the reconstructed mesh to reduce the geometry complexity',
    default=False)

# Mesh tessellation level
bpy.types.Scene.MeshTessellationLevel = bpy.props.FloatProperty(
    name='Factor',
    description='Mesh tessellation level (between 0.1 and 1.0)',
    default=1.0, min=0.05, max=1.0)

# Auto-detected meta balls resolution
bpy.types.Scene.MetaBallAutoResolution = bpy.props.BoolProperty(
    name="Auto Detected Resolution",
    description='Detects the resolution of the meta balls object based on the radius of the '
                'smallest sample in the morphology. You can disable this option and set a '
                'user-specific resolution below',
    default=True)

# Mesh color
bpy.types.Scene.MetaBallResolution = bpy.props.FloatProperty(
    name="Resolution",
    default=vmv.consts.Meshing.META_RESOLUTION,
    min=vmv.consts.Meshing.MIN_META_BALL_RESOLUTION,
    max=vmv.consts.Meshing.MAX_META_BALL_RESOLUTION,
    description="The resolution of the meta object")

# Rendering resolution
bpy.types.Scene.MeshRenderingResolution = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Resolution.RESOLUTION_ITEMS,
    name='Type',
    default=vmv.enums.Rendering.Resolution.FIXED_RESOLUTION)

# Rendering views
bpy.types.Scene.MeshRenderingView = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.View.VIEW_ITEMS,
    name='View', default=vmv.enums.Rendering.View.FRONT)

# Projection
bpy.types.Scene.MeshCameraProjection = bpy.props.EnumProperty(
    items=vmv.enums.Rendering.Projection.PROJECTION_ITEMS,
    name='Projection', default=vmv.enums.Rendering.Projection.ORTHOGRAPHIC)

# Exported mesh file formats
bpy.types.Scene.ExportedMeshFormat = bpy.props.EnumProperty(
    items=vmv.enums.Meshing.ExportFormat.FILE_FORMATS_ITEMS,
    name='Format', default=vmv.enums.Meshing.ExportFormat.PLY)

# Mesh materials
bpy.types.Scene.MeshMaterial = bpy.props.EnumProperty(
    items=vmv.enums.Shader.MATERIAL_ITEMS,
    name="Material",
    default=vmv.enums.Shader.LAMBERT_WARD)

# Mesh color
bpy.types.Scene.MeshColor = bpy.props.FloatVectorProperty(
    name="Mesh Color", subtype='COLOR',
    default=vmv.consts.Color.LIGHT_RED_COLOR, min=0.0, max=1.0,
    description="The color of the reconstructed mesh surface")

# 360 rendering progress bar
bpy.types.Scene.MeshRenderingProgress = bpy.props.IntProperty(
    name="Rendering Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Image resolution
bpy.types.Scene.MeshFrameResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the mesh',
    default=vmv.consts.Image.DEFAULT_RESOLUTION,
    min=vmv.consts.Image.MIN_RESOLUTION,
    max=vmv.consts.Image.MAX_RESOLUTION)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.MeshFrameScaleFactor = bpy.props.FloatProperty(
    name="Scale",
    default=vmv.consts.Image.DEFAULT_IMAGE_SCALE_FACTOR,
    min=vmv.consts.Image.MIN_IMAGE_SCALE_FACTOR,
    max=vmv.consts.Image.MAX_IMAGE_SCALE_FACTOR,
    description="The scale factor for rendering a mesh to scale")

# Reconstruction time
bpy.types.Scene.MeshReconstructionTime = bpy.props.FloatProperty(
    name="Reconstruction Time (Sec)",
    description="The time it takes to reconstruct the vasculature mesh",
    default=0, min=0, max=1000000)
