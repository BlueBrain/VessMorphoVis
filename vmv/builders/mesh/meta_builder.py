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

# System imports
import time

# Blender imports
import bpy
from mathutils import Vector

# Internal modules
import vmv
import vmv.builders
import vmv.enums
import vmv.mesh
import vmv.skeleton
import vmv.utilities
import vmv.scene
import vmv.shading
from .base import MeshBuilder


####################################################################################################
# @MetaBuilder
####################################################################################################
class MetaBuilder(MeshBuilder):
    """Mesh builder that creates high quality meshes with nice bifurcations based on meta objects"""

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self,
                 morphology,
                 options):
        """Constructor

        :param morphology:
            A given morphology skeleton to create the mesh for.
        :param options:
            Loaded options from VessMorphoVis.
        """

        # Base
        MeshBuilder.__init__(self, morphology=morphology, options=options)

        # Meta object skeleton, used to build the skeleton of the morphology
        self.meta_skeleton = None

        # A scale factor that was figured out by trial and error to correct the scaling of the radii
        self.magic_scale_factor = 1.575

        # The radius of the smallest sample in the morphology
        self.smallest_radius = 1e10

    ################################################################################################
    # @create_meta_segment
    ################################################################################################
    def create_meta_segment(self,
                            p1,
                            p2,
                            r1,
                            r2):
        """Constructs a segment that is composed of two points with a meta object.

        :param p1:
            First point coordinate.
        :param p2:
            Second point coordinate.
        :param r1:
            First point radius.
        :param r2:
            Second point radius.
        """

        # Segment vector
        segment = p2 - p1
        segment_length = segment.length

        # Make sure that the segment length is not zero
        # TODO: Verify this when the radii are greater than the distance
        if segment_length < 0.001:
            return

        # Verify the radii, or fix them
        if r1 < 0.001 * segment_length:
            r1 = 0.001 * segment_length
        if r2 < 0.001 * segment_length:
            r2 = 0.001 * segment_length

        if r1 < self.smallest_radius:
            self.smallest_radius = r1
        if r2 < self.smallest_radius:
            self.smallest_radius = r2

        # Compute the deltas between the first and last points along the segments
        dr = r2 - r1
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        dz = p2[2] - p1[2]

        # Keep track on the distance traveled along the segment while building, initially 0
        travelled_distance = 0.0

        # Local points, initially at the first point
        r = r1
        x = p1[0]
        y = p1[1]
        z = p1[2]

        # Construct the meta elements along the segment
        i = 0
        while travelled_distance < segment_length:

            # Make a meta ball (or sphere) at this point
            meta_element = self.meta_skeleton.elements.new()

            # Set its radius
            if i == 0:
                meta_element.radius = r * 0.90
            else:
                meta_element.radius = r

            # Update its coordinates
            meta_element.co = (x, y, z)

            # Proceed to the next point
            travelled_distance += 0.5 * r

            r = r1 + (travelled_distance * dr / segment_length)

            # Get the next point
            x = p1[0] + (travelled_distance * dx / segment_length)
            y = p1[1] + (travelled_distance * dy / segment_length)
            z = p1[2] + (travelled_distance * dz / segment_length)

            i += 1

    ################################################################################################
    # @create_meta_section
    ################################################################################################
    def create_meta_section(self,
                            section):
        """Create a section with meta objects.

        :param section:
            A given section to extrude a mesh around it.
        """

        # Get the list of samples
        samples = section.samples

        # Ensure that the section has at least two samples, otherwise it will give an error
        if len(samples) < 2:
            return

        # Fixed radii
        if self.options.morphology.radii == vmv.enums.Morphology.Radii.FIXED:

            # Proceed segment by segment
            for i in range(len(samples) - 1):

                # Create the meta segment
                self.create_meta_segment(
                    p1=samples[i].point,
                    p2=samples[i + 1].point,
                    r1=self.options.morphology.sections_fixed_radii_value * self.magic_scale_factor,
                    r2=self.options.morphology.sections_fixed_radii_value * self.magic_scale_factor)

        # Scaled radii
        elif self.options.morphology.radii == vmv.enums.Morphology.Radii.SCALED:

            # Get the scale value
            scale = self.options.morphology.sections_radii_scale

            # Proceed segment by segment
            for i in range(len(samples) - 1):
                # Create the meta segment
                self.create_meta_segment(
                    p1=samples[i].point,
                    p2=samples[i + 1].point,
                    r1=samples[i].radius * self.magic_scale_factor * scale,
                    r2=samples[i + 1].radius * self.magic_scale_factor * scale)

        # Minimum threshold
        elif self.options.morphology.radii == vmv.enums.Morphology.Radii.MINIMUM:

            # Get the scale value
            value = self.options.morphology.sections_radii_minimum

            # Proceed segment by segment
            for i in range(len(samples) - 1):

                if samples[i].radius < value:
                    r1 = value
                else:
                    r1 = samples[i].radius

                if samples[i + 1].radius < value:
                    r2 = value
                else:
                    r2 = samples[i + 1].radius

                # Create the meta segment
                self.create_meta_segment(
                    p1=samples[i].point,
                    p2=samples[i + 1].point,
                    r1=r1 * self.magic_scale_factor,
                    r2=r2 * self.magic_scale_factor)

        # Default radii as specified in the morphology file
        else:

            # Proceed segment by segment
            for i in range(len(samples) - 1):

                # Create the meta segment
                self.create_meta_segment(
                    p1=samples[i].point,
                    p2=samples[i + 1].point,
                    r1=samples[i].radius * self.magic_scale_factor,
                    r2=samples[i + 1].radius * self.magic_scale_factor)

    ################################################################################################
    # @initialize_meta_object
    ################################################################################################
    def build_meta_object(self):
        """Builds the meta object of the sections.
        """

        # For every section, in the morphology, create a meta-section
        for i, section in enumerate(self.morphology.sections_list):

            # Current iteration
            vmv.utilities.show_progress('\t\t* Progress', i, len(self.morphology.sections_list))

            # Create the section
            self.create_meta_section(section)

        # Process done
        vmv.utilities.show_progress('\t\t* Progress', len(self.morphology.sections_list),
                                    len(self.morphology.sections_list), True)

    ################################################################################################
    # @initialize_meta_object
    ################################################################################################
    def initialize_meta_object(self):
        """Constructs and initialize a new meta object that will be the basis of the mesh.
        """

        # Create a new meta skeleton that will be used to reconstruct the skeleton frame
        self.meta_skeleton = bpy.data.metaballs.new(self.morphology.name)

        # Create a new meta object that reflects the reconstructed mesh at the end of the operation
        self.mesh = bpy.data.objects.new(self.morphology.name, self.meta_skeleton)

        # Get a reference to the scene
        scene = bpy.context.scene

        # Link the meta object to the scene
        scene.collection.objects.link(self.mesh)

        # Update the resolution of the meta skeleton
        self.meta_skeleton.resolution = 1.0

    ################################################################################################
    # @finalize_meta_object
    ################################################################################################
    def finalize_meta_object(self):
        """Converts the meta object to a mesh and get it ready for export or visualization.
        """

        # Header
        # vmv.logger.header('Meshing the Meta Object')

        if self.options.mesh.meta_auto_resolution:
            self.meta_skeleton.resolution = self.smallest_radius * 0.9
        else:
            self.meta_skeleton.resolution = self.options.mesh.meta_resolution

        # Update the interface
        vmv.logger.info('MetaBall resolution: [%f]' % self.meta_skeleton.resolution)
        self.options.mesh.meta_resolution = self.meta_skeleton.resolution

        # Deselect all objects
        vmv.scene.ops.deselect_all()

        # Select the mesh
        self.mesh = bpy.context.scene.objects[self.morphology.name]
        self.mesh.select_set(True)
        bpy.context.view_layer.objects.active = self.mesh

        # Convert it to a mesh from meta-balls
        bpy.ops.object.convert(target='MESH')

        # Update its name with the mesh suffix to be able to locate it
        self.mesh = bpy.context.scene.objects[self.morphology.name + '.001']
        self.mesh.name = self.morphology.name + vmv.consts.Suffix.MESH_SUFFIX

        # Re-select it again to be able to perform post-processing operations in it
        self.mesh.select_set(True)

        # Tessellate Mesh
        self.tessellate_mesh()

        # Set the mesh to be the active object
        bpy.context.view_layer.objects.active = self.mesh

    ################################################################################################
    # @tessellate_mesh
    ################################################################################################
    def tessellate_mesh(self):

        # Ensure that the tessellation level is within range
        if 0.01 < self.options.mesh.tessellation_ratio < 1.0:

            # Decimate each mesh object
            vmv.mesh.ops.decimate_mesh_object(
                mesh_object=self.mesh,
                decimation_ratio=self.options.mesh.tessellation_ratio)

            # Adjust the texture mapping
            vmv.shading.adjust_material_uv(mesh_object=self.mesh)

    ################################################################################################
    # @build
    ################################################################################################
    def build_mesh(self):
        """Reconstructs the vascular mesh using meta objects.
        """

        vmv.logger.header('Building Mesh: MetaBalls')

        # Clear the scene
        vmv.scene.clear_scene()

        # Initialize the meta object
        start = time.time()
        vmv.logger.info('Initialization')
        self.initialize_meta_object()

        # Build the meta object
        vmv.logger.info('Building Meta Object')
        self.build_meta_object()

        # Finalize the meta object and create the actual mesh
        vmv.logger.info('Reconstructing Mesh')
        self.finalize_meta_object()
        end = time.time()

        # Time
        vmv.logger.info('Building Time [ %f ]' % (end - start))

        # Finalize the meta object and construct a solid object
        # We can here create the materials at the end to avoid any issues
        vmv.logger.info('Assigning Material')
        self.create_skeleton_materials()

        # Assign the material to the mesh
        self.assign_material_to_mesh()

        # Mission done
        vmv.logger.header('Done!')

        return self.mesh
