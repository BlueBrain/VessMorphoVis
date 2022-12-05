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
import pandas
from matplotlib import pyplot, patches

# Internal imports
from vmv.consts import Suffix
import vmv.analysis.plotting as vmv_plotting
import vmv.utilities


####################################################################################################
# @plot_scatter
####################################################################################################
def plot_scatter(data_frame,
                 x_keyword,
                 y_keyword,
                 x_label,
                 y_label,
                 output_prefix,
                 output_directory,
                 title=None,
                 fig_size=(10, 10),
                 dpi=vmv.consts.Image.DPI,
                 light_color=vmv.consts.Color.CM_BLUE_LIGHT,
                 dark_color=vmv.consts.Color.CM_BLUE_DARK,
                 plot_styles=vmv.utilities.PlotStyle(),
                 save_pdf=False,
                 save_svg=False):

    # Set the styles
    vmv_plotting.set_plotting_styles(plot_styles=plot_styles)

    # Construct the figure
    fig, ax = pyplot.subplots(1, 1)
    fig.set_size_inches(fig_size[0], fig_size[1])
    fig.set_tight_layout('w_pad')

    # Plot
    xdata = data_frame[x_keyword]
    ydata = data_frame[y_keyword]
    ax.scatter(xdata, ydata, marker='+', color=dark_color)

    # Set the axis style
    vmv_plotting.add_default_axis_styles(ax=ax, plot_styles=plot_styles)
    ax.set_xlim(left=0)

    # Text
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title, pad=plot_styles.title_pad) if title is not None else None

    # Save the figure
    vmv_plotting.save_figure(output_prefix='%s%s' % (output_prefix, Suffix.SCATTER),
                             output_directory=output_directory,
                             dpi=dpi, svg=save_svg, pdf=save_pdf)

    # Reset to clean
    vmv_plotting.reset_matplotlib()


####################################################################################################
# plot_scatter_data_along_x_y_z
####################################################################################################
def plot_scatter_data_along_x_y_z(data_frame,
                                  x_keyword,
                                  output_prefix,
                                  output_directory,
                                  x_label,
                                  title=None,
                                  fig_size=(10, 10),
                                  dpi=vmv.consts.Image.DPI,
                                  light_color=vmv.consts.Color.CM_BLUE_LIGHT,
                                  dark_color=vmv.consts.Color.CM_BLUE_DARK,
                                  plot_styles=vmv.utilities.PlotStyle(),
                                  save_pdf=False,
                                  save_svg=False):

    for i, axis in enumerate(vmv.consts.Keys.AXES):
        plot_scatter(
            data_frame=data_frame,
            x_keyword=x_keyword, y_keyword=axis,
            x_label=x_label, y_label=r'Distance along %s-axis ($\mu$m)' % axis,
            output_prefix=output_prefix + '-%s' % axis,
            output_directory=output_directory,
            title=title, fig_size=fig_size, dpi=dpi,
            light_color=vmv.consts.Color.CM_LIGHT_COLORS[i],
            dark_color=vmv.consts.Color.CM_DARK_COLORS[i],
            plot_styles=plot_styles, save_pdf=save_pdf, save_svg=save_svg)


