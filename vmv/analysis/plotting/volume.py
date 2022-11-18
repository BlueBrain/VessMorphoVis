####################################################################################################
# Copyright (c) 2019 - 2022, EPFL / Blue Brain Project
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
import pandas

# Internal imports
import vmv
import vmv.analysis.plotting as vmv_plotting
from vmv.consts import Keys, Prefix


def plot_volume_analysis_statistics(morphology,
                                    output_directory,
                                    sections_centers=None):

    # Collect the data frame
    data_frame = vmv.analysis.perform_volume_analysis(
        sections=morphology.sections_list, sections_centers=sections_centers)

    # Section Volume ###############################################################################
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SECTION_VOLUME,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SECTION_VOLUME),
        output_directory=output_directory,
        y_label=r'Section Volume ($\mu$m³)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_VOLUME,
        x_label='Section Volume' + r' ($\mu$m³)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SECTION_VOLUME),
        output_directory=output_directory)

    # Segment Mean Volume ##########################################################################
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_MEAN_VOLUME,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_MEAN_VOLUME),
        output_directory=output_directory,
        y_label=r'Segment Mean Volume per Section ($\mu$m³)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_MEAN_VOLUME,
        x_label='Segment Mean Volume per Section' + r' ($\mu$m³)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_MEAN_VOLUME),
        output_directory=output_directory)

    # Segment Volume Range #########################################################################
    vmv_plotting.plot_range_data_along_xyz(
        data_frame=data_frame,
        min_keyword=Keys.SEGMENT_MIN_VOLUME,
        mean_keyword=Keys.SEGMENT_MEAN_VOLUME,
        max_keyword=Keys.SEGMENT_MAX_VOLUME,
        x_label='Segment Volume Range\nper Section' + r' ($\mu$m³)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME_RANGE),
        output_directory=output_directory)

    # Segment Volume Ratio #########################################################################
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_VOLUME_RATIO,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME_RATIO),
        output_directory=output_directory,
        y_label='Segment Volume Ratio (per Section)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_VOLUME_RATIO,
        x_label='Segment Volume Ratio per Section',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME_RATIO),
        output_directory=output_directory)

    per_segment_data_frame = vmv.analysis.perform_per_segment_volume_analysis(
        sections=morphology.sections_list)

    # Segment Mean Volume ##########################################################################
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=per_segment_data_frame, data_key=Keys.SEGMENT_VOLUME,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME),
        output_directory=output_directory,
        y_label=r'Segment Volume ($\mu$m³)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=per_segment_data_frame, x_keyword=vmv.consts.Keys.SEGMENT_VOLUME,
        x_label='Segment Volume' + r' ($\mu$m³)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME),
        output_directory=output_directory)

