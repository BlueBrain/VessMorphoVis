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

# System imports
import sys
import os
import subprocess

# Blender imports
import bpy
import bpy.utils.previews

# Internal imports
import vmv
import vmv.enums
import vmv.interface
import vmv.utilities

vmv_icons = None


####################################################################################################
# @IOPanel
####################################################################################################
class VMV_AboutPanel(bpy.types.Panel):
    """VMV About Us panel"""

    ################################################################################################
    # Panel parameters
    ################################################################################################
    bl_label = 'About'
    bl_idname = "OBJECT_PT_VMV_About"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = 'VessMorphoVis'
    bl_options = {'DEFAULT_CLOSED'}

    ################################################################################################
    # @draw
    ################################################################################################
    def draw(self,
             context):
        """Draw the panel.

        :param context:
            Blender context.
        """

        # Get a reference to the panel layout
        layout = self.layout

        # Credits
        credits_column = layout.column()
        credits_column.label(text='Copyrights (c)')
        credits_column.label(text='Blue Brain Project (BBP)', icon='PMARKER')
        credits_column.label(text='Ecole Polytechnique Federale de Lausanne (EPFL)', icon='PMARKER')
        credits_column.separator()

        credits_column.label(text='License')
        credits_column.label(text='GPL', icon='UNLOCKED')
        credits_column.separator()

        credits_column.label(text='Main Author')
        credits_column.label(text='Marwan Abdellah', icon='OUTLINER_DATA_ARMATURE')
        credits_column.separator()
        credits_column.label(text='Advisors')
        credits_column.label(text='Samuel Lapere', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Henry Markram', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Felix Schürmann', icon='OUTLINER_DATA_ARMATURE')
        credits_column.separator()
        credits_column.label(text='Credits')
        credits_column.label(text='Nadir Román Guerrero', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Caitlin Monney', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Pablo Blinder', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Stéphanie Battini', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Alexis Arnaudon', icon='OUTLINER_DATA_ARMATURE')
        credits_column.label(text='Eleftherios Zisis', icon='OUTLINER_DATA_ARMATURE')
        credits_column.separator()

        # Version
        version_column = layout.column()
        version = vmv.utilities.get_vmv_version()
        version_column.label(text='Version: %d.%d.%d' % (version[0], version[1], version[2]))

        update_button = layout.column()
        update_button.operator('update.nmv', emboss=True, icon='NODETREE')
        update_button.operator('open.github', emboss=True, icon='SCRIPT')
        update_button.operator('open.wiki', emboss=True, icon='URL')


####################################################################################################
# @VMV_OpenDocumentation
####################################################################################################
class VMV_OpenDocumentation(bpy.types.Operator):
    """Open the Github repository page"""

    # Operator parameters
    bl_idname = "open.wiki"
    bl_label = "Documentation"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/VessMorphoVis/wiki')
        return {'FINISHED'}


####################################################################################################
# @VMV_OpenRepository
####################################################################################################
class VMV_OpenRepository(bpy.types.Operator):
    """Open the Github repository page"""

    # Operator parameters
    bl_idname = "open.github"
    bl_label = "Code"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        import webbrowser
        webbrowser.open('https://github.com/BlueBrain/VessMorphoVis')
        return {'FINISHED'}


####################################################################################################
# @VMV_UpdateVessMorphoVis
####################################################################################################
class VMV_UpdateVessMorphoVis(bpy.types.Operator):
    """Update VessMorphoVis"""

    # Operator parameters
    bl_idname = "update.nmv"
    bl_label = "Update"

    ################################################################################################
    # @execute
    ################################################################################################
    def execute(self,
                context):
        """Execute the operator.

        :param context:
            Blender context
        :return:
            'FINISHED'
        """

        # git must be installed to update the tool.
        if not vmv.utilities.command_exists('git'):
            self.report({'INFO'}, 'Cannot update VessMorphoVis! git must be installed.')
            return {'FINISHED'}

        # TODO: Verify git or use wget or curl.
        # TODO: Ignore this option for windows.

        # Get the current path
        current_path = os.path.dirname(os.path.realpath(__file__))

        # Go to the main directory and pull the latest master
        os.chdir(current_path)
        shell_command = 'git pull origin master'
        vmv.logger.log('Updating VessMorphoVis ...')
        subprocess.call(shell_command, shell=True)

        # Call blender and exit this one
        shell_command = '%s &' % bpy.app.binary_path
        vmv.logger.log('Restarting Blender with VessMorphoVis ...')
        subprocess.call(shell_command, shell=True)

        # Exiting blender
        exit(0)

        return {'FINISHED'}


####################################################################################################
# @register_panel
####################################################################################################
def register_panel():
    """Registers all the classes in this panel"""

    # Panel
    bpy.utils.register_class(VMV_AboutPanel)

    # Buttons
    bpy.utils.register_class(VMV_UpdateVessMorphoVis)
    bpy.utils.register_class(VMV_OpenRepository)
    bpy.utils.register_class(VMV_OpenDocumentation)


####################################################################################################
# @unregister_panel
####################################################################################################
def unregister_panel():
    """Un-registers all the classes in this panel"""

    # Panel
    bpy.utils.unregister_class(VMV_AboutPanel)

    # Buttons
    bpy.utils.unregister_class(VMV_UpdateVessMorphoVis)
    bpy.utils.unregister_class(VMV_OpenRepository)
    bpy.utils.unregister_class(VMV_OpenDocumentation)
