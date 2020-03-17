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
# @Shading
####################################################################################################
class Shading:
    """Shading enumerators
    """

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        pass

    # Glossy shader, for workbench renderer
    GLOSSY_WORKBENCH = 'GLOSSY_SHADER'

    # Matte shader, for workbench renderer
    MATTE_WORKBENCH = 'MATTE_SHADER'

    # Flat or 'shade-less' shader, for cycles renderer
    FLAT_CYCLES = 'FLAT_SHADER'

    # Electron microscopy shader, for cycles renderer
    ELECTRON_CYCLES = 'ELECTRON_SHADER'

    # Artistic glossy shader, for cycles renderer
    ARTISTIC_GLOSSY_CYCLES = 'ARTISTIC_GLOSSY_SHADER'

    # Glossy bympy shader
    ARTISTIC_BUMPY_CYCLES = 'ARTISTIC_BUMPY_SHADER'



    # Toon shader, for cycles
    TOON = 'TOON_SHADER'





    # Glossy shader
    GLOSSY = 'GLOSSY_SHADER'





    # Electron (dark) shader
    ELECTRON_DARK = 'ELECTRON_DARK_SHADER'

    # Super resolution electron (light) shader
    SUPER_ELECTRON_LIGHT = 'SUPER_ELECTRON_LIGHT_SHADER'

    # Super resolution electron (dark) shader
    SUPER_ELECTRON_DARK = 'SUPER_ELECTRON_DARK_SHADER'

    # Sub-surface scattering shader
    SUB_SURFACE_SCATTERING = 'SUB_SURFACE_SCATTERING_SHADER'

    # Shadow
    SHADOW = 'SHADOW_SHADER'

    # Plastic
    PLASTIC = 'PLASTIC_SHADER'

    # Cracks
    CRACKS = 'CRACKS_SHADER'

    # Grid
    GRID = 'GRID_SHADER'

    # Granular
    GRANULAR = 'GRANULAR_SHADER'

    # Wave
    WAVE = 'WAVE_SHADER'

    # Voronoi
    VORONOI = 'VORONOI_SHADER'

    # Ceramic
    CERAMIC = 'CERAMIC_SHADER'

    # Skin
    SKIN = 'SKIN_SHADER'

    ################################################################################################
    # get_enum
    ################################################################################################
    @staticmethod
    def get_enum(shader_type):
        """Return the shader enumerator from the type

        :param shader_type:
            The type of the shader.create_poly_lines_object
        :return:
            The shader enumerator.
        """
        if shader_type == 'glossy':
            return Shading.GLOSSY_WORKBENCH
        if shader_type == 'matte':
            return Shading.MATTE_WORKBENCH
        elif shader_type == 'flat':
            return Shading.FLAT_CYCLES
        elif shader_type == 'electron':
            return Shading.ELECTRON_CYCLES
        elif shader_type == 'artistic-glossy':
            return Shading.ARTISTIC_GLOSSY_CYCLES
        elif shader_type == 'artistic-bumpy':
            return Shading.ARTISTIC_BUMPY_CYCLES


        elif shader_type == 'electron-dark':
            return Shading.ELECTRON_DARK
        elif shader_type == 'super-electron-light':
            return Shading.SUPER_ELECTRON_LIGHT
        elif shader_type == 'super-electron-dark':
            return Shading.SUPER_ELECTRON_DARK
        elif shader_type == 'shadow':
            return Shading.SHADOW
        elif shader_type == 'glossy':
            return Shading.GLOSSY

        elif shader_type == 'plastic':
            return Shading.PLASTIC
        elif shader_type == 'cracks':
            return Shading.CRACKS
        elif shader_type == 'grid':
            return Shading.GRID
        elif shader_type == 'granular':
            return Shading.GRANULAR
        elif shader_type == 'wave':
            return Shading.WAVE
        elif shader_type == 'voroni':
            return Shading.VORONOI
        elif shader_type == 'ceramic':
            return Shading.CERAMIC
        elif shader_type == 'skin':
            return Shading.SKIN
        else:
            return Shading.GLOSSY_WORKBENCH

    ################################################################################################
    # A list of all the available materials
    ################################################################################################
    MATERIAL_ITEMS = [
        (GLOSSY_WORKBENCH,
         'Glossy',
         "Apply a glossy and specular shader to the surface of the reconstructed data"),

        (MATTE_WORKBENCH,
         'Matte',
         "Apply a matte shader to the surface of the reconstructed data"),

        (FLAT_CYCLES,
         'Flat',
         "Apply a flat shader to the surface of the reconstructed data, where it looks like "
         "an emitting surface. Note the the depth information cannot be revealed"),

        (ELECTRON_CYCLES,
         'Electron Microscope',
         "Apply an EM shader to the surface of the data, as appears under the electron microscope"),

        (ARTISTIC_GLOSSY_CYCLES,
         'Artistic Glossy',
         "Apply an artistic glossy shader to the surface of the data and render with high quality "
         "Cycles renderer. "
         "Note that the rendering time will be quite high when you use this material"),

        (ARTISTIC_BUMPY_CYCLES,
         'Artistic Bumpy',
         "Apply an artistic bumpy shader to the surface of the data and render with high quality "
         "Cycles renderer. "
         "Note that the rendering time will be quite high when you use this material"),
    ]

    ################################################################################################
    # A list of the artistic materials that can be used to render high quality images
    ################################################################################################
    ARTISTIC_MATERIALS = [
        ARTISTIC_GLOSSY_CYCLES,
        ARTISTIC_BUMPY_CYCLES,
        SKIN
    ]
