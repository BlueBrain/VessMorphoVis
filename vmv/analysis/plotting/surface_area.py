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

# Internal imports
import vmv
import vmv.analysis.plotting as vmv_plotting
from vmv.consts import Keys, Prefix, Geometry


####################################################################################################
# @plot_surface_area_analysis_statistics
####################################################################################################
def plot_surface_area_analysis_statistics(morphology,
                                          output_directory,
                                          pdf_report=None,
                                          sections_centers=None):
    
    if pdf_report is not None:
        pdf_report.alias_nb_pages()
        pdf_report.add_page()

        # Compute the Surface Area items 
        sa_items = vmv.analysis.compute_surface_area_analysis_items(
            sections=vmv.interface.MorphologyObject.sections_list)

        pdf_report.add_central_title(text='Surface Area Analysis')
        current_y = 30

        pdf_report.add_default_table_cell(
            quantity='Total surface area (µm²)',
            value=sa_items.total_morphology_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Minimum segment surface area (µm²)',
            value=sa_items.minimum_segment_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Smallest (non-zero) segment surface area (µm²)',
            value=sa_items.minimum_non_zero_segment_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Maximum segment surface area (µm²)',
            value=sa_items.maximum_segment_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Mean segment surface area (µm²)',
            value=sa_items.mean_segment_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Global segment surface area ratio (minimum-to-maximum)',
            value=sa_items.global_segment_surface_area_ratio, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Global segment surface area factor (maximum-to-minimum)',
            value=sa_items.global_segment_surface_area_ratio_factor, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Minimum segment surface area ratio per section (minimum-to-maximum)',
            value=sa_items.minimum_segment_surface_area_ratio_per_section, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Maximum segment surface area ratio per section (minimum-to-maximum)',
            value=sa_items.maximum_segment_surface_area_ratio_per_section, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Mean segment surface area ratio per section (minimum-to-maximum)',
            value=sa_items.mean_segment_surface_area_ratio_per_section, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Number of segments with zero surface area',
            value=sa_items.number_segments_with_zero_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Minimum section surface area (µm²)',
            value=sa_items.minimum_section_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Maximum section surface area (µm²)',
            value=sa_items.maximum_section_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Mean section surface area (µm²)',
            value=sa_items.mean_section_surface_area, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Global section surface area ratio (minimum-to-maximum)',
            value=sa_items.global_section_surface_area_ratio, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Global section surface area ratio (maximum-to-minimum)',
            value=1. / sa_items.global_section_surface_area_ratio, y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

        pdf_report.add_default_table_cell(
            quantity='Number of sections with zero surface area',
            value=sa_items.number_sections_with_zero_surface_area,
            y_start=current_y)
        current_y += Geometry.TABLE_CELL_HEIGHT

    # Collect the data frame
    data_frame = vmv.analysis.perform_surface_area_analysis(
        sections=morphology.sections_list, sections_centers=sections_centers)

    section_surface_area_histogram = vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SECTION_SURFACE_AREA,
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SECTION_SURFACE_AREA),
        output_directory=output_directory,
        y_label=r'Section Surface Area ($\mu$m²)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Radius scatter x, y, z
    section_surface_area_scatter_xyz = vmv_plotting.plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_SURFACE_AREA,
        x_label=r'Section Surface Area ($\mu$m²)',
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SECTION_SURFACE_AREA),
        output_directory=output_directory)

    segment_mean_surface_area_histogram = vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_MEAN_SURFACE_AREA,
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SEGMENT_MEAN_SURFACE_AREA),
        output_directory=output_directory,
        y_label=r'Segment Mean Surface Area ($\mu$m²)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Surface Area ratio per section
    segment_surface_area_ratio_histogram = vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_SURFACE_AREA_RATIO,
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SEGMENT_SURFACE_AREA_RATIO),
        output_directory=output_directory,
        y_label='Segment Surface Area Ratio (per Section)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    segment_surface_area_ratio_scatter_xyz = vmv_plotting.plot_average_profiles_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_SURFACE_AREA_RATIO,
        x_axis_label='Segment Surface Area Ratio\n(per Section)',
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SEGMENT_SURFACE_AREA_RATIO),
        output_directory=output_directory)

    # Radius scatter x, y, z
    vmv_plotting.plot_scatter_data_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SEGMENT_SURFACE_AREA_RATIO,
        x_label='Segment Surface Area Ratio\n(per Section)',
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SEGMENT_SURFACE_AREA_RATIO),
        output_directory=output_directory)
