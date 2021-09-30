####################################################################################################
# Copyright (c) 2019 - 2021, EPFL / Blue Brain Project
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

# Blender imports
import bpy

# Input ############################################################################################
# Morphology file
bpy.types.Scene.VMV_MorphologyFile = bpy.props.StringProperty(
    name='Morphology File',
    description='Select a specific vasculature morphology to load',
    default='Select File', maxlen=2048,  subtype='FILE_PATH')

# Center the loaded morphology at the origin
bpy.types.Scene.VMV_CenterMorphologyAtOrigin = bpy.props.BoolProperty(
    name='Center At Origin',
    description='Center the loaded morphology at the origin',
    default=True)

# Center the loaded morphology at the origin
bpy.types.Scene.VMV_ResampleMorphology = bpy.props.BoolProperty(
    name='Resample Morphology',
    description='Resample the morphology to remove unwanted samples',
    default=False)

# Output ###########################################################################################
# Output directory
bpy.types.Scene.VMV_OutputDirectory = bpy.props.StringProperty(
    name='Output Directory',
    description='Select a directory where the results will be generated',
    default='Select Directory', maxlen=2048, subtype='DIR_PATH')

# Use default paths for the artifacts
bpy.types.Scene.VMV_DefaultArtifactsRelativePath = bpy.props.BoolProperty(
    name='Use Default Output Hierarchy',
    description='Use the default sub-paths for the artifacts',
    default=True)

# Images relative path
bpy.types.Scene.VMV_ImagesPath = bpy.props.StringProperty(
    name='Images',
    description='Relative path where the images will be generated',
    default='images', maxlen=1000)

# Sequences relative path
bpy.types.Scene.VMV_SequencesPath = bpy.props.StringProperty(
    name='Sequences',
    description='Relative path where the sequences will be generated',
    default='sequences', maxlen=1000)

# Meshes relative path
bpy.types.Scene.VMV_MeshesPath = bpy.props.StringProperty(
    name='Meshes',
    description='Relative path where the sequences will be generated',
    default='meshes', maxlen=1000)

# Morphologies relative path
bpy.types.Scene.VMV_MorphologiesPath = bpy.props.StringProperty(
    name='Morphologies',
    description='Relative path where the morphologies will be generated',
    default='morphologies', maxlen=1000)

# Analysis relative path
bpy.types.Scene.VMV_AnalysisPath = bpy.props.StringProperty(
    name='Analysis',
    description='Relative path where the analysis reports will be generated',
    default='analysis', maxlen=1000)

# File summary #####################################################################################
# File name
bpy.types.Scene.VMV_MorphologyName = bpy.props.StringProperty(
    name='File',
    description='The name of the morphology file as located on the file system',
    default='', maxlen=1000)

# Number of samples in the morphology
bpy.types.Scene.VMV_NumberMorphologySamples = bpy.props.IntProperty(
    name='Number of Samples',
    description='The total number of samples (or vertices) in the loaded morphology',
    default=0, min=0, max=100000000)

# Number of sections in the morphology
bpy.types.Scene.VMV_NumberMorphologySections = bpy.props.IntProperty(
    name='Number of Sections',
    description='The total number of sections (or strands) in the loaded morphology',
    default=0, min=0, max=100000000)

# Simulations ######################################################################################
# Radius variations
bpy.types.Scene.VMV_RadiusVariationsSteps = bpy.props.IntProperty(
    name='Radius Variations',
    description='Number of steps for radius variations. If this value is zero, this means that '
                'the file does not contain any radius variations',
    default=0, min=0, max=1000000)

# Flow variations
bpy.types.Scene.VMV_FlowVariationsSteps = bpy.props.IntProperty(
    name='Flow Variations',
    description='Number of steps for flow variations. If this value is zero, this means that '
                'the file does not contain any flow variations or simulations',
    default=0, min=0, max=1000000)

# Pressure variations
bpy.types.Scene.VMV_PressureVariationsSteps = bpy.props.IntProperty(
    name='Pressure Variations',
    description='Number of steps for pressure variations. If this value is zero, this means that '
                'the file does not contain any pressure variations or simulations',
    default=0, min=0, max=1000000)

# Stats. ###########################################################################################
# Loading time
bpy.types.Scene.VMV_MorphologyLoadingTime = bpy.props.FloatProperty(
    name='Loading Morphology (Sec)',
    description='The time it takes to load the vasculature morphology from file',
    default=0, min=0, max=1000000)

# Drawing time
bpy.types.Scene.VMV_MorphologyDrawingTime = bpy.props.FloatProperty(
    name='Drawing Morphology (Sec)',
    description='The time it takes to draw the loaded vasculature morphology',
    default=0, min=0, max=1000000)
