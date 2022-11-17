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
import os
import math
import numpy
import seaborn
import pandas
import matplotlib.pyplot as pyplot
import matplotlib.cm as colormap

# Internal imports
from vmv.consts import Suffix
import vmv.utilities
import vmv.analysis.plotting as vmv_plotting


####################################################################################################
# @plot_histogram_with_box_plot
####################################################################################################
def plot_histogram_with_box_plot(data_frame,
                                 data_key,
                                 output_prefix,
                                 output_directory,
                                 y_label,
                                 x_label='Count',
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

    # Create a new figure and adjust its size
    fig, (ax1, ax2) = pyplot.subplots(1, 2, sharey=True, gridspec_kw={'width_ratios': [3, 1]})
    fig.set_size_inches(fig_size[0], fig_size[1])
    fig.set_tight_layout('w_pad')

    # Get the data, with which the histogram will be drawn
    data = data_frame[data_key]

    # Add the histogram (ax1)
    x, y, _ = ax1.hist(data, color=dark_color, orientation='horizontal', edgecolor='white',
                       bins=bins, zorder=3)

    # Set the axis style
    vmv_plotting.add_default_axis_styles(ax=ax1, plot_styles=plot_styles)

    # Text
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.set_title(title, pad=plot_styles.title_pad) if title is not None else None

    # Add box-plot (ax2)
    bp = ax2.boxplot(data, showfliers=True,
                     flierprops=dict(marker=plot_styles.box_plot_marker,
                                     markersize=plot_styles.box_plot_marker_size,
                                     alpha=plot_styles.box_plot_alpha,
                                     markerfacecolor=light_color,
                                     markeredgecolor=dark_color))

    # Styles for the box-plot
    for spine in ['left', 'right', 'top', 'bottom']:
        ax2.spines[spine].set_visible(False)
    for box in bp['boxes']:
        box.set(color=dark_color, linewidth=plot_styles.line_width * 0.6)
    for whisker in bp['whiskers']:
        whisker.set(color=dark_color, linewidth=plot_styles.line_width * 0.5)
    for cap in bp['caps']:
        cap.set(color=dark_color, linewidth=plot_styles.line_width * 0.65,
                xdata=cap.get_xdata() + (-0.01, 0.01))
    for median in bp['medians']:
        median.set(color=dark_color, linewidth=plot_styles.line_width * 0.65)

    # Set its transparency to zero
    ax2.patch.set_alpha(0.0)
    ax2.tick_params(axis='both', which='both', left=False, bottom=False, labelbottom=False)
    ax2.grid(False)

    # Save the figure
    vmv_plotting.save_figure(output_prefix='%s%s' % (output_prefix, Suffix.HISTOGRAM),
                             output_directory=output_directory,
                             dpi=dpi, svg=save_svg, pdf=save_pdf)

    # Reset to clean
    vmv_plotting.reset_matplotlib()


####################################################################################################
# plot_histograms_along_x_y_z
####################################################################################################
def plot_histograms_along_x_y_z(data_frame,
                                output_prefix,
                                output_directory,
                                x_label='Count',
                                title=None,
                                bins=50,
                                fig_size=(6, 10),
                                dpi=150,
                                plot_styles=vmv.utilities.PlotStyle(),
                                save_pdf=False,
                                save_svg=False):

    for i, axis in enumerate(vmv.consts.Keys.AXES):
        plot_histogram_with_box_plot(
            data_frame=data_frame,
            data_key=axis,
            output_prefix=output_prefix + '-%s' % axis,
            output_directory=output_directory,
            y_label=r'Distance along %s-axis ($\mu$m)' % axis,
            title=title, x_label=x_label,
            bins=bins, fig_size=fig_size, dpi=dpi, plot_styles=plot_styles,
            light_color=vmv.consts.Color.CM_LIGHT_COLORS[i],
            dark_color=vmv.consts.Color.CM_DARK_COLORS[i],
            save_svg=save_svg, save_pdf=save_pdf)
