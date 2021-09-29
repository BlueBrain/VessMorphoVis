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

# System imports
import time

# Blender imports
import bpy
from mathutils import Vector

# Internal imports
import vmv.bbox
import vmv.builders
import vmv.consts
import vmv.enums
import vmv.file
import vmv.skeleton
import vmv.interface
import vmv.utilities
import vmv.rendering
import vmv.shading
from .meshing_panel_ops import *


####################################################################################################
# @VMV_MeshingPanel
####################################################################################################
class VMV_MeshingPanel(bpy.types.Panel):
    """The meshing panel of VMV"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_label = 'Meshing'
    bl_idname = "OBJECT_PT_VMV_Meshing"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'VessMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @update_mesh_material
    ################################################################################################
    def update_mesh_material(self,
                             context):

        # If the mesh object is not None
        if vmv.interface.MeshObject is not None:

            # Create the materials
            material = vmv.shading.create_material(
                name='mesh', color=context.scene.VMV_MeshColor,
                material_type=context.scene.VMV_MeshShader)

            vmv.interface.Options.mesh.material = context.scene.VMV_MeshShader

            vmv.interface.MeshObject.active_material = material

            # Create an illumination specific for the given material
            vmv.shading.create_material_specific_illumination(
                material_type=material, camera_view=vmv.interface.Options.mesh.camera_view)

    ################################################################################################
    # @update_mesh_color
    ################################################################################################
    def update_mesh_color(self,
                          context):
        """Updates the mesh color on-the-fly once the color is changed from the palette.

        :param context:
            Blender context.
        """

        # If the mesh object is not None
        if vmv.interface.MeshObject is not None:

            # Get the color from the palette
            color = context.scene.VMV_MeshColor

            # Update the mesh color
            vmv.interface.MeshObject.active_material.diffuse_color = \
                Vector((color[0], color[1], color[2], 1.0))

    ################################################################################################
    # Panel options
    ################################################################################################
    # Meshing technique
    bpy.types.Scene.VMV_MeshingTechnique = bpy.props.EnumProperty(
        items=vmv.enums.Meshing.Technique.MESHING_TECHNIQUES_ITEMS,
        name='Technique',
        default=vmv.enums.Meshing.Technique.PIECEWISE_WATERTIGHT)

    # Auto-detected meta balls resolution
    bpy.types.Scene.VMV_MetaBallAutoResolution = bpy.props.BoolProperty(
        name='Auto',
        description='Detects the resolution of the meta balls object based on the radius of the '
                    'smallest sample in the morphology. You can disable this option and set a '
                    'user-specific resolution below.',
        default=True)

    # Mesh color
    bpy.types.Scene.VMV_MetaBallResolution = bpy.props.FloatProperty(
        name='',
        default=vmv.consts.Meshing.META_RESOLUTION,
        min=vmv.consts.Meshing.MIN_META_BALL_RESOLUTION,
        max=vmv.consts.Meshing.MAX_META_BALL_RESOLUTION,
        description='The resolution of the meta object. Note that if this value is smaller than '
                    '0.01, it might take very long time to mesh the skeleton. It also depends on '
                    'the number of vertices or samples in the morphology.')

    # Mesh tessellation flag
    bpy.types.Scene.VMV_TessellateMesh = bpy.props.BoolProperty(
        name='Tessellation',
        description='Tessellate the reconstructed mesh to reduce the geometry complexity.',
        default=False)

    # Mesh tessellation level
    bpy.types.Scene.VMV_MeshTessellationRatio = bpy.props.FloatProperty(
        name='Ratio',
        description='Mesh tessellation ratio (between 0.01 and 1.0)',
        default=1.0, min=0.01, max=1.0)

    # Color parameters #############################################################################
    # Mesh material
    bpy.types.Scene.VMV_MeshShader = bpy.props.EnumProperty(
        items=vmv.enums.Shader.SHADER_ITEMS,
        name='Shader',
        default=vmv.enums.Shader.LAMBERT_WARD,
        update=update_mesh_material)

    # Mesh color
    bpy.types.Scene.VMV_MeshColor = bpy.props.FloatVectorProperty(
        name='Mesh Color', subtype='COLOR',
        default=vmv.consts.Color.LIGHT_RED_COLOR, min=0.0, max=1.0,
        description='The color of the reconstructed mesh surface',
        update=update_mesh_color)

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel.

        :param context:
            Panel context.
        """

        # Add the mesh reconstruction options to the panel
        add_meshing_options(layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # Add the color options to the panel
        add_color_options(layout=self.layout, scene=context.scene, options=vmv.interface.Options)

        # Add the mesh reconstruction button to the panel
        add_mesh_reconstruction_button(layout=self.layout, scene=context.scene)

        # Draw the mesh rendering options
        add_rendering_options(layout=self.layout, scene=context.scene,
                              options=vmv.interface.Options)

        # Draw the mesh export options
        add_mesh_export_options(layout=self.layout, scene=context.scene)

        # If the morphology is loaded, enable the layout, otherwise make it disabled by default
        if vmv.interface.MorphologyLoaded:
            self.layout.enabled = True
        else:
            self.layout.enabled = False


####################################################################################################
# @VMV_ReconstructMesh
####################################################################################################
class VMV_ReconstructMesh(bpy.types.Operator):
    """Reconstructs the mesh of the vasculature"""

    # Operator parameters
    bl_idname = "reconstruct.mesh"
    bl_label = "Reconstruct Mesh"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Executes the operator

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Clear the scene
        vmv.scene.clear_scene()

        # Starting timer
        start_reconstruction = time.time()

        # Meta builder
        if context.scene.VMV_MeshingTechnique == vmv.enums.Meshing.Technique.META_BALLS:
            builder = vmv.builders.MetaBuilder(morphology=vmv.interface.MorphologyObject,
                                               options=vmv.interface.Options)

        # Using the piece-wise
        else:
            builder = vmv.builders.PolylineBuilder(
                morphology=vmv.interface.MorphologyObject, options=vmv.interface.Options)

        # Build the vascular mesh
        vmv.interface.MeshObject = builder.build_mesh()

        # Update the interface with some parameters
        context.scene.VMV_MetaBallResolution = vmv.interface.Options.mesh.meta_resolution

        # Reconstruction done
        reconstruction_done = time.time()
        context.scene.VMV_MeshReconstructionTime = reconstruction_done - start_reconstruction

        # Done
        return {'FINISHED'}


####################################################################################################
# @VMV_RenderMeshImage
####################################################################################################
class VMV_RenderMeshImage(bpy.types.Operator):
    """Renders the mesh of the vasculature"""

    # Operator parameters
    bl_idname = "render_mesh.image"
    bl_label = "Render Image"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Executes the operator

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        if not vmv.scene.is_there_any_mesh_in_scene():
            self.report({'WARNING'}, 'The scene does not contain any mesh to render!')
            return {'FINISHED'}

        # Report the process starting in the UI
        self.report({'INFO'}, 'Rendering Mesh ... Wait Please')

        # Start timer
        start_rendering = time.time()

        # Render the mesh image
        vmv.render_mesh_image(panel=self, scene=context.scene,
                              rendering_view=vmv.interface.Options.mesh.camera_view,
                              camera_projection=vmv.interface.Options.mesh.camera_projection,
                              add_background_plane=not vmv.Options.mesh.transparent_background)

        # End timer
        end_rendering = time.time()

        # Update the panel
        context.scene.VMV_MeshRenderingTime = end_rendering - start_rendering

        # Report the process termination in the UI
        self.report({'INFO'}, 'Rendering Mesh Done')

        # Done
        return {'FINISHED'}


####################################################################################################
# @VMV_RenderMesh360
####################################################################################################
class VMV_RenderMesh360(bpy.types.Operator):
    """Render a 360 view of the reconstructed mesh"""

    # Operator parameters
    bl_idname = "render_mesh.360"
    bl_label = "Render 360"

    # Timer parameters
    event_timer = None
    timer_limits = 0
    start_time = 0

    # 360 bounding box
    bounding_box_360 = None

    # Output data
    output_directory = None

    ################################################################################################
    # @modal
    ################################################################################################
    def modal(self,
              context,
              event):
        """Threading and non-blocking handling.

        :param context:
            Panel context.
        :param event:
            A given event for the panel.
        """

        # Cancelling event, if using right click or exceeding the time limit of the simulation
        if event.type in {'RIGHTMOUSE', 'ESC'} or self.timer_limits > 360:

            # Reset the timer limits
            self.timer_limits = 0

            # Stats.
            rendering_time = time.time()
            context.scene.VMV_MeshRenderingTime = rendering_time - self.start_time

            # Refresh the panel context
            self.cancel(context)

            # Done
            return {'FINISHED'}

        # Timer event, where the function is executed here on a per-frame basis
        if event.type == 'TIMER':

            # Set the frame name
            image_name = '%s/%s' % (
                self.output_directory, '{0:05d}'.format(self.timer_limits))

            # Render at a specific resolution
            if context.scene.VMV_MeshRenderingResolution == \
                    vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

                # Render the image
                vmv.rendering.render_at_angle(
                    scene_objects=vmv.get_list_of_meshes_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_resolution=context.scene.VMV_MeshFrameResolution,
                    image_name=image_name)

            # Render at a specific scale factor
            else:

                # Render the image
                vmv.rendering.render_at_angle_to_scale(
                    scene_objects=vmv.get_list_of_meshes_in_scene(),
                    angle=self.timer_limits,
                    bounding_box=self.bounding_box_360,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_scale_factor=context.scene.VMV_MeshFrameScaleFactor,
                    image_name=image_name)

            # Update the progress shell
            vmv.utilities.show_progress('Rendering', self.timer_limits, 360)

            # Update the progress bar
            context.scene.VMV_MeshRenderingProgress = int(100 * self.timer_limits / 360.0)

            # Upgrade the timer limits
            self.timer_limits += 1

        # Next frame
        return {'PASS_THROUGH'}

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator

        :param context:
            Panel context.
        """

        # Make sure that the scene contains any mesh to be rendered
        if not vmv.scene.is_there_any_mesh_in_scene():
            self.report({'WARNING'}, 'The scene does not contain any mesh to render!')
            return {'FINISHED'}

        # Verify the presence of the sequences directory before rendering
        vmv.interface.verify_sequences_directory(panel=self)

        # A reference to the bounding box that will be used for the rendering
        rendering_bbox = vmv.bbox.compute_scene_bounding_box_for_meshes()

        # Compute a 360 bounding box to fit the arbors
        self.bounding_box_360 = vmv.bbox.compute_360_bounding_box(
            rendering_bbox, rendering_bbox.center)

        # Stretch the bounding box by few microns
        self.bounding_box_360.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)

        # Create a specific directory for this mesh
        self.output_directory = '%s/%s_mesh_360' % (
            vmv.interface.Options.io.sequences_directory,
            vmv.interface.MorphologyObject.name)
        vmv.file.ops.clean_and_create_directory(self.output_directory)

        # Use the event timer to update the UI during the soma building
        wm = context.window_manager
        self.event_timer = wm.event_timer_add(time_step=0.01, window=context.window)
        wm.modal_handler_add(self)

        # Done
        return {'RUNNING_MODAL'}

    ################################################################################################
    # @cancel
    ################################################################################################
    def cancel(self, context):
        """Cancel the panel processing and return to the interaction mode.

        :param context:
            Panel context.
        """

        # Multi-threading
        wm = context.window_manager
        wm.event_timer_remove(self.event_timer)

        # Report the process termination in the UI
        self.report({'INFO'}, 'Morphology Rendering Done')

        # Confirm operation done
        return {'FINISHED'}


####################################################################################################
# @VMV_ReconstructMesh
####################################################################################################
class VMV_ExportMesh(bpy.types.Operator):
    """Export the reconstructed mesh to a file"""

    # Operator parameters
    bl_idname = "export.mesh"
    bl_label = "Export"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Executes the operator

        Keyword arguments:
        :param context:
            Operator context.
        :return:
            {'FINISHED'}
        """

        # Make sure that the scene contains any mesh to export
        if not vmv.scene.is_there_any_mesh_in_scene():
            self.report({'WARNING'}, 'The scene does not contain any mesh to export!')
            return {'FINISHED'}

        # Verify the presence of the meshes directory before exporting
        vmv.interface.verify_meshes_directory(panel=self)

        # Select the mesh object that corresponding to the morphology to be exported
        mesh_object = vmv.scene.select_object_containing_string(vmv.consts.Suffix.MESH_SUFFIX)

        # Make sure that the mesh object is not None
        if mesh_object is None:
            self.report({'WARNING'}, 'The scene does not contain any mesh to export!')
            return {'FINISHED'}

        # Export the mesh
        vmv.file.export_mesh_object(
            mesh_object=mesh_object, output_directory=vmv.interface.Options.io.meshes_directory,
            file_name=mesh_object.name, file_format=context.scene.VMV_ExportedMeshFormat)

        # Done
        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(VMV_MeshingPanel)

    # Mesh reconstruction button
    bpy.utils.register_class(VMV_ReconstructMesh)

    # Mesh rendering buttons
    bpy.utils.register_class(VMV_RenderMeshImage)
    bpy.utils.register_class(VMV_RenderMesh360)

    # Mesh export button
    bpy.utils.register_class(VMV_ExportMesh)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(VMV_MeshingPanel)

    # Mesh reconstruction button
    bpy.utils.unregister_class(VMV_ReconstructMesh)

    # Mesh rendering buttons
    bpy.utils.unregister_class(VMV_RenderMeshImage)
    bpy.utils.unregister_class(VMV_RenderMesh360)

    # Mesh export button
    bpy.utils.unregister_class(VMV_ExportMesh)
