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
import math
import matplotlib.pyplot as pyplot
import pandas

# Internal imports
import vmv.analysis.plotting as vmv_plotting
import vmv.utilities


####################################################################################################
# plot_average_profile_with_range
####################################################################################################
def plot_average_profile_with_range(data_frame,
                                    y_keyword,
                                    x_keyword,
                                    x_label,
                                    y_label,
                                    output_prefix,
                                    output_directory,
                                    title=None,
                                    bins=50,
                                    fig_size=(6, 10),
                                    dpi=150,
                                    light_color=vmv.consts.Color.CM_BLUE_LIGHT,
                                    dark_color=vmv.consts.Color.CM_BLUE_DARK,
                                    plot_styles=vmv.utilities.PlotStyle(),
                                    save_pdf=False,
                                    save_svg=False):
    # Set the styles
    vmv_plotting.set_plotting_styles(plot_styles=plot_styles)

    # Sort the data-frame by the Y-axis
    data_frame = data_frame.sort_values(by=[y_keyword])

    # Construct the groups
    groups = data_frame.groupby(pandas.cut(data_frame[y_keyword], bins=bins))

    # Construct the groups
    _mean = groups.mean()
    _min = groups.min()
    _max = groups.max()

    # Construct the range
    p_min = _min[x_keyword].values
    p_max = _max[x_keyword].values

    # Construct the figure
    fig, ax = pyplot.subplots(1, 1)
    fig.set_size_inches(fig_size[0], fig_size[1])
    fig.set_tight_layout('w_pad')

    # Plot the data
    ax.plot(_mean[x_keyword].values, _mean[y_keyword].values, color=dark_color)
    ax.fill_betweenx(_mean[y_keyword].values, p_max, p_min, color=light_color, alpha=0.25)

    # Set the axis style
    vmv_plotting.add_default_axis_styles(ax=ax, plot_styles=plot_styles)

    # Text
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title, pad=plot_styles.title_pad) if title is not None else None

    # X-axis bins, only two bins
    x_ticks = [math.floor(min(_min[x_keyword].values)), math.ceil(max(_max[x_keyword].values))]
    ax.set_xlim(0, math.ceil(max(_max[x_keyword].values)))
    ax.set_xticks(x_ticks)

    # Save the figure
    vmv_plotting.save_figure(output_prefix=output_prefix, output_directory=output_directory,
                             dpi=dpi, svg=save_svg, pdf=save_pdf)

    # Reset to clean
    vmv_plotting.reset_matplotlib()


####################################################################################################
# plot_average_profiles_along_x_y_z
####################################################################################################
def plot_average_profiles_along_x_y_z(data_frame,
                                      x_keyword,
                                      x_axis_label,
                                      output_prefix,
                                      output_directory,
                                      title=None):

    for i, axis in enumerate(vmv.consts.Keys.AXES):
        vmv_plotting.plot_average_profile_with_range(
            data_frame=data_frame,
            y_keyword=axis,
            x_keyword=x_keyword,
            x_label=x_axis_label,
            y_label=r'Distance along %s-axis ($\mu$m)' % axis,
            title=title,
            output_prefix=output_prefix + '-%s' % axis,
            output_directory=output_directory,
            light_color=vmv.consts.Color.CM_LIGHT_COLORS[i],
            dark_color=vmv.consts.Color.CM_DARK_COLORS[i])


