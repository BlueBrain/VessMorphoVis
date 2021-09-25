####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
# Author(s): Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of VessMorphoVis <https://github.com/BlueBrain/VessMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################


# Blender imports
import bpy

# Internal imports
import vmv
import vmv.consts
import vmv.enums
import vmv.scene
import vmv.utilities


####################################################################################################
# @create_default_illumination
####################################################################################################
def create_default_illumination():
    """Creates an illumination specific for the default shader.
    """

    # Deselect all
    vmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(-0.78, 0.000, -0.78),
                      (0.000, 3.140, 0.000),
                      (1.570, 0.000, 0.000),
                      (-1.57, 0.000, 0.000),
                      (0.000, 1.570, 0.000),
                      (0.000, -1.57, 0.000)]

    # Add the lights
    for i, angle in enumerate(light_rotation):
        if vmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.energy = 0.5
        else:
            bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.use_specular = True if i == 0 else False
            lamp_reference.data.energy = 0.5


####################################################################################################
# @create_shadow_illumination
####################################################################################################
def create_shadow_illumination():
    """Creates an illumination specific for the shadow shader.
    """

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not vmv.scene.ops.is_object_in_scene_by_name('LampUp'):
        vmv.scene.ops.deselect_all()

        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampUp'
        lamp_reference.data.name = "LampUp"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0
        lamp_reference.rotation_euler[0] = 1.5708
        bpy.data.lamps['LampUp'].node_tree.nodes["Emission"].inputs[1].default_value = 5

        vmv.scene.ops.deselect_all()
        bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampDown'
        lamp_reference.data.name = "LampDown"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0
        lamp_reference.rotation_euler[0] = -1.5708
        bpy.data.lamps['LampDown'].node_tree.nodes["Emission"].inputs[1].default_value = 5


####################################################################################################
# @create_glossy_illumination
####################################################################################################
def create_glossy_illumination():
    """Creates an illumination specific for the glossy shader.
    """

    vmv.scene.ops.clear_lights()

    # deselect all
    vmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(0.000, 0, 0.000),
                      (-1.57, 0.000, 0.000),
                      (0.000, -1.57, 0.000)]

    light_position = [(0, 0, 0.1),
                      (0, 0.1, 0),
                      (-0.1, 0, 0)]

    # Add the light sources
    for i, angle in enumerate(light_rotation):

        if vmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=light_position[i])
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.energy = 2.5

        else:
            lamp_data = bpy.data.lamps.new(name='Lamp%d' % i, type='HEMI')
            lamp_object = bpy.data.objects.new(name='Lamp%d' % i, object_data=lamp_data)
            bpy.context.scene.objects.link(lamp_object)
            lamp_object.rotation_euler = angle
            lamp_object.location = light_position[i]
            bpy.data.lamps['Lamp%d' % i].use_nodes = True
            bpy.data.lamps['Lamp%d' % i].node_tree.nodes["Emission"].inputs[
                1].default_value = 1e5


####################################################################################################
# @create_glossy_bumpy_illumination
####################################################################################################
def create_glossy_bumpy_illumination():
    """Creates an illumination specific for the glossy-bumpy shader.
    """

    # Deselect all
    vmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(-1.57, 0.000, 0.000),
                      (0.000, 1.570, 0.000),
                      (0.000, -1.57, 0.000)]

    # Add the lights
    for i, angle in enumerate(light_rotation):
        if vmv.utilities.is_blender_280():
            bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.energy = 10
        else:
            bpy.ops.object.lamp_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            lamp_reference.data.use_specular = True if i == 0 else False
            lamp_reference.data.energy = 10


####################################################################################################
# @create_material_specific_illumination
####################################################################################################
def create_material_specific_illumination(material_type):
    """Create a specific illumination that corresponds to a given material.

    :param material_type:
        Material type.
    """

    # Lambert Ward
    if material_type == vmv.enums.Shader.LAMBERT_WARD:
        return create_default_illumination()

    # Glossy bumpy
    elif material_type == vmv.enums.Shader.GLOSSY_BUMPY:
        return create_glossy_illumination()

    # Glossy
    elif material_type == vmv.enums.Shader.GLOSSY:
        return create_glossy_illumination()

    elif material_type == vmv.enums.Shader.GLOSSY_BUMPY:
        return create_glossy_bumpy_illumination()

    # Default, just use the lambert shader illumination
    else:
        return create_default_illumination()


####################################################################################################
# @create_default_illumination
####################################################################################################
def create_default_illumination(camera_view=vmv.enums.Rendering.View.FRONT):
    """
    """

    # Clear all the lights
    vmv.scene.ops.clear_lights()

    # Deselect all
    vmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(-0.78, 0.000, -0.78),
                      (0.000, 3.140, 0.000),
                      (1.570, 0.000, 0.000),
                      (-1.57, 0.000, 0.000),
                      (0.000, 1.570, 0.000),
                      (0.000, -1.57, 0.000)]

    # Add the lights
    for i, angle in enumerate(light_rotation):
        bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'Lamp%d' % i
        lamp_reference.data.name = "Lamp%d" % i
        lamp_reference.rotation_euler = angle
        lamp_reference.data.energy = 0.5


