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

# System imports
import bpy

# Blender imports
from mathutils import Vector

# Internal imports
import vmv
import vmv.utilities


####################################################################################################
# @clear_default_scene
####################################################################################################
def clear_default_scene():
    """Clear the default scene loaded in Blender: the ['Cube', 'Lamp' and 'Camera'].
    """

    # Iterate over all the objects in the scene, and remove the 'Cube', 'Lamp' and 'Camera' if exist
    for scene_object in bpy.context.scene.objects:

        # Object selection
        if scene_object.name == 'Cube' or \
           scene_object.name == 'Lamp' or \
           scene_object.name == 'Camera':
            scene_object.select_set(True)

            # Delete the object
            bpy.ops.object.delete()


####################################################################################################
# @clear_scene
####################################################################################################
def clear_scene():
    """Clear a scene and remove all the existing objects in it and unlink their references.

    NOTE: This function targets clearing meshes, curve, objects and materials.
    """

    # Disable the output
    vmv.utilities.disable_std_output()

    # Select each object in the scene
    for scene_object in bpy.context.scene.objects:
        scene_object.select_set(True)

    # Delete all the objects
    bpy.ops.object.delete()

    # Unlink all the objects in all the layers
    for scene in bpy.data.scenes:
        for scene_object in scene.objects:
            scene.objects.unlink(scene_object)

    # Select all the meshes, unlink them and clear their data
    for scene_mesh in bpy.data.meshes:
        scene_mesh.user_clear()
        bpy.data.meshes.remove(scene_mesh)

    # Select all the curves, unlink them and clear their data
    for scene_curve in bpy.data.curves:
        scene_curve.user_clear()
        bpy.data.curves.remove(scene_curve)

    # Select all the scene objects, unlink them and clear their data
    for scene_object in bpy.data.objects:
        scene_object.user_clear()
        bpy.data.objects.remove(scene_object)

    # Select all the scene materials, unlink them and clear their data
    for scene_material in bpy.data.materials:
        scene_material.user_clear()
        bpy.data.materials.remove(scene_material)

    # Enable the output again
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
        if 'morphology_skeleton' in material.name:
            material.user_clear()
            bpy.data.materials.remove(material)


####################################################################################################
# @select_all
####################################################################################################
def select_all():
    """Select all the objects in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to True.
    for scene_object in bpy.context.scene.objects:
        scene_object.select_set(True)


####################################################################################################
# @deselect_all
####################################################################################################
def deselect_all():
    """Deselect all the objects in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to False.
    for scene_object in bpy.context.scene.objects:
        scene_object.select_set(False)


####################################################################################################
# @select_objects
####################################################################################################
def select_objects(object_list):
    """Select all the objects in a given list.

    :param object_list:
        A list of objects that exist in the scene.
    """

    # Set the '.select' flag of all the objects in the scene to True
    for scene_object in object_list:
        scene_object.select_set(True)


####################################################################################################
# @select_object_by_name
####################################################################################################
def select_object_by_name(object_name):
    """Select an object in the scene given its name.

    :param object_name:
        The name of object to be selected.
    """

    # Set the '.select' flag of the object to True
    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            scene_object.select_set(True)


####################################################################################################
# @select_object_containing_string
####################################################################################################
def select_object_containing_string(search_string):
    """Selects an object in the scene that contains a given string.

    :param search_string:
        A sub-string that is contained in the name of the object.
    :return:
        A reference to the selected object.
    """

    # Deselect all the objects
    deselect_all()

    for scene_object in bpy.context.scene.objects:
        if search_string in scene_object.name:

            # Select it
            scene_object.select_set(True)

            # Return it
            return scene_object


####################################################################################################
# @deselect_object_by_name
####################################################################################################
def deselect_object_by_name(object_name):
    """Deselect an object in the scene given its name.

    :param object_name:
        The name of object to be deselected.
    """

    # Set the '.select' flag of the object to False
    for scene_object in bpy.context.scene.objects:
        if scene_object.name == object_name:
            scene_object.select_set(False)


####################################################################################################
# @select_all_meshes_in_scene
####################################################################################################
def select_all_meshes_in_scene():
    """Select all the mesh objects (those of type 'MESH') in the scene.
    """

    # Deselect all the objects in the scene
    deselect_all()

    # Select only the objects of type meshes
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            scene_object.select_set(True)


####################################################################################################
# @deselect_all_meshes_in_scene
####################################################################################################
def deselect_all_meshes_in_scene():
    """Deselect all the mesh objects (those of type 'MESH') in the scene.
    """

    # Select only the objects of type meshes
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'MESH':
            scene_object.select_set(False)


####################################################################################################
# @select_all_curves_in_scene
####################################################################################################
def select_all_curves_in_scene():
    """Selects all the curve objects (those of type 'CURVE') in the scene.
    """

    # Deselect all the objects in the scene
    deselect_all()

    # Deselect only the objects of type curves
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            scene_object.select_set(True)


