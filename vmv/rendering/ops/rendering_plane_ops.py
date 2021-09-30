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

# Blender imports
import math

import bpy
from mathutils import Vector

# Internal imports
import vmv
import vmv.consts
import vmv.utilities
import vmv.mesh
import vmv.geometry
import vmv.scene
import vmv.shading


####################################################################################################
# @assign_material_to_background_plane
####################################################################################################
def assign_material_to_background_plane(plane_mesh):
    """Assigns material to the background plane.

    :param plane_mesh:
        The input plane mesh.
    """

    # If the rendering engine is cycles, then create a cycles material
    if bpy.context.scene.render.engine == 'CYCLES':
        material = vmv.shading.load_background_material()
    else:
        material = vmv.shading.create_lambert_ward_material(
            name='background',
            color=vmv.consts.Color.VERY_WHITE,
            specular=vmv.consts.Color.VERY_WHITE,
            switch_scene_shading=False)

    # Assign it
    vmv.shading.set_material_to_object(mesh_object=plane_mesh, material_reference=material)


####################################################################################################
# @add_background_plane_for_front_camera
####################################################################################################
def add_background_plane_for_front_camera(bounding_box):
    """Add a stylish plane that would reveal the shadow of the object and make the rendering
    stand out.

    :param bounding_box:
        Morphology or mesh bounding box.
    :return:
        A reference to the constructed plane.
    """

    # Plane location
    location = Vector((bounding_box.center[0],
                       bounding_box.center[1],
                       -vmv.consts.RenderingPlanes.BACKGROUND_PLANE_Z))

    # Add a plane
    plane_mesh = vmv.geometry.create_plane(size=1, location=location, name='background_plane')

    # Scale it
    vmv.scene.scale_object(scene_object=plane_mesh,
                           x=bounding_box.bounds[0] * 2,
                           y=bounding_box.bounds[1] * 2)

    # Select this plane
    vmv.scene.set_active_object(plane_mesh)

    # Set the pivot to the origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Smooth the surface for the shading
    vmv.mesh.shade_smooth_object(mesh_object=plane_mesh)

    # Assign the material to the background
    assign_material_to_background_plane(plane_mesh=plane_mesh)

    # Return a reference to the final plane
    return plane_mesh


####################################################################################################
# @add_background_plane_for_side_camera
####################################################################################################
def add_background_plane_for_side_camera(bounding_box):
    """Add a stylish plane that would reveal the shadow of the object and make the rendering
    stand out.

    :param bounding_box:
        Morphology or mesh bounding box.
    :return:
        A reference to the constructed plane.
    """

    # Plane location
    location = Vector((vmv.consts.RenderingPlanes.BACKGROUND_PLANE_Z,
                       bounding_box.center[1], bounding_box.center[2]))

    # Add a plane
    plane_mesh = vmv.geometry.create_plane(size=1, location=location, name='background_plane')

    # Scale it
    vmv.scene.scale_object(scene_object=plane_mesh,
                           x=bounding_box.bounds[1] * 2,
                           y=bounding_box.bounds[2] * 2)

    # Rotate it at 90 degrees
    vmv.scene.rotate_object(scene_object=plane_mesh, y=math.radians(90))

    # Select this plane
    vmv.scene.set_active_object(plane_mesh)

    # Set the pivot to the origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Smooth the surface for the shading
    vmv.mesh.shade_smooth_object(mesh_object=plane_mesh)

    # Assign the material to the background
    assign_material_to_background_plane(plane_mesh=plane_mesh)

    # Return a reference to the final plane
    return plane_mesh


####################################################################################################
# add_background_plane_for_top_camera
####################################################################################################
def add_background_plane_for_top_camera(bounding_box):
    """Add a stylish plane that would reveal the shadow of the object and make the rendering
    stand out.

    :param bounding_box:
        Morphology or mesh bounding box.
    :return:
        A reference to the constructed plane.
    """

    # Plane location
    location = Vector((bounding_box.center[0],
                       vmv.consts.RenderingPlanes.BACKGROUND_PLANE_Z,
                       bounding_box.center[2]))

    # Add a plane
    plane_mesh = vmv.geometry.create_plane(size=1, location=location, name='background_plane')

    # Rotate it at 90 degrees
    vmv.scene.rotate_object(scene_object=plane_mesh, x=math.radians(90))

    # Scale it
    vmv.scene.scale_object(scene_object=plane_mesh,
                           x=bounding_box.bounds[0] * 2,
                           y=bounding_box.bounds[2] * 2)

    # Select this plane
    vmv.scene.set_active_object(plane_mesh)

    # Set the pivot to the origin
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # Smooth the surface for the shading
    vmv.mesh.shade_smooth_object(mesh_object=plane_mesh)

    # Assign the material to the background
    assign_material_to_background_plane(plane_mesh=plane_mesh)

    # Return a reference to the final plane
    return plane_mesh


####################################################################################################
# add_background_plane
####################################################################################################
def add_background_plane(bounding_box,
                         camera_view):
    """Add a stylish plane that would reveal the shadow of the object and make the rendering
    stand out.

    :param bounding_box:
        Morphology or mesh bounding box.
    :param camera_view:
        The view of the camera used for the rendering.
    :return:
        A reference to the created plane.
    """

    # Front
    if camera_view == vmv.enums.Rendering.View.FRONT or \
       camera_view == vmv.enums.Rendering.View.FRONT_360:
        return add_background_plane_for_front_camera(bounding_box)

    # Side
    elif camera_view == vmv.enums.Rendering.View.SIDE:
        return add_background_plane_for_side_camera(bounding_box)

    # Top
    elif camera_view == vmv.enums.Rendering.View.TOP:
        return add_background_plane_for_top_camera(bounding_box)

    # Ignore, but return None to handle any errors
    else:
        return None



