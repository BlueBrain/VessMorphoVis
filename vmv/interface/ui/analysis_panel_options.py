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

# Total morphology length
bpy.types.Scene.MorphologyTotalLength = bpy.props.FloatProperty(
    name='Total Length',
    description='The total length of the morphology skeleton',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Number of samples
bpy.types.Scene.NumberSamples = bpy.props.IntProperty(
    name='Total # Samples',
    description='The total number of samples in the morphology skeleton',
    default=0, subtype='FACTOR')

# Number of segments
bpy.types.Scene.NumberSegments = bpy.props.IntProperty(
    name='Total # Segments',
    description='The total number of segments in the morphology skeleton',
    default=0,  subtype='FACTOR')

# Number of sections
bpy.types.Scene.NumberSections = bpy.props.IntProperty(
    name='Total # Sections',
    description='The total number of sections in the morphology skeleton',
    default=0, subtype='FACTOR')

# Number of sections with two samples only
bpy.types.Scene.NumberSectionsWithTwoSamples = bpy.props.IntProperty(
    name='# Sections with 2 Samples',
    description='The number of sections that have only two samples',
    default=0, subtype='FACTOR')

# Number of loops
bpy.types.Scene.NumberLoops = bpy.props.IntProperty(
    name='Total # Loops',
    description='The total number of loops in the morphology skeleton',
    default=0, subtype='FACTOR')

# Number of components
bpy.types.Scene.NumberComponents = bpy.props.IntProperty(
    name='# Components',
    description='The number of components of separate structures in the morphology skeleton',
    default=0, subtype='FACTOR')

# Minimum sample radius
bpy.types.Scene.MinimumSampleRadius = bpy.props.FloatProperty(
    name='Min. Sample Radius',
    description='The minimum radius of the samples for the whole morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Maximum sample radius
bpy.types.Scene.MaximumSampleRadius = bpy.props.FloatProperty(
    name='Max. Sample Radius',
    description='The maximum radius of the samples for the whole morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Average sample radius
bpy.types.Scene.AverageSampleRadius = bpy.props.FloatProperty(
    name='Avg. Sample Radius',
    description='The average radius of the samples for the whole morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Minimum segment length
bpy.types.Scene.MinimumSegmentLength = bpy.props.FloatProperty(
    name='Min. Segment Length',
    description='The minimum length of the segments along the entire morphology skeleton',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Maximum segment length
bpy.types.Scene.MaximumSegmentLength = bpy.props.FloatProperty(
    name='Max. Segment Length',
    description='The maximum length of the segments along the entire morphology skeleton',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Average segment length
bpy.types.Scene.AverageSegmentLength = bpy.props.FloatProperty(
    name='Avg. Segment Length',
    description='The average length of the segments along the entire morphology skeleton',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Minimum section length
bpy.types.Scene.MinimumSectionLength = bpy.props.FloatProperty(
    name='Min. Section Length',
    description='The minimum length of the section along the entire morphology skeleton',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Maximum section length
bpy.types.Scene.MaximumSectionLength = bpy.props.FloatProperty(
    name='Max. Section Length',
    description='The maximum length of the section along the entire morphology skeleton',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Average section length
bpy.types.Scene.AverageSectionLength = bpy.props.FloatProperty(
    name='Avg. Section Length',
    description='The average length of the section along the entire morphology skeleton',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Number short sections
bpy.types.Scene.NumberShortSections = bpy.props.IntProperty(
    name='# Short Sections',
    description='The total number of short sections along the morphology, where the sum of the '
                'radii of the first and last samples is smaller than the section length',
    default=0, subtype='FACTOR')

# Number zero-radius samples
bpy.types.Scene.NumberZeroRadiusSamples = bpy.props.IntProperty(
    name='# Zero-radius Samples',
    description='The total number of the sample with zero radius in the morphology skeleton',
    default=0, subtype='FACTOR')

# Number of duplicated sections
bpy.types.Scene.NumberDuplicatedSamples = bpy.props.IntProperty(
    name='# Duplicated Samples',
    description='The total number of duplicated samples in the morphology skeleton that '
                'are almost in the same position',
    default=0, subtype='FACTOR')

# Bounding box
bpy.types.Scene.BBoxPMinX = bpy.props.FloatProperty(
    name='X',
    description='X-coordinate of PMin',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BBoxPMinY = bpy.props.FloatProperty(
    name='Y',
    description='Y-coordinate of PMin',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BBoxPMinZ = bpy.props.FloatProperty(
    name='Z',
    description='Z-coordinate of PMin',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BBoxPMaxX = bpy.props.FloatProperty(
    name='X',
    description='X-coordinate of PMax',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BBoxPMaxY = bpy.props.FloatProperty(
    name='Y',
    description='Y-coordinate of PMax',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BBoxPMaxZ = bpy.props.FloatProperty(
    name='Z',
    description='Z-coordinate of PMax',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BBoxCenterX = bpy.props.FloatProperty(
    name='X',
    description='X-coordinate of center of the morphology',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BBoxCenterY = bpy.props.FloatProperty(
    name='Y',
    description='Y-coordinate of center of the morphology',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BBoxCenterZ = bpy.props.FloatProperty(
    name='Z',
    description='Z-coordinate of center of the morphology',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BoundsX = bpy.props.FloatProperty(
    name='X',
    description='Morphology width',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BoundsY = bpy.props.FloatProperty(
    name='Y',
    description='Morphology height',
    min=-1e10, max=1e10, subtype='FACTOR')
bpy.types.Scene.BoundsZ = bpy.props.FloatProperty(
    name='Z',
    description='Morphology depth',
    min=-1e10, max=1e10, subtype='FACTOR')

# Analysis time
bpy.types.Scene.MorphologyAnalysisTime = bpy.props.FloatProperty(
    name='Analysis Time (Sec)',
    default=0, min=0, max=1000000)