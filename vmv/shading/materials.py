####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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

# System imports
import os 

# Blender imports
import bpy
import mathutils

# Internal imports
import vmv
import vmv.consts
import vmv.enums
import vmv.scene


####################################################################################################
# @import_shader
####################################################################################################
def import_shader(shader_name):
    """Import a shader from  the NeuroMorphoVis shading library.

    :param shader_name:
        The name of the shader file in the library.
    :return:
        A reference to the shader after being loaded into blender.
    """

    # Get the path of this file
    current_file = os.path.dirname(os.path.realpath(__file__))
    shaders_directory = '%s/shaders/%s.blend/Material' % (current_file, shader_name)

    # Import the material
    bpy.ops.wm.append(filename='material', directory=shaders_directory)

    # Get a reference to the material
    material_reference = bpy.data.materials['material']

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_workbench_material
####################################################################################################
def create_workbench_material(name,
                              color=vmv.consts.Color.WHITE,
                              roughness=0.0,
                              metallic=0.0):
    """Creates a material that can be only used with the Workbench renderer.

    :param name:
        Material name.
    :param color:
        Diffuse component.
    :param roughness:
        Material roughness, 0.0 for glossy, 1.0 for matte.
    :param metallic:
        Material metallic, 0.0 for glossy, 1.0 for matte.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Set the current rendering engine to WORKBENCH
    if not current_scene.render.engine == 'BLENDER_WORKBENCH':
        current_scene.render.engine = 'BLENDER_WORKBENCH'

    # Create a new material (color) and assign it to the line
    color = mathutils.Vector((color[0], color[1], color[2], 1.0))

    # Create a new material (color) and assign it to the line
    line_material = bpy.data.materials.new('color.%s' % name)
    line_material.diffuse_color = color

    # Zero-metallic and roughness
    line_material.roughness = roughness
    line_material.metallic = metallic

    # Return a reference to the material
    return line_material


####################################################################################################
# @create_flat_material
####################################################################################################
def create_flat_material(name,
                         color=vmv.consts.Color.WHITE):
    """Creates a flat shader that can be used with Cycles.
    The shader is quite simple and uses an emitting color that is sufficient to render it with one
    sample per pixel.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='flat-material')

    # Rename the material
    material_reference.name = str(name)

    # Set, or FORCE, the number of samples per pixel to ONE
    bpy.context.scene.cycles.samples = 1

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2]

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_electron_light_material
####################################################################################################
def create_electron_light_material(name,
                                   color=vmv.consts.Color.WHITE):
    """Creates a light electron shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='electron-light-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_artistic_glossy_material
####################################################################################################
def create_artistic_glossy_material(name,
                                    color=vmv.consts.Color.DEFAULT_BLOOD_COLOR):
    """Creates a an artistic glossy shader for Cycles rendering.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Use de-noising
    current_scene.view_layers['View Layer'].cycles.use_denoising = True

    # Import the material from the library
    material_reference = import_shader(shader_name='artistic-glossy')

    # Rename the material
    material_reference.name = str(name)

    # Return a reference to the material
    return material_reference

####################################################################################################
# @create_super_electron_light_material
####################################################################################################
def create_super_electron_light_material(name,
                                         color=vmv.consts.Color.WHITE):
    """Creates a light electron shader that can be used with Cycles..

    :param name:
        Material name
    :param color:
        Material color, by default white.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='super-electron-light-material')

    # Rename the material
    material_reference.name = str(name)

    # Set, or FORCE, the number of samples per pixel to ONE
    bpy.context.scene.cycles.samples = 1

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_shadow_material
####################################################################################################
def create_shadow_material(name,
                           color=vmv.consts.Color.WHITE):
    """Creates a material with shadow. This requires creating two light sources if they don't exist
    in the scene.

    This function imports the shadow-material from the materials library and updates its parameters.

    :param name:
        Material name.
    :param color:
        Material color, by default white.
    :return:
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='shadow-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_super_electron_light_material
####################################################################################################
def create_super_electron_light_material(name,
                                         color=vmv.consts.Color.WHITE):
    """Creates a light electron shader.

    :param name:
        Material name
    :param color:
        Material color, by default white.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='super-electron-light-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_super_electron_dark_material
####################################################################################################
def create_super_electron_dark_material(name,
                                        color=vmv.consts.Color.WHITE):
    """Creates a light electron shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='super-electron-dark-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference





####################################################################################################
# @create_flat_material
####################################################################################################
def create_voroni_cells_material(name,
                                 color=vmv.consts.Color.WHITE):
    """Creates a voroni shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='voroni-cells')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2]

    # Return a reference to the material
    return material_reference




####################################################################################################
# @create_electron_dark_material
####################################################################################################
def create_electron_dark_material(name,
                                  color=vmv.consts.Color.WHITE):
    """Creates a light electron shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='electron-dark-material')

    # Rename the material
    material_reference.name = str(name)

    # Update the color gradient
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[0] = color[0]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[1] = color[1]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[0].color[2] = color[2]
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[0] = color[0] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[1] = color[1] / 2.0
    material_reference.node_tree.nodes['ColorRamp'].color_ramp.elements[1].color[2] = color[2] / 2.0

    # Return a reference to the material
    return material_reference





