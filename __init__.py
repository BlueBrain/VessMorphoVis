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

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2019, Blue Brain Project / EPFL"
__credits__     = ["Juan Hernando"]
__version__     = "0.3.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"

import time

####################################################################################################
# Add-on information
####################################################################################################
bl_info = {
    # The name of your add-on. This is shown in the add-on tab in Blender's user preferences
    "name": "VessMorphoVis",
    # The main author(s) of this add-on
    "author": "Marwan Abdellah, Blue Brain Project at EPFL",
    # A tuple, containing the add-on version
    "version": (0, 3, 0),
    # The earliest Blender version this add-on will work with. If you're not sure what versions of
    # Blender this add-on is compatible with, use the version of Blender you're developing
    # the add-on with.
    "blender": (3, 5, 0),
    # Description
    "description": "Vasculature morphology reconstruction, analysis, meshing and visualization.",
    # Optional: specifies the wiki URL for an add-on.
    # This will appear in this add-on listing as "Documentation".
    'wiki_url': 'https://github.com/BlueBrain/VessMorphoVis',
    # This support can be either 'OFFICIAL', 'COMMUNITY', or 'TESTING'. 'OFFICIAL' should only be
    # used if this add-on is included with Blender.
    # (If you're not sure, don't use 'OFFICIAL'.) 'COMMUNITY' and 'TESTING' are both fine to use.
    # Note that 'TESTING' add-ons aren't shown by default in Blender's add-on list.
    "support": 'COMMUNITY',
    # Add-on category; shown on the left side of Blender's add-on list to make filtering simpler.
    # This must be one of the categories as listed in Blender's add-on tab; if it's not, it will
    # create a new category for your add-on (which may be good or bad.)
    # Don't create new categories to make your add-on stand out.
    "category": "3D View"
}

# System imports
import sys
import os
import importlib
import subprocess

# Append the modules path to the system paths to be able to load the internal python modules
sys.path.append(os.path.dirname(os.path.realpath(__file__)))


####################################################################################################
# @install_dependencies
####################################################################################################
def install_dependencies():
    """Installs the dependencies of VMV on-the-fly using the internal Python of Blender.
    """

    # Dependencies list
    pip_wheels = [['numpy', 'numpy'],
                  ['matplotlib', 'matplotlib'],
                  ['seaborn', 'seaborn'],
                  ['pandas', 'pandas'],
                  ['h5', 'h5py'],
                  ['PIL', 'Pillow']]
                  #['morphio', 'morphio']]

    # Ensuring Pipe
    shell_command = '%s -m ensurepip' % sys.executable
    subprocess.call(shell_command, shell=True)

    print("* Validating Dependencies")
    for wheel in pip_wheels:
        try:
            print("\t* Importing %s" % wheel[1])
            importlib.import_module(wheel[0])
            print("\t    * OK %s" % wheel[1])
        except ImportError:
            print("\t* Installing %s" % wheel[1])
            shell_command = '%s -m pip install %s' % (sys.executable, wheel[1])
            subprocess.call(shell_command, shell=True)


####################################################################################################
# @install_dependencies
####################################################################################################
if "bpy" in locals():

    # Install the dependencies
    install_dependencies()

    # Import the modules
    import vmv.interface.ui.io_panel
    import vmv.interface.ui.analysis_panel
    import vmv.interface.ui.morphology_panel
    import vmv.interface.ui.meshing_panel
    import vmv.interface.ui.about_panel

    # Reloading the modules

    importlib.reload(vmv.interface.ui.io_panel)
    importlib.reload(vmv.interface.ui.analysis_panel)
    importlib.reload(vmv.interface.ui.morphology_panel)
    importlib.reload(vmv.interface.ui.meshing_panel)
    importlib.reload(vmv.interface.ui.about_panel)

    vmv.logger.header('Loading VessMorphoVis')
    vmv.logger.info('Version (%s)' % str(__version__))
    vmv.logger.info('Copyrights © Blue Brain Project (BBP) - EPFL')
    vmv.logger.info('Author(s): Marwan Abdellah')

else:

    # Install the dependencies
    install_dependencies()

    # Import the modules
    import vmv.interface.ui.io_panel
    import vmv.interface.ui.analysis_panel
    import vmv.interface.ui.morphology_panel
    import vmv.interface.ui.meshing_panel
    import vmv.interface.ui.about_panel

    vmv.logger.header('Loading VessMorphoVis')
    vmv.logger.info('Version (%s)' % str(__version__))
    vmv.logger.info('Copyrights © Blue Brain Project (BBP) - EPFL')
    vmv.logger.info('Author(s): Marwan Abdellah')


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
    vmv.interface.ui.about_panel.register_panel()


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
    vmv.interface.ui.about_panel.unregister_panel()


####################################################################################################
# __main__
####################################################################################################
if __name__ == "__main__":

    # Register the add-on
    register()
