
# System imports
import os
import copy

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
    if vmv.interface.MorphologyObject is None:
        layout.enabled = False
    else:
        layout.enabled = True


####################################################################################################
# @validate_output_directory
####################################################################################################
def validate_output_directory(panel):
    """Validates the existence of the output directory.

    :param panel:
        An object of a UI panel.
    """

    # Ensure that there is a valid directory where the images will be written to
    if vmv.interface.Options.io.output_directory is None:
        panel.report({'ERROR'}, vmv.consts.Messages.PATH_NOT_SET)
        return {'FINISHED'}

    # At first, try to create it
    if not vmv.file.ops.path_exists(vmv.interface.Options.io.output_directory):
        vmv.file.ops.clean_and_create_directory(vmv.interface.Options.io.output_directory)

    # Then, check if it exists or not
    if not vmv.file.ops.path_exists(vmv.interface.Options.io.output_directory):
        panel.report({'ERROR'}, vmv.consts.Messages.INVALID_OUTPUT_PATH)
        return {'FINISHED'}


####################################################################################################
# @verify_images_directory
####################################################################################################
def verify_images_directory(panel):
    """Validates the existence of the images directory, before rendering.

    :param panel:
        An object of a UI panel.
    """

    # Validate the output directory in advance
    validate_output_directory(panel=panel)

    # Create the images directory if it does not exist
    if not vmv.file.ops.path_exists(vmv.interface.Options.io.images_directory):
        vmv.file.ops.clean_and_create_directory(vmv.interface.Options.io.images_directory)


####################################################################################################
# @verify_sequences_directory
####################################################################################################
def verify_sequences_directory(panel):
    """Validates the existence of the sequences directory, before rendering.

    :param panel:
        An object of a UI panel.
    """

    # Validate the output directory in advance
    validate_output_directory(panel=panel)

    # Create the images directory if it does not exist
    if not vmv.file.ops.path_exists(vmv.interface.Options.io.sequences_directory):
        vmv.file.ops.clean_and_create_directory(vmv.interface.Options.io.sequences_directory)


####################################################################################################
# @verify_meshes_directory
####################################################################################################
def verify_meshes_directory(panel):
    """Validates the existence of the meshes directory, before exporting.

    :param panel:
        An object of a UI panel.
    """

    # Validate the output directory in advance
    validate_output_directory(panel=panel)

    # Create the images directory if it does not exist
    if not vmv.file.ops.path_exists(vmv.interface.Options.io.meshes_directory):
        vmv.file.ops.clean_and_create_directory(vmv.interface.Options.io.meshes_directory)


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
# @render_morphology_image
####################################################################################################
def render_morphology_image(panel,
                            scene,
                            rendering_view,
                            camera_projection,
                            add_background_plane):
    """Renders an image of morphology in the scene.

    :param panel:
       UI Panel.
    :param scene:
       A reference to the Blender scene.
    :param rendering_view:
       Rendering view.
    :param camera_projection:
       The projection of the camera.
    :param add_background_plane:
       Adds a background plane to the final image.
    """

    # Verify the presence of the images directory
    vmv.interface.verify_images_directory(panel=panel)

    # Compute the bounding box for the available meshes only
    bounding_box = vmv.bbox.compute_scene_bounding_box()

    # Image name
    image_name = 'MORPHOLOGY_%s_%s' % (vmv.interface.Options.morphology.label, rendering_view)

    # Stretch the bounding box by few microns and some distance to highlight the rendering
    rendering_bbox = copy.deepcopy(bounding_box)
    rendering_bbox.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)
    rendering_bbox.extend_bbox(delta=bounding_box.compute_diagonal() * 0.1)

    # Draw the morphology scale bar
    if scene.VMV_RenderMorphologyScaleBar:
        scale_bar = vmv.interface.draw_scale_bar(
            bounding_box=rendering_bbox,
            material_type=vmv.interface.Options.morphology.material,
            view=vmv.Options.morphology.camera_view)

    # Render at a specific resolution
    if scene.VMV_MorphologyRenderingResolution == vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:

        # Render the morphology
        vmv.rendering.render(
            bounding_box=rendering_bbox,
            camera_view=rendering_view,
            camera_projection=camera_projection,
            image_resolution=scene.VMV_MorphologyImageResolution,
            image_name=image_name,
            image_directory=vmv.interface.Options.io.images_directory,
            add_background_plane=add_background_plane)

    # Render at a specific scale factor
    else:

        # Render the morphology
        vmv.rendering.render_to_scale(
            bounding_box=rendering_bbox,
            camera_view=vmv.Options.morphology.camera_view,
            image_scale_factor=scene.VMV_MorphologyImageScaleFactor,
            image_name=image_name,
            image_directory=vmv.interface.Options.io.images_directory,
            add_background_plane=add_background_plane)

    # Delete the morphology scale bar, if rendered
    if scene.VMV_RenderMorphologyScaleBar:
        vmv.scene.delete_object_in_scene(scene_object=scale_bar)


