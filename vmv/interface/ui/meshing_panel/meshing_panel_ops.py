####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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
import vmv.interface


####################################################################################################
# @add_color_options
####################################################################################################
def add_color_options(layout,
                      scene,
                      options):
    """Adds the color options to the user interface.

    :param layout:
        Panel layout.
    :param scene:
        Context scene.
    :param options:
        System options.
    """

    # Coloring parameters
    title_row = layout.row()
    title_row.label(text='Colors & Shaders:', icon='COLOR')

    # Mesh shader
    material_row = layout.row()
    material_row.prop(scene, 'VMV_MeshShader')
    options.mesh.material = scene.VMV_MeshShader

    # Mesh color
    color_row = layout.row()
    color_row.prop(scene, 'VMV_MeshColor')
    options.mesh.color = scene.VMV_MeshColor
