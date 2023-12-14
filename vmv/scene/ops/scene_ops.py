####################################################################################################
# Copyright (c) 2019 - 2023, EPFL / Blue Brain Project
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
import bpy

# Blender imports
from mathutils import Vector

# Internal imports
import vmv.bbox
import vmv.bops
import vmv.mesh
import vmv.utilities


####################################################################################################
# @update_scene
####################################################################################################
def update_scene():
    """Updates the scene and the 3d view after any transformation."""

    bpy.context.view_layer.update()


####################################################################################################
# @view_axis
####################################################################################################
def view_axis(axis='TOP'):
    """Views the given axis (or projection) in the 3D viewport.

    :param axis:
        An enum in ['LEFT', 'RIGHT', 'BOTTOM', 'TOP', 'FRONT', 'BACK'].
    """

    vmv.bops.view_axis(axis=axis)


####################################################################################################
# @select_object
####################################################################################################
def select_object(scene_object):
    """Selects a given object in the scene. If a previous object is already selected, both
    objects will be selected.

    :param scene_object:
        A given scene object to be selected.
    """

    if vmv.utilities.is_blender_280():
        scene_object.select_set(True)
    else:
        scene_object.select = True


####################################################################################################
# @deselect_object
####################################################################################################
def deselect_object(scene_object):
    """Deselects a given object in the scene.

    :param scene_object:
        A given scene object to be deselected.
    """

    if vmv.utilities.is_blender_280():
        scene_object.select_set(False)
    else:
        scene_object.select = False


####################################################################################################
# @is_object_existing
####################################################################################################
def is_object_existing(scene_object):
    """Verifies if a given object still exists in the scene or not.

    :param scene_object:
         A reference to the given scene object to verify its existence.
    :return:
        True if the object exists, False otherwise.
    """

    # None cannot exist in the system
    if scene_object is None:
        return False

    for i_object in bpy.data.objects:
        if i_object.name == scene_object.name:
            return True
    return False


####################################################################################################
# @is_object_deleted
####################################################################################################
def is_object_deleted(scene_object):
    """Checks if an object indicated by the given reference is in the scene or not.

    :param scene_object:
        A reference to the given scene object to verify its deletion.
    :return:
        True if the object is deleted, otherwise False and the object is still in the scene.
    """

    return not is_object_existing(scene_object=scene_object)


####################################################################################################
# @set_transparent_background
####################################################################################################
def set_transparent_background():
    """Sets the background to transparent."""

    if vmv.utilities.is_blender_280():
        bpy.context.scene.render.film_transparent = True
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    else:
        bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
        bpy.context.scene.render.image_settings.color_mode = 'RGBA'


####################################################################################################
# @set_colors_to_raw
####################################################################################################
def set_colors_to_raw():
    """Use RAW colors with FLAT shading to lighten the results."""

    bpy.context.scene.view_settings.view_transform = 'Raw'


####################################################################################################
# @set_colors_to_filimc
####################################################################################################
def set_colors_to_filimc():
    """Use filmic mode for rendering."""

    bpy.context.scene.view_settings.view_transform = 'Filmic'


