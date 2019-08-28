
# System imports
import os

# Blender imports
import bpy

# Internal imports
import vmv
import vmv.consts
import vmv.enums
import vmv.interface
import vmv.skeleton
import vmv.bbox
import vmv.rendering


####################################################################################################
# @load_morphology
####################################################################################################
def load_icons():
    """Loads the external icons.
    """
    vmv.interface.ui_icons = bpy.utils.previews.new()
    images_path = '%s/../../../data/images' % os.path.dirname(os.path.realpath(__file__))
    vmv.interface.ui_icons.load("github", os.path.join(images_path, "github-logo.png"), 'IMAGE')
    vmv.interface.ui_icons.load("bbp", os.path.join(images_path, "bbp-logo.png"), 'IMAGE')
    vmv.interface.ui_icons.load("epfl", os.path.join(images_path, "epfl-logo.png"), 'IMAGE')
    vmv.interface.ui_icons.load("vmv", os.path.join(images_path, "vmv-logo.png"), 'IMAGE')


####################################################################################################
# @load_morphology
####################################################################################################
def unload_icons():
    """Unloads the external icons, after loading them to Blender.
    """

    # Remove the icons
    bpy.utils.previews.remove(vmv.interface.ui_icons)


####################################################################################################
# @load_morphology
####################################################################################################
def enable_or_disable_layout(layout):
    """Activates or deactivates the layout based on the status of the morphology.

    :param layout:
        A given layout to enable or disable.
    """
    if vmv.interface.ui_morphology is None:
        layout.enabled = False
    else:
        layout.enabled = True


####################################################################################################
# @validate_output_directory
####################################################################################################
def validate_output_directory(panel_object,
                              context_scene):
    """Validates the existence of the output directory.

    :param panel_object:
        An object of a UI panel.

    :param context_scene:
        Current scene in the rendering context.
    """

    # Ensure that there is a valid directory where the images will be written to
    if vmv.interface.ui_options.io.output_directory is None:
        panel_object.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
        return {'FINISHED'}

    if not vmv.file.ops.path_exists(context_scene.OutputDirectory):
        panel_object.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
        return {'FINISHED'}


####################################################################################################
# @render_mesh_image
####################################################################################################
def render_morphology_image(panel_object,
                            context_scene,
                            view):
    """Renders an image of the morphology reconstructed in the scene.

    :param panel_object:
        UI Panel.
    :param context_scene:
        A reference to the Blender scene.
    :param view:
        Rendering view.
    """

    # Validate the output directory
    vmv.interface.ui.validate_output_directory(
        panel_object=panel_object, context_scene=context_scene)

    # Create the images directory if it does not exist
    if not vmv.file.ops.path_exists(vmv.interface.ui_options.io.images_directory):
        vmv.file.ops.clean_and_create_directory(vmv.interface.ui_options.io.images_directory)

    # Report the process starting in the UI
    panel_object.report({'INFO'}, 'Rendering ... Wait')

    # Compute the bounding box for a close up view
    if context_scene.MorphologyRenderingView == \
            vmv.enums.Skeletonization.Rendering.View.CLOSE_UP_VIEW:

        # Compute the bounding box for a close up view
        bounding_box = vmv.bbox.compute_unified_extent_bounding_box(
            extent=context_scene.MeshCloseUpSize)

    # Compute the bounding box for a mid shot view
    elif context_scene.MorphologyRenderingView == \
            vmv.enums.Skeletonization.Rendering.View.MID_SHOT_VIEW:

        # Compute the bounding box for the available meshes only
        bounding_box = vmv.bbox.compute_scene_bounding_box_for_curves()

    # Compute the bounding box for the wide shot view that correspond to the whole morphology
    else:

        # Compute the full morphology bounding box
        bounding_box = vmv.skeleton.compute_full_morphology_bounding_box(
            morphology=vmv.interface.ui_morphology)

    # Get the view prefix
    if view == vmv.enums.Camera.View.FRONT:
        view_prefix = 'FRONT'
    elif view == vmv.enums.Camera.View.SIDE:
        view_prefix = 'SIDE'
    elif view == vmv.enums.Camera.View.TOP:
        view_prefix = 'TOP'
    else:
        view_prefix = ''

    # Render at a specific resolution
    if context_scene.RenderingType == \
            vmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the image
        vmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=view,
            image_resolution=context_scene.MorphologyFrameResolution,
            image_name='MORPHOLOGY_%s_%s' % (view_prefix, vmv.interface.ui_options.morphology.label),
            image_directory=vmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context_scene.KeepMeshCameras)

    # Render at a specific scale factor
    else:

        # Render the image
        vmv.rendering.render_to_scale(
            bounding_box=bounding_box,
            camera_view=view,
            image_scale_factor=context_scene.MorphologyFrameScaleFactor,
            image_name='MORPHOLOGY_%s_%s' % (view_prefix, vmv.interface.ui_options.morphology.label),
            image_directory=vmv.interface.ui_options.io.images_directory,
            keep_camera_in_scene=context_scene.KeepMeshCameras)

    # Report the process termination in the UI
    panel_object.report({'INFO'}, 'Rendering Done')


####################################################################################################
# @render_mesh_image
####################################################################################################
def render_mesh_image(panel_object,
                      context_scene,
                      rendering_view,
                      camera_projection):
    """Renders an image of  mesh in the scene.

    :param panel_object:
        UI Panel.
    :param context_scene:
        A reference to the Blender scene.
    :param rendering_view:
        Rendering view.
    :param camera_projection:
        The projection of the camera.
    """

    # Validate the output directory
    vmv.interface.ui.validate_output_directory(
        panel_object=panel_object, context_scene=context_scene)

    # Create the images directory if it does not exist
    if not vmv.file.ops.path_exists(vmv.interface.ui_options.io.images_directory):
        vmv.file.ops.clean_and_create_directory(vmv.interface.ui_options.io.images_directory)

    # Report the process starting in the UI
    panel_object.report({'INFO'}, 'Rendering ... Wait')

    # Get the view prefix
    if rendering_view == vmv.enums.Camera.View.FRONT:
        view_prefix = 'FRONT'
    elif rendering_view == vmv.enums.Camera.View.SIDE:
        view_prefix = 'SIDE'
    elif rendering_view == vmv.enums.Camera.View.TOP:
        view_prefix = 'TOP'
    else:
        view_prefix = 'FRONT'

    # Render at a specific resolution
    if context_scene.MeshRenderingResolution == \
            vmv.enums.Meshing.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the image
        vmv.rendering.render(
            bounding_box=vmv.bbox.compute_scene_bounding_box_for_meshes(),
            camera_view=rendering_view,
            camera_projection=camera_projection,
            image_resolution=context_scene.MeshFrameResolution,
            image_name='MESH_%s_%s' % (view_prefix, vmv.interface.ui_options.morphology.label),
            image_directory=vmv.interface.ui_options.io.images_directory)

    # Render at a specific scale factor
    else:

        # Render the image
        vmv.rendering.render_to_scale(
            bounding_box=vmv.bbox.compute_scene_bounding_box_for_meshes(),
            camera_view=rendering_view,
            camera_projection=camera_projection,
            image_scale_factor=context_scene.MeshFrameScaleFactor,
            image_name='MESH_%s_%s' % (view_prefix, vmv.interface.ui_options.morphology.label),
            image_directory=vmv.interface.ui_options.io.images_directory)

    # Report the process termination in the UI
    panel_object.report({'INFO'}, 'Rendering Done')
