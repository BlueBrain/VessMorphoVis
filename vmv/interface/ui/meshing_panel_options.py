####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
    items=[(vmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT,
            'Piecewise Watertight',
            'Piecewise watertight meshing, where a group of connected section will be created '
            'as a single watertight mesh, but the whole mesh will not be watertight. '
            'This approach is the fast and used to create a proxy mesh for visualization'),
           (vmv.enums.Meshing.Technique.SKINNING,
            'Skinning',
            'Skinning-based meshing. The loops will be handled accurately, but the final mesh '
            'is not guaranteed to be watertight'),
           (vmv.enums.Meshing.Technique.META_BALLS,
            'Meta Balls',
            'Creates watertight mesh models using meta balls. This method is SLOW and can '
            'take few hours to make a mesh based on the resolution and setting'), ],
    name='Method', default=vmv.enums.Meshing.Technique.META_BALLS)

# Auto-detected meta balls resolution
bpy.types.Scene.MetaBallAutoResolution = bpy.props.BoolProperty(
    name="Auto Detected",
    description='Detects the resolution of the meta balls object based on the radius of the '
                'smallest sample in the morphology',
    default=True)

# Mesh color
bpy.types.Scene.MetaBallResolution = bpy.props.FloatProperty(
    name="Resolution",
    default=vmv.consts.Meshing.META_RESOLUTION, min=0.01, max=5.0,
    description="The resolution of the meta object")

# Rendering resolution
bpy.types.Scene.MeshRenderingResolution = bpy.props.EnumProperty(
    items=[(vmv.enums.Rendering.Resolution.FIXED_RESOLUTION,
            'Fixed',
            'Renders an image of the mesh at a specific resolution given by the user'),
           (vmv.enums.Rendering.Resolution.TO_SCALE,
            'To Scale',
            'Renders an image of the mesh at factor of the exact scale')],
    name='Type',
    default=vmv.enums.Rendering.Resolution.FIXED_RESOLUTION)

# Rendering views
bpy.types.Scene.MeshRenderingView = bpy.props.EnumProperty(
    items=[(vmv.enums.Rendering.View.FRONT,
            'Front View',
            'Render the front view of the mesh'),
           (vmv.enums.Rendering.View.SIDE,
            'Side View',
            'Renders the side view of the mesh'),
           (vmv.enums.Rendering.View.TOP,
            'Top View',
            'Renders the top view of the mesh')],
    name='View', default=vmv.enums.Rendering.View.TOP)

# Projection
bpy.types.Scene.MeshCameraProjection = bpy.props.EnumProperty(
    items=[(vmv.enums.Rendering.Projection.ORTHOGRAPHIC,
            'Orthographic',
            'Render an orthographic projection of the mesh. '
            'This type of rendering is accurate and crucial for scientific images'),
           (vmv.enums.Rendering.Projection.PERSPECTIVE,
            'Perspective',
            'Renders a perspective projection of the mesh.'
            'This type of rendering is more for artistic style')],
    name='Projection', default=vmv.enums.Rendering.Projection.ORTHOGRAPHIC)

# Exported mesh file formats
bpy.types.Scene.ExportedMeshFormat = bpy.props.EnumProperty(
    items=[(vmv.enums.Meshing.ExportFormat.PLY,
            'Stanford (.ply)',
            'Export the mesh to a .ply file'),
           (vmv.enums.Meshing.ExportFormat.OBJ,
            'Wavefront(.obj)',
            'Export the mesh to a .obj file'),
           (vmv.enums.Meshing.ExportFormat.STL,
            'Stereolithography CAD (.stl)',
            'Export the mesh to an .stl file'),
           (vmv.enums.Meshing.ExportFormat.OFF,
            'Object File Format (.off)',
            'Export the mesh to an .off file'),
           (vmv.enums.Meshing.ExportFormat.BLEND,
            'Blender File (.blend)',
            'Export the mesh as a .blend file')],
    name='Format', default=vmv.enums.Meshing.ExportFormat.PLY)

# Mesh materials
bpy.types.Scene.MeshMaterial = bpy.props.EnumProperty(
    items=vmv.enums.Shading.MATERIAL_ITEMS,
    name="Material",
    default=vmv.enums.Shading.LAMBERT_WARD)

# Mesh color
bpy.types.Scene.MeshColor = bpy.props.FloatVectorProperty(
    name="Mesh Color", subtype='COLOR',
    default=vmv.consts.Color.GRAY, min=0.0, max=1.0,
    description="The color of the reconstructed mesh surface")

# 360 rendering progress bar
bpy.types.Scene.MeshRenderingProgress = bpy.props.IntProperty(
    name="Rendering Progress",
    default=0, min=0, max=100, subtype='PERCENTAGE')

# Image resolution
bpy.types.Scene.MeshFrameResolution = bpy.props.IntProperty(
    name='Resolution',
    description='The resolution of the image generated from rendering the mesh',
    default=512, min=128, max=1024 * 10)

# Frame scale factor 'for rendering to scale option '
bpy.types.Scene.MeshFrameScaleFactor = bpy.props.FloatProperty(
    name="Scale", default=1.0, min=1.0, max=100.0,
    description="The scale factor for rendering a mesh to scale")