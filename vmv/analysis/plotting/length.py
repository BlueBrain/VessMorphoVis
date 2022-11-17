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


####################################################################################################
# @plot_length_analysis_statistics
####################################################################################################
def plot_length_analysis_statistics(morphology,
                                    output_directory,
                                    sections_centers=None):

    data_frame = vmv.analysis.perform_length_analysis(
        sections=morphology.sections_list, sections_centers=sections_centers)

    # Section Length
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SECTION_LENGTH,
        output_prefix='%s-%s-histogram' % (morphology.name, Prefix.SECTION_LENGTH),
        output_directory=output_directory,
        y_label=r'Section Length ($\mu$m)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Mean section radius profile
    vmv_plotting.plot_average_profiles_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_LENGTH,
        x_axis_label=r'Section Length ($\mu$m)',
        output_prefix='%s-%s' % (morphology.name, Prefix.SECTION_LENGTH),
        output_directory=output_directory)

    # Distribution of mean section radius
    vmv_plotting.plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_LENGTH,
        x_label=r'Section Length ($\mu$m)',
        output_prefix='%s-%s-scatter' % (morphology.name, Prefix.SECTION_LENGTH),
        output_directory=output_directory)


    # Segment mean Length
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_MEAN_LENGTH,
        output_prefix='%s-%s-histogram' % (morphology.name, Prefix.SEGMENT_MEAN_LENGTH),
        output_directory=output_directory,
        y_label=r'Segment Mean Length ($\mu$m)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Mean section radius profile
    vmv_plotting.plot_average_profiles_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_MEAN_LENGTH,
        x_axis_label=r'Segment Mean Length ($\mu$m)',
        output_prefix='%s-%s' % (morphology.name, Prefix.SEGMENT_MEAN_LENGTH),
        output_directory=output_directory)

    # Distribution of mean section radius
    vmv_plotting.plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_MEAN_LENGTH,
        x_label=r'Segment Mean Length ($\mu$m)',
        output_prefix='%s-%s-scatter' % (morphology.name, Prefix.SEGMENT_MEAN_LENGTH),
        output_directory=output_directory)

    # Section radius range
    vmv_plotting.plot_range_data_along_xyz(data_frame=data_frame,
                                           min_keyword=Keys.SEGMENT_MIN_LENGTH,
                                           mean_keyword=Keys.SEGMENT_MEAN_LENGTH,
                                           max_keyword=Keys.SEGMENT_MAX_LENGTH,
                                           x_label=r'Segment Length Range per Section ($\mu$m)',
                                           output_prefix='segment-length-distribution',
                                           output_directory=output_directory)

    # Segment length ratio
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_LENGTH_RATIO,
        output_prefix='%s-%s-histogram' % (morphology.name, Prefix.SEGMENT_LENGTH_RATIO),
        output_directory=output_directory,
        y_label=r'Segment Length Ratio (per Section)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Mean section radius profile
    vmv_plotting.plot_average_profiles_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_LENGTH_RATIO,
        x_axis_label=r'Segment Length Ratio (per Section)',
        output_prefix='%s-%s' % (morphology.name, Prefix.SEGMENT_LENGTH_RATIO),
        output_directory=output_directory)


    vmv_plotting.plot_scatter_data_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_LENGTH_RATIO,
        x_label=r'Segment Length Ratio (per section)',
        output_prefix='%s-%s-scatter' % (morphology.name, Prefix.SEGMENT_LENGTH_RATIO),
        output_directory=output_directory)


    # Find the data frame with sections that have short sections
    short_sections = list()
    for index, row in data_frame.iterrows():
        if row[Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO] < 1.0:
            short_sections.append(row)
    short_sections_data_frame = pandas.DataFrame(
        short_sections, columns=[Keys.SECTION_INDEX,
                                 Keys.X, Keys.Y, Keys.Z,
                                 Keys.SECTION_LENGTH,
                                 Keys.SEGMENT_MIN_LENGTH,
                                 Keys.SEGMENT_MEAN_LENGTH,
                                 Keys.SEGMENT_MAX_LENGTH,
                                 Keys.SEGMENT_LENGTH_RATIO,
                                 Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO,
                                 Keys.SECTION_SAMPLING_DENSITY])

    vmv_plotting.plot_histograms_along_x_y_z(
        data_frame=short_sections_data_frame,
        output_prefix='%s-%s-histogram' % (morphology.name, Prefix.SHORT_SECTIONS),
        output_directory=output_directory)

    vmv_plotting.plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO,
        x_label=r'Terminal Thickness / Length (per section)',
        output_prefix='%s-%s-scatter' % (morphology.name, Prefix.SHORT_SECTIONS),
        output_directory=output_directory)
