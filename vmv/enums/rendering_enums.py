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


####################################################################################################
# @Rendering
####################################################################################################
class Rendering:
    """Rendering options
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    ################################################################################################
    # @View
    ################################################################################################
    class View:
        """Rendering view options
        """

        # Front view
        FRONT_VIEW = 'RENDERING_FRONT_VIEW'

        # Side view
        SIDE_VIEW = 'RENDERING_SIDE_VIEW'

        # Top view
        TOP_VIEW = 'RENDERING_TOP_VIEW'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Front view
            if argument == 'front':
                return Rendering.View.FRONT_VIEW

            # Side view
            elif argument == 'side':
                return Rendering.View.SIDE_VIEW

            # Top view
            elif argument == 'top':
                return Rendering.View.TOP_VIEW

            # By default use the front view
            else:
                return Rendering.View.FRONT_VIEW

    ################################################################################################
    # @Resolution
    ################################################################################################
    class Resolution:
        """Rendering resolution options
        """

        # Rendering to scale (for figures)
        TO_SCALE = 'RENDER_TO_SCALE'

        # Rendering based on a user defined resolution
        FIXED_RESOLUTION = 'RENDER_AT_FIXED_RESOLUTION'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # To scale
            if argument == 'to-scale':
                return Rendering.Resolution.TO_SCALE

            # Fixed resolution
            elif argument == 'fixed':
                return Rendering.Resolution.FIXED_RESOLUTION

            # By default render at the specified resolution
            else:
                return Rendering.Resolution.FIXED_RESOLUTION

    ################################################################################################
    # @Projection
    ################################################################################################
    class Projection:
        """Rendering projection options
        """

        # Orthographic
        ORTHOGRAPHIC = 'RENDER_ORTHOGRAPHIC'

        # Perspective
        PERSPECTIVE = 'RENDER_PERSPECTIVE'

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # To scale
            if argument == 'orthographic':
                return Rendering.Projection.ORTHOGRAPHIC

            # Fixed resolution
            elif argument == 'perspective':
                return Rendering.Projection.PERSPECTIVE

            # By default render orthographic images
            else:
                return Rendering.Projection.ORTHOGRAPHIC

