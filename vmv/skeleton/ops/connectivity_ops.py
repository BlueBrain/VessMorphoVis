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

# System import
import copy

# Blender imports
import bmesh

# Internal imports
import vmv.bmeshi
import vmv.mesh
import vmv.bmeshi


####################################################################################################
# @construct_branching_connectivity_using_simplified_edges_non_optimized
####################################################################################################
def construct_branching_connectivity_using_simplified_edges_non_optimized(morphology):

    double_edge_sections_list = list()
    for i, i_section in enumerate(morphology.sections_list):
        if (i_section.samples[0].point - i_section.samples[-1].point).length < 0.00001:
            print('Loop section')
        else:
            double_edge_sections_list.extend(i_section.construct_two_edge_sections(index=i))

    lengths = list()
    count = int(len(double_edge_sections_list) / 2)
    for i in range(0, count, 2):
        s1 = double_edge_sections_list[i]
        s2 = double_edge_sections_list[i + 1]
        lengths.append((s1.sample_1.point - s2.sample_2.point).length)

    # Create a new bmesh object to construct the graph of the simplified morphology
    simplified_morphology_graph_bmesh = vmv.bmeshi.create_bmesh_object()

    # Construct the vertices of the bmesh object
    for i_section in double_edge_sections_list:
        # Add the first sample of the edge (first sample of the actual section)
        vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
            simplified_morphology_graph_bmesh, i_section.sample_1.point)

        # Add the second sample of the edge (last sample of the actual section)
        vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
            simplified_morphology_graph_bmesh, i_section.sample_2.point)

    # Update the lookup table of the vertices to be able to add the edges
    simplified_morphology_graph_bmesh.verts.ensure_lookup_table()

    # Construct the edges of the bmesh object
    vertex_index = 0
    for i in range(len(double_edge_sections_list)):
        v1 = simplified_morphology_graph_bmesh.verts[vertex_index]
        v2 = simplified_morphology_graph_bmesh.verts[vertex_index + 1]
        simplified_morphology_graph_bmesh.edges.new((v1, v2))
        vertex_index += 2

    # Update the lookup table of the edges to be able to use the bmesh (indexing operations)
    simplified_morphology_graph_bmesh.edges.ensure_lookup_table()

    bmesh.ops.remove_doubles(simplified_morphology_graph_bmesh,
                             verts=simplified_morphology_graph_bmesh.verts,
                             dist=0.00001)

    # Convert the bmesh to a mesh
    graph_mesh = vmv.bmeshi.convert_bmesh_to_mesh(bmesh_object=simplified_morphology_graph_bmesh,
                                                  name='%s Graph' % 'Example')

    return graph_mesh


####################################################################################################
# @construct_branching_connectivity_using_simplified_edges
####################################################################################################
def construct_branching_connectivity_using_simplified_edges(morphology):

    # Construct the EdgeSection's list (simplified morphology) from the actual morphology
    edge_sections_list = morphology.construct_edge_sections()

    lengths = list()
    for section in edge_sections_list:
        lengths.append((section.sample_1-section.sample_2).length)
    lengths.sort()

    # Create a new bmesh object to construct the graph of the simplified morphology
    simplified_morphology_graph_bmesh = vmv.bmeshi.create_bmesh_object()

    # Construct the vertices of the bmesh object
    for i_section in edge_sections_list:

        # Add the first sample of the edge (first sample of the actual section)
        vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
            simplified_morphology_graph_bmesh, i_section.sample_1)

        # Add the second sample of the edge (last sample of the actual section)
        vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
            simplified_morphology_graph_bmesh, i_section.sample_2)

    # Update the lookup table of the vertices to be able to add the edges
    simplified_morphology_graph_bmesh.verts.ensure_lookup_table()

    # Construct the edges of the bmesh object
    vertex_index = 0
    for i in range(len(edge_sections_list)):
        v1 = simplified_morphology_graph_bmesh.verts[vertex_index]
        v2 = simplified_morphology_graph_bmesh.verts[vertex_index + 1]
        simplified_morphology_graph_bmesh.edges.new((v1, v2))
        vertex_index += 2

    # Update the lookup table of the edges to be able to use the bmesh (indexing operations)
    simplified_morphology_graph_bmesh.edges.ensure_lookup_table()

    bmesh.ops.remove_doubles(
        simplified_morphology_graph_bmesh,
        verts=simplified_morphology_graph_bmesh.verts, dist=0.0001)

    # Convert the bmesh to a mesh
    graph_mesh = vmv.bmeshi.convert_bmesh_to_mesh(bmesh_object=simplified_morphology_graph_bmesh,
                                                  name='%s Graph' % 'Example')

    return graph_mesh