####################################################################################################
# @plot_scatter_data_with_closeups
####################################################################################################
def plot_scatter_data_with_closeups_if_needed(data_frame,
                                              x_keyword,
                                              y_keyword,
                                              x_label,
                                              y_label,
                                              output_prefix,
                                              output_directory,
                                              title=None,
                                              fig_size=(10, 10),
                                              dpi=vmv.consts.Image.DPI,
                                              light_color=vmv.consts.Color.CM_BLUE_LIGHT,
                                              dark_color=vmv.consts.Color.CM_BLUE_DARK,
                                              plot_styles=vmv.utilities.PlotStyle(),
                                              save_pdf=False,
                                              save_svg=False):

    # Set the styles
    vmv_plotting.set_plotting_styles(plot_styles=plot_styles)

    # Get the data columns
    xdata = data_frame[x_keyword]
    ydata = data_frame[y_keyword]

    # Check if the X-data has points between 0 and 1
    number_points = 0
    for x in xdata:
        if 1 > x > 0:
            number_points += 1

    # Use the normal scatter plot. Otherwise, use the closeups to show the data
    if number_points == 0:
        plot_scatter(data_frame=data_frame,
                     x_keyword=x_keyword, y_keyword=y_keyword, x_label=x_label, y_label=y_label,
                     output_prefix=output_prefix, output_directory=output_directory,
                     title=title,  fig_size=fig_size, dpi=dpi,
                     light_color=light_color, dark_color=dark_color,
                     plot_styles=plot_styles, save_pdf=save_pdf, save_svg=save_svg)
        return

    # Construct the figure
    fig, (ax1, ax2) = pyplot.subplots(1, 2, sharey=True, gridspec_kw={'width_ratios': [3, 1]})
    fig.set_size_inches(fig_size[0], fig_size[1])
    fig.set_tight_layout('w_pad')

    # Plot
    ax1.scatter(xdata, ydata, marker='+', linewidth=1, color=dark_color, alpha=0.5)
    ax1.set_xlim(left=0)

    # Set the axis style
    vmv_plotting.add_default_axis_styles(ax=ax1, plot_styles=plot_styles)
    ax1.grid(axis='y')

    # Text
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.set_title(title, pad=plot_styles.title_pad) if title is not None else None

    # X-axis bins, only two bins
    xbins = [0, math.ceil(max(xdata))]
    ax1.set_xlim(0, math.ceil(max(xdata)))
    ax1.set_xticks(xbins)

    # Add the closeup to the right
    ax2.scatter(xdata, ydata,
                marker=plot_styles.scatter_plot_marker, linewidth=1,
                color=dark_color, alpha=0.75, zorder=10)

    # Adding the plot style for the patch
    vmv_plotting.add_patch_styles(ax=ax2, plot_styles=plot_styles)
    ax2.add_patch(patches.Rectangle((0, min(ydata)),
                                    width=1.0, height=max(ydata) - min(ydata),
                                    linewidth=plot_styles.line_width,
                                    facecolor='white', edgecolor='black', zorder=0))

    # Save the figure
    vmv_plotting.save_figure(output_prefix='%s%s' % (output_prefix, Suffix.SCATTER),
                             output_directory=output_directory,
                             dpi=dpi, svg=save_svg, pdf=save_pdf)

    # Reset to clean
    vmv_plotting.reset_matplotlib()


####################################################################################################
# plot_scatter_data_with_closeups_if_needed_along_x_y_z
####################################################################################################
def plot_scatter_data_with_closeups_if_needed_along_x_y_z(
        data_frame,
        x_keyword,
        output_prefix,
        output_directory,
        x_label,
        title=None,
        fig_size=(10, 10),
        dpi=vmv.consts.Image.DPI,
        light_color=vmv.consts.Color.CM_BLUE_LIGHT,
        dark_color=vmv.consts.Color.CM_BLUE_DARK,
        plot_styles=vmv.utilities.PlotStyle(),
        save_pdf=False,
        save_svg=False):

    for i, axis in enumerate(vmv.consts.Keys.AXES):
        plot_scatter_data_with_closeups_if_needed(
            data_frame=data_frame,
            x_keyword=x_keyword, y_keyword=axis,
            x_label=x_label, y_label=r'Distance along %s-axis ($\mu$m)' % axis,
            output_prefix=output_prefix + '-%s' % axis,
            output_directory=output_directory,
            title=title, fig_size=fig_size, dpi=dpi,
            light_color=vmv.consts.Color.CM_LIGHT_COLORS[i],
            dark_color=vmv.consts.Color.CM_DARK_COLORS[i],
            plot_styles=plot_styles, save_pdf=save_pdf, save_svg=save_svg)


