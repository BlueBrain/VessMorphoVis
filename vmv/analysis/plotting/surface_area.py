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
from vmv.consts import Keys, Prefix


####################################################################################################
# @plot_surface_area_analysis_statistics
####################################################################################################
def plot_surface_area_analysis_statistics(morphology,
                                          output_directory,
                                          sections_centers=None):

    # Collect the data frame
    data_frame = vmv.analysis.perform_surface_area_analysis(
        sections=morphology.sections_list, sections_centers=sections_centers)

    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SECTION_SURFACE_AREA,
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SECTION_SURFACE_AREA),
        output_directory=output_directory,
        y_label=r'Section Surface Area ($\mu$m²)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Radius scatter x, y, z
    vmv_plotting.plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SECTION_SURFACE_AREA,
        x_label=r'Section Surface Area ($\mu$m²)',
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SECTION_SURFACE_AREA),
        output_directory=output_directory)

    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_MEAN_SURFACE_AREA,
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SEGMENT_MEAN_SURFACE_AREA),
        output_directory=output_directory,
        y_label=r'Segment Mean Surface Area ($\mu$m²)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    # Section radius range
    vmv_plotting.plot_range_data_along_xyz(
        data_frame=data_frame,
        min_keyword=Keys.SEGMENT_MIN_SURFACE_AREA,
        mean_keyword=Keys.SEGMENT_MEAN_SURFACE_AREA,
        max_keyword=Keys.SEGMENT_MAX_SURFACE_AREA,
        x_label='Segment Surface Area Range\nper Section' + r' ($\mu$m²)',
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SEGMENT_MEAN_SURFACE_AREA),
        output_directory=output_directory)

    # Surface Area ratio per section
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SEGMENT_SURFACE_AREA_RATIO,
        output_prefix='%s_%s_%s' % (morphology.name,
                                    Prefix.SURFACE_AREA, Prefix.SEGMENT_SURFACE_AREA_RATIO),
        output_directory=output_directory,
        y_label='Segment Surface Area Ratio (per Section)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)

    vmv_plotting.plot_average_profiles_along_x_y_z(
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
