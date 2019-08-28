"""bmesh_object_ops.py:
    A set of utilities and operators for handling bmesh objects.
"""

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2017, Blue Brain Project / EPFL"
__version__     = "0.1.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

# Blender modules
import bpy, bmesh


####################################################################################################
# @convert_to_mesh_object
####################################################################################################
def convert_to_mesh_object(bmesh_object,
                           name='mesh'):
    """Converts the bmesh to a new mesh object and rename it. This operation returns a reference to
    the created object.

    :param bmesh_object:
        An input bmesh object.
    :param name:
        The name of the mesh object.
    :return:
        Returns a reference to the converted object.
    """

    # Create a new mesh object and convert the bmesh object to it
    mesh_object = bpy.data.meshes.new(name)
    bmesh_object.to_mesh(mesh_object)

    # Return a reference to the mesh object
    return mesh_object


####################################################################################################
# @convert_from_mesh_object
####################################################################################################
def convert_from_mesh_object(mesh_object):
    """
    Converts the mesh object to a bmesh object and returns a reference to it.

    :param mesh_object: An input mesh object.
    :return: A reference to the bmesh object.
    """

    # Return a reference to the bmesh created from the object.
    return bmesh.from_edit_mesh(mesh_object.data)


####################################################################################################
# @convert_to_mesh_object
####################################################################################################
def link_to_new_object_in_scene(bmesh_object,
                                name='bmesh'):
    """
    Converts the bmesh to a new mesh object, renames it and links it to the scene as a blender
    object such that you can see it in the interface.
    This operation returns a reference to the created blender object.

    :param bmesh_object: An input bmesh object.
    :param name: The name of the object.
    :return: A reference to the linked object.
    """

    # Create a mesh object from the bmesh
    mesh_object = convert_to_mesh_object(bmesh_object, name)

    # Create a blender object, link it to the scene
    object = bpy.data.objects.new(name, mesh_object)
    bpy.context.scene.collection.objects.link(object)

    # Return a reference to it
    return object


####################################################################################################
# @link_to_existing_object_in_scene
####################################################################################################
def link_to_existing_object_in_scene(bmesh_object,
                                     scene_object):
    """
    Links the bmesh object to an existing object in the scene.

    :param bmesh_object: An input bmesh object.
    :param scene_object: An object existing in the scene where the bmesh object will be linked to.
    """

    # Link the bmesh to the given object, and update the mesh.
    bmesh_object.to_mesh(scene_object.data)
    bmesh.update_edit_mesh(scene_object.data, True)


####################################################################################################
# @convert_bmesh_to_mesh
####################################################################################################
def convert_bmesh_to_mesh(bmesh_object,
                          name='bmesh'):
    """Convert a bmesh object to a mesh object.

    :param bmesh_object:
        An input bmesh object.
    :param name:
        The name of the object.
    :return:
        A reference to the converted mesh.
    """

    return link_to_new_object_in_scene(bmesh_object=bmesh_object, name=name)


####################################################################################################
# @convert_bmesh_to_mesh
####################################################################################################
def delete_bmesh(bmesh_object):
    """Deletes a bmesh object.

    :param bmesh_object:
        A given bmesh object to delete.
    """
    bmesh.ops.delete(bmesh_object, geom=bmesh_object.faces)


####################################################################################################
# @delete_bmesh_list
####################################################################################################
def delete_bmesh_list(bmesh_list):
    """Delete a list of bmesh objects.

    :param bmesh_list:
        A list of bmesh objects to be deleted.
    """

    for bmesh_object in bmesh_list:
        delete_bmesh(bmesh_object)