####################################################################################################
# @set_background_color
####################################################################################################
def set_background_color(color,
                         transparent=False):
    """Sets the background image properties.

    :param color:
        A given color.
    :param transparent:
        A flag to indicate if the image is transparent or not. Setting this flag to True overrides
        the color.
    """

    if vmv.utilities.is_blender_280():

        # Transparency
        bpy.context.scene.render.film_transparent = transparent

        # Image mode to avoid the alpha channel issues
        if transparent:
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'
        else:
            bpy.context.scene.render.image_settings.color_mode = 'RGB'

            # If Workbench render is used, adjust the color as follows
            if bpy.context.scene.render.engine == 'BLENDER_WORKBENCH':

                # Set the color selected
                bpy.context.scene.world.color = color

                # Fix the WHITE BUG
                if color[0] > 0.9 and color[1] > 0.9 and color[2] > 0.9:
                    bpy.context.scene.world.color = vmv.consts.Color.VERY_WHITE

            # Cycles and Eevee
            else:

                # Get a reference to the WORLD
                world = bpy.data.worlds['World']

                # Use nodes
                world.use_nodes = True

                # Get the background node
                bg = world.node_tree.nodes['Background']

                # Set the color
                bg.inputs[0].default_value = (color[0], color[1], color[2], 1)

                # Fix the WHITE BUG
                if color[0] > 0.9 and color[1] > 0.9 and color[2] > 0.9:
                    bg.inputs[0].default_value = (10, 10, 10, 1)
    else:

        # Transparency background
        if transparent:
            bpy.context.scene.render.alpha_mode = 'TRANSPARENT'
            bpy.context.scene.render.image_settings.color_mode = 'RGBA'

        # Non-transparent background
        else:

            # If Cycles
            if bpy.context.scene.render.engine == 'CYCLES':

                # Get a reference to the WORLD
                world = bpy.data.worlds['World']

                # Use nodes
                world.use_nodes = True

                # Get the background node
                bg = world.node_tree.nodes['Background']

                # Set the color
                bg.inputs[0].default_value = (color[0], color[1], color[2], 1)

                # Fix the WHITE BUG
                if color[0] > 0.9 and color[1] > 0.9 and color[2] > 0.9:
                    bg.inputs[0].default_value = (10, 10, 10, 1)

            # If Blender render
            else:
                bpy.context.scene.render.alpha_mode = 'SKY'
                bpy.context.scene.render.image_settings.color_mode = 'RGB'

                # Color
                bpy.context.scene.world.horizon_color = color

                # Fix the WHITE BUG
                if color[0] > 0.9 and color[1] > 0.9 and color[2] > 0.9:
                    bpy.context.scene.world.horizon_color = vmv.consts.Color.VERY_WHITE


####################################################################################################
# @get_active_object
####################################################################################################
def get_active_object():
    """Returns a reference to the active object in the scene.

    :return:
        A reference to the active object in the scene.
    """

    if vmv.utilities.is_blender_280():
        return bpy.context.active_object
    else:
        return bpy.context.scene.objects.active


####################################################################################################
# @link_object_to_scene
####################################################################################################
def link_object_to_scene(input_object):
    """Links a reconstructed object to the scene.

    :param input_object:
        A reference to the given object that will be linked to the scene.
    """

    if vmv.utilities.is_blender_280():
        bpy.context.scene.collection.objects.link(input_object)
    else:
        bpy.context.scene.objects.link(input_object)


####################################################################################################
# @unlink_object_from_scene
####################################################################################################
def unlink_object_from_scene(scene_object):
    """Links a reconstructed object to the scene.

    :param scene_object:
        A reference to the scene object to be unlinked from the scene.
    """

    if vmv.utilities.is_blender_280():
        bpy.context.scene.collection.objects.unlink(scene_object)
    else:
        bpy.context.scene.objects.unlink(scene_object)


####################################################################################################
# @hide_object
####################################################################################################
def hide_object(scene_object):
    """Hides a shown object in the scene.

    :param scene_object:
        The reference to the given scene object to be hidden.
    """

    if vmv.utilities.is_blender_280():
        scene_object.hide_viewport = True
    else:
        scene_object.hide = True


####################################################################################################
# @unhide_object
####################################################################################################
def unhide_object(scene_object):
    """Shows a hidden object in the scene.

    :param scene_object:
        The reference to the given scene object to be shown after it was hidden.
    """

    if vmv.utilities.is_blender_280():
        scene_object.hide_viewport = False
    else:
        scene_object.hide = False


####################################################################################################
# @clear_default_scene
####################################################################################################
def clear_default_scene():
    """Clear the default scene loaded in Blender: the ['Cube', 'Lamp' and 'Camera']."""

    # Iterate over all the objects in the scene, and remove the 'Cube', 'Lamp' and 'Camera' if exist
    for scene_object in bpy.context.scene.objects:

        # Object selection
        if scene_object.name == 'Cube' or scene_object.name == 'Lamp' or scene_object.name == 'Camera':
            select_object(scene_object)

            # Delete the object, quietly
            vmv.utilities.disable_std_output()
            bpy.ops.object.delete()
            vmv.utilities.enable_std_output()


