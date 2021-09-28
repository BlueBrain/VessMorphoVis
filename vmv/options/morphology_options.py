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

# Internal imports
import vmv
import vmv.consts
import vmv.enums


####################################################################################################
# @MorphologyOptions
####################################################################################################
class MorphologyOptions:
    """Configuration options for reconstructing a morphology skeleton.
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Morphology file path
        self.file_path = None

        # Morphology file name
        self.file_name = None

        # Morphology label, based on the morphology file name
        self.label = None

        # The visualization type requested by the user
        self.visualization_type = vmv.enums.Morphology.Visualization.STRUCTURE

        # The method used to build the morphology skeleton object in the scene from the raw file
        self.builder = vmv.enums.Morphology.Builder.SECTIONS

        # Skeleton style, ORIGINAL by default
        self.skeleton = vmv.enums.Morphology.Style.ORIGINAL

        # The radii of the sections (as specified in the morphology file, scaled with a given
        # scale factor, or constant at given fixed value)
        self.radii = vmv.enums.Morphology.Radii.AS_SPECIFIED

        # A scale factor for the radii of the sections
        self.sections_radii_scale = 1.0

        # A fixed and unified value for the radii of all the sections in the morphology
        self.sections_fixed_radii_value = 1.0

        # The minimum radius of the samples
        self.sections_radii_minimum = 0.5

        # Threshold radius, where any section with lower radius values will not drawn
        self.threshold_radius = vmv.consts.Math.INFINITY

        # Load the morphology at the global coordinates, otherwise center it at the origin
        self.global_coordinates = False

        # Adaptive resampling of the sections to reduce the number of samples
        self.adaptive_resampling = False

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = vmv.consts.Bevel.BEVEL_OBJECT_SIDES

        # Morphology material
        self.material = vmv.enums.Shader.LAMBERT_WARD

        # Color coding scheme 
        self.color_coding = vmv.enums.ColorCoding.DEFAULT

        # Render scale bar to the image, ONLY in case of ORTHOGRAPHIC projection
        self.render_scale_bar = False

        # Load the morphology at the global coordinates, otherwise center it at the origin
        self.global_coordinates = False

        # Adaptive resampling of the sections to reduce the number of samples
        self.adaptive_resampling = False

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = vmv.consts.Bevel.BEVEL_OBJECT_SIDES

        # Morphology material
        self.material = vmv.enums.Shader.LAMBERT_WARD

        # Color coding scheme
        self.color_coding = vmv.enums.ColorCoding.DEFAULT

        # Render scale bar to the image, ONLY in case of ORTHOGRAPHIC projection
        self.render_scale_bar = False

        # Set a transparent background for the rendered image
        self.transparent_background = True

        # Morphology color-map name (this is probably loaded from the CLI)
        self.color_map = vmv.enums.ColorMaps.PLASMA

        # The resolution of the colormap (number of samples)
        self.color_map_resolution = vmv.consts.Color.COLORMAP_RESOLUTION

        # Morphology color-map colors (this is probably set from the GUI)
        self.color_map_colors = list()

        # Base morphology color
        self.color = vmv.consts.Color.LIGHT_RED_COLOR

        # Alternating morphology color (use for ALTERNATING_COLORS schemes)
        self.alternating_color = vmv.consts.Color.BLACK

        # SKELETON RENDERING #######################################################################
        # Camera view
        self.camera_view = vmv.enums.Rendering.View.FRONT

        # Camera projection
        self.camera_projection = vmv.enums.Rendering.Projection.ORTHOGRAPHIC

        # Image resolution is based on scale or to a fixed resolution
        self.resolution_basis = vmv.enums.Rendering.Resolution.FIXED_RESOLUTION

        # Render a static frame of the skeleton
        self.render = False

        # Render a 360 sequence of the reconstructed skeleton
        self.render_360 = False

        # The scale factor used to scale the morphology rendering frame, default 1.0
        self.resolution_scale_factor = 1.0

        # Export the morphology to .H5 file
        self.export_h5 = False

        # Export the morphology skeleton to .BLEND file for rendering using tubes
        self.export_blend = False
