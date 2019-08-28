####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2019, Blue Brain Project / EPFL"
__credits__     = ["Juan Hernando"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


bl_info = {
    "name": "VessMorphoVis",
    "author": "Marwan Abdellah",
    "version": (1, 2, 0),
    "blender": (2, 80, 0),
    "location": "Properties > Material",
    "description": "Allows managing UI translations directly from Blender "
        "(update main .po files, update scripts' translations, etc.)",
    "warning": "Still in development, not all features are fully implemented yet!",
    "wiki_url": "http://wiki.blender.org/index.php/Dev:Doc/How_to/Translate_Blender",
    "support": 'OFFICIAL',
    "category": "System"}


# System imports
import sys
import os
import imp

# Append the modules path to the system paths to be able to load the internal python modules
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

if "bpy" in locals():

    # Import the modules
    import vmv.interface.ui.io_panel
    import vmv.interface.ui.analysis_panel
    import vmv.interface.ui.morphology_panel
    import vmv.interface.ui.meshing_panel

    # Reloading the modules
    imp.reload(vmv.interface.ui.io_panel)
    imp.reload(vmv.interface.ui.analysis_panel)
    imp.reload(vmv.interface.ui.morphology_panel)
    imp.reload(vmv.interface.ui.meshing_panel)

else:

    # Import the modules
    import vmv.interface.ui.io_panel
    import vmv.interface.ui.analysis_panel
    import vmv.interface.ui.morphology_panel
    import vmv.interface.ui.meshing_panel


####################################################################################################
# @register
####################################################################################################
def register():
    """Register the different modules of the interface.
    """

    # Register panels
    vmv.interface.ui.io_panel.register_panel()
    vmv.interface.ui.analysis_panel.register_panel()
    vmv.interface.ui.morphology_panel.register_panel()
    vmv.interface.ui.meshing_panel.register_panel()


####################################################################################################
# @unregister
####################################################################################################
def unregister():
    """Unregister the different modules of the interface.
    """

    # Un-register panels
    vmv.interface.ui.io_panel.unregister_panel()
    vmv.interface.ui.analysis_panel.unregister_panel()
    vmv.interface.ui.morphology_panel.unregister_panel()
    vmv.interface.ui.meshing_panel.unregister_panel()


####################################################################################################
# __main__
####################################################################################################
if __name__ == "__main__":

    # Register the add-on
    register()