####################################################################################################
# @clear_scene
####################################################################################################
def clear_scene():
    """Clears a scene, removes all existing objects in it and unlink their references."""

    # Make all the objects in the scene visible
    for scene_object in bpy.context.scene.objects:
        unhide_object(scene_object)

    # Select each object in the scene
    for scene_object in bpy.context.scene.objects:
        select_object(scene_object)

    # Delete the object
    vmv.utilities.disable_std_output()
    bpy.ops.object.delete()
    vmv.utilities.enable_std_output()

    # Unlink all the objects in all the layers
    for scene in bpy.data.scenes:
        for scene_object in scene.objects:
            vmv.utilities.disable_std_output()
            unlink_object_from_scene(scene_object)
            vmv.utilities.enable_std_output()

    # Select all the meshes, unlink them and clear their data
    for scene_mesh in bpy.data.meshes:
        vmv.utilities.disable_std_output()
        bpy.data.meshes.remove(scene_mesh, do_unlink=True)
        vmv.utilities.enable_std_output()

    # Select all the curves, unlink them and clear their data
    for scene_curve in bpy.data.curves:
        vmv.utilities.disable_std_output()
        bpy.data.curves.remove(scene_curve, do_unlink=True)
        vmv.utilities.enable_std_output()

    # Select all the scene objects, unlink them and clear their data
    for scene_object in bpy.data.objects:
        vmv.utilities.disable_std_output()
        bpy.data.objects.remove(scene_object, do_unlink=True)
        vmv.utilities.enable_std_output()

    # Select all the scene materials, unlink them and clear their data
    for scene_material in bpy.data.materials:
        vmv.utilities.disable_std_output()
        bpy.data.materials.remove(scene_material, do_unlink=True)
        vmv.utilities.enable_std_output()


####################################################################################################
# @clear_lights
####################################################################################################
def clear_lights():
    """Clears all the lights in the scene."""

    # Iterate over all the objects in the scene, and remove the objects of type LIGHT
    for scene_object in bpy.context.scene.objects:

        # Object selection, select by type
        if 'LIGHT' in scene_object.type:
            select_object(scene_object)

            # Delete the object
            vmv.utilities.disable_std_output()
            bpy.ops.object.delete()
            vmv.utilities.enable_std_output()

    # Select all the light, unlink them and clear their data
    if vmv.utilities.is_blender_280():
        for scene_lamp in bpy.data.lights:
            vmv.utilities.disable_std_output()
            bpy.data.lights.remove(scene_lamp, do_unlink=True)
            vmv.utilities.enable_std_output()

    else:
        for scene_lamp in bpy.data.lamps:
            vmv.utilities.disable_std_output()
            bpy.data.lamps.remove(scene_lamp, do_unlink=True)
            vmv.utilities.enable_std_output()


####################################################################################################
# @clear_scene_materials
####################################################################################################
def clear_scene_materials():
    """Cleans all the materials in the scene.
    NOTE: This function is called every time a scene is being drawn to avoid overloading the memory.
    """

    # Clear all the materials that are already present in the scene
    for material in bpy.data.materials:
        material.user_clear()
        bpy.data.materials.remove(material)


####################################################################################################
# @clear_scene_materials
####################################################################################################
def clear_material_with_name(name):
    """Clears a material with a specific name.

    :param name:
        Material name.
    """

    # Clear a specific material with a given name
    for material in bpy.data.materials:

        # Make sure that is has the same name
        if material.name == name:
            material.user_clear()
            bpy.data.materials.remove(material)


####################################################################################################
# @select_all
####################################################################################################
def select_all():
    """Selects all the objects in the scene."""

    for scene_object in bpy.context.scene.objects:
        select_object(scene_object)


####################################################################################################
# @deselect_all
####################################################################################################
def deselect_all():
    """Deselects all the objects in the scene."""

    for scene_object in bpy.context.scene.objects:
        deselect_object(scene_object)


####################################################################################################
# @select_objects
####################################################################################################
def select_objects(object_list):
    """Selects all the objects in a given list.

    :param object_list:
        A list of objects that must exist in the scene.
    """

    # For each object in the scene, verify its existence and then selects it
    for scene_object in object_list:
        if is_object_existing(scene_object=scene_object):
            select_object(scene_object=scene_object)


####################################################################################################
# @select_object_by_name
####################################################################################################
def select_object_by_name(object_name):
    """Selects an object in the scene given its name.

    :param object_name:
        The name of object to be selected.
    """

    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            select_object(scene_object)


####################################################################################################
# @select_object_containing_string
####################################################################################################
def select_object_containing_string(search_string):
    """Select an object in the scene given part of its name.

    :param search_string:
        The name of first object that contains part of the given string.
    """

    for scene_object in bpy.context.scene.objects:
        if search_string in scene_object.name:
            select_object(scene_object)
            return scene_object


####################################################################################################
# @deselect_object_by_name
####################################################################################################
def deselect_object_by_name(object_name):
    """Deselects an object in the scene given its name.

    :param object_name:
        The name of object to be deselected.
    """

    # Set the '.select' flag of the object to False
    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            deselect_object(scene_object)