####################################################################################################
# @plot_range_data
####################################################################################################
def plot_range_data(data_frame,
                    y_key,
                    min_keyword,
                    mean_keyword,
                    max_keyword,
                    x_label,
                    y_label,
                    output_prefix,
                    output_directory,
                    title=None,
                    fig_size=(10, 10),
                    dpi=vmv.consts.Image.DPI,
                    light_color=vmv.consts.Color.CM_BLUE_LIGHT,
                    dark_color=vmv.consts.Color.CM_BLUE_DARK,
                    plot_styles=vmv.utilities.PlotStyle(),
                    save_pdf=False,
                    save_svg=False):

    # Sort the data-frame by the given axis
    df_sorted = data_frame.sort_values(by=[y_key], inplace=False)

    # Independent axis
    ydata = df_sorted[y_key]

    # Data: minimum, average and maximum
    xdata_min = df_sorted[min_keyword]
    xdata_avg = df_sorted[mean_keyword]
    xdata_max = df_sorted[max_keyword]

    # Construct the error bars
    error_min = list()
    error_max = list()
    for i_avg, i_max, i_min in zip(xdata_avg, xdata_max, xdata_min):
        error_max.append(i_max - i_avg)
        error_min.append(i_avg - i_min)
    asymmetric_error = [error_min, error_max]

    # Set the styles
    vmv_plotting.set_plotting_styles(plot_styles=plot_styles)

    # Construct the figure
    fig, ax = pyplot.subplots(1, 1)
    fig.set_size_inches(fig_size[0], fig_size[1])
    fig.set_tight_layout('w_pad')

    # Plot
    ax.errorbar(xdata_avg, ydata, xerr=asymmetric_error, fmt='.',
                color=light_color, ecolor=dark_color, alpha=0.75, zorder=1)
    ax.set_xlim(left=0)

    # Set the axis style
    vmv_plotting.add_default_axis_styles(ax=ax, plot_styles=plot_styles)

    # Text
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title, pad=plot_styles.title_pad) if title is not None else None

    # Save the figure
    png_image_path = vmv_plotting.save_figure(
        output_prefix='%s%s' % (output_prefix, Suffix.RANGE), output_directory=output_directory,
        dpi=dpi, svg=save_svg, pdf=save_pdf)

    # Reset to clean
    vmv_plotting.reset_matplotlib()

    return png_image_path


####################################################################################################
# plot_range_data_along_xyz
####################################################################################################
def plot_range_data_along_xyz(data_frame,
                              min_keyword,
                              mean_keyword,
                              max_keyword,
                              x_label,
                              output_prefix,
                              output_directory,
                              title=None,
                              fig_size=(10, 10),
                              dpi=vmv.consts.Image.DPI,
                              plot_styles=vmv.utilities.PlotStyle(),
                              save_pdf=False,
                              save_svg=False):
    # A list that will contain the paths of the resulting imagers
    results = list()

    for i, axis in enumerate(vmv.consts.Keys.AXES):

        results.append(plot_range_data(data_frame,
                        y_key=axis,
                        min_keyword=min_keyword,
                        mean_keyword=mean_keyword,
                        max_keyword=max_keyword,
                        x_label=x_label, y_label=r'Distance along %s-axis ($\mu$m)' % axis,
                        output_prefix=output_prefix + '-%s' % axis,
                        output_directory=output_directory,
                        title=title, fig_size=fig_size, dpi=dpi,
                        light_color=vmv.consts.Color.CM_LIGHT_COLORS[i],
                        dark_color=vmv.consts.Color.CM_DARK_COLORS[i],
                        plot_styles=plot_styles, save_pdf=save_pdf, save_svg=save_svg))
    return results


