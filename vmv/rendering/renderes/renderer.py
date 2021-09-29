####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
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
import vmv
import vmv.consts
import vmv.enums
import vmv.rendering


################################################################################################
# @render
################################################################################################
def render(bounding_box,
           camera_view=vmv.enums.Rendering.View.FRONT,
           camera_projection=vmv.enums.Rendering.Projection.ORTHOGRAPHIC,
           image_resolution=vmv.consts.Image.DEFAULT_RESOLUTION,
           image_name='image',
           image_directory=None,
           add_background_plane=False,
           keep_camera_in_scene=False):
    """Render the reconstructed mesh to a .PNG image.

    :param bounding_box:
        The bounding box of the view requested to be rendered.
    :param camera_view:
        The view of the camera, by default FRONT.
    :param camera_projection:
        The projection of the camera, by default ORTHOGRAPHIC.
    :param image_resolution:
        The resolution of the image, by default 1024.
    :param image_name:
        The name of the image, by default 'image'.
    :param image_directory:
        The directory where the image will be rendered. If the directory is set to None,
        then the prefix is included in @image_name.
    :param add_background_plane:
        Adds a background plane to the final image.
    :param keep_camera_in_scene:
        Keep the camera used to do the rendering after the rendering is done.
    """

    # Create a camera
    skeleton_camera = vmv.rendering.Camera('VMVCamera_%s' % camera_view)

    # Image path prefix, i.e. w/o extension which will be added later
    image_prefix = \
        '%s/%s' % (image_directory, image_name) if image_directory is not None else image_name

    # Render an image
    skeleton_camera.render_scene(bounding_box=bounding_box,
                                 camera_view=camera_view,
                                 camera_projection=camera_projection,
                                 image_resolution=image_resolution,
                                 image_name=image_prefix,
                                 add_background_plane=add_background_plane,
                                 keep_camera_in_scene=keep_camera_in_scene)


################################################################################################
# @render_to_scale
################################################################################################
def render_to_scale(bounding_box,
                    camera_view=vmv.enums.Rendering.View.FRONT,
                    image_scale_factor=vmv.consts.Image.DEFAULT_IMAGE_SCALE_FACTOR,
                    image_name='image',
                    image_directory=None,
                    add_background_plane=False,
                    keep_camera_in_scene=False):
    """Render the reconstructed mesh to scale to a .PNG image.

    :param bounding_box:
        The bounding box of the view requested to be rendered.
    :param camera_view:
        The view of the camera, by default FRONT.
    :param image_scale_factor:
        The factor used to scale the resolution of the image the image, by default 1.
    :param image_name:
        The name of the image, by default 'MESH'.
    :param image_directory:
        The directory where the image will be rendered. If the directory is set to None,
        then the prefix is included in @image_name.
    :param add_background_plane:
        Adds a background plane to the final image.
    :param keep_camera_in_scene:
        Keep the camera used to do the rendering after the rendering is done.
    """

    # Create a camera
    skeleton_camera = vmv.rendering.Camera('MeshCamera_%s' % camera_view)

    # Image path prefix, i.e. w/o extension which will be added later
    image_prefix = '%s/%s' % (
        image_directory, image_name) if image_directory is not None else image_name

    # Render an image
    skeleton_camera.render_scene_to_scale(bounding_box=bounding_box,
                                          camera_view=camera_view,
                                          scale_factor=image_scale_factor,
                                          image_name=image_prefix,
                                          add_background_plane=add_background_plane,
                                          keep_camera_in_scene=keep_camera_in_scene)


################################################################################################
# @render_at_angle
################################################################################################
def render_at_angle(scene_objects,
                    angle,
                    bounding_box,
                    camera_view=vmv.enums.Rendering.View.FRONT_360,
                    image_resolution=vmv.consts.Image.DEFAULT_RESOLUTION,
                    image_name='image',
                    add_background_plane=False,
                    image_directory=None):
    """Render the mesh to a .PNG image at a specific angle.

    :param scene_objects:
        A list of all the objects that belong to the reconstructed mesh.
    :param angle:
        The angle the frame will be rendered at.
    :param bounding_box:
        The bounding box of the view requested to be rendered.
    :param camera_view:
        The view of the camera, by default FRONT.
    :param image_resolution:
        The resolution of the image, by default 512.
    :param image_name:
        The name of the image, by default 'SKELETON'.
    :param add_background_plane:
        Adds a background plane to the scene.
    :param image_directory:
        The directory where the image will be rendered. If the directory is set to None,
        then the prefix is included in @image_name.
    """

    # Rotate all the objects as if they are a single object
    for scene_object in scene_objects:

        # Ignore the background plane if it exists
        if scene_object.name == 'background_plane':
            continue

        # Rotate the mesh object around the y axis
        scene_object.rotation_euler[1] = angle * 2 * 3.14 / 360.0

    # Render the image
    render(bounding_box=bounding_box, camera_view=camera_view, image_resolution=image_resolution,
           image_name=image_name, add_background_plane=add_background_plane,
           keep_camera_in_scene=False)


################################################################################################
# @render_at_angle_to_scale
################################################################################################
def render_at_angle_to_scale(scene_objects,
                             angle,
                             bounding_box,
                             camera_view=vmv.enums.Rendering.View.FRONT_360,
                             image_scale_factor=vmv.consts.Image.DEFAULT_IMAGE_SCALE_FACTOR,
                             image_name='image',
                             add_background_plane=False,
                             image_directory=None):
    """Render the mesh to a .PNG image at a specific angle.

    :param scene_objects:
        A list of all the objects that belong to the reconstructed mesh.
    :param angle:
        The angle the frame will be rendered at.
    :param bounding_box:
        The bounding box of the view requested to be rendered.
    :param camera_view:
        The view of the camera, by default FRONT.
    :param image_scale_factor:
        The factor used to scale the resolution of the image the image, by default 1.
    :param image_name:
        The name of the image, by default 'SKELETON'.
    :param add_background_plane:
        Adds a background plane to the final image.
    :param image_directory:
        The directory where the image will be rendered. If the directory is set to None,
        then the prefix is included in @image_name.
    """

    # Rotate all the objects as if they are a single object
    for scene_object in scene_objects:

        # Rotate the mesh object around the y axis
        scene_object.rotation_euler[1] = angle * 2 * 3.14 / 360.0

    # Render the image to scale
    render_to_scale(bounding_box=bounding_box,
                    camera_view=camera_view,
                    image_scale_factor=image_scale_factor,
                    image_name=image_name,
                    add_background_plane=add_background_plane,
                    keep_camera_in_scene=False)