####################################################################################################
# @select_all_meshes_in_scene
####################################################################################################
def select_all_meshes_in_scene():
    """Selects all the mesh objects (those of type 'MESH') in the scene."""

    # Deselect all the objects in the scene
    deselect_all()

    # Select only the objects of type MESH
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            select_object(scene_object)


####################################################################################################
# @deselect_all_meshes_in_scene
####################################################################################################
def deselect_all_meshes_in_scene():
    """Deselect all the mesh objects (those of type 'MESH') in the scene."""

    # Deselect only the objects of type MESH
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            deselect_object(scene_object)


####################################################################################################
# @select_all_curves_in_scene
####################################################################################################
def select_all_curves_in_scene():
    """Selects all the curve objects (those of type 'CURVE') in the scene."""

    # Deselect all the objects in the scene
    deselect_all()

    # Deselect only the objects of type CURVE
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            select_object(scene_object)


####################################################################################################
# @deselect_all_curves_in_scene
####################################################################################################
def deselect_all_curves_in_scene():
    """Deselects all the curve objects (those of type 'CURVE') in the scene."""

    # Deselect only the objects of type CURVE
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            deselect_object(scene_object)


####################################################################################################
# @get_list_of_meshes_in_scene
####################################################################################################
def get_list_of_meshes_in_scene():
    """Return a list of references to all the meshes (objects of type 'MESH') in the scene.

    :return:
        A list of references to all the meshes (objects of type 'MESH') in the scene.
    """

    # Select only the objects of type MESH, and append their references to the list
    mesh_list = list()
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            mesh_list.append(scene_object)

    # Return a reference to the list
    return mesh_list


####################################################################################################
# @get_list_of_curves_in_scene
####################################################################################################
def get_list_of_curves_in_scene():
    """Return a list of references to all the curves (objects of type 'CURVE') in the scene.

    :return:
        A list of references to all the curves (objects of type 'CURVE') in the scene
    """

    # Select only the objects of type CURVE, and append their references to the list
    curve_list = list()
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            curve_list.append(scene_object)

    # Return a reference to the list
    return curve_list


####################################################################################################
# @get_list_of_objects_in_scene
####################################################################################################
def get_list_of_objects_in_scene():
    """Return a list of references to all the objects in the scene.

    :return:
        A list of references to all the objects in the scene
    """

    # Simply add all the objects
    object_list = list()
    for scene_object in bpy.context.scene.objects:
        object_list.append(scene_object)

    # Return a reference to the list
    return object_list


####################################################################################################
# @get_reference_to_object_by_name
####################################################################################################
def get_reference_to_object_by_name(object_name):
    """Return a reference to an object in the scene given its name.

    :param object_name:
        The name of object.
    :return:
        A reference to the selected object.
    """

    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            return scene_object


####################################################################################################
# @get_list_of_objects_containing_string
####################################################################################################
def get_list_of_objects_containing_string(search_string):
    """Gets a list of objects whose names contain the given search string.

    :param search_string:
        A search string used to query the objects in the scene.
    :return:
        A list of scene objects whose names contain the given search string.
    """

    objects_list = list()
    for scene_object in bpy.context.scene.objects:
        if search_string in scene_object.name:
            objects_list.append(scene_object)
    return objects_list


####################################################################################################
# @get_list_of_mesh_objects_containing_string
####################################################################################################
def get_list_of_mesh_objects_containing_string(search_string):
    """Gets a list of meshes whose names contain the given search string.

    :param search_string:
        A search string used to query the objects in the scene.
    :return:
        A list of meshes whose names contain the given search string.
    """

    objects_list = list()
    for scene_object in bpy.context.scene.objects:
        if search_string in scene_object.name and scene_object.type == 'MESH':
            objects_list.append(scene_object)
    return objects_list


####################################################################################################
# @delete_object
####################################################################################################
def delete_object_in_scene(scene_object):
    """Deletes a given object from the scene.

    :param scene_object:
        A given object to be deleted from the scene.
    """

    # Deselect all the other objects in the scene
    deselect_all()

    # If the object is hidden, show it to be able to delete it
    unhide_object(scene_object)

    # Select this particular object, to highlight it
    select_object(scene_object)

    # Delete the selected object
    vmv.utilities.disable_std_output()
    bpy.ops.object.delete(use_global=False)
    vmv.utilities.enable_std_output()


