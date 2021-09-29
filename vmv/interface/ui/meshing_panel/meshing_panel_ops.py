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
import vmv.interface


####################################################################################################
# @add_meshing_options
####################################################################################################
def add_meshing_options(layout,
                        scene,
                        options):
    """Adds the reconstruction, or meshing options to the meshing panel UI.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Title
    layout.row().label(text='Meshing Options', icon='SURFACE_DATA')

    # Meshing technique
    layout.row().prop(scene, 'VMV_MeshingTechnique', icon='OUTLINER_OB_EMPTY')

    # Meta-balls-specific algorithm options
    if scene.VMV_MeshingTechnique == vmv.enums.Meshing.Technique.META_BALLS:

        row = layout.row()
        row.label(text='Resolution')

        # Auto meta-ball resolution
        row.prop(scene, 'VMV_MetaBallAutoResolution', icon='OUTLINER_OB_EMPTY')
        options.mesh.meta_auto_resolution = scene.VMV_MetaBallAutoResolution

        resolution_row = row.row()
        resolution_row.prop(scene, 'VMV_MetaBallResolution')
        options.mesh.meta_resolution = scene.VMV_MetaBallResolution

        # Meta-ball resolution, if the auto-resolution option is not checked
        if scene.VMV_MetaBallAutoResolution:
            resolution_row.enabled = False
        else:
            resolution_row.enabled = True

    # Mesh tessellation
    row = layout.row()
    row.prop(scene, 'VMV_TessellateMesh')
    row = row.row()
    row.prop(scene, 'VMV_MeshTessellationRatio')

    # If tessellation is disabled, use 1.0 to disable the tessellation
    if not scene.VMV_TessellateMesh:
        options.mesh.tessellation_ratio = 1.0
        row.enabled = False
    else:
        options.mesh.tessellation_ratio = scene.VMV_MeshTessellationRatio


####################################################################################################
# @add_mesh_reconstruction_button
####################################################################################################
def add_mesh_reconstruction_button(layout,
                                   scene):
    """Adds the mesh reconstruction button to the meshing panel UI.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    """

    # Title
    layout.row().label(text='Mesh Reconstruction', icon='PARTICLE_POINT')

    # Mesh reconstruction button
    layout.row().operator('reconstruct.mesh', icon='MESH_DATA')

    # If the morphology is loaded only, print the performance stats.
    if vmv.interface.MorphologyLoaded:

        # Title
        layout.row().label(text='Stats', icon='RECOVER_LAST')

        # Reconstruction time
        row = layout.row()
        row.prop(scene, 'VMV_MeshReconstructionTime')
        row.enabled = False


####################################################################################################
# @add_color_options
####################################################################################################
def add_color_options(layout,
                      scene,
                      options):
    """Adds the color options to the meshing panel UI.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Title
    layout.row().label(text='Colors & Shaders', icon='COLOR')

    # Mesh shader
    layout.row().prop(scene, 'VMV_MeshShader')
    options.mesh.material = scene.VMV_MeshShader

    # Mesh color
    layout.row().prop(scene, 'VMV_MeshColor')
    options.mesh.color = scene.VMV_MeshColor


####################################################################################################
# @add_rendering_options
####################################################################################################
def add_rendering_options(layout,
                          scene,
                          options):
    """Adds the rendering options to the meshing panel UI.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Title
    layout.row().label(text='Rendering Options', icon='RENDER_STILL')

    # Rendering resolution
    row = layout.row()
    row.label(text='Resolution')
    row.prop(scene, 'VMV_MeshRenderingResolution', expand=True)

    # If a fixed resolution is set
    if scene.VMV_MeshRenderingResolution == vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:
        row = layout.row()
        row.label(text='Frame Resolution')
        row.prop(scene, 'VMV_MeshFrameResolution')
        row.enabled = True

    # Otherwise, add the scale factor option
    else:
        row = layout.row()
        row.label(text='Resolution Scale')
        row.prop(scene, 'VMV_MeshFrameScaleFactor')
        row.enabled = True

    # Rendering view column
    layout.column().prop(scene, 'VMV_MeshRenderingView', icon='AXIS_FRONT')
    options.mesh.camera_view = scene.VMV_MeshRenderingView

    # Rendering projection column only for a fixed resolution
    if scene.VMV_MeshRenderingResolution == vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

        # Due to a bug in the workbench renderer in Blender, we will allow the
        # perspective projection for all the materials that use cycles and have high number of
        # samples per pixel, mainly the artistic rendering.
        if options.mesh.material in vmv.enums.Shader.SUB_SURFACE_SCATTERING:
            layout.column().prop(scene, 'VMV_MeshCameraProjection ', icon='AXIS_FRONT')
            options.mesh.camera_projection = scene.VMV_MeshCameraProjection

        # Set it by default to ORTHOGRAPHIC
        else:
            options.mesh.camera_projection = vmv.enums.Rendering.Projection.ORTHOGRAPHIC

    # Set it by default to ORTHOGRAPHIC
    else:
        options.mesh.camera_projection = vmv.enums.Rendering.Projection.ORTHOGRAPHIC

    # Add scale bar option
    layout.row().prop(scene, 'VMV_RenderMeshScaleBar')
    vmv.interface.Options.mesh.render_scale_bar = scene.VMV_RenderMeshScaleBar

    # Background
    background_row = layout.row()
    background_row.prop(scene, 'VMV_TransparentMeshBackground')
    options.mesh.transparent_background = scene.VMV_TransparentMeshBackground

    # Rendering button
    layout.row().operator('render_mesh.image', icon='MESH_DATA')

    # Render animation row
    layout.row().label(text='Render Animation', icon='CAMERA_DATA')
    row = layout.row(align=True)
    row.operator('render_mesh.360', icon='FORCE_MAGNETIC')
    row.enabled = True

    # Rendering progress bar
    row = layout.row()
    row.prop(scene, 'VMV_MeshRenderingProgress')
    row.enabled = False

    # Rendering time
    row = layout.row()
    row.prop(scene, 'VMV_MeshRenderingTime')
    row.enabled = False


####################################################################################################
# @add_mesh_export_options
####################################################################################################
def add_mesh_export_options(layout,
                            scene):
    """Adds the rendering options to the meshing panel UI.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    """

    # Title
    layout.row().label(text='Export Mesh As', icon='MESH_UVSPHERE')

    # Exported format
    layout.row().prop(scene, 'VMV_ExportedMeshFormat', icon='GROUP_VERTEX')
    layout.row().operator('export.mesh', icon='MESH_DATA')