####################################################################################################
# @render_mesh_image
####################################################################################################
def render_mesh_image(panel,
                      scene,
                      rendering_view,
                      camera_projection,
                      add_background_plane):
    """Renders an image of  mesh in the scene.

    :param panel:
        UI Panel.
    :param scene:
        A reference to the Blender scene.
    :param rendering_view:
        Rendering view.
    :param camera_projection:
        The projection of the camera.
    :param add_background_plane:
        Adds a background plane to the final image.
    """

    # Verify the presence of the images directory
    vmv.interface.verify_images_directory(panel=panel)

    # Compute the bounding box for the available meshes only
    bounding_box = vmv.bbox.compute_scene_bounding_box_for_meshes()

    # Image name
    image_name = 'MESH_%s_%s' % (vmv.interface.Options.morphology.label, rendering_view)

    # Stretch the bounding box by few microns
    rendering_bbox = copy.deepcopy(bounding_box)
    rendering_bbox.extend_bbox(delta=vmv.consts.Image.GAP_DELTA)
    rendering_bbox.extend_bbox(delta=bounding_box.compute_diagonal() * 0.1)

    # Draw the scale bar
    if scene.VMV_RenderMeshScaleBar:
        scale_bar = vmv.interface.draw_scale_bar(
            bounding_box=rendering_bbox,
            material_type=vmv.interface.Options.mesh.material,
            view=vmv.Options.mesh.camera_view)

    # Render at a specific RESOLUTION
    if scene.VMV_MeshRenderingResolution == vmv.enums.Rendering.Resolution.FIXED_RESOLUTION:
        vmv.rendering.render(
            bounding_box=rendering_bbox,
            camera_view=rendering_view,
            camera_projection=camera_projection,
            image_resolution=scene.VMV_MeshFrameResolution,
            image_name=image_name,
            image_directory=vmv.interface.Options.io.images_directory,
            add_background_plane=add_background_plane)

    # Render at a specific SCALE FACTOR
    else:
        vmv.rendering.render_to_scale(
            bounding_box=rendering_bbox,
            camera_view=rendering_view,
            image_scale_factor=scene.VMV_MeshFrameScaleFactor,
            image_name=image_name,
            image_directory=vmv.interface.Options.io.images_directory,
            add_background_plane=add_background_plane)

    # Delete the scale bar, if rendered
    if scene.VMV_RenderMeshScaleBar:
        vmv.scene.delete_object_in_scene(scene_object=scale_bar)


####################################################################################################
# @is_vascular_morphology_in_scene
####################################################################################################
def is_vascular_morphology_in_scene():
    """Makes sure that the morphology is loaded and drawn in the scene.

    :return:
        True if the morphology skeleton is in the scene, False otherwise.
    """

    # Make sure that the morphology is loaded and drawn in the scene
    if vmv.interface.MorphologyObject is not None:
        if vmv.scene.is_object_in_scene_by_name('%s%s' % (
                vmv.interface.MorphologyObject.name, vmv.consts.Suffix.MORPHOLOGY_SUFFIX)):
            return True
    return False


####################################################################################################
# @is_vascular_mesh_in_scene
####################################################################################################
def is_vascular_mesh_in_scene():
    """Makes sure that the vascular mesh is in the scene.

    :return:
        True if the vascular mesh is in the scene, False otherwise.
    """

    # Make sure that the morphology is loaded and drawn in the scene
    if vmv.interface.MorphologyObject is not None:
        if vmv.scene.is_object_in_scene_by_name('%s%s' % (
                vmv.interface.MorphologyObject.name, vmv.consts.Suffix.MESH_SUFFIX)):
            return True
    return False
