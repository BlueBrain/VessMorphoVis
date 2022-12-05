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
# @plot_radius_analysis_statistics_for_zero_radius_samples
####################################################################################################
def plot_radius_analysis_statistics_for_zero_radius_samples(data_frame,
                                                            output_prefix,
                                                            output_directory):

    # Verify if the dataset has any zero-radius samples
    zero_radius_data = list()
    for index, row in data_frame.iterrows():
        if row[Keys.SAMPLE_RADIUS] < 1e-5:
            zero_radius_data.append(row)

    # If True, then construct the data-frame and plot the distributions
    if len(zero_radius_data) > 0:
        zero_radius_data_frame = pandas.DataFrame(zero_radius_data,
                                                  columns=[Keys.SAMPLE_RADIUS, Keys.X, Keys.Y,
                                                           Keys.Z])

        vmv_plotting.plot_histograms_along_x_y_z(
            data_frame=zero_radius_data_frame,
            output_prefix='%s-%s' % (output_prefix, Prefix.ZERO_RADIUS_SAMPLES),
            output_directory=output_directory)


####################################################################################################
# @plot_radius_analysis_from_samples_list
####################################################################################################
def plot_radius_analysis_from_samples_list(morphology,
                                           output_directory):

    # Analyze the radii of the samples only
    # TODO: Use the samples_list instead of the sections_list
    data_frame = vmv.analysis.analyze_samples_radii_xyz(morphology.sections_list)

    # Plot the average radius profiles along XYZ
    # TODO: Adjust the unit in case mm is used, probably set it from the UI
    vmv_plotting.plot_average_profiles_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SAMPLE_RADIUS,
        x_axis_label=r'Vessel Mean Radius ($\mu$m)',
        output_prefix='%s-%s' % (morphology.name, Prefix.VESSEL_RADIUS),
        output_directory=output_directory)

    # Radius scatter x, y, z
    vmv_plotting.plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SAMPLE_RADIUS,
        x_label=r'Vessel Radius ($\mu$m)',
        output_prefix='%s-%s-scatter' % (morphology.name, Prefix.VESSEL_RADIUS),
        output_directory=output_directory)

    # Vessel radius histogram
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SAMPLE_RADIUS,
        output_prefix='%s-%s' % (morphology.name, Prefix.VESSEL_RADIUS),
        output_directory=output_directory,
        y_label=r'Vessel Radius ($\mu$m)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Zero-radius samples
    plot_radius_analysis_statistics_for_zero_radius_samples(
        data_frame=data_frame, output_prefix=morphology.name, output_directory=output_directory)


####################################################################################################
# @plot_radius_analysis_from_sections_list
####################################################################################################
def plot_radius_analysis_from_sections_list(morphology,
                                            output_directory):

    data_frame = vmv.analysis.analyse_per_section_radius(morphology.sections_list)

    # Section radius range
    vmv_plotting.plot_range_data_along_xyz(data_frame=data_frame,
                                           min_keyword=Keys.SECTION_MIN_RADIUS,
                                           mean_keyword=Keys.SECTION_MEAN_RADIUS,
                                           max_keyword=Keys.SECTION_MAX_RADIUS,
                                           x_label=r'Radius Range per Section ($\mu$m)',
                                           output_prefix='section-radius-distribution',
                                           output_directory=output_directory)

    # Mean section radius histogram
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SECTION_MEAN_RADIUS,
        output_prefix='%s-%s' % (morphology.name, Prefix.SECTION_MEAN_RADIUS),
        output_directory=output_directory,
        y_label=r'Mean Section Radius ($\mu$m)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Mean section radius profile
    vmv_plotting.plot_average_profiles_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_MEAN_RADIUS,
        x_axis_label=r'Section Mean Radius ($\mu$m)',
        output_prefix='%s-%s' % (morphology.name, Prefix.SECTION_MEAN_RADIUS),
        output_directory=output_directory)

    # Distribution of mean section radius
    vmv_plotting.plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_MEAN_RADIUS,
        x_label=r'Section Mean Radius ($\mu$m)',
        output_prefix='%s-%s-scatter' % (morphology.name, Prefix.SECTION_MEAN_RADIUS),
        output_directory=output_directory)

    # Radius ratio per section histogram
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SECTION_RADIUS_RATIO,
        output_prefix='%s-%s' % (morphology.name, Prefix.SECTION_RADIUS_RATIO),
        output_directory=output_directory,
        y_label=r'Section Radius Ratio',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    vmv_plotting.plot_average_profiles_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_RADIUS_RATIO,
        x_axis_label=r'Section Mean Radius ($\mu$m)',
        output_prefix='%s-%s' % (morphology.name, Prefix.SECTION_RADIUS_RATIO),
        output_directory=output_directory)

    # Distribution of radius ratio per section
    vmv_plotting.plot_scatter_data_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_RADIUS_RATIO,
        x_label=r'Radius Ratio (per section)',
        output_prefix='%s-%s-scatter' % (morphology.name, Prefix.SECTION_RADIUS_RATIO),
        output_directory=output_directory)


####################################################################################################
# @plot_radius_analysis_statistics
####################################################################################################
def plot_radius_analysis_statistics(morphology,
                                    output_directory):

    plot_radius_analysis_from_samples_list(morphology, output_directory)

    plot_radius_analysis_from_sections_list(morphology, output_directory)