####################################################################################################
# @deselect_all_curves_in_scene
####################################################################################################
def deselect_all_curves_in_scene():
    """Deselects all the curve objects (those of type 'CURVE') in the scene.
    """

    # Deselect only the objects of type curves
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            scene_object.select_set(False)


####################################################################################################
# @get_list_of_meshes_in_scene
####################################################################################################
def get_list_of_meshes_in_scene():
    """Return a list of references to all the meshes (objects of type 'MESH') in the scene.

    :return:
        A list of references to all the meshes (objects of type 'MESH') in the scene.
    """

    # Mesh list
    mesh_list = list()

    # Select only the objects of type meshes, and append their references to the list
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

    # Curve list
    curve_list = list()

    # Select only the objects of type meshes, and append their references to the list
    for scene_object in bpy.context.scene.objects:
        if scene_object.type == 'CURVE':
            curve_list.append(scene_object)

    # Return a reference to the list
    return curve_list


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
# @delete_object
####################################################################################################
def delete_object_in_scene(scene_object):
    """Delete a given object from the scene.

    :param scene_object:
        A given object to be deleted from the scene.
    """

    # Deselect all the other objects in the scene
    deselect_all()

    # Select this particular object, to highlight it
    scene_object.select_set(True)

    # Delete the selected object
    bpy.ops.object.delete(use_global=False)


####################################################################################################
# @delete_list_objects
####################################################################################################
def delete_list_objects(object_list):
    """Delete a given list of objects in the scene.

    :param object_list:
        A list of objects to be deleted from the scene.
    """

    # Deselects all objects in the scene
    deselect_all()

    # Delete object by object from the list
    for scene_object in object_list:

        # Select this particular object, to highlight it
        scene_object.select_set(True)

        # Delete the selected object
        bpy.ops.object.delete(use_global=False)


####################################################################################################
# @delete_all
####################################################################################################
def delete_all():
    """Delete all the objects in the scene.
    """

    # Deselect all the objects in the scene
    deselect_all()

    # Delete object by object from the scene
    for scene_object in bpy.context.scene.objects:

        # Select this particular object, to highlight it
        scene_object.select_set(True)

        # Delete the selected object
        bpy.ops.object.delete(use_global=False)


####################################################################################################
# @set_active_object
####################################################################################################
def set_active_object(scene_object):
    """Set the active object in the scene to the given one.

    :param scene_object:
        A given object in the scene that is desired to be active.

    :return
        A reference to the active object.
    """

    # Deselects all objects in the scene
    deselect_all()

    # Select the object
    scene_object.select_set(True)

    # Set it active
    bpy.context.view_layer.objects.active = scene_object

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
    vmv.scene.ops.scale_object_uniformly(scene_object, unified_scale_factor)


####################################################################################################
# @scale_object_uniformly
####################################################################################################
def center_mesh_object(scene_object):
    """Center a given mesh object at the origin.

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
    bpy.ops.object.convert(target='MESH')

    # Return the mesh object
    return scene_object


####################################################################################################
# @duplicate_object
####################################################################################################
def duplicate_object(original_object,
                     duplicated_object_name=None,
                     link_to_scene=True):
    """
    Duplicates an object in the scene and returns a reference to the duplicated object.

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
        scene_object.select_set(False)

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
        bpy.context.scene.collection.objects.link(duplicated_object)

        # Deselect all the objects in the scene
        for scene_object in bpy.context.scene.objects:
            scene_object.select_set(False)

    # Return a reference to the duplicate object
    return duplicated_object


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
    """View all the objects in the scene.
    """

    # Switch to the top view
    bpy.ops.view3d.viewnumpad(type='TOP')

    # View all the objects in the scene
    bpy.ops.view3d.view_all()


####################################################################################################
# @join_objects
####################################################################################################
def join_objects(object_list,
                 name='joint'):
    """Join all the objects into one only and rename it.

    :param object_list:
        An input list of objects to be joint.
    :param name:
        The name of the outcome.
    :return:
        A joint mesh.
    """

    # If the input list does not contain any meshes, return None
    if len(object_list) == 0:
        return None

    # If the input list contains only one mesh, return a reference to it
    if len(object_list) == 1:
        return object_list[1]

    # Deselect everything in the scene
    deselect_all()

    # Select all the sections in the sections list
    for mesh_object in object_list:

        # Select the mesh object
        mesh_object.select_set(True)

    # Set the 0th mesh to be active
    bpy.context.view_layer.objects.active = object_list[0]

    # Set tha parenting order, the parent mesh is becoming an actual parent
    bpy.ops.object.parent_set()

    # Join the two meshes in one object
    bpy.ops.object.join()

    # Get a reference to the resulting object
    result = bpy.context.active_object

    # Rename it
    result.name = name

    # Return a reference to the resulting mesh
    return result


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
