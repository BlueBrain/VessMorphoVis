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
# @Rendering
####################################################################################################
class Rendering:
    """Rendering enumerators
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
        """Camera view enumerator
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        # Front view
        FRONT = 'FRONT'

        # Side view
        SIDE = 'SIDE'

        # Top view
        TOP = 'TOP'

        # 360
        FRONT_360 = 'FRONT_360_VIEW'

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Front
            if argument == 'front':
                return Rendering.View.FRONT

            # Side
            elif argument == 'side':
                return Rendering.View.SIDE

            # Top
            elif argument == 'top':
                return Rendering.View.TOP

            # 360 from front view
            elif argument == '360':
                return Rendering.View.FRONT_360

            # By default, use the front view
            else:
                return Rendering.View.FRONT

    ################################################################################################
    # @Projection
    ################################################################################################
    class Projection:
        """Camera projection enumerator
        """

        ############################################################################################
        # @__init__
        ############################################################################################
        def __init__(self):
            pass

        # Orthographic
        ORTHOGRAPHIC = 'ORTHOGRAPHIC_VIEW'

        # Perspective
        PERSPECTIVE = 'PERSPECTIVE_VIEW'

        ############################################################################################
        # @get_enum
        ############################################################################################
        @staticmethod
        def get_enum(argument):

            # Orthographic
            if argument == 'orthographic':
                return Rendering.Projection.ORTHOGRAPHIC

            # Perspective
            elif argument == 'perspective':
                return Rendering.Projection.PERSPECTIVE

            # By default, use orthographic
            else:
                return Rendering.Projection.ORTHOGRAPHIC

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

