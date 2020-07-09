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

# Blender imports
import bpy

# Morphology file
bpy.types.Scene.MorphologyFile = bpy.props.StringProperty(
    name="Morphology File",
    description="Select a specific vasculature morphology to load",
    default='Select File', maxlen=2048,  subtype='FILE_PATH')

# Morphology directory
bpy.types.Scene.MorphologyDirectory = bpy.props.StringProperty(
    name="Morphology Directory",
    description="Select a directory to mesh all the morphologies in it",
    default="Select Directory", maxlen=2048, subtype='DIR_PATH')

# Output directory
bpy.types.Scene.OutputDirectory = bpy.props.StringProperty(
    name="Output Directory",
    description="Select a directory where the results will be generated",
    default="Select Directory", maxlen=2048, subtype='DIR_PATH')

# Use default paths for the artifacts
bpy.types.Scene.DefaultArtifactsRelativePath = bpy.props.BoolProperty(
    name="Use Default Output Hierarchy",
    description="Use the default sub-paths for the artifacts",
    default=True)

# Images relative path
bpy.types.Scene.ImagesPath = bpy.props.StringProperty(
    name="Images",
    description="Relative path where the images will be generated",
    default="images", maxlen=1000)

# Sequences relative path
bpy.types.Scene.SequencesPath = bpy.props.StringProperty(
    name="Sequences",
    description="Relative path where the sequences will be generated",
    default="sequences", maxlen=1000)

# Meshes relative path
bpy.types.Scene.MeshesPath = bpy.props.StringProperty(
    name="Meshes",
    description="Relative path where the sequences will be generated",
    default="meshes", maxlen=1000)

# Morphologies relative path
bpy.types.Scene.MorphologiesPath = bpy.props.StringProperty(
    name="Morphologies",
    description="Relative path where the morphologies will be generated",
    default="morphologies", maxlen=1000)

# Analysis relative path
bpy.types.Scene.AnalysisPath = bpy.props.StringProperty(
    name="Analysis",
    description="Relative path where the analysis reports will be generated",
    default="analysis", maxlen=1000)

# Center the loaded morphology at the origin
bpy.types.Scene.CenterMorphologyAtOrigin = bpy.props.BoolProperty(
    name="Center At Origin",
    description="Center the loaded morphology at the origin",
    default=True)

# Center the loaded morphology at the origin
bpy.types.Scene.ResampleMorphology = bpy.props.BoolProperty(
    name="Resample Morphology",
    description="Resample the morphology skeleton remove unwanted samples",
    default=False)

# Loading time
bpy.types.Scene.MorphologyLoadingTime = bpy.props.FloatProperty(
    name="Loading Morphology (Sec)",
    description="The time it takes to load the vasculature morphology from file",
    default=0, min=0, max=1000000)

# Drawing time
bpy.types.Scene.MorphologyDrawingTime = bpy.props.FloatProperty(
    name="Drawing Morphology (Sec)",
    description="The time it takes to draw the loaded vasculature morphology",
    default=0, min=0, max=1000000)