####################################################################################################
# @delete_list_objects
####################################################################################################
def delete_list_objects(object_list):
    """Deletes a given list of objects in the scene.

    :param object_list:
        A list of objects to be deleted from the scene.
    """

    # Deselects all objects in the scene
    deselect_all()

    # Delete object by object from the list
    for scene_object in object_list:

        # The object must exist in the scene to be deleted
        if is_object_existing(scene_object=scene_object):

            # If the object is hidden, show it to be able to delete it
            unhide_object(scene_object)

            # Select this particular object, to highlight it
            select_object(scene_object)

            # Delete the selected object
            vmv.utilities.disable_std_output()
            bpy.ops.object.delete(use_global=False)
            vmv.utilities.enable_std_output()


####################################################################################################
# @delete_all
####################################################################################################
def delete_all():
    """Deletes all the objects in the scene."""

    # Deselect all the objects in the scene
    deselect_all()

    # Delete object by object from the scene
    for scene_object in bpy.context.scene.objects:

        # Select this particular object, to highlight it
        select_object(scene_object)

        vmv.utilities.disable_std_output()
        bpy.ops.object.delete(use_global=False)
        vmv.utilities.enable_std_output()


####################################################################################################
# @set_active_object
####################################################################################################
def set_active_object(scene_object):
    """Set the active object in the scene to the given one. This object will be selected.

    :param scene_object:
        A given object in the scene that is desired to be active.

    :return:
        A reference to the active object.
    """

    # Deselects all objects in the scene
    deselect_all()

    # Select the object
    select_object(scene_object)

    # Set it active
    if vmv.utilities.is_blender_280():
        bpy.context.view_layer.objects.active = scene_object
    else:
        bpy.context.scene.objects.active = scene_object

    # Return a reference to the mesh object again for convenience
    return scene_object


####################################################################################################
# @rotate_object
####################################################################################################
def rotate_object(scene_object,
                  x=0.0, y=0.0, z=0.0):
    """Rotate the given object in the scene using Euler rotation.

    :param scene_object:
        A given object in the scene to be rotated.
    :param x:
        X angle.
    :param y:
        Y angle.
    :param z:
        Z angle.
    """

    # Rotate the object
    scene_object.rotation_euler = (x, y, z)


####################################################################################################
# @reset_orientation_of_objects
####################################################################################################
def reset_orientation_of_objects(scene_objects):
    """Reset the orientation of a group of objects in the scene.

    :param scene_objects:
        List of objects in the scene.
    """

    # Rotate all the objects as if they are a single object
    for scene_object in scene_objects:
        scene_object.rotation_euler[0] = 0
        scene_object.rotation_euler[1] = 0
        scene_object.rotation_euler[2] = 0


####################################################################################################
# @get_object_orientation
####################################################################################################
def get_object_orientation(scene_object):
    """Return the Euler orientation of the object.

    :param scene_object:
        A given object in the scene.
    :return:
        The current orientation of the given object in the scene.
    """

    # Returns the orientation vector
    return scene_object.rotation_euler


####################################################################################################
# @translate_object
####################################################################################################
def translate_object(scene_object,
                     shift):
    """Set the given object a given location in the scene.

    :param scene_object:
        A given object in the scene to be translated.
    :param shift:
        A given shift to translate the object.
    """

    # Set location
    scene_object.location += shift


####################################################################################################
# @set_object_location
####################################################################################################
def set_object_location(scene_object,
                        location):
    """Set the given object a given location in the scene.

    :param scene_object:
        A given object in the scene to be translated.
    :param location:
        The new (or desired) location of the object.
    """

    # Set location
    scene_object.location = location


####################################################################################################
# @get_object_location
####################################################################################################
def get_object_location(scene_object):
    """Return the location of the given object in the scene.

    :param scene_object:
        The object required to know its current location.
    :return:
        The current location of the object.
    """

    # Returns the location vector
    return scene_object.location


####################################################################################################
# @scale_object
####################################################################################################
def scale_object(scene_object,
                 x=1.0, y=1.0, z=1.0):
    """Scale the given object in the scene non-uniformly.

    :param scene_object:
        The object to be scaled.
    :param x:
        X scale factor.
    :param y:
        Y scale factor.
    :param z:
        Z scale factor.
    """

    # Scale the object
    scene_object.scale = (x, y, z)


####################################################################################################
# @get_object_scale
####################################################################################################
def get_object_scale(scene_object):
    """Return the scale of the given object.

    :param scene_object:
        A given object in the scene.
    :return:
        The current scale of the given object.
    """

    # Returns the orientation vector
    return scene_object.scale


