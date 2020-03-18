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


####################################################################################################
# @Args
####################################################################################################
class Args:
    """System arguments
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # Blender arguments
    ################################################################################################
    # Executable
    BLENDER_EXECUTABLE = '--blender'

    ################################################################################################
    # Input arguments
    ################################################################################################
    # What is the input source to the workflow
    INPUT_SOURCE = '--input'

    # A single morphology file
    MORPHOLOGY_FILE = '--morphology-file'

    # A directory containing a group of morphology files
    MORPHOLOGY_DIRECTORY = '--morphology-directory'

    ################################################################################################
    # Output arguments
    ################################################################################################
    # The root output directory
    OUTPUT_DIRECTORY = '--output-directory'

    ################################################################################################
    # Analysis arguments
    ################################################################################################
    # Analyze morphology
    ANALYZE_MORPHOLOGY = '--analyze-morphology'

    ################################################################################################
    # Morphology arguments
    ################################################################################################
    # Reconstruct the morphology skeleton
    RECONSTRUCT_MORPHOLOGY_SKELETON = '--reconstruct-morphology-skeleton'

    # Morphology reconstruction algorithm
    MORPHOLOGY_RECONSTRUCTION_ALGORITHM = '--morphology-reconstruction-algorithm'

    # Morphology skeleton style
    MORPHOLOGY_SKELETON = '--morphology-skeleton'

    # Sections radii
    SECTIONS_RADII = '--sections-radii'

    # Radii scale factor
    RADII_SCALE_FACTOR = '--radii-scale-factor'

    # Radii fixed section
    FIXED_SECTION_RADIUS = '--fixed-section-radius'

    # Minimum section radius
    MINIMUM_SECTION_RADIUS = '--minimum-section-radius'

    # Morphology bevel object sides
    MORPHOLOGY_BEVEL_SIDES = '--bevel-sides'

    ################################################################################################
    # Materials and colors arguments
    ################################################################################################

    # Morphology color
    MORPHOLOGY_COLOR = '--morphology-color'

    # Mesh color
    MESH_COLOR = '--mesh-color'

    # Shader
    SHADER = '--shader'

    ################################################################################################
    # Meshing arguments
    ################################################################################################
    # Reconstruct vascular mesh
    RECONSTRUCT_VASCULAR_MESH = '--reconstruct-vascular-mesh'

    # Vascular meshing algorithm
    NEURON_MESHING_ALGORITHM = '--meshing-algorithm'

    # Mesh edges
    MESH_EDGES = '--edges'

    # Mesh surface
    MESH_SURFACE = '--surface'

    # Mesh tessellation level
    MESH_TESSELLATION_LEVEL = '--tessellation-level'

    # MetaBalls resolution setting
    META_BALLS_RESOLUTION_SETTING = '--meta-balls-resolution-setting'

    # MetaBalls resolution value
    META_BALLS_RESOLUTION = '--meta-balls-resolution'

    ################################################################################################
    # Geometry export arguments
    ################################################################################################
    # Export morphology .SWC
    EXPORT_VMV_MORPHOLOGY = '--export-morphology-vmv'

    # Export .H5 morphology
    EXPORT_H5_MORPHOLOGY = '--export-morphology-h5'

    # Export .BLEND morphology
    EXPORT_BLEND_MORPHOLOGY = '--export-morphology-blend'

    # Export the vascular mesh as .PLY
    EXPORT_PLY_MESH = '--export-vascular-mesh-ply'

    # Export the vascular mesh as .OBJ
    EXPORT_OBJ_MESH = '--export-vascular-mesh-obj'

    # Export the vascular mesh as .STL
    EXPORT_STL_MESH = '--export-vascular-mesh-stl'

    # Export the vascular mesh as .BLEND
    EXPORT_BLEND_MESH = '--export-vascular-mesh-blend'

    # Export each part of the vascular mesh as a separate file for tagging
    EXPORT_INDIVIDUALS = '--export-individuals'

    ################################################################################################
    # Rendering arguments
    ################################################################################################
    # Render a static image of the vascular morphology skeleton
    RENDER_VASCULAR_MORPHOLOGY = '--render-vascular-morphology'

    # Render a 360 sequence of the vascular morphology skeleton
    RENDER_VASCULAR_MORPHOLOGY_360 = '--render-vascular-morphology-360'

    # Render a static image of the reconstructed vascular mesh
    RENDER_VASCULAR_MESH = '--render-vascular-mesh'

    # Render a 360 sequence of the reconstructed vascular mesh
    RENDER_VASCULAR_MESH_360 = '--render-vascular-mesh-360'

    # Rendering an image to scale
    RENDER_TO_SCALE = '--render-to-scale'

    # The part of the skeleton that will be rendered
    RENDERING_VIEW = '--rendering-view'

    # The view or the direction of the camera
    CAMERA_VIEW = '--camera-view'

    # The projection or the camera
    CAMERA_PROJECTION = '--camera-projection'

    # The resolution of full-view (mid-shot or wide-shot) images
    FULL_VIEW_RESOLUTION = '--full-view-resolution'

    # Scale factor for increasing the resolution of the to-scale images
    RESOLUTION_SCALE_FACTOR = '--resolution-scale-factor'

    ################################################################################################
    # Execution arguments
    ################################################################################################
    # Execution node
    EXECUTION_NODE = '--execution-node'

    # Number of core to run the frame work
    NUMBER_CORES = '--number-cores'

    # Job granularity
    JOB_GRANULARITY = '--job-granularity'
