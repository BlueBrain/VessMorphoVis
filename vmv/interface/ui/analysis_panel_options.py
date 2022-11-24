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

# Alignment X-segment length
bpy.types.Scene.SegmentLengthX = bpy.props.FloatProperty(
    name='Segments\' Length in X',
    description='The total segment length along the X-axis in microns.',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Alignment Y-segment length
bpy.types.Scene.SegmentLengthY = bpy.props.FloatProperty(
    name='Segments\' Length in Y',
    description='The total segment length along the Y-axis in microns.',
    subtype='FACTOR', min=0, max=1e32, precision=5)

# Alignment Z-segment length
bpy.types.Scene.SegmentLengthZ = bpy.props.FloatProperty(
    name='Segments\' Length in Z',
    description='The total segment length along the Z-axis in microns.',
    subtype='FACTOR', min=0, max=1e32, precision=5)

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


# Surface Area Analysis ############################################################################
bpy.types.Scene.TotalSurfaceArea = bpy.props.FloatProperty(
    name='Total Surface Area',
    description='The total surface area of the morphology computed from individual segments in the '
                'morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MinimumSegmentSurfaceArea = bpy.props.FloatProperty(
    name='Min. Segment Surface Area',
    description='The surface area of the smallest segment in the morphology skeleton (in µm²).'
                'Note that this value could be zero if the segment has zero radius or zero length',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.SmallestSegmentSurfaceArea = bpy.props.FloatProperty(
    name='Smallest (non-zero) Segment Surface Area',
    description='The surface area of the smallest \'valid\' segment (that has no zero-radius nor '
                'zero-length) in the morphology skeleton (in µm²). Normally, the value of this '
                'quantity should be similar to the Min. Segment Surface Area. '
                'Nevertheless If this value is zero, this means that all the segments in the '
                'morphology have zero surface areas',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MaximumSegmentSurfaceArea = bpy.props.FloatProperty(
    name='Max. Segment Surface Area',
    description='The surface area of the largest segment in the morphology skeleton (in µm²)',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MeanSegmentSurfaceArea = bpy.props.FloatProperty(
    name='Mean Segment Surface Area',
    description='The mean segment surface area in the morphology skeleton (in µm²)',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.GlobalSegmentSurfaceAreaRatio = bpy.props.FloatProperty(
    name='Global Segment Surface Area Ratio',
    description='The ratio between the surface area of the smallest (valid, or non-zero) segment '
                'to that of the largest segment in the morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.GlobalSegmentSurfaceAreaRatioFactor = bpy.props.FloatProperty(
    name='Global Segment Surface Area Ratio Factor',
    description='The scale factor representing the ratio between the surface area of the largest '
                'segment to that of the smallest segment in the morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.NumberZeroSurfaceAreaSegments = bpy.props.IntProperty(
    name='# Sections with Zero Surface Area',
    description='The number of  segments in the morphology',
    default=0, subtype='FACTOR')

bpy.types.Scene.MinimumSectionSurfaceArea = bpy.props.FloatProperty(
    name='Min. Section Surface Area',
    description='The surface area of the smallest section in the morphology skeleton (in µm²).'
                'Note that this value could be zero if the section is composed of segments with '
                'zero surface area',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.SmallestSectionSurfaceArea = bpy.props.FloatProperty(
    name='Smallest (non-zero) Section Surface Area',
    description='The volume of the smallest \'valid\' section (that has no zero-surface-area '
                'segments) in the morphology skeleton (in µm²). Normally, the value of this '
                'quantity should be similar to the Min. Section Surface Area.'
                'Nevertheless If this value is zero, this means that all the sections in the '
                'morphology have zero surface area',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MaximumSectionSurfaceArea = bpy.props.FloatProperty(
    name='Max. Section Surface Area',
    description='The surface area of the largest section in the morphology skeleton (in µm²)',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MeanSectionSurfaceArea = bpy.props.FloatProperty(
    name='Mean Section Surface Area',
    description='The mean section surface area in the morphology skeleton (in µm²)',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.GlobalSectionSurfaceAreaRatio = bpy.props.FloatProperty(
    name='Global Section Surface Area Ratio',
    description='The ratio between the surface area of the smallest (valid) section to that of the '
                'largest section in the morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.GlobalSectionSurfaceAreaRatioFactor = bpy.props.FloatProperty(
    name='Global Section Surface Area Ratio Factor',
    description='The scale factor representing the ratio between the surface area of the largest '
                'section to that of the smallest section in the morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.NumberZeroSurfaceAreaSections = bpy.props.IntProperty(
    name='# Sections with Zero Surface Area',
    description='The number of sections with zero surface area in the morphology',
    default=0, subtype='FACTOR')

# Volume Analysis ##################################################################################
bpy.types.Scene.TotalVolume = bpy.props.FloatProperty(
    name='Total Volume',
    description='The total volume of the morphology computed from individual segments in the '
                'morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MinimumSegmentVolume = bpy.props.FloatProperty(
    name='Min. Segment Volume',
    description='The volume of the smallest segment in the morphology skeleton (in µm³).'
                'Note that this value could be zero if the segment has zero radius or zero length',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.SmallestSegmentVolume = bpy.props.FloatProperty(
    name='Smallest (non-zero) Segment Volume',
    description='The volume of the smallest \'valid\' segment (that has no zero-radius nor '
                'zero-length) in the morphology skeleton (in µm³). Normally, the value of this '
                'quantity should be similar to the Min. Segment Volume. '
                'Nevertheless If this value is zero, this means that all the segments in the '
                'morphology have zero volumes',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MaximumSegmentVolume = bpy.props.FloatProperty(
    name='Max. Segment Volume',
    description='The volume of the largest segment in the morphology skeleton (in µm³)',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MeanSegmentVolume = bpy.props.FloatProperty(
    name='Mean Segment Volume',
    description='The mean segment volume in the morphology skeleton (in µm³)',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.GlobalSegmentVolumeRatio = bpy.props.FloatProperty(
    name='Global Segment Volume Ratio',
    description='The ratio between the volume of the smallest (valid) segment to that of the '
                'largest segment in the morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.GlobalSegmentVolumeRatioFactor = bpy.props.FloatProperty(
    name='Global Segment Volume Ratio Factor',
    description='The scale factor representing the ratio between the volume of the largest '
                'segment to that of the smallest segment in the morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.NumberZeroVolumeSegments = bpy.props.IntProperty(
    name='# Zero-volume Segments',
    description='The number of the zero-volume segments in the morphology',
    default=0, subtype='FACTOR')

bpy.types.Scene.MinimumSectionVolume = bpy.props.FloatProperty(
    name='Min. Section Volume',
    description='The volume of the smallest section in the morphology skeleton (in µm³).'
                'Note that this value could be zero if the section is composed of segments with '
                'zero volume',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.SmallestSectionVolume = bpy.props.FloatProperty(
    name='Smallest (non-zero) Section Volume',
    description='The volume of the smallest \'valid\' section (that has no zero-volume segments) '
                'in the morphology skeleton (in µm³). Normally, the value of this '
                'quantity should be similar to the Min. Section Volume.'
                'Nevertheless If this value is zero, this means that all the sections in the '
                'morphology have zero volumes',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MaximumSectionVolume = bpy.props.FloatProperty(
    name='Max. Section Volume',
    description='The volume of the largest section in the morphology skeleton (in µm³)',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.MeanSectionVolume = bpy.props.FloatProperty(
    name='Mean Section Volume',
    description='The mean section volume in the morphology skeleton (in µm³)',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.GlobalSectionVolumeRatio = bpy.props.FloatProperty(
    name='Global Section Volume Ratio',
    description='The ratio between the volume of the smallest (valid) section to that of the '
                'largest section in the morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.GlobalSectionVolumeRatioFactor = bpy.props.FloatProperty(
    name='Global Section Volume Ratio Factor',
    description='The scale factor representing the ratio between the volume of the largest '
                'section to that of the smallest section in the morphology',
    subtype='FACTOR', min=0, max=1e32, precision=5)

bpy.types.Scene.NumberZeroVolumeSections = bpy.props.IntProperty(
    name='# Zero-volume Sections',
    description='The number of the zero-volume sections in the morphology',
    default=0, subtype='FACTOR')


