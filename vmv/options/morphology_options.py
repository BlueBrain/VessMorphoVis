####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
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
        self.morphology_file_path = None

        # Morphology file name
        self.morphology_file_name = None

        # Morphology label (based on the morphology file name)
        self.label = None

        # Skeletonization style, ORIGINAL by default
        self.skeleton = vmv.enums.Skeletonization.Style.ORIGINAL

        # Branching of the morphologies in the connected modes, either based on angles or radii
        self.branching = vmv.enums.Skeletonization.Branching.ANGLES

        # Color
        self.color = vmv.consts.Color.GRAY

        # The radii of the sections (as specified in the morphology file, scaled with a given
        # scale factor, or constant at given fixed value)
        self.radii = vmv.enums.Skeletonization.Radii.AS_SPECIFIED

        # A scale factor for the radii of the sections
        self.sections_radii_scale = 1.0

        # A fixed and unified value for the radii of all the sections in the morphology
        self.sections_fixed_radii_value = 1.0

        # Threshold radius, where any section with lower radius values will not drawn
        self.threshold_radius = vmv.consts.Math.INFINITY

        # Global coordinates
        self.global_coordinates = False

        # Adaptive resampling of the sections to reduce the number of samples
        self.adaptive_resampling = False

        # Number of sides of the bevel object used to scale the sections
        # This parameter controls the quality of the reconstructed morphology
        self.bevel_object_sides = vmv.consts.Bevel.BEVEL_OBJECT_SIDES

        # Selected a method to reconstruct the morphology
        self.reconstruction_method = vmv.enums.Skeletonization.Method.CONNECTED_SECTIONS

        # Morphology material
        self.material = vmv.enums.Shading.LAMBERT_WARD

        # SKELETON RENDERING #######################################################################
        # Camera view
        self.camera_view = vmv.enums.Camera.View.FRONT

        # Image resolution is based on scale or to a fixed resolution
        self.resolution_basis = vmv.enums.Skeletonization.Rendering.Resolution.FIXED_RESOLUTION

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
