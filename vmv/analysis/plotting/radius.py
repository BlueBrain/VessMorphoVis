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
# @plot_radius_analysis_statistics
####################################################################################################
def plot_radius_analysis_statistics(morphology,
                                    output_directory):

    # Analyze the radii of the samples only
    # TODO: Use the samples_list instead of the sections_list
    data_frame = vmv.analysis.analyze_samples_radii_xyz(morphology.sections_list)

    # Plot the average radius profiles along XYZ
    # TODO: Adjust the unit in case mm is used, probably set it from the UI
    vmv_plotting.plot_average_profiles_along_x_y_z(
        data_frame=data_frame, x_keyword=vmv.consts.Keys.SAMPLE_RADIUS,
        x_axis_label=r'Vessel Mean Radius ($\mu$m)',
        output_prefix=Prefix.VESSEL_RADIUS, output_directory=output_directory)

    # Vessel radius histogram
    vmv_plotting.plot_histogram_with_box_plot(
        data_frame=data_frame, data_key=Keys.SAMPLE_RADIUS,
        output_prefix='%s-histogram' % Prefix.VESSEL_RADIUS, output_directory=output_directory,
        y_label=r'Vessel Radius ($\mu$m)',
        light_color=vmv.consts.Color.CM_ORANGE_LIGHT, dark_color=vmv.consts.Color.CM_ORANGE_DARK)