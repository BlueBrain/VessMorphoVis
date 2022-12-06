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
import vmv.utilities
import vmv.analysis.plotting as vmv_plotting
from vmv.consts import Keys, Prefix, Geometry


####################################################################################################
# @add_structure_analysis_table_to_pdf_report
####################################################################################################
def add_structure_analysis_table_to_pdf_report(structure_items,
                                               pdf_report):
    # Create a new page in the PDF report
    pdf_report.alias_nb_pages()
    pdf_report.add_page()

    # Title
    pdf_report.add_central_title(text='Structure Analysis')
    current_y = Geometry.PDF_PAGE_Y_START

    pdf_report.add_default_table_cell(
        quantity='Total number of unique samples in the morphology',
        value=structure_items.number_unique_samples, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Total number of samples in the morphology',
        value=structure_items.number_samples, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Total number of segments in the morphology',
        value=structure_items.number_segments, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Total number of sections in the morphology',
        value=structure_items.number_sections, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Number of sections with one segment',
        value=structure_items.number_sections_with_one_segment, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Minimum number of samples per section',
        value=structure_items.minimum_number_samples_per_section, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Maximum number of samples per section',
        value=structure_items.maximum_number_samples_per_section, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Mean number of samples per section',
        value=structure_items.mean_number_samples_per_section, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT

    pdf_report.add_default_table_cell(
        quantity='Number of short sections in the morphology',
        value=structure_items.number_short_sections, y_start=current_y)
    current_y += Geometry.TABLE_CELL_HEIGHT


####################################################################################################
# @plot_radius_analysis_statistics
####################################################################################################
def plot_structure_analysis_statistics(morphology,
                                       output_directory,
                                       pdf_report=None):

    if pdf_report is not None:

        # Get the structure items
        structure_items = vmv.analysis.compute_structure_analysis_items(morphology)

        # Add the results to the report
        add_structure_analysis_table_to_pdf_report(
            structure_items=structure_items, pdf_report=pdf_report)

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
    number_samples_per_section_histogram = vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.NUMBER_SAMPLES_PER_SECTION,
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.NUMBER_SAMPLES_PER_SECTION),
        output_directory=output_directory,
        y_label='Number of Samples (per Section)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT,
        dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    number_samples_per_section_scatter_xyz = vmv_plotting.plot_range_and_scatter_combined_along_xyz(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.NUMBER_SAMPLES_PER_SECTION,
        x_label='Number of Samples (per Section)',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.NUMBER_SAMPLES_PER_SECTION),
        output_directory=output_directory)

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

    number_sections_with_one_segment_xyz = vmv_plotting.plot_histograms_along_x_y_z(
        data_frame=sections_with_single_segment_data_frame,
        title='# Sections with 1 Segment',
        output_prefix='%s_%s_%s' % (morphology.name, Prefix.STRUCTURE,
                                    Prefix.SECTIONS_WITH_SINGLE_SEGMENTS),
        output_directory=output_directory)

    if pdf_report is not None:

        # Add a new page
        pdf_report.add_page()

        current_y = Geometry.PAPER_START_Y
        pdf_report.add_section_title(text='Number of Samples per Section Histogram',
                                     x_start=0, y_start=current_y)
        current_y += Geometry.DELTA_Y_TEXT
        pdf_report.image(number_samples_per_section_histogram,
                         Geometry.PDF_PAGE_X_MARGIN, current_y, 0, Geometry.FIGURE_HEIGHT)
        current_y += Geometry.DELTA_Y_FIGURE

        # Section volume distribution
        pdf_report.add_section_title(text='Distribution of Number of Samples per Section',
                                     x_start=0, y_start=current_y)
        current_y += Geometry.DELTA_Y_TEXT
        for i in range(3):
            x_start = vmv.utilities.compute_x_starting_point(figure_count=3, figure_number=i)
            if i == 0:
                pdf_report.image(number_samples_per_section_scatter_xyz[0], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
            elif i == 1:
                pdf_report.image(number_samples_per_section_scatter_xyz[1], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
            elif i == 2:
                pdf_report.image(number_samples_per_section_scatter_xyz[2], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
        current_y += Geometry.DELTA_Y_FIGURE

        # Section volume distribution
        pdf_report.add_section_title(text='Number of Sections with 1 Segment Histograms',
                                     x_start=0, y_start=current_y)
        current_y += Geometry.DELTA_Y_TEXT
        for i in range(3):
            x_start = vmv.utilities.compute_x_starting_point(figure_count=3, figure_number=i)
            if i == 0:
                pdf_report.image(number_sections_with_one_segment_xyz[0], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
            elif i == 1:
                pdf_report.image(number_sections_with_one_segment_xyz[1], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
            elif i == 2:
                pdf_report.image(number_sections_with_one_segment_xyz[2], x_start, current_y,
                                 0, Geometry.FIGURE_HEIGHT)
        current_y += Geometry.DELTA_Y_FIGURE