####################################################################################################
# @scale_object_uniformly
####################################################################################################
def scale_object_uniformly(scene_object,
                           scale_factor=1.0):
    """Scale the given object uniformly in XYZ.

    :param scene_object:
        A given object in the scene.
    :param scale_factor:
        Uniform scale factor.
    """

    # Scale the object.
    scale_object(scene_object, x=scale_factor, y=scale_factor, z=scale_factor)


####################################################################################################
# @scale_mesh_object_to_fit_within_unity_cube
####################################################################################################
def scale_mesh_object_to_fit_within_unity_cube(scene_object,
                                               scale_factor=1):
    """Scale a given mesh object within a cube.

    :param scene_object:
        A given scene object.
    :param scale_factor:
        A scale factor to rescale the unity cube.
    """

    # Compute the bounding box of the mesh
    mesh_bbox = vmv.bbox.get_object_bounding_box(scene_object)

    # Get the largest dimension of the mesh
    largest_dimension = mesh_bbox.bounds[0]
    if mesh_bbox.bounds[1] > largest_dimension:
        largest_dimension = mesh_bbox.bounds[1]
    if mesh_bbox.bounds[2] > largest_dimension:
        largest_dimension = mesh_bbox.bounds[2]

    # Compute the scale factor
    unified_scale_factor = scale_factor / largest_dimension

    # Scale the mesh
    scale_object_uniformly(scene_object, unified_scale_factor)


####################################################################################################
# @scale_object_uniformly
####################################################################################################
def center_mesh_object(scene_object):
    """Center a given mesh object at the origin.
    TODO: There is an already existing BLender-funtion that does this feature.

    :param scene_object:
        A mesh object to be centered at the origin of the scene based on its bounding box.
    """

    # Compute the object bounding box center from all the vertices of the object
    bbox_center = Vector((0, 0, 0))
    p_max = Vector((-1e10, -1e10, -1e10))
    p_min = Vector((1e10, 1e10, 1e10))

    for vertex in scene_object.data.vertices:
        if vertex.co[0] > p_max[0]:
            p_max[0] = vertex.co[0]
        if vertex.co[1] > p_max[1]:
            p_max[1] = vertex.co[1]
        if vertex.co[2] > p_max[2]:
            p_max[2] = vertex.co[2]
        if vertex.co[0] < p_min[0]:
            p_min[0] = vertex.co[0]
        if vertex.co[1] < p_min[1]:
            p_min[1] = vertex.co[1]
        if vertex.co[2] < p_min[2]:
            p_min[2] = vertex.co[2]
    bounds = p_max - p_min
    bbox_center = p_min + (0.5 * bounds)

    # For each vertex in the mesh, center it
    for vertex in scene_object.data.vertices:
        vertex.co = vertex.co - bbox_center


####################################################################################################
# @rotate_object_towards_target
####################################################################################################
def rotate_object_towards_target(scene_object,
                                 object_normal,
                                 target_point):
    """Rotate a given object in the scene towards a target point using Euler rotation.

    :param scene_object:
        A given object in the scene.
    :param object_normal:
        Object normal.
    :param target_point:
        The target point for the rotation.
    """

    # Get the location of the object
    object_location = get_object_location(scene_object)

    # Compute the rotation direction
    rotation_direction = (target_point - object_location).normalized()

    # Compute the rotation difference, based on the normal
    rotation_difference = object_normal.rotation_difference(rotation_direction)

    # Get the euler angles
    rotation_euler = rotation_difference.to_euler()

    # Update the rotation angles
    scene_object.rotation_euler[0] = (rotation_euler[0])
    scene_object.rotation_euler[1] = (rotation_euler[1])
    scene_object.rotation_euler[2] = (rotation_euler[2])


####################################################################################################
# @convert_object_to_mesh
####################################################################################################
def convert_object_to_mesh(scene_object):
    """Convert a scene object (for example curve or poly-line) to a surface mesh.

    :param scene_object:
        A given scene object, for example curve or poly-line.
    :return:
        A reference to the created mesh object.
    """

    # Deselects all objects in the scene
    set_active_object(scene_object)

    # Convert the given object to a mesh
    vmv.bops.convert_to_mesh()

    # Return the mesh object
    return scene_object


