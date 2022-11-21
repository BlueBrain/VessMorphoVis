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
# @plot_radius_analysis_statistics
####################################################################################################
def plot_structure_analysis_statistics(morphology,
                                       output_directory):
    # Collect the data frame
    data_frame = vmv.analysis.analyze_samples_radii_xyz(sections=morphology.sections_list)

    vmv_plotting.plot_histograms_along_x_y_z(
        data_frame=data_frame,
        title=r'Samples Density (per $\mu$m)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.SAMPLES_DENSITY),
        output_directory=output_directory)

    # Collect the data frame
    data_frame = vmv.analysis.analyze_samples_per_section(sections=morphology.sections_list)

    # Number of Samples per Section ################################################################
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.NUMBER_SAMPLES_PER_SECTION,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.NUMBER_SAMPLES_PER_SECTION),
        output_directory=output_directory,
        y_label='Number of Samples (per Section)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT,
        dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    vmv_plotting.plot_range_and_scatter_combined(
        data_frame=data_frame,
        x_keyword=vmv.consts.Keys.NUMBER_SAMPLES_PER_SECTION, y_keyword=Keys.SECTION_INDEX,
        x_label='Number of Samples (per Section)',  y_label='Section Index',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT,
        dark_color=vmv.consts.Color.CM_ORANGE_DARK,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.NUMBER_SAMPLES_PER_SECTION),
        output_directory=output_directory)




    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.NUMBER_SEGMENTS_PER_SECTION,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.NUMBER_SEGMENTS_PER_SECTION),
        output_directory=output_directory,
        y_label='Number of Segments (per Section)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT,
        dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.NUMBER_SAMPLES_PER_SECTION,
        x_label='Number of Samples (per Section)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.NUMBER_SAMPLES_PER_SECTION),
        output_directory=output_directory)

    vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.NUMBER_SEGMENTS_PER_SECTION,
        x_label='Number of Segments (per Section)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.NUMBER_SEGMENTS_PER_SECTION),
        output_directory=output_directory)

    # Find the data frame with sections that have single segments only
    sections_with_single_segment = list()
    for index, row in data_frame.iterrows():
        if row[Keys.NUMBER_SEGMENTS_PER_SECTION] == 1:
            sections_with_single_segment.append(row)
    sections_with_single_segment_data_frame = pandas.DataFrame(
        sections_with_single_segment, columns=[Keys.SECTION_INDEX,
                                               Keys.NUMBER_SAMPLES_PER_SECTION,
                                               Keys.NUMBER_SEGMENTS_PER_SECTION,
                                               Keys.X, Keys.Y, Keys.Z])

    vmv_plotting.plot_histograms_along_x_y_z(
        data_frame=sections_with_single_segment_data_frame,
        title='# Sections with 1 Segment',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.SECTIONS_WITH_SINGLE_SEGMENTS),
        output_directory=output_directory)