####################################################################################################
# @construct_branching_connectivity_using_simplified_edges_four
####################################################################################################
def construct_branching_connectivity_using_simplified_edges_four(morphology):
    for i, i_section in enumerate(morphology.sections_list):
        i_section.index = i

    edge_sections_list = list()
    for i, i_section in enumerate(morphology.sections_list):
        edge_sections_list.extend(i_section.construct_four_edges_sections(index=i))

    import vmv.bmeshi

    # Create a new bmesh object to construct the graph of the simplified morphology
    simplified_morphology_graph_bmesh = vmv.bmeshi.create_bmesh_object()

    # Construct the vertices of the bmesh object
    for i_section in edge_sections_list:

        # Add the first sample of the edge (first sample of the actual section)
        vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
            simplified_morphology_graph_bmesh, i_section.sample_1)

        # Add the second sample of the edge (last sample of the actual section)
        vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
            simplified_morphology_graph_bmesh, i_section.sample_2)

    # Update the lookup table of the vertices to be able to add the edges
    simplified_morphology_graph_bmesh.verts.ensure_lookup_table()

    # Construct the edges of the bmesh object
    vertex_index = 0
    for i in range(len(edge_sections_list)):
        v1 = simplified_morphology_graph_bmesh.verts[vertex_index]
        v2 = simplified_morphology_graph_bmesh.verts[vertex_index + 1]
        simplified_morphology_graph_bmesh.edges.new((v1, v2))
        vertex_index += 2

    # Update the lookup table of the edges to be able to use the bmesh (indexing operations)
    simplified_morphology_graph_bmesh.edges.ensure_lookup_table()

    bmesh.ops.remove_doubles(simplified_morphology_graph_bmesh,
                             verts=simplified_morphology_graph_bmesh.verts,
                             dist=0.00001)

    # Convert the bmesh to a mesh
    import vmv.bmeshi
    graph_mesh = vmv.bmeshi.convert_bmesh_to_mesh(
        bmesh_object=simplified_morphology_graph_bmesh,
        name='%s Graph' % 'Example')

    # draw the sections
    bevel = vmv.mesh.create_bezier_circle(vertices=8, name='B1')

    import vmv.geometry
    for i, i_section in enumerate(morphology.sections_list):
        data = [vmv.skeleton.ops.get_color_coded_section_poly_line_with_single_color(
            section=i_section)]

        skeleton = vmv.geometry.create_poly_lines_object_from_poly_lines_data(
            poly_lines_data=data,
            name='Section %d' % i_section.index, bevel_object=bevel,
            poly_line_type='POLY')


####################################################################################################
# @get_number_components_in_graph
####################################################################################################
def get_number_components_in_graph(morphology):

    # Create the bmesh object
    bmesh_object = vmv.bmeshi.create_bmesh_object()

    # Build the graph bmesh from the sections
    for i_section in morphology.sections_list:

        # The section must have at least two samples to be considered
        if len(i_section.samples) < 2:
            continue

        # Add the corresponding vertex of the first sample of the section
        vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
            bmesh_object, i_section.samples[0].point)

        # Add the vertices of the rest of samples
        for j in range(1, len(i_section.samples)):
            vmv.bmeshi.add_vertex_to_bmesh_without_lookup(
                bmesh_object, i_section.samples[j].point)

    # Update the geometry of the bmesh to be able to query it
    bmesh_object.verts.ensure_lookup_table()

    # Construct the edges
    vertex_index = 0
    for i_section in morphology.sections_list:
        for j in range(0, len(i_section.samples) - 1):
            v1 = bmesh_object.verts[j + vertex_index]
            v2 = bmesh_object.verts[j + vertex_index + 1]
            bmesh_object.edges.new((v1, v2))
        vertex_index += len(i_section.samples)

    # Convert the bmesh to a mesh
    mesh = vmv.bmeshi.convert_bmesh_to_mesh(bmesh_object=bmesh_object, name='Graph')
    vmv.scene.set_active_object(mesh)

    # The graph mesh must be active
    vmv.scene.set_active_object(mesh)

    # Remove the duplicate vertices from the graph
    vmv.mesh.remove_doubles(mesh_object=mesh, distance=0.00001)

    # The graph mesh must be active
    vmv.scene.set_active_object(mesh)

    # Separate the graph mesh into partitions
    vmv.bops.separate_mesh_partitions()

    # Get a list of all the graph partitions meshes
    graph_partitions = vmv.scene.get_list_of_objects_containing_string('Graph')

    # Store the number of components
    number_components = copy.deepcopy(len(graph_partitions))

    # Delete all the objects in the scene
    vmv.scene.delete_list_objects(graph_partitions)

    # Return the result
    return number_components