####################################################################################################
# @duplicate_object
####################################################################################################
def duplicate_object(original_object,
                     duplicated_object_name=None,
                     link_to_scene=True):
    """Duplicates an object in the scene and returns a reference to the duplicated object.

    :param original_object:
        The original object that will be duplicated in the scene.
    :param duplicated_object_name:
        The name of the new object.
    :param link_to_scene:
        Link the duplicate object to the scene.
    :return:
        A reference to the duplicated object.
    """

    # Deselect all the objects in the scene
    for scene_object in bpy.context.scene.objects:
        deselect_object(scene_object)

    # Duplicate the object
    duplicated_object = original_object.copy()

    # Make this a real duplicate (not linked)
    duplicated_object.data = original_object.data.copy()

    # Update the duplicate name
    if duplicated_object_name is None:
        duplicated_object.name = str(original_object.name) + '_duplicate'
    else:
        duplicated_object.name = str(duplicated_object_name)

    # Link it to the scene
    if link_to_scene:
        link_object_to_scene(duplicated_object)

        # Deselect all the objects in the scene
        for scene_object in bpy.context.scene.objects:
            deselect_object(scene_object)

    # Return a reference to the duplicate object
    return duplicated_object


####################################################################################################
# @clone_mesh_objects_into_joint_mesh
####################################################################################################
def clone_mesh_objects_into_joint_mesh(mesh_objects):
    """Clones a list of mesh objects and join the clones into a single object.

    NOTE: This function is normally used to export a mesh object without affecting any mesh in
    the scene.

    :param mesh_objects:
        A list of mesh objects in the scene.
    :return:
        A joint mesh object that can be used directly to export a mesh.
    """

    # Deselect all the other objects in the scene
    deselect_all()

    # Clones the mesh objects to join them together to export the mesh
    cloned_mesh_objects = list()
    for mesh_object in mesh_objects:
        cloned_mesh_objects.append(duplicate_object(mesh_object))

    # Join all the mesh objects in a single object
    joint_mesh_object = vmv.mesh.join_mesh_objects(cloned_mesh_objects)

    # Deselect all the other objects in the scene
    deselect_all()

    # Activate the joint mesh object
    select_objects([joint_mesh_object])
    set_active_object(joint_mesh_object)

    # Return the clones mesh
    return joint_mesh_object


####################################################################################################
# @is_object_in_scene
####################################################################################################
def is_object_in_scene(input_object):
    """Verify if a given object exists in the scene or not.

    :param input_object:
        A given object to be checked if it exists in the scene or not.
    :return:
        True or False.
    """

    # If the object is None, then it cannot exist in the scene
    if input_object is None:
        return False

    # Loop over all the objects in the scene, and check by name
    for scene_object in bpy.context.scene.objects:

        # Verify
        if scene_object.name == input_object.name:

            # Yes it exists
            return True

    # No, it doesn't exist
    return False


####################################################################################################
# @is_object_in_scene_by_name
####################################################################################################
def is_object_in_scene_by_name(object_name):
    """Verify if a given object identified by its name exists in the scene or not.

    :param object_name:
        The object name.
    :return:
        True or False.
    """
    # If the object is None, then it cannot exist in the scene
    if object_name is None:
        return False

    # Loop over all the objects in the scene, and check by name
    for scene_object in bpy.context.scene.objects:

        # Verify the name
        if scene_object.name == object_name:

            # Yes it exists
            return True

    # No, it doesn't exist
    return False


####################################################################################################
# @view_all_scene
####################################################################################################
def view_all_scene():
    """Views all the objects in the scene."""

    # Switch to the top view
    if vmv.utilities.is_blender_280():
        pass
    else:
        bpy.ops.view3d.viewnumpad(type='TOP')

    # View all the objects in the scene
    bpy.ops.view3d.view_all()

    # Update the end
    bpy.context.space_data.clip_end = 1e5


####################################################################################################
# @view_region
####################################################################################################
def view_region(x=0, y=0, delta=1):
    """View a specific region in the scene.

    :param x:
        Minimum X.
    :param y:
        Minimum Y.
    :param delta:
        Delta
    """
    bpy.ops.view3d.zoom(mx=x, my=y, delta=delta)

    # Update the end
    bpy.context.space_data.clip_end = 1e4