####################################################################################################
# @create_artistic_glossy_illumination
####################################################################################################
def create_artistic_glossy_illumination(camera_view=vmv.enums.Rendering.View.FRONT):
    """Creates illumination for the artistic glossy shader for Cycles rendering.
    :return:
    """

    # Clear all the lights
    vmv.scene.ops.clear_lights()

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not vmv.scene.ops.is_object_in_scene_by_name('LampUp'):
        vmv.scene.ops.deselect_all()

        bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampUp'
        lamp_reference.data.name = "LampUp"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0
        lamp_reference.rotation_euler[0] = 0
        lamp_reference.rotation_euler[1] = 0
        lamp_reference.rotation_euler[2] = 0
        lamp_reference.data.color[0] = 0.75
        lamp_reference.data.color[1] = 1.0
        lamp_reference.data.color[2] = 1.0
        lamp_reference.data.energy = 10

        if camera_view == vmv.enums.Rendering.View.TOP:
            lamp_reference.rotation_euler[0] = 3.14159
        else:
            lamp_reference.rotation_euler[0] = -1.5708

        vmv.scene.ops.deselect_all()
        bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampDown'
        lamp_reference.data.name = "LampDown"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0
        lamp_reference.rotation_euler[0] = 0
        lamp_reference.rotation_euler[1] = 0
        lamp_reference.rotation_euler[2] = 0
        lamp_reference.data.color[0] = 1.0
        lamp_reference.data.color[1] = 1.0
        lamp_reference.data.color[2] = 0.75
        lamp_reference.data.energy = 10

        if camera_view == vmv.enums.Rendering.View.TOP:
            lamp_reference.rotation_euler[0] = 0
        else:
            lamp_reference.rotation_euler[0] = 1.5708


####################################################################################################
# @create_shadow_illumination
####################################################################################################
def create_shadow_illumination(camera_view=vmv.enums.Rendering.View.FRONT):

    # Clear all the lights
    vmv.scene.ops.clear_lights()

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not vmv.scene.ops.is_object_in_scene_by_name('LampUp'):
        vmv.scene.ops.deselect_all()

        bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampUp'
        lamp_reference.data.name = "LampUp"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0
        lamp_reference.rotation_euler[0] = 1.5708
        bpy.data.lamps['LampUp'].node_tree.nodes["Emission"].inputs[1].default_value = 5

        vmv.scene.ops.deselect_all()
        bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
        lamp_reference = bpy.context.object
        lamp_reference.name = 'LampDown'
        lamp_reference.data.name = "LampDown"
        lamp_reference.location[0] = 0
        lamp_reference.location[1] = 0
        lamp_reference.location[2] = 0
        lamp_reference.rotation_euler[0] = -1.5708
        bpy.data.lamps['LampDown'].node_tree.nodes["Emission"].inputs[1].default_value = 5


####################################################################################################
# @create_glossy_bumpy_illumination
####################################################################################################
def create_glossy_bumpy_illumination(camera_view=vmv.enums.Rendering.View.FRONT):

    vmv.scene.ops.clear_lights()

    # deselect all
    vmv.scene.ops.deselect_all()

    # Multiple light sources from different directions
    light_rotation = [(0.000, 3.140, 0.000),
                      (-1.57, 0.000, 0.000),
                      (0.000, -1.57, 0.000)]

    # Add the light sources
    for i, angle in enumerate(light_rotation):
        lamp_data = bpy.data.lamps.new(name='HemiLamp%d' % i, type='HEMI')
        lamp_object = bpy.data.objects.new(name='HemiLamp%d' % i, object_data=lamp_data)
        bpy.context.scene.objects.link(lamp_object)
        lamp_object.rotation_euler = angle
        bpy.data.lamps['HemiLamp%d' % i].use_nodes = True
        bpy.data.lamps['HemiLamp%d' % i].node_tree.nodes["Emission"].inputs[1].default_value = 10


####################################################################################################
# @create_voronoi_cells_illumination
####################################################################################################
def create_voronoi_cells_illumination(camera_view=vmv.enums.Rendering.View.FRONT):
    """
    :param name:
    :return:
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # If no light sources in the scene, then create two sources one towards the top and the
    # other one towards the bottom
    if not vmv.scene.ops.is_object_in_scene_by_name('DefaultLamp'):
        vmv.scene.ops.deselect_all()

        light_rotation = [(0.000, 0.000, 0.000),
                          (0.000, 3.140, 0.000),
                          (1.570, 0.000, 0.000),
                          (-1.57, 0.000, 0.000),
                          (0.000, 1.570, 0.000),
                          (0.000, -1.57, 0.000)]

        for i, angle in enumerate(light_rotation):
            bpy.ops.object.light_add(type='SUN', radius=1, location=(0, 0, 0))
            lamp_reference = bpy.context.object
            lamp_reference.name = 'Lamp%d' % i
            lamp_reference.data.name = "Lamp%d" % i
            lamp_reference.rotation_euler = angle
            bpy.data.lamps['Lamp%d' % i].node_tree.nodes["Emission"].inputs[1].default_value = 2.5


####################################################################################################
# @create_illumination
####################################################################################################
def create_material_specific_illumination(material_type,
                                          camera_view=vmv.enums.Rendering.View.FRONT):
    """Create a specific illumination that corresponds to a given material.
    :param material_type:
        Material type.
    :param camera_view:
        The rendering view of the camera. FRONT, SIDE or TOP.
    """

    # Lambert Ward
    if material_type == vmv.enums.Shader.LAMBERT_WARD:
        return create_default_illumination(camera_view=camera_view)

    # Lambert Ward
    elif material_type == vmv.enums.Shader.PLASTIC:
        return create_artistic_glossy_illumination(camera_view=camera_view)

    # Glossy bumpy
    elif material_type == vmv.enums.Shader.GLOSSY_BUMPY:
        return create_artistic_glossy_illumination(camera_view=camera_view)

    # Voronoi
    elif material_type == vmv.enums.Shader.GLOSSY_BUMPY:
        return create_voronoi_cells_illumination(camera_view=camera_view)

    # Default, just use the lambert shader illumination
    else:
        return create_default_illumination(camera_view=camera_view)
