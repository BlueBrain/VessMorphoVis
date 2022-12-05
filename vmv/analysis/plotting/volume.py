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
import vmv.utilities
from vmv.consts import Keys, Prefix, Geometry


def plot_volume_analysis_statistics(morphology,
                                    output_directory,
                                    sections_centers=None,
                                    pdf_report=None):

    # Add the data to the PDF report
    if pdf_report is not None:
        pdf_report.alias_nb_pages()
        pdf_report.add_page()

        v_items = vmv.analysis.compute_volume_analysis_items(
            sections=vmv.interface.MorphologyObject.sections_list)

        pdf_report.add_central_title(text='Volume Analysis')
        current_y = 30

        pdf_report.add_default_table_cell(
            quantity='Total volume',
            value=v_items.total_morphology_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Minimum segment volume',
            value=v_items.minimum_segment_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Smallest (non-zero) segment volume',
            value=v_items.minimum_non_zero_segment_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Maximum segment volume',
            value=v_items.maximum_segment_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Mean segment volume',
            value=v_items.mean_segment_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Global segment volume ratio (minimum-to-maximum)',
            value=v_items.global_segment_volume_ratio, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Global segment volume factor (maximum-to-minimum)',
            value=v_items.global_segment_volume_ratio_factor, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Minimum segment volume ratio (minimum-to-maximum) per section',
            value=v_items.minimum_segment_volume_ratio_per_section, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Maximum segment volume ratio (minimum-to-maximum) per section',
            value=v_items.maximum_segment_volume_ratio_per_section, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Mean segment volume ratio (minimum-to-maximum) per section',
            value=v_items.mean_segment_volume_ratio_per_section, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Number of segments with zero volume',
            value=v_items.number_segments_with_zero_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Minimum section volume',
            value=v_items.minimum_section_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Maximum section volume',
            value=v_items.maximum_section_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Mean section volume',
            value=v_items.mean_section_volume, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Global section volume ratio (minimum-to-maximum)',
            value=v_items.global_section_volume_ratio, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Number of sections with zero volume',
            value=v_items.number_sections_with_zero_volume,
            y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

    # Collect the data frame
    data_frame = vmv.analysis.perform_volume_analysis(
        sections=morphology.sections_list, sections_centers=sections_centers)

    # Section Volume ###############################################################################
    section_volume_histogram = vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SECTION_VOLUME,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SECTION_VOLUME),
        output_directory=output_directory,
        fig_size=(10, 10),
        y_label=r'Section Volume ($\mu$m³)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    section_volume_scatter_xyz = vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_VOLUME,
        x_label='Section Volume' + r' ($\mu$m³)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SECTION_VOLUME),
        output_directory=output_directory)

    # Segment Mean Volume ##########################################################################
    segment_mean_volume_histogram = vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_MEAN_VOLUME,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_MEAN_VOLUME),
        output_directory=output_directory,
        y_label=r'Segment Mean Volume per Section ($\mu$m³)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    segment_mean_volume_scatter_xyz = vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_MEAN_VOLUME,
        x_label='Segment Mean Volume per Section' + r' ($\mu$m³)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_MEAN_VOLUME),
        output_directory=output_directory)

    # Segment Volume Range #########################################################################
    segment_volume_range_xyz = vmv_plotting.plot_range_data_along_xyz(
        data_frame=data_frame,
        min_keyword=Keys.SEGMENT_MIN_VOLUME,
        mean_keyword=Keys.SEGMENT_MEAN_VOLUME,
        max_keyword=Keys.SEGMENT_MAX_VOLUME,
        x_label='Segment Volume Range\nper Section' + r' ($\mu$m³)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME_RANGE),
        output_directory=output_directory)

    # Segment Volume Ratio #########################################################################
    segment_volume_ratio_histogram = vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_VOLUME_RATIO,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME_RATIO),
        output_directory=output_directory,
        y_label='Segment Volume Ratio (per Section)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    segment_volume_ratio_scatter_xyz = vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_VOLUME_RATIO,
        x_label='Segment Volume Ratio per Section',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME_RATIO),
        output_directory=output_directory)

    per_segment_data_frame = vmv.analysis.perform_per_segment_volume_analysis(
        sections=morphology.sections_list)

    # Segment Mean Volume ##########################################################################
    segment_volume_histogram =  vmv_plotting.plot_histogram_with_box_plot(
        data_frame=per_segment_data_frame, data_key=Keys.SEGMENT_VOLUME,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME),
        output_directory=output_directory,
        y_label=r'Segment Volume ($\mu$m³)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    segment_volume_scatter_xyz = vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=per_segment_data_frame, x_keyword=vmv.consts.Keys.SEGMENT_VOLUME,
        x_label='Segment Volume' + r' ($\mu$m³)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.VOLUME, Prefix.SEGMENT_VOLUME),
        output_directory=output_directory)


    if pdf_report is not None:

        pdf_report.add_page()

        # Section volume histogram
        current_y = Geometry.PAPER_START_Y
        pdf_report.add_section_title(text='Section Volume Histogram', x_start=0, y_start=current_y)
        current_y += Geometry.DELTA_Y_TEXT
        pdf_report.image(section_volume_histogram,
                         Geometry.PDF_PAGE_X_MARGIN, current_y, 0, Geometry.FIGURE_HEIGHT)
        current_y += Geometry.DELTA_Y_FIGURE

        # Section volume distribution
        pdf_report.add_section_title(text='Distribution of Sections\' Volumes', x_start=0,
                                     y_start=current_y)
        current_y += Geometry.DELTA_Y_TEXT
        for i in range(3):
            x_start = vmv.utilities.compute_x_starting_point(figure_count=3, figure_number=i)
            if i == 0:
                pdf_report.image(section_volume_scatter_xyz[0], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
            elif i == 1:
                pdf_report.image(section_volume_scatter_xyz[1], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
            elif i == 2:
                pdf_report.image(section_volume_scatter_xyz[2], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
        current_y += Geometry.DELTA_Y_FIGURE

        # Segment volume histogram
        pdf_report.add_section_title(text='Segment Volume Histogram', x_start=0, y_start=current_y)
        current_y += Geometry.DELTA_Y_TEXT
        pdf_report.image(segment_volume_histogram,
                         Geometry.PDF_PAGE_X_MARGIN, current_y, 0, Geometry.FIGURE_HEIGHT)
        current_y += Geometry.DELTA_Y_FIGURE

        # Segment volume distribution
        pdf_report.add_section_title(text='Distribution of Segments\' Volumes', x_start=0,
                                     y_start=current_y)
        current_y += Geometry.DELTA_Y_TEXT
        for i in range(3):
            x_start = vmv.utilities.compute_x_starting_point(figure_count=3, figure_number=i)
            if i == 0:
                pdf_report.image(segment_volume_scatter_xyz[0], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
            elif i == 1:
                pdf_report.image(segment_volume_scatter_xyz[1], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
            elif i == 2:
                pdf_report.image(segment_volume_scatter_xyz[2], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
        current_y += Geometry.DELTA_Y_FIGURE

    pdf_report.add_page()

    current_y = Geometry.PAPER_START_Y
    pdf_report.add_section_title(
        text='Segment Mean Volume (per Section) Histogram', x_start=0, y_start=current_y)
    current_y += Geometry.DELTA_Y_TEXT
    pdf_report.image(segment_mean_volume_histogram,
                     Geometry.PDF_PAGE_X_MARGIN, current_y, 0, Geometry.FIGURE_HEIGHT)
    current_y += Geometry.DELTA_Y_FIGURE

    # Segment volume distribution
    pdf_report.add_section_title(
        text='Distribution of Segment Mean Volume (per Section)', x_start=0, y_start=current_y)
    current_y += Geometry.DELTA_Y_TEXT
    for i in range(3):
        x_start = vmv.utilities.compute_x_starting_point(figure_count=3, figure_number=i)
        if i == 0:
            pdf_report.image(segment_mean_volume_scatter_xyz[0], x_start, current_y,
                             0, Geometry.FIGURE_HEIGHT)
        elif i == 1:
            pdf_report.image(segment_mean_volume_scatter_xyz[1], x_start, current_y,
                             0, Geometry.FIGURE_HEIGHT)
        elif i == 2:
            pdf_report.image(segment_mean_volume_scatter_xyz[2], x_start, current_y,
                             0, Geometry.FIGURE_HEIGHT)
    current_y += Geometry.DELTA_Y_FIGURE

    pdf_report.add_section_title(
        text='Segment Volume Ratio (per Section) Histogram', x_start=0, y_start=current_y)
    current_y += Geometry.DELTA_Y_TEXT
    pdf_report.image(segment_volume_ratio_histogram,
                     Geometry.PDF_PAGE_X_MARGIN, current_y, 0, Geometry.FIGURE_HEIGHT)
    current_y += Geometry.DELTA_Y_FIGURE

    pdf_report.add_section_title(
        text='Distribution of Segment Volume Ratio (per Section)', x_start=0, y_start=current_y)
    current_y += Geometry.DELTA_Y_TEXT
    for i in range(3):
        x_start = vmv.utilities.compute_x_starting_point(figure_count=3, figure_number=i)
        if i == 0:
            pdf_report.image(segment_volume_ratio_scatter_xyz[0], x_start, current_y,
                             0, Geometry.FIGURE_HEIGHT)
        elif i == 1:
            pdf_report.image(segment_volume_ratio_scatter_xyz[1], x_start, current_y,
                             0, Geometry.FIGURE_HEIGHT)
        elif i == 2:
            pdf_report.image(segment_volume_ratio_scatter_xyz[2], x_start, current_y,
                             0, Geometry.FIGURE_HEIGHT)
    current_y += Geometry.DELTA_Y_FIGURE

