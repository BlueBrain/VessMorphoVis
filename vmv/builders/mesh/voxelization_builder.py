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
import time

# Internal modules
import vmv.bmeshi
import vmv.geometry
import vmv.mesh
import vmv.utilities
from .base import MeshBuilder


####################################################################################################
# @VoxelizationBuilder
####################################################################################################
class VoxelizationBuilder(MeshBuilder):
    """Mesh builder that creates watertight meshes for the vascular morphology."""

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

        # Builder name
        self.builder_name = 'VoxelizationBuilder'

        # Final mesh center
        self.center = (0.0, 0.0, 0.0)

        # Create the skeleton materials during the initialization
        self.create_skeleton_materials()

        # The actual smallest radius in the morphology, used to find the voxelization resolution
        self.smallest_radius = 1e5

    ################################################################################################
    # @generate_optimized_sections_mesh
    ################################################################################################
    def generate_optimized_sections_mesh(self,
                                         use_nurbs=False):
        """Generates an optimized sections mesh by splitting the mesh into low- and high-quality
        components, depending on the average radius of each section. This reduces the voxelization
        time considerably and meanwhile improves the cross-sectional quality of the mesh.

        :param use_nurbs:
            If this flag is set, we will use NURBS interpolation to build the sectional geometry.
        :return:
            A reference to the resulting proxy mesh of the sections.
        """

        # Determining the smallest radius in the morphology
        tqdm = vmv.utilities.import_module('tqdm')
        if tqdm:
            _loop = tqdm.tqdm(self.morphology.sections_list,
                              desc='\t* Computing Sections Radii Distribution',
                              bar_format=vmv.consts.String.BAR_FORMAT)
        else:
            _loop = self.morphology.sections_list

        min_sample_radius = 1e10
        max_sample_radius = -1e10
        average_section_radii = list()
        for i_section in _loop:
            average_section_radius = 0
            for i_sample in i_section.samples:
                average_section_radius += i_sample.radius
                if i_sample.radius < min_sample_radius:
                    min_sample_radius = i_sample.radius
                if i_sample.radius > max_sample_radius:
                    max_sample_radius = i_sample.radius
            average_section_radius /= float(len(i_section.samples))
            average_section_radii.append(average_section_radius)

        # Compute the median radius
        median_radius = vmv.utilities.find_median(average_section_radii)
        self.smallest_radius = min_sample_radius

        # Filter the sections based on the mean radius
        low_quality_sections = list()
        high_quality_sections = list()
        if tqdm:
            _loop = tqdm.tqdm(range(len(self.morphology.sections_list)),
                              desc='\t* Generating Poly-line Sectional Geometry',
                              bar_format=vmv.consts.String.BAR_FORMAT)
        else:
            _loop = range(len(self.morphology.sections_list))
        for i in _loop:
            if average_section_radii[i] < median_radius:
                low_quality_sections.append(self.morphology.sections_list[i])
            else:
                high_quality_sections.append(self.morphology.sections_list[i])

        low_resolution_poly_lines = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_with_single_color(
                section=section, duplicate_terminal_samples=use_nurbs)
            for section in low_quality_sections]

        high_resolution_poly_lines = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_with_single_color(
                section=section, duplicate_terminal_samples=use_nurbs)
            for section in high_quality_sections]

        low_resolution_bevel = vmv.mesh.create_bezier_circle(vertices=8, name='LR Bevel')
        high_resolution_bevel = vmv.mesh.create_bezier_circle(vertices=16, name='HR Bevel')

        # Create a poly-line object from the data
        low_resolution_poly_line_object = vmv.geometry.create_poly_lines_object_from_poly_lines_data(
            poly_lines_data=low_resolution_poly_lines,
            name='Low Resolution Sections', bevel_object=low_resolution_bevel,
            poly_line_type='NURBS' if use_nurbs else 'POLY')

        # Create a poly-line object from the data
        high_resolution_poly_line_object = (
            vmv.geometry.create_poly_lines_object_from_poly_lines_data(
                poly_lines_data=high_resolution_poly_lines,
                name='High Resolution Sections', bevel_object=high_resolution_bevel,
                poly_line_type='NURBS' if use_nurbs else 'POLY'))

        low_resolution_object_mesh = vmv.scene.convert_object_to_mesh(
            scene_object=low_resolution_poly_line_object)

        high_resolution_object_mesh = vmv.scene.convert_object_to_mesh(
            scene_object=high_resolution_poly_line_object)

        # Merge the two mesh objects into a single mesh
        return vmv.mesh.join_mesh_objects(
            mesh_list=[low_resolution_object_mesh, high_resolution_object_mesh],
            name='Skeleton')

    ################################################################################################
    # @generate_sections_mesh
    ################################################################################################
    def generate_sections_mesh(self,
                               cross_sectional_sides=32,
                               use_nurbs=False):
        """Generates a proxy mesh for the sections. All the sections have the same interpolation
        and cross-sectional sides.

        :param use_nurbs:
            If this flag is set, we will use NURBS interpolation to build the sectional geometry.
        :param cross_sectional_sides:
            Number of sides of the bevel object used to reconstruct the cross-sectional geometry.
        :return:
            A reference to the resulting proxy mesh of the sections.
        """

        # Collect the poly-line data in a list
        poly_line_data = [
            vmv.skeleton.ops.get_color_coded_section_poly_line_with_single_color(
                section=section, duplicate_terminal_samples=use_nurbs)
            for section in self.morphology.sections_list]

        # Determining the smallest radius in the morphology
        tqdm = vmv.utilities.import_module('tqdm')
        if tqdm:
            _loop = tqdm.tqdm(poly_line_data,
                              desc='\t* Detecting Minimum Radius',
                              bar_format=vmv.consts.String.BAR_FORMAT)
        else:
            _loop = poly_line_data
        for poly_line in _loop:
            for sample in poly_line.samples:
                if sample[1] < self.smallest_radius:
                    self.smallest_radius = sample[1]

        # Create a bevel object
        bevel_object = vmv.mesh.create_bezier_circle(vertices=cross_sectional_sides, name='Bevel')

        # Create a poly-line object from the data
        poly_line_object = vmv.geometry.create_poly_lines_object_from_poly_lines_data(
            poly_lines_data=poly_line_data, name='Skeleton', bevel_object=bevel_object,
            poly_line_type='NURBS' if use_nurbs else 'POLY')

        # Convert the resulting poly-line object into a mesh object and return a reference to it
        return vmv.scene.convert_object_to_mesh(scene_object=poly_line_object)

    ################################################################################################
    # @generate_branching_mesh
    ################################################################################################
    def generate_branching_mesh(self):
        """Generates a composite mesh of all the branching samples to bridge the different sections
        of the morphology. This function is much faster than the @generate_terminal_samples_mesh
        as it creates meshes, only at the branching samples to avoid duplicating the data."""

        # Obtain a data list containing the locations and radii of the branching samples
        branching_samples_data = self.morphology.get_branching_samples_data()

        # Creating a bmesh object
        bmesh_object = vmv.bmeshi.create_bmesh_object_from_spheres_list_using_icospheres(
            spheres_list=branching_samples_data, subdivisions=2)

        # Creating the corresponding mesh
        return vmv.bmeshi.convert_bmesh_to_mesh(bmesh_object=bmesh_object, name='Branching')

    ################################################################################################
    # @generate_terminal_samples_mesh
    ################################################################################################
    def generate_terminal_samples_mesh(self):
        """Generates a composite mesh of all the terminal samples of every section in the morphology
        to bridge the different sections of the morphology. This function is slower than the
        @generate_branching_mesh function, but it is mainly used to validate the reconstruction
        quality of the resulting mesh."""

        # A list that will contain all the bmesh objects resulting at the terminal samples
        bmesh_objects_list = list()

        # Verify the installation of the tqdm module in the system
        tqdm = vmv.utilities.import_module('tqdm')
        if tqdm:
            _loop = tqdm.tqdm(self.morphology.sections_list,
                              desc='\t* Terminal Samples', bar_format=vmv.consts.String.BAR_FORMAT)
        else:
            _loop = self.morphology.sections_list

        # Do it on a per-section basis
        for i_section in _loop:

            # References to first and last samples
            first_sample = i_section.samples[0]
            last_sample = i_section.samples[-1]

            # Create the first sample bmesh and append it to the list
            first_sample_bmesh = vmv.bmeshi.create_ico_sphere(
                radius=first_sample.radius, location=first_sample.point, subdivisions=2)
            bmesh_objects_list.append(first_sample_bmesh)

            # Create the last sample bmesh and append it to the list
            last_sample_bmesh = vmv.bmeshi.create_ico_sphere(
                radius=last_sample.radius, location=last_sample.point, subdivisions=2)
            bmesh_objects_list.append(last_sample_bmesh)

        # Join all the bmesh objects into a single one
        terminal_samples_bmesh = vmv.bmeshi.join_bmeshes_list(bmeshes_list=bmesh_objects_list)

        # Release the bmesh objects
        for bmesh_object in bmesh_objects_list:
            bmesh_object.free()
            del bmesh_object

        # Convert the bmesh object into a mesh object and return the resulting object
        return vmv.bmeshi.convert_bmesh_to_mesh(
            bmesh_object=terminal_samples_bmesh, name='Terminals')

    ################################################################################################
    # @remesh_proxy_mesh
    ################################################################################################
    def remesh_proxy_mesh(self,
                          branching_mesh,
                          sections_mesh):
        """Generates a re-meshed watertight mesh using the voxelization re-meshing modifier given
        two input meshes for the sections and branching samples.

        :param branching_mesh:
            A proxy mesh of the branching samples.
        :param sections_mesh:
            A proxy mesh of the sections.
        """

        # Merge branching and section meshes to a single proxy mesh (with multiple partitions)
        self.mesh = vmv.mesh.join_mesh_objects(
            mesh_list=[branching_mesh, sections_mesh], name='Vascular Proxy Mesh')

        # Apply the voxelization modifier to the proxy mesh to create a single manifold
        vmv.mesh.remesh_using_voxelization(
            mesh_object=self.mesh, voxel_size=self.smallest_radius * 0.5)

    ################################################################################################
    # @build_mesh
    ################################################################################################
    def build_mesh(self):
        """Reconstructs the vascular mesh.

        :return:
            A reference to the reconstructed vascular mesh.
        """

        vmv.logger.header('Building Mesh: %s' % self.builder_name)

        # Update the center of the mesh to the center of the bounding box of the morphology
        self.center = self.morphology.bounding_box.center

        # Create the branching mesh
        start = time.time()
        vmv.logger.info('Generating Branching Mesh, without Terminals')
        branching_mesh = self.generate_branching_mesh()

        # Create the terminal samples mesh
        # vmv.logger.info('Generating Branching Mesh, with Terminals')
        # branching_mesh = self.generate_terminal_samples_mesh()

        # Create the sections mesh
        vmv.logger.info('Generating Sections Mesh')
        # sections_mesh = self.generate_sections_mesh()
        sections_mesh = self.generate_optimized_sections_mesh()

        # Re-mesh the proxy mesh into a single manifold
        vmv.logger.info('Re-meshing and Reconstructing Vascular Mesh: Resolution [%f]' %
                        (self.smallest_radius * 0.5))
        self.remesh_proxy_mesh(branching_mesh=branching_mesh, sections_mesh=sections_mesh)
        end = time.time()

        # Time
        vmv.logger.info('Building Time [ %f ]' % (end - start))

        # Triangulate the resulting mesh
        vmv.mesh.triangulate_mesh_object(mesh_object=self.mesh)

        # Assign the material to the mesh
        self.assign_material_to_mesh()

        # Update its name with the mesh suffix to be able to locate it
        self.set_default_mesh_name()

        # Tessellate Mesh
        self.tessellate_mesh()

        # Mission done
        vmv.logger.header('Done!')

        # Return a reference to the created mesh
        return self.mesh