####################################################################################################
# @set_scene_transparency
####################################################################################################
def set_scene_transparency(transparent=False):
    """Enables or disables scene transparency.

    :param transparent:
        If True, switch to the transparent mode, otherwise normal mode.
    """

    # If Workbench render is used, adjust the color as follows
    if bpy.context.scene.render.engine == 'BLENDER_WORKBENCH':

        bpy.context.scene.display.shading.light = 'STUDIO'
        bpy.context.scene.display.shading.studio_light = 'Default'
        bpy.context.scene.display.shading.show_xray = transparent

    if vmv.utilities.is_blender_280():
        views3d = [a for a in bpy.context.screen.areas if a.type == 'VIEW_3D']
        for a in views3d:
            shading = a.spaces.active.shading
            shading.show_xray = transparent


####################################################################################################
# @switch_scene_shading
####################################################################################################
def switch_scene_shading(shading_type='SOLID'):
    """Switches the scene panel to the given shading type

    :param shading_type:
        One of the following: 'WIREFRAME', '(SOLID)', 'MATERIAL', 'RENDERED'
    """

    if vmv.utilities.is_blender_280():
        areas = bpy.context.workspace.screens[0].areas
        for area in areas:
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = shading_type


####################################################################################################
# @switch_interface_to_edit_mode
####################################################################################################
def switch_interface_to_edit_mode():
    """Switches the user interface to the edit mode style."""

    if vmv.utilities.is_blender_280():

        # Update the transparency
        set_scene_transparency(True)

        # Use the solid mode
        switch_scene_shading('SOLID')

        # Increase the vertex size
        bpy.context.preferences.themes['Default'].view_3d.vertex_size = 8

        # Make the vertex red
        bpy.context.preferences.themes['Default'].view_3d.vertex.r = 1.0
        bpy.context.preferences.themes['Default'].view_3d.vertex.g = 0.0
        bpy.context.preferences.themes['Default'].view_3d.vertex.b = 0.0

        # Make the selected vertex white
        bpy.context.preferences.themes['Default'].view_3d.vertex_select.r = 1.0
        bpy.context.preferences.themes['Default'].view_3d.vertex_select.g = 1.0
        bpy.context.preferences.themes['Default'].view_3d.vertex_select.b = 1.0

        # Make the wire white to be able to see it
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.r = 1.0
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.g = 1.0
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.b = 1.0


####################################################################################################
# @switch_interface_to_visualization_mode
####################################################################################################
def switch_interface_to_visualization_mode():
    """Switches the user interface to the visualization mode style."""

    if vmv.utilities.is_blender_280():

        # Update the transparency
        set_scene_transparency(False)

        # Solid mode
        switch_scene_shading('SOLID')

        # Make the vertex black again
        bpy.context.preferences.themes['Default'].view_3d.vertex.r = 0.0
        bpy.context.preferences.themes['Default'].view_3d.vertex.g = 0.0
        bpy.context.preferences.themes['Default'].view_3d.vertex.b = 0.0

        # Adjust the vertex size to the default value
        bpy.context.preferences.themes['Default'].view_3d.vertex_size = 3

        # Make the wire black again
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.r = 0.0
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.g = 0.0
        bpy.context.preferences.themes['Default'].view_3d.wire_edit.b = 0.0


####################################################################################################
# @extend_clipping_planes
####################################################################################################
def extend_clipping_planes(clip_start=0.01,
                           clip_end=1e5):
    """Extends the clipping frustum of the scene in the UI.
    :param clip_start:
        The distance to the starting clipping plane, default 0.01.
    :param clip_end:
        The distance to the rear clipping plane, default 1e5.
    """

    # Starting clipping plane
    bpy.context.space_data.clip_start = clip_start

    # Ending clipping plane
    bpy.context.space_data.clip_end = clip_end


####################################################################################################
# @get_object_by_name
####################################################################################################
def get_object_by_name(object_name):
    """Gets an object in the scene given its name.
    :param object_name:
        The name of object to be returned.
    """

    # For every object in the scene, check its name
    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            return scene_object

    # If there is no object defined by the name , return None
    return None


####################################################################################################
# @is_there_any_mesh_in_scene
####################################################################################################
def is_there_any_mesh_in_scene():
    """Detects if the scene has any mesh or not.

    :return:
        True if there is at least a single mesh in the scene, and False otherwise.
    """

    # For every object in the scene, detect if this object is a mesh or not
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            return True
    return False


####################################################################################################
# @is_there_any_morphology_in_scene
####################################################################################################
def is_there_any_morphology_in_scene():
    """Detects if the scene has any morphology or not.

    :return:
        True if there is at least a single morphology or polyline in the scene, and False otherwise.
    """

    # For every object in the scene, detect if this object is a polyline or not
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            return True
    return False



