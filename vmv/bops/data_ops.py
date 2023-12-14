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

# Blender imports
import bpy


####################################################################################################
# @get_materials_in_scene
####################################################################################################
def get_materials_in_scene():
    """Returns a list of all the materials in the scene.

    :return:
        A list of all the materials in the scene.
    """

    return bpy.data.materials


####################################################################################################
# @delete_material_from_scene
####################################################################################################
def delete_material_from_scene(material):
    """Deletes a given material that exists in the scene.

    :param material:
        A given material to be deleted.
    """

    material.user_clear()
    bpy.data.materials.remove(material)


####################################################################################################
# @create_new_metaballs
####################################################################################################
def create_new_metaballs(name):
    """Creates a new meta-balls object with a specific name.

    :param name:
        The name of the created meta-balls object.
    :return:
        A reference to the created meta-balls object.
    """

    return bpy.data.metaballs.new(name)


####################################################################################################
# @create_new_metaballs_object_from_data
####################################################################################################
def create_new_metaballs_object_from_data(name,
                                          metaballs_data):
    """Creates a new meta-balls object from input meta-balls data object.

    :param name:
        The name of the created object.
    :param metaballs_data:
        Input meta-balls data
    :return:
        A reference to teh created meta-balls object.
    """

    return bpy.data.objects.new(name, metaballs_data)

