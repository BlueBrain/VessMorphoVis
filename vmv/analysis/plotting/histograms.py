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
def plot_horizontal_histogram_with_box_plot(data_frame,
                                            data_key,
                                            output_prefix,
                                            output_directory,
                                            x_label,
                                            y_label='Count',
                                            title=None,
                                            bins=50,
                                            fig_size=(10, 10),
                                            dpi=vmv.consts.Image.DPI,
                                            light_color=vmv.consts.Color.CM_BLUE_LIGHT,
                                            dark_color=vmv.consts.Color.CM_BLUE_DARK,
                                            plot_styles=vmv.utilities.PlotStyle(),
                                            save_pdf=False,
                                            save_svg=False):

    # Set the styles
    vmv_plotting.set_plotting_styles(plot_styles=plot_styles)

    # Create a new figure and adjust its size
    fig, (ax1, ax2) = pyplot.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [1, 3]})
    fig.set_size_inches(fig_size[0], fig_size[1])
    fig.set_tight_layout('h_pad')

    # Get the data, with which the histogram will be drawn
    data = data_frame[data_key]

    # Add box-plot (ax2)
    bp = ax1.boxplot(data, showfliers=True, vert=False,
                     flierprops=dict(marker=plot_styles.box_plot_marker,
                                     markersize=plot_styles.box_plot_marker_size,
                                     alpha=plot_styles.box_plot_alpha,
                                     markerfacecolor=light_color,
                                     markeredgecolor=dark_color))

    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)

    # Styles for the box-plot
    for spine in ['left', 'right', 'top', 'bottom']:
        ax1.spines[spine].set_visible(False)
    for box in bp['boxes']:
        box.set(color=dark_color, linewidth=plot_styles.line_width * 0.6)
    for whisker in bp['whiskers']:
        whisker.set(color=dark_color, linewidth=plot_styles.line_width * 0.5)
    for cap in bp['caps']:
        cap.set(color=dark_color, linewidth=plot_styles.line_width * 0.65)
    for median in bp['medians']:
        median.set(color=dark_color, linewidth=plot_styles.line_width * 0.65)

    # Shift the closeup a little to the right
    bp_position = ax1.get_position()
    #bp_position.y0 = bp_position.y0 + 0.1
    #bp_position.y1 = bp_position.y1 + 0.1
    ax1.set_position(bp_position)

    # Set its transparency to zero
    ax1.patch.set_alpha(0.0)
    ax1.tick_params(axis='both', which='both', left=False, bottom=False, labelbottom=False)
    ax1.grid(False)

    # Add the histogram (ax1)
    y, x, _ = ax2.hist(data, color=dark_color, orientation='vertical', edgecolor='white',
                       bins=bins, zorder=3)

    # X-axis ticks
    left = 0
    right = int(math.ceil(max(x)))
    #ax2.set_xlim(left=left, right=right)
    #ax2.set_xticks([left, right])

    # Y-axis ticks
    #max_y = max(y)
    #min_y = min(y)
    #if 1 >= min_y >= 0 and 0 <= max_y <= 1:
    #    ax2.set_ylim(bottom=0, top=1)
    #else:
    #    ax2.set_ylim(bottom=int(math.floor(min_y)), top=int(math.ceil(max_y)))

    # Set the axis style
    # vmv_plotting.add_default_axis_styles(ax=ax1, plot_styles=plot_styles)

    for spine in ['left', 'bottom']:
        ax2.spines[spine].set_position(('outward', plot_styles.spines_shift))
        ax2.spines[spine].set_color('black')
        ax2.spines[spine].set_linewidth(plot_styles.line_width)
    for spine in ['right', 'top']:
        ax2.spines[spine].set_visible(False)
    ax2.tick_params(axis='both', which='both', bottom=True, left=True,
                    width=plot_styles.line_width, length=plot_styles.tick_length)
    ax2.grid(axis='x')

    # Text
    ax2.set_xlabel(x_label)
    ax2.set_ylabel(y_label)
    ax1.set_title(title, pad=plot_styles.title_pad) if title is not None else None

    # Save the figure
    vmv_plotting.save_figure(output_prefix='%s%s' % (output_prefix, Suffix.HISTOGRAM),
                             output_directory=output_directory,
                             dpi=dpi, svg=save_svg, pdf=save_pdf)

    # Reset to clean
    vmv_plotting.reset_matplotlib()


####################################################################################################
# plot_histograms_along_x_y_z
####################################################################################################
def plot_horizontal_histogram_along_x_y_z(data_frame,
                                          output_prefix,
                                          output_directory,
                                          label='Count',
                                          title=None,
                                          bins=50,
                                          fig_size=(10, 10),
                                          dpi=vmv.consts.Image.DPI,
                                          plot_styles=vmv.utilities.PlotStyle(),
                                          save_pdf=False,
                                          save_svg=False):

    for i, axis in enumerate(vmv.consts.Keys.AXES):
        plot_horizontal_histogram_with_box_plot(
            data_frame=data_frame,
            data_key=axis,
            output_prefix=output_prefix + '-%s' % axis,
            output_directory=output_directory,
            title=title, x_label=r'Distance along %s-axis ($\mu$m)' % axis, y_label=label,
            bins=bins, fig_size=fig_size, dpi=dpi, plot_styles=plot_styles,
            light_color=vmv.consts.Color.CM_LIGHT_COLORS[i],
            dark_color=vmv.consts.Color.CM_DARK_COLORS[i],
            save_svg=save_svg, save_pdf=save_pdf)


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
                                 fig_size=(10, 10),
                                 dpi=vmv.consts.Image.DPI,
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

    # X-axis ticks
    left = 0
    right = math.ceil(max(x))
    ax1.set_xlim(left=left, right=right)
    ax1.set_xticks([left, right])

    # Y-axis ticks
    max_y = max(y)
    min_y = min(y)
    if 1 >= min_y >= 0 and 0 <= max_y <= 1:
        ax1.set_ylim(bottom=0, top=1)
    else:
        ax1.set_ylim(bottom=math.floor(min_y), top=math.ceil(max_y))

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

    # Save the figure and return the path of the resulting PNG image
    png_image_path = vmv_plotting.save_figure(
        output_prefix='%s%s' % (output_prefix, Suffix.HISTOGRAM), output_directory=output_directory,
        dpi=dpi, svg=save_svg, pdf=save_pdf)

    # Reset to clean
    vmv_plotting.reset_matplotlib()

    # Return the path to the PNG image
    return png_image_path


####################################################################################################
# plot_histograms_along_x_y_z
####################################################################################################
def plot_histograms_along_x_y_z(data_frame,
                                output_prefix,
                                output_directory,
                                x_label='Count',
                                title=None,
                                bins=50,
                                fig_size=(10, 10),
                                dpi=vmv.consts.Image.DPI,
                                plot_styles=vmv.utilities.PlotStyle(),
                                save_pdf=False,
                                save_svg=False):

    results = list()
    for i, axis in enumerate(vmv.consts.Keys.AXES):
        results.append(plot_histogram_with_box_plot(
            data_frame=data_frame,
            data_key=axis,
            output_prefix=output_prefix + '-%s' % axis,
            output_directory=output_directory,
            y_label=r'Distance along %s-axis ($\mu$m)' % axis,
            title=title, x_label=x_label,
            bins=bins, fig_size=fig_size, dpi=dpi, plot_styles=plot_styles,
            light_color=vmv.consts.Color.CM_LIGHT_COLORS[i],
            dark_color=vmv.consts.Color.CM_DARK_COLORS[i],
            save_svg=save_svg, save_pdf=save_pdf))

    return results