####################################################################################################
# @plot_scatter
####################################################################################################
def plot_range_and_scatter_combined(data_frame,
                                    x_keyword,
                                    y_keyword,
                                    x_label,
                                    y_label,

                                    output_prefix,
                                    output_directory,
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

    # Sort the data-frame by the Y-axis
    data_frame = data_frame.sort_values(by=[y_keyword])

    # Get references to the X and Y data, for the scatter plots
    xdata = data_frame[x_keyword]
    ydata = data_frame[y_keyword]

    # Construct the groups
    groups = data_frame.groupby(pandas.cut(data_frame[y_keyword],
                                           bins=len(ydata) if len(ydata) < 50 else bins))
    _mean = groups.mean()
    _min = groups.min()
    _max = groups.max()
    p_min = _min[x_keyword].values
    p_max = _max[x_keyword].values

    # Do we need an inset for the closeup between 0 and 1
    min_x_value = min(xdata)
    max_x_value = max(xdata)
    if min_x_value < 1.0 and max_x_value > 1.0:
        fig, (ax1, ax2, ax3) = pyplot.subplots(1, 3, sharey=True,
                                               gridspec_kw={'width_ratios': [3, 3, 1]})
    else:
        # Construct the figure
        fig, (ax1, ax2) = pyplot.subplots(1, 2, sharey=True,
                                          gridspec_kw={'width_ratios': [1, 1]})

    # Figure size
    fig.set_size_inches(fig_size[0], fig_size[1])
    fig.set_tight_layout('w_pad')

    # Plot the range data and set the styles
    ax1.plot(_mean[x_keyword].values, _mean[y_keyword].values, color=dark_color)
    ax1.fill_betweenx(_mean[y_keyword].values, p_max, p_min, color=light_color, alpha=0.75)
    vmv_plotting.add_default_axis_styles(ax=ax1, plot_styles=plot_styles)
    ax1.set_xlim(left=0)
    ax1.set_xlim(right=1.0) if max_x_value <= 1.0 else None

    # Plot the scatter data and set the styles
    xdata = data_frame[x_keyword]
    ydata = data_frame[y_keyword]
    ax2.scatter(xdata, ydata, marker='+', color=dark_color)
    vmv_plotting.add_default_axis_styles(ax=ax2, plot_styles=plot_styles)
    ax2.set_xlim(left=0)
    ax2.set_xlim(right=1.0) if max_x_value <= 1.0 else None

    # Add the closeup to the right, if needed
    if min_x_value < 1.0 and max_x_value > 1.0:
        ax3.scatter(xdata, ydata,
                    marker=plot_styles.scatter_plot_marker, linewidth=1,
                    color=dark_color, alpha=0.75, zorder=10)

        # Adding the plot style for the patch
        vmv_plotting.add_patch_styles(ax=ax3, plot_styles=plot_styles)
        ax3.add_patch(patches.Rectangle((0, min(ydata)),
                                        width=1.0, height=max(ydata) - min(ydata),
                                        linewidth=plot_styles.line_width,
                                        facecolor='white', edgecolor='black', zorder=0))

    # Text
    fig.text(0.5, -0.05, x_label, ha='center', va='center', fontsize=plot_styles.font_size)
    ax1.set_ylabel(y_label)
    ax1.set_title(title, pad=plot_styles.title_pad) if title is not None else None

    # Save the figure
    png_image_path = vmv_plotting.save_figure(
        output_prefix='%s%s' % (output_prefix, Suffix.DISTRIBUTION),
        output_directory=output_directory, dpi=dpi, svg=save_svg, pdf=save_pdf)

    # Reset to clean
    vmv_plotting.reset_matplotlib()

    return png_image_path


####################################################################################################
# plot_range_and_scatter_combined_along_xyz
####################################################################################################
def plot_range_and_scatter_combined_along_xyz(data_frame,
                                              x_keyword,
                                              output_prefix,
                                              output_directory,
                                              x_label,
                                              title=None,
                                              bins=50,
                                              fig_size=(10, 10),
                                              dpi=vmv.consts.Image.DPI,
                                              plot_styles=vmv.utilities.PlotStyle(),
                                              save_pdf=False,
                                              save_svg=False):

    # A list that will contain the paths of the resulting imagers
    results = list()

    for i, axis in enumerate(vmv.consts.Keys.AXES):
        results.append(plot_range_and_scatter_combined(
            data_frame=data_frame,
            x_keyword=x_keyword, y_keyword=axis,
            x_label=x_label, y_label=r'Distance along %s-axis ($\mu$m)' % axis,
            output_prefix=output_prefix + '-%s' % axis,
            output_directory=output_directory,
            title=title, bins=bins, fig_size=fig_size, dpi=dpi,
            light_color=vmv.consts.Color.CM_LIGHT_COLORS[i],
            dark_color=vmv.consts.Color.CM_DARK_COLORS[i],
            plot_styles=plot_styles, save_pdf=save_pdf, save_svg=save_svg))

    return results