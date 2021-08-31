
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
    vmv.interface.Icons = bpy.utils.previews.new()
    images_path = '%s/../../../data/images' % os.path.dirname(os.path.realpath(__file__))
    vmv.interface.Icons.load("github", os.path.join(images_path, "github-logo.png"), 'IMAGE')
    vmv.interface.Icons.load("bbp", os.path.join(images_path, "bbp-logo.png"), 'IMAGE')
    vmv.interface.Icons.load("epfl", os.path.join(images_path, "epfl-logo.png"), 'IMAGE')
    vmv.interface.Icons.load("vmv", os.path.join(images_path, "vmv-logo.png"), 'IMAGE')


####################################################################################################
# @load_morphology
####################################################################################################
def load_fonts():
    """Loads all the fonts to the add-on.
    """

    # Get all the font files in the fonts directory
    font_files = vmv.file.get_files_in_directory(
        directory=vmv.consts.Paths.FONTS_DIRECTORY, file_extension='ttf')

    # Load fonts
    for font_file in font_files:
        font = '%s/%s' % (vmv.consts.Paths.FONTS_DIRECTORY, font_file)
        bpy.data.fonts.load(font)


####################################################################################################
# @load_morphology
####################################################################################################
def unload_icons():
    """Unloads the external icons, after loading them to Blender.
    """

    # Remove the icons
    bpy.utils.previews.remove(vmv.interface.Icons)


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
    if Globals.Options.io.output_directory is None:
        panel_object.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
        return {'FINISHED'}

    if not vmv.file.ops.path_exists(context_scene.VMV_OutputDirectory):
        panel_object.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
        return {'FINISHED'}


####################################################################################################
# @configure_output_directory
####################################################################################################
def configure_output_directory(options,
                               context=None):
    """Configures the output directory after loading the data.

    :param options:
        System options.
    :param context:
        Context.
    """

    # If the output directory is not set
    if options.io.output_directory is None or 'Select Directory' in options.io.output_directory:

        # Suggest an output directory at the home folder
        suggested_output_folder = '%s/vessmorphovis-output' % os.path.expanduser('~')

        # Check if the output directory already exists or not
        if os.path.exists(suggested_output_folder):

            # Update the system options
            vmv.interface.Options.io.output_directory = suggested_output_folder

            # Update the UI
            context.scene.VMV_OutputDirectory = suggested_output_folder

        # Otherwise, create it
        else:

            # Try to create the directory there
            try:

                # Create the directory
                os.mkdir(suggested_output_folder)

                # Update the system options
                vmv.interface.Options.io.output_directory = suggested_output_folder

                # Update the UI
                context.scene.VMV_OutputDirectory = suggested_output_folder

            # Voila
            except ValueError:
                pass

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
    if not vmv.file.ops.path_exists(Globals.Options.io.images_directory):
        vmv.file.ops.clean_and_create_directory(Globals.Options.io.images_directory)

    # Report the process starting in the UI
    panel_object.report({'INFO'}, 'Rendering ... Wait')

    # Compute the bounding box for a close up view
    if context_scene.MorphologyRenderingView == \
            vmv.enums.Rendering.View.CLOSE_UP_VIEW:

        # Compute the bounding box for a close up view
        bounding_box = vmv.bbox.compute_unified_extent_bounding_box(
            extent=context_scene.MeshCloseUpSize)

    # Compute the bounding box for a mid shot view
    elif context_scene.MorphologyRenderingView == \
            vmv.enums.Rendering.View.MID_SHOT_VIEW:

        # Compute the bounding box for the available meshes only
        bounding_box = vmv.bbox.compute_scene_bounding_box_for_curves()

    # Compute the bounding box for the wide shot view that correspond to the whole morphology
    else:

        # Compute the full morphology bounding box
        bounding_box = vmv.skeleton.compute_full_morphology_bounding_box(
            morphology=vmv.interface.ui_morphology)

    # Get the view prefix
    if view == vmv.enums.Rendering.View.FRONT:
        view_prefix = 'FRONT'
    elif view == vmv.enums.Rendering.View.SIDE:
        view_prefix = 'SIDE'
    elif view == vmv.enums.Rendering.View.TOP:
        view_prefix = 'TOP'
    else:
        view_prefix = ''

    # Render at a specific resolution
    if context_scene.RenderingType == \
            vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the image
        vmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=view,
            image_resolution=context_scene.VMV_MorphologyImageResolution,
            image_name='MORPHOLOGY_%s_%s' % (view_prefix, Globals.Options.morphology.label),
            image_directory=Globals.Options.io.images_directory,
            keep_camera_in_scene=context_scene.KeepMeshCameras)

    # Render at a specific scale factor
    else:

        # Render the image
        vmv.rendering.render_to_scale(
            bounding_box=bounding_box,
            camera_view=view,
            image_scale_factor=context_scene.VMV_MorphologyImageScaleFactor,
            image_name='MORPHOLOGY_%s_%s' % (view_prefix, Globals.Options.morphology.label),
            image_directory=Globals.Options.io.images_directory,
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
    if not vmv.file.ops.path_exists(Globals.Options.io.images_directory):
        vmv.file.ops.clean_and_create_directory(Globals.Options.io.images_directory)

    # Report the process starting in the UI
    panel_object.report({'INFO'}, 'Rendering ... Wait')

    # Get the view prefix
    if rendering_view == vmv.enums.Rendering.View.FRONT:
        view_prefix = 'FRONT'
    elif rendering_view == vmv.enums.Rendering.View.SIDE:
        view_prefix = 'SIDE'
    elif rendering_view == vmv.enums.Rendering.View.TOP:
        view_prefix = 'TOP'
    else:
        view_prefix = 'FRONT'

    bounding_box = vmv.bbox.compute_scene_bounding_box_for_meshes()

    # If background plane is required
    background_plane = vmv.rendering.add_background_plane(
        bounding_box=bounding_box, camera_view=vmv.options.mesh.camera_view)

    # Render at a specific resolution
    if context_scene.MeshRenderingResolution == \
            vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the image
        vmv.rendering.render(
            bounding_box=bounding_box,
            camera_view=rendering_view,
            camera_projection=camera_projection,
            image_resolution=context_scene.MeshFrameResolution,
            image_name='MESH_%s_%s' % (view_prefix, Globals.Options.morphology.label),
            image_directory=Globals.Options.io.images_directory)

    # Render at a specific scale factor
    else:

        # Render the image
        vmv.rendering.render_to_scale(
            bounding_box=bounding_box,
            camera_view=rendering_view,
            image_scale_factor=context_scene.MeshFrameScaleFactor,
            image_name='MESH_%s_%s' % (view_prefix, Globals.Options.morphology.label),
            image_directory=Globals.Options.io.images_directory)

    # Report the process termination in the UI
    panel_object.report({'INFO'}, 'Rendering Done')