####################################################################################################
# @create_default_material
####################################################################################################
def create_lambert_ward_material(name,
                                 color=vmv.consts.Color.WHITE):
    """Creates a a texture material.

    :param name:
        Material name.
    :param color:
        Diffuse component.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Set the current rendering engine to WORKBENCH
    if not current_scene.render.engine == 'BLENDER_WORKBENCH':
        current_scene.render.engine = 'BLENDER_WORKBENCH'

    # Create a new material (color) and assign it to the line
    color = mathutils.Vector((color[0], color[1], color[2], 1.0))

    # Create a new material (color) and assign it to the line
    line_material = bpy.data.materials.new('color.%s' % name)
    line_material.diffuse_color = color

    # Zero-metallic and roughness
    line_material.roughness = 0
    line_material.metallic = 0

    # Return a reference to the material
    return line_material


####################################################################################################
# @create_glossy_material
####################################################################################################
def create_glossy_material(name,
                           color=vmv.consts.Color.WHITE):
    """Creates a glossy shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='glossy')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[2] = color[2]

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_glossy_material
####################################################################################################
def create_glossy_bumpy_material(name,
                                 color=vmv.consts.Color.WHITE):
    """Creates a glossy bumpy shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Switch the rendering engine to cycles to be able to create the material
    if not current_scene.render.engine == 'CYCLES':
        current_scene.render.engine = 'CYCLES'

    # Import the material from the library
    material_reference = import_shader(shader_name='glossy-bumpy')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["RGB"].outputs[0].default_value[2] = color[2]

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_ceramic_material
####################################################################################################
def create_ceramic_material(name,
                            color=vmv.consts.Color.WHITE):
    """Creates a glossy bumpy shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Import the material from the library
    material_reference = import_shader(shader_name='ceramic')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["Group"].inputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["Group"].inputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["Group"].inputs[0].default_value[2] = color[2]

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_skin_material
####################################################################################################
def create_skin_material(name,
                         color=vmv.consts.Color.WHITE):
    """Creates a glossy bumpy shader.

    :param name:
        Material name
    :param color:
        Material color.
    :return:
        A reference to the material.
    """

    # Get active scene
    current_scene = bpy.context.scene

    # Import the material from the library
    material_reference = import_shader(shader_name='skin')

    # Rename the material
    material_reference.name = str(name)

    material_reference.node_tree.nodes["Group"].inputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["Group"].inputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["Group"].inputs[0].default_value[2] = color[2]

    material_reference.node_tree.nodes["Group.001"].inputs[0].default_value[0] = color[0]
    material_reference.node_tree.nodes["Group.001"].inputs[0].default_value[1] = color[1]
    material_reference.node_tree.nodes["Group.001"].inputs[0].default_value[2] = color[2]

    # Return a reference to the material
    return material_reference


####################################################################################################
# @create_material
####################################################################################################
def create_material(name,
                    color,
                    material_type):
    """Create a specific material given its type and color.

    :param name:
        Material name.
    :param color:
        Material color.
    :param material_type:
        Material type.
    :return:
        A reference to the created material
    """

    # Glossy, for the workbench renderer
    if material_type == vmv.enums.Shading.GLOSSY_WORKBENCH:
        return create_workbench_material(name='%s_color' % name, color=color)

    # Matte, for the workbench renderer
    elif material_type == vmv.enums.Shading.MATTE_WORKBENCH:
        return create_workbench_material(
            name='%s_color' % name, color=color, roughness=1.0, metallic=1.0)

    # Flat
    elif material_type == vmv.enums.Shading.FLAT_CYCLES:
        return create_flat_material(name='%s_color' % name, color=color)

    # EM shader
    elif material_type == vmv.enums.Shading.ELECTRON_CYCLES:
        return create_electron_light_material(name='%s_color' % name, color=color)

    # Artistic glossy shader
    elif material_type == vmv.enums.Shading.ARTISTIC_GLOSSY_CYCLES:
        return create_artistic_glossy_material(name='%s_color' % name, color=color)

    # Glossy bumpy
    elif material_type == vmv.enums.Shading.ARTISTIC_BUMPY_CYCLES:
        return create_glossy_bumpy_material(name='%s_color' % name, color=color)

    # Default
    else:
        return create_lambert_ward_material(name='%s_color' % name, color=color)


####################################################################################################
# @set_material_to_object
####################################################################################################
def set_material_to_object(mesh_object,
                           material_reference):
    """Assign the given material to a given mesh object.

    :param mesh_object:
        A surface mesh object.
    :param material_reference:
        The material to be assigned to the object.
    """

    # Clear the previous materials assigned to this mesh object
    mesh_object.data.materials.clear()

    # Assign the material to the given object.
    mesh_object.data.materials.append(material_reference)


####################################################################################################
# @adjust_material_uv
####################################################################################################
def adjust_material_uv(mesh_object,
                       size=1):
    """Update the texture space of the created meshes

    :param mesh_object:
        A given mesh object.
    :param size:
        The texture space size of the material, by default set to 1.
    """
    # Select the mesh
    mesh_object.select = True

    # Set the 'auto_texspace' to False
    bpy.context.object.data.use_auto_texspace = False

    # Update the texture space size
    bpy.context.object.data.texspace_size[0] = size
    bpy.context.object.data.texspace_size[1] = size
    bpy.context.object.data.texspace_size[2] = size
