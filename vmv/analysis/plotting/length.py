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
from vmv.consts import Keys, Prefix, Geometry


####################################################################################################
# @add_length_analysis_table_to_pdf_report
####################################################################################################
def add_length_analysis_table_to_pdf_report(length_items,
                                            pdf_report):

    # Create a new page in the PDF report
    pdf_report.alias_nb_pages()
    pdf_report.add_page()

    # Title
    pdf_report.add_central_title(text='Length Analysis')
    current_y = Geometry.PDF_PAGE_Y_START

    pdf_report.add_default_table_cell(
        quantity='Total morphology length (µm)',
        value=length_items.total_morphology_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Minimum segment length (µm)',
        value=length_items.minimum_segment_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Shortest (non-zero) segment length (µm)',
        value=length_items.minimum_non_zero_segment_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Maximum segment length (µm)',
        value=length_items.maximum_segment_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Mean segment length (µm)',
        value=length_items.mean_segment_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Global segment length ratio (minimum-to-maximum)',
        value=length_items.global_segment_length_ratio, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Global segment length ratio (maximum-to-minimum)',
        value=1./length_items.global_segment_length_ratio, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Number of segments with zero length',
        value=length_items.number_segments_with_zero_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Minimum section length (µm)',
        value=length_items.minimum_section_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Shortest (non-zero) section length (µm)',
        value=length_items.minimum_non_zero_section_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Maximum section length (µm)',
        value=length_items.maximum_section_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Mean section length (µm)',
        value=length_items.mean_section_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Global section length ratio (minimum-to-maximum)',
        value=length_items.global_section_length_ratio, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Global section length ratio (maximum-to-minimum)',
        value=1. / length_items.global_section_length_ratio, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Number of sections with zero length',
        value=length_items.number_sections_with_zero_length, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT


####################################################################################################
# @plot_length_analysis_statistics
####################################################################################################
def plot_length_analysis_statistics(morphology,
                                    output_directory,
                                    pdf_report=None,
                                    sections_centers=None):

    if pdf_report is not None:

        # Get the radius items
        length_items = vmv.analysis.compute_length_analysis_items(morphology.sections_list)

        # Add the results to the report
        add_length_analysis_table_to_pdf_report(
            length_items=length_items, pdf_report=pdf_report)

    data_frame = vmv.analysis.perform_length_analysis(
        sections=morphology.sections_list, sections_centers=sections_centers)

    # Section Length
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SECTION_LENGTH,
        output_prefix='%s-%s' % (morphology.name, Prefix.SECTION_LENGTH),
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
        output_prefix='%s-%s' % (morphology.name, Prefix.SEGMENT_MEAN_LENGTH),
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
        output_prefix='%s-%s' % (morphology.name, Prefix.SEGMENT_LENGTH_RATIO),
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
        output_prefix='%s-%s' % (morphology.name, Prefix.SHORT_SECTIONS),
        output_directory=output_directory)

    vmv_plotting.plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO,
        x_label=r'Terminal Thickness / Length (per section)',
        output_prefix='%s-%s-scatter' % (morphology.name, Prefix.SHORT_SECTIONS),
        output_directory=output_directory)
