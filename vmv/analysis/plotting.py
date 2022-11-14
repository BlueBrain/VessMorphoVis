####################################################################################################
# Copyright (c) 2019 - 2020, EPFL / Blue Brain Project
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
import matplotlib.pyplot as pyplot
import matplotlib.font_manager as font_manager
import matplotlib.cm as colormap

# Internal imports
import vmv.consts
import vmv.utilities


####################################################################################################
# @load_fonts
####################################################################################################
def load_fonts():
    """Imports all the fonts required for plotting.
    """

    # Import the fonts
    font_dirs = [os.path.dirname(vmv.consts.Paths.FONTS_DIRECTORY)]
    font_dirs.extend([os.path.dirname(os.path.realpath(__file__)) + '/../fonts/'])
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)


####################################################################################################
# @read_dist_file
####################################################################################################
def read_dist_file(file_path,
                   invert=False):
    """Reads the distribution file into a list.

    :param file_path:
        The path to the input file.
    :param invert:
        If set to True, invert the read values.
    :return:
    """

    # Data list
    data = list()

    # Open the file
    f = open(file_path, 'r')
    for line in f:
        if 'inf' in line:
            continue
        content = line.strip(' ').split(' ')
        value = float(content[1])
        if invert:
            value = 1.0 / value
        data.append(value)
    f.close()

    # Return a list of the data read from the file
    return data


####################################################################################################
# @set_styles
####################################################################################################
def set_styles(font='Arial',
               font_size=30,
               axes_grid=False,
               axes_linewidth=2):
    """Sets the styles for plotting a figure.

    :param font:
        Font name.
    :param font_size:
        Font size, default 30.
    :param axes_grid:
        Whether the grid is on or off, default = False.
    :param axes_linewidth:
        The width of all lines in a figure, default 2.
    """
    pyplot.rcParams['axes.grid'] = axes_grid
    pyplot.rcParams['grid.linestyle'] = '-'
    pyplot.rcParams['font.family'] = font
    pyplot.rcParams['axes.linewidth'] = axes_linewidth
    pyplot.rcParams['axes.labelweight'] = 'regular'
    pyplot.rcParams['axes.labelsize'] = font_size
    pyplot.rcParams['xtick.labelsize'] = font_size
    pyplot.rcParams['ytick.labelsize'] = font_size
    pyplot.rcParams['legend.fontsize'] = font_size
    pyplot.rcParams['axes.titlesize'] = font_size
    pyplot.rcParams['axes.autolimit_mode'] = 'round_numbers'


def plot_scatter_data_with_closeups(df,
                                    idep_keyword,
                                    dep_keyword,
                                    idep_axis_label,
                                    dep_axis_label,
                                    font_size=30,
                                    figure_width=10,
                                    figure_height=10,
                                    spines_shift=10,
                                    line_width=2,
                                    light_color='r',
                                    dark_color='b',
                                    output_directory="",
                                    output_prefix="",
                                    dpi=300,
                                    save_pdf=False,
                                    save_svg=False):

    # Set the default styles
    set_styles(font_size=font_size, axes_linewidth=line_width)

    # Create a new figure and adjust its size
    fig, (ax1, ax2) = pyplot.subplots(1, 2, sharey=True)
    fig.set_size_inches(figure_width, figure_height)

    # Sort the dataframe by the given axis
    df_sorted = df.sort_values(by=[idep_keyword], inplace=False)

    # Independent axis
    indep = df_sorted[idep_keyword]

    # Data
    data = df_sorted[dep_keyword]

    # Plot
    ax1.errorbar(data, indep, fmt='+', color=light_color,
                 ecolor=dark_color,
                 alpha=0.75, zorder=1)

    # Adjust the spine parameters
    for spine in ['left', 'bottom']:
        ax1.spines[spine].set_position(('outward', spines_shift))
        ax1.spines[spine].set_color('black')
        ax1.spines[spine].set_linewidth(2)
    for spine in ['right', 'top']:
        ax1.spines[spine].set_visible(False)
    ax1.tick_params(axis='both', width=line_width, length=5, which='both', bottom=True,
                    left=True)
    ax1.grid(False)
    # ax1.set_ylabel(label, labelpad=5)

    ax1.set_ylabel(idep_axis_label)
    ax1.set_xlabel(dep_axis_label)

    # X-axis bins, only two bins
    xbins = [0, math.ceil(max(data))]
    ax1.grid(axis='y')
    ax1.set_xlim(0, math.ceil(max(data)))
    ax1.set_xticks(xbins)

    # Set the title
    # ax1.set_title(title, pad=25)

    # Add the closeup to the right
    h21 = ax2.errorbar(data, indep, fmt='+', color=light_color, alpha=0.75, zorder=10,
                       label='Mean Radius')

    # Adjust the spine parameters
    for spine in ['left', 'bottom']:
        ax2.spines[spine].set_position(('outward', spines_shift))
        ax2.spines[spine].set_color('black')
        ax2.spines[spine].set_linewidth(2)
    for spine in ['left', 'top', 'right']:
        ax2.spines[spine].set_visible(False)
    ax2.tick_params(axis='both', width=2, which='both', bottom=True, left=False)
    ax2.set_xlim(left=-0.1, right=1.1)
    ax2.axes.get_yaxis().set_visible(False)
    ax2.grid(False)

    if -1e-10 < min(indep) < 1e-10:
        ax1.set_ylim(bottom=0)
        ax2.set_ylim(bottom=0)

    # Shift the closeup a little to the right
    bp_position = ax2.get_position()
    bp_position.x0 = bp_position.x0 + 0.025
    bp_position.x1 = bp_position.x1 + 0.025
    ax2.set_position(bp_position)

    from matplotlib import patches
    rectangle = patches.Rectangle((0, min(indep)), width=1.0, height=max(indep) - min(indep),
                                  linewidth=2,
                                  facecolor='white', edgecolor='black')
    ax2.add_patch(rectangle)

    # Save PNG by default
    pyplot.savefig('%s/distribution-%s.png' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True)

    # Save PDF
    pyplot.savefig('%s/distribution-%s.pdf' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True) if save_pdf else None

    # Save SVG
    pyplot.savefig('%s/distribution-%s.svg' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True) if save_svg else None


####################################################################################################
# @plot_range_data_xyz_with_closeups
####################################################################################################
def plot_range_data_closeups(df,
                              data_key,
                              min_keyword='Min',
                              mean_keyword='Mean',
                              max_keyword='Max',
                              label="",
                              title="",
                              font_size=30,
                              figure_width=8,
                              figure_height=10,
                              spines_shift=10,
                              line_width=2,
                              dpi=300,
                              light_color='r',
                              dark_color='b',
                              output_directory="",
                              output_prefix="",
                              save_pdf=False,
                              save_svg=False):

    # Construct the color-maps
    #pastel1 = colormap.get_cmap('Pastel1')
    #set1 = colormap.get_cmap('Set1')
    #light_colors = [pastel1.colors[0], pastel1.colors[2], pastel1.colors[1]]
    #dark_colors = [set1.colors[0], set1.colors[2], set1.colors[1]]

    #for ii, axis in enumerate(['X', 'Y', 'Z']):
    #    light_color = light_colors[ii]
    #    dark_color = dark_colors[ii]

    # Set the default styles
    set_styles(font_size=font_size, axes_linewidth=line_width)

    # Create a new figure and adjust its size
    fig, (ax1, ax2) = pyplot.subplots(1, 2, sharey=True)
    fig.set_size_inches(figure_width, figure_height)

    # Sort the dataframe by the given axis
    df_sorted = df.sort_values(by=[data_key], inplace=False)

    # Independent axis
    indep = df_sorted[data_key]

    # Data: minimum, average and maximum
    dmin = df_sorted[min_keyword]
    davg = df_sorted[mean_keyword]
    dmax = df_sorted[max_keyword]

    # Construct the error bars
    error_min = list()
    error_max = list()
    for iavg, imax, imin in zip(davg, dmax, dmin):
        error_max.append(imax - iavg)
        error_min.append(iavg - imin)
    asymmetric_error = [error_min, error_max]

    # Plot
    ax1.errorbar(davg, indep, xerr=asymmetric_error, fmt='.', color=light_color,
                 ecolor=dark_color,
                 alpha=0.75, zorder=1)

    # Adjust the spine parameters
    for spine in ['left', 'bottom']:
        ax1.spines[spine].set_position(('outward', spines_shift))
        ax1.spines[spine].set_color('black')
        ax1.spines[spine].set_linewidth(2)
    for spine in ['right', 'top']:
        ax1.spines[spine].set_visible(False)
    ax1.tick_params(axis='both', width=line_width, length=5, which='both', bottom=True,
                    left=True)
    ax1.grid(False)
    ax1.set_ylabel(label, labelpad=5)

    min_x = min(dmin)
    max_x = max(dmax)
    range_ = max_x - min_x
    if 0.1 * range_ > min_x > 0:
        ax1.set_xlim(left=0)

    # Set the title
    ax1.set_title(title, pad=25)

    # Add the closeup to the right
    h21 = ax2.errorbar(davg, indep, fmt='.', color=light_color, alpha=0.75, zorder=10,
                       label='Mean Radius')
    h22 = ax2.errorbar(dmin, indep, fmt='+', color=light_color, alpha=0.75, zorder=10,
                       label='Minimum Radius')
    ax2.legend(numpoints=1, facecolor='white', framealpha=0.75,
               bbox_to_anchor=(0, 0.9, 1., .102), loc=0, labelspacing=0.25,
               handlelength=0.2, handletextpad=0.5, frameon=True,
               fontsize=int(font_size * 0.75)).set_zorder(100)

    # Adjust the spine parameters
    for spine in ['left', 'bottom']:
        ax2.spines[spine].set_position(('outward', spines_shift))
        ax2.spines[spine].set_color('black')
        ax2.spines[spine].set_linewidth(2)
    for spine in ['left', 'top', 'right']:
        ax2.spines[spine].set_visible(False)
    ax2.tick_params(axis='both', width=2, which='both', bottom=True, left=False)
    ax2.set_xlim(left=-0.1, right=1.1)
    ax2.axes.get_yaxis().set_visible(False)
    ax2.grid(False)

    if -1e-10 < min(indep) < 1e-10:
        ax1.set_ylim(bottom=0)
        ax2.set_ylim(bottom=0)

    # Shift the closeup a little to the right
    bp_position = ax2.get_position()
    bp_position.x0 = bp_position.x0 + 0.025
    bp_position.x1 = bp_position.x1 + 0.025
    ax2.set_position(bp_position)

    from matplotlib import patches
    rectangle = patches.Rectangle((0, min(indep)), width=1.0, height=max(indep) - min(indep),
                                  linewidth=1, facecolor='white', edgecolor='black')
    ax2.add_patch(rectangle)

    # Save PNG by default
    pyplot.savefig('%s/%s.png' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True)

    # Save PDF
    pyplot.savefig('%s/%s.pdf' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True) if save_pdf else None

    # Save SVG
    pyplot.savefig('%s/%s.svg' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True) if save_svg else None


####################################################################################################
# @plot_range_data_xyz_with_closeups
####################################################################################################
def plot_range_data_xyz_with_closeups(df,
                                      min_keyword='Min',
                                      mean_keyword='Mean',
                                      max_keyword='Max',
                                      label="",
                                      title="",
                                      font_size=30,
                                      figure_width=8,
                                      figure_height=10,
                                      spines_shift=10,
                                      line_width=2,
                                      dpi=300,
                                      output_directory="",
                                      output_prefix="",
                                      save_pdf=False,
                                      save_svg=False):

    # Construct the color-maps
    pastel1 = colormap.get_cmap('Pastel1')
    set1 = colormap.get_cmap('Set1')
    light_colors = [pastel1.colors[0], pastel1.colors[2], pastel1.colors[1]]
    dark_colors = [set1.colors[0], set1.colors[2], set1.colors[1]]

    for ii, axis in enumerate(['X', 'Y', 'Z']):
        light_color = light_colors[ii]
        dark_color = dark_colors[ii]

        # Set the default styles
        set_styles(font_size=font_size, axes_linewidth=line_width)

        # Create a new figure and adjust its size
        fig, (ax1, ax2) = pyplot.subplots(1, 2, sharey=True)
        fig.set_size_inches(figure_width, figure_height)

        # Sort the dataframe by the given axis
        df_sorted = df.sort_values(by=[axis], inplace=False)

        # Independent axis
        indep = df_sorted[axis]

        # Data: minimum, average and maximum
        dmin = df_sorted[min_keyword]
        davg = df_sorted[mean_keyword]
        dmax = df_sorted[max_keyword]

        # Construct the error bars
        error_min = list()
        error_max = list()
        for iavg, imax, imin in zip(davg, dmax, dmin):
            error_max.append(imax - iavg)
            error_min.append(iavg - imin)
        asymmetric_error = [error_min, error_max]

        # Plot
        ax1.errorbar(davg, indep, xerr=asymmetric_error, fmt='.', color=light_color,
                     ecolor=dark_color,
                     alpha=0.75, zorder=1)

        # Adjust the spine parameters
        for spine in ['left', 'bottom']:
            ax1.spines[spine].set_position(('outward', spines_shift))
            ax1.spines[spine].set_color('black')
            ax1.spines[spine].set_linewidth(2)
        for spine in ['right', 'top']:
            ax1.spines[spine].set_visible(False)
        ax1.tick_params(axis='both', width=line_width, length=5, which='both', bottom=True,
                        left=True)
        ax1.set_xlim(left=0, right=max(dmax))
        ax1.grid(False)
        ax1.set_ylabel(label, labelpad=5)

        if -1e-10 < min(indep) < 1e-10:
            ax1.set_ylim(bottom=0)
            ax2.set_ylim(bottom=0)

        # Set the title
        ax1.set_title(title, pad=25)

        # Add the closeup to the right
        h21 = ax2.errorbar(davg, indep, fmt='.', color=light_color, alpha=0.9,
                           label='Mean Radius')
        h22 = ax2.errorbar(dmin, indep, fmt='+', color=dark_color, alpha=0.9,
                           label='Minimum Radius')
        ax2.legend(loc='upper left', numpoints=1)
        ax2.legend(bbox_to_anchor=(0, 1.05, 1., .102), loc=0, labelspacing=0.25,
                   handlelength=0.2, handletextpad=0.5, frameon=False,
                   fontsize=int(font_size * 0.75))

        # Adjust the spine parameters
        for spine in ['left', 'bottom']:
            ax2.spines[spine].set_position(('outward', spines_shift))
            ax2.spines[spine].set_color('black')
            ax2.spines[spine].set_linewidth(2)
        for spine in ['left', 'top', 'right']:
            ax2.spines[spine].set_visible(False)
        ax2.tick_params(axis='both', width=2, which='both', bottom=True, left=False)
        ax2.set_xlim(left=-0.1, right=1.1)
        ax2.axes.get_yaxis().set_visible(False)
        ax2.grid(False)

        # Shift the closeup a little to the right
        bp_position = ax2.get_position()
        bp_position.x0 = bp_position.x0 + 0.025
        bp_position.x1 = bp_position.x1 + 0.025
        ax2.set_position(bp_position)

        # Add the inset
        x1, y1 = [-0.1, -0.1], [min(indep), max(indep)]
        x2, y2 = [1.1, 1.1], [min(indep), max(indep)]
        x3, y3 = [-0.1, 1.1], [min(indep), min(indep)]
        x4, y4 = [-0.1, 1.1], [max(indep), max(indep)]
        pyplot.plot(x1, y1, x2, y2, linestyle='dashed', color='k', linewidth=2)
        pyplot.plot(x3, y3, x4, y4, linestyle='dashed', color='k', linewidth=2)

        # Save PNG by default
        pyplot.savefig('%s/distribution-%s-%s.png' % (output_directory, output_prefix, axis),
                       dpi=dpi, bbox_inches='tight', transparent=True)

        # Save PDF
        pyplot.savefig('%s/distribution-%s-%s.pdf' % (output_directory, output_prefix, axis),
                       dpi=dpi, bbox_inches='tight', transparent=True) if save_pdf else None

        # Save SVG
        pyplot.savefig('%s/distribution-%s-%s.svg' % (output_directory, output_prefix, axis),
                       dpi=dpi, bbox_inches='tight', transparent=True) if save_svg else None


####################################################################################################
# @plot_normalized_histogram
####################################################################################################
def plot_normalized_histogram(data,
                              output_directory,
                              output_prefix,
                              title=None,
                              figure_width=3,
                              figure_height=10,
                              bins=50,
                              color='red',
                              axvline_color='black',
                              bin_width=0.95,
                              save_pdf=False,
                              save_svg=False,
                              dpi=150):
    """Plot normalized histograms of the input data.

    :param data:
        A list of data.
    :param output_directory:
        The directory where the results will be written
    :param output_prefix:
        The output prefix.
    :param title:
        The title of the figure.
    :param figure_width:
        The width of the figure.
    :param figure_height:
        The height of the figure.
    :param bins:
        Number of bins in the histogram.
    :param color:
        The color of the histogram.
    :param axvline_color:
        The color of the Y-axis.
    :param bin_width:
        The width of the bins.
    :param save_pdf:
        Save the figure as a PDF.
    :param save_svg:
        Save the figure as an SVG file.
    :param dpi:
        The dots per inch.
    """

    load_fonts()

    font_size = 30
    seaborn.set_style("whitegrid")
    pyplot.rcParams['axes.grid'] = 'True'
    pyplot.rcParams['grid.linestyle'] = '-'
    pyplot.rcParams['grid.linewidth'] = 1.0
    pyplot.rcParams['grid.color'] = 'black'
    pyplot.rcParams['grid.alpha'] = 0.1
    pyplot.rcParams['font.family'] = 'NimbusSanL'
    pyplot.rcParams['font.style'] = 'normal'
    pyplot.rcParams['axes.labelweight'] = 'light'
    pyplot.rcParams['axes.linewidth'] = 1.0
    pyplot.rcParams['axes.labelsize'] = font_size
    pyplot.rcParams['xtick.labelsize'] = font_size * 1
    pyplot.rcParams['ytick.labelsize'] = font_size * 1
    pyplot.rcParams['legend.fontsize'] = font_size
    pyplot.rcParams['figure.titlesize'] = font_size
    pyplot.rcParams['axes.titlesize'] = font_size
    pyplot.rcParams['xtick.major.pad'] = '10'
    pyplot.rcParams['ytick.major.pad'] = '10'
    pyplot.rcParams['axes.edgecolor'] = '1'
    pyplot.rcParams['axes.autolimit_mode'] = 'round_numbers'
    pyplot.rcParams['axes.xmargin'] = 0
    pyplot.rcParams['axes.ymargin'] = 0

    # Compute the ranges
    min_value = min(data)
    max_value = max(data)

    # Clear figure, getting ready for a new figure
    pyplot.clf()

    # A new figure with the given dimensions size
    figure = pyplot.figure(figsize=(figure_width, figure_height))
    ax = figure.add_subplot(111)
    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()
    ry, rx = numpy.histogram(data, bins=bins, range=(min_value, max_value))

    ry = ry / max(ry)
    x_min = min(rx)
    x_max = max(rx)
    delta = x_max - x_min
    step = delta / bins
    bins = vmv.utilities.sample_range(x_min, x_max, bins)

    # Right histogram
    pyplot.barh(bins, ry, color=color, height=step * bin_width)

    # Right box plot
    rvalue = 1.25
    bpr = pyplot.boxplot(data, positions=[rvalue], showfliers=True,
                         flierprops=dict(marker='o', markersize=5, alpha=0.5,
                                         markerfacecolor=color, markeredgecolor=color))

    for box in bpr['boxes']:
        box.set(color=color, linewidth=1)
    for whisker in bpr['whiskers']:
        whisker.set(color=color, linewidth=1)
    for cap in bpr['caps']:
        cap.set(color=color, linewidth=1, xdata=cap.get_xdata() + (-0.025, 0.025))
    for median in bpr['medians']:
        median.set(color=axvline_color, linewidth=1)

    # Only plot the Y-axis
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(True)

    # Remove any labels
    pyplot.xlabel('')
    if title is not None:
        pyplot.ylabel(title, labelpad=20)
    else:
        pyplot.ylabel('')
    pyplot.gca().yaxis.set_major_locator(pyplot.MaxNLocator(10))

    ax.spines["left"].set_color('black')
    ax.spines['left'].set_linewidth(1)

    # The central line
    pyplot.axvline(0.0)
    pyplot.axvline(linewidth=2, color=axvline_color)
    pyplot.tick_params(axis='both', width=2, which='both', bottom=True, left=True)

    # Save PNG by default
    pyplot.savefig('%s/distribution-%s.png' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight')

    # Save PDF
    pyplot.savefig('%s/distribution-%s.pdf' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight') if save_pdf else None

    # Save SVG
    pyplot.savefig('%s/distribution-%s.svg' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight') if save_svg else None

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()

    # Return a reference to the PNG image
    return output_prefix + '-distribution.png'


def plot_scatter_xx(df, x_keyword, y_keyword, figure_width, figure_height):

    # Adjusting the figure size
    fig, ax = pyplot.subplots(1)
    fig.set_size_inches(figure_width, figure_height)

    seaborn.scatterplot(data=df, x=x_keyword, y=y_keyword)

    # Save SVG
    pyplot.savefig('/home/abdellah/vessmorphovis-output/example.png')




####################################################################################################
# @plot_range
####################################################################################################
def plot_range(avg_value,
               min_value,
               max_value,
               title,
               label,
               color,
               output_directory,
               figure_width=10,
               figure_height=2):
    """Plot a range.
    """

    # Tight layout
    pyplot.tight_layout()

    # Set the font size
    font_size = 30

    # Adjusting the matplotlib parameters
    pyplot.rcParams['axes.grid'] = 'False'
    pyplot.rcParams['font.family'] = 'NimbusSanL'
    pyplot.rcParams['axes.linewidth'] = 0
    pyplot.rcParams['axes.labelsize'] = font_size
    pyplot.rcParams['axes.labelweight'] = 'regular'
    pyplot.rcParams['xtick.labelsize'] = font_size
    pyplot.rcParams['ytick.labelsize'] = font_size
    pyplot.rcParams['legend.fontsize'] = font_size
    pyplot.rcParams['axes.titlesize'] = font_size
    pyplot.rcParams['axes.autolimit_mode'] = 'round_numbers'
    pyplot.rcParams['axes.xmargin'] = 0
    pyplot.rcParams['axes.ymargin'] = 0

    # Adjusting the figure size
    fig, ax = pyplot.subplots(figsize=(figure_width, figure_height))

    # Only plot the X-axis
    pyplot.yticks([])

    # Plot the bar
    ax.barh([0], [avg_value], xerr=[[avg_value - min_value], [max_value - avg_value]],
            height=0.001, color=color, error_kw={'elinewidth': 1.5, 'capsize': 2.0})

    # Set the title
    ax.set_xlabel(title, labelpad=0.25)

    # Adjust the spines
    ax.spines["bottom"].set_color('black')
    ax.spines['bottom'].set_linewidth(2)

    # Plot the ticks
    pyplot.tick_params(axis='x', width=2, which='both', bottom=True)

    # Save the figure
    pyplot.savefig('%s/range-%s.png' % (output_directory, label), bbox_inches='tight')

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()


####################################################################################################
# @plot_average_profile
####################################################################################################
def plot_average_profile(df,
                         label,
                         title,
                         df_keyword,
                         output_directory,
                         figure_width=3,
                         figure_height=10,
                         bins=50):
    """Plot average profile of a given data frame with respect X, Y and Z axes.
@Mare
    :param df:
        Data frame.
    :param label:
        Figure label.
    :param title:
        Figure title.
    :param df_keyword:
        The keyword in the df used to plot the figure.
    :param output_directory:
        The path to the directory where the file will be written.
    :param figure_width:
        Figure width
    :param figure_height:
        Figure height
    :param bins:
        Number of bins.
    """

    for axis in ['X', 'Y', 'Z']:

        # Sort the data frame
        f = df.sort_values(by=[axis], inplace=False)

        # Get the data, the Y-axis is the distance, the X-axis is the keyword
        x = list(f[axis])
        y = list(f[df_keyword])

        x_range, y_average, y_range, y_samples = \
            vmv.analysis.compute_average_profile_from_arranged_data(x, y, bins)

        # Clear figure, getting ready for a new figure
        pyplot.clf()

        # A new figure with the given dimensions size
        figure = pyplot.figure(figsize=(figure_width, figure_height))
        ax = figure.add_subplot(111)

        # Axes limits
        min_y = min(y)
        max_y = max(y)
        ax.set_xlim(left=0, right=math.ceil(max_y))
        x_label_distance = (max_y - min_y) * 0.1
        ax.spines['left'].set_position(('data', -x_label_distance))

        ax.grid(False)

        ax.spines["bottom"].set_color('black')
        ax.spines["left"].set_color('black')
        ax.spines['left'].set_linewidth(2)
        ax.spines['bottom'].set_linewidth(2)
        pyplot.tick_params(axis='both', width=2, which='both', bottom=True, left=True)

        pyplot.tight_layout()

        # Create a new frame for the plot to combine both
        frame = pyplot.gca()

        # Only plot the Y-axis
        frame.axes.get_xaxis().set_visible(True)
        frame.axes.get_yaxis().set_visible(True)

        if axis == 'X':
            color = 'red'
        elif axis == 'Y':
            color = 'green'
        else:
            color = 'blue'
        # Remove any labels
        pyplot.xlabel(title)
        pyplot.ylabel('Distance along %s axis (μm)' % axis, labelpad=20)
        pyplot.plot(y_average, x_range, '-', color=color)

        p_min = y_range[:, 0]
        p_max = y_range[:, 1]
        pyplot.fill_betweenx(x_range, p_max, p_min, color=color, alpha=0.2)

        pyplot.savefig('%s/%s-%s.png' % (output_directory, label, axis), bbox_inches='tight')

        # Close figure to reset
        pyplot.clf()
        pyplot.cla()
        pyplot.close()


def plot_distribution_with_range(df,
                                 label,
                                 title,
                                 df_sorting_keyword,
                                 df_average_keyword,
                                 df_minimum_keyword,
                                 df_maximum_keyword,
                                 output_directory,
                                 figure_width=5,
                                 figure_height=20):
    # Tight layout
    pyplot.tight_layout()

    # Set the font size
    font_size = 30

    # Adjusting the matplotlib parameters
    pyplot.rcParams['axes.grid'] = 'False'
    pyplot.rcParams['font.family'] = 'NimbusSanL'
    pyplot.rcParams['axes.linewidth'] = 0
    pyplot.rcParams['axes.labelsize'] = font_size
    pyplot.rcParams['axes.labelweight'] = 'regular'
    pyplot.rcParams['xtick.labelsize'] = font_size
    pyplot.rcParams['ytick.labelsize'] = font_size
    pyplot.rcParams['legend.fontsize'] = font_size
    pyplot.rcParams['axes.titlesize'] = font_size
    pyplot.rcParams['axes.autolimit_mode'] = 'round_numbers'
    pyplot.rcParams['axes.xmargin'] = 0
    pyplot.rcParams['axes.ymargin'] = 0

    # Sort the data frame
    f = df.sort_values(by=[df_average_keyword], inplace=False)

    # Get the minimum, maximum and average data arrays
    data_minimum = list(f[df_minimum_keyword])
    data_maximum = list(f[df_maximum_keyword])
    data_average = list(f[df_average_keyword])

    # A new figure with the given dimensions size
    figure = pyplot.figure(figsize=(figure_width, figure_height))
    ax = figure.add_subplot(111)

    # Independent axis
    independent_axis = f[df_average_keyword]

    ax.set_xlim(left=math.floor(min(data_minimum)), right=math.ceil(max(data_maximum)))
    # x_label_distance = (max_y - min_y) * 0.1
    # ax.spines['left'].set_position(('data', -x_label_distance))

    min_y = min(data_minimum)
    max_y = max(data_maximum)
    ax.set_xlim(left=0, right=math.ceil(max_y))
    x_label_distance = (max_y - min_y) * 0.1
    ax.spines['left'].set_position(('data', -x_label_distance))

    ax.grid(False)

    ax.spines["bottom"].set_color('black')
    ax.spines["left"].set_color('black')
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    pyplot.tick_params(axis='both', width=2, which='both', bottom=True, left=True)

    pyplot.tight_layout()

    # Create a new frame for the plot to combine both
    frame = pyplot.gca()

    # Only plot the Y-axis
    frame.axes.get_xaxis().set_visible(True)
    frame.axes.get_yaxis().set_visible(True)

    # Remove any labels
    pyplot.xlabel(title)
    pyplot.ylabel('Section Index', labelpad=20)
    # pyplot.plot(data_average, independent_axis, '-', color='b')

    variance = list()
    for item1, item2 in zip(data_maximum, data_minimum):
        variance.append(item1 - item2)

    pyplot.errorbar(data_average, independent_axis, xerr=variance, fmt='.k')

    # pyplot.fill_betweenx(independent_axis, data_maximum, data_minimum, color='r', alpha=0.2)

    pyplot.savefig('%s/%s-%s.png' % (output_directory, label, 'R'), bbox_inches='tight')

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()















####################################################################################################
# @plot_histogram
####################################################################################################
def plot_histogram(data_frame, data_key,
                   label, title,
                   output_directory, output_prefix,
                   top_limit=None, figure_width=5, figure_height=10,
                   bins=50, color='r', font_size=30, line_width=1, padding=10, x_label='Count',
                   dpi=300, save_pdf=False, save_svg=False):

    # Set the default styles
    set_styles(font_size=font_size, axes_linewidth=line_width)

    # Create a new figure and adjust its size
    fig, (ax1, ax2) = pyplot.subplots(1, 2, sharey=True)
    fig.set_size_inches(figure_width, figure_height)

    # Get the data, with which the histogram will be drawn
    data = data_frame[data_key]

    # Plot the horizontal histogram (ax1)
    x, y, _ = ax1.hist(data, color=color, orientation='horizontal', edgecolor='white', bins=bins)
    for spine in ['left', 'bottom']:
        ax1.spines[spine].set_position(('outward', 10))
        ax1.spines[spine].set_color('black')
        ax1.spines[spine].set_linewidth(line_width)
    for spine in ['right', 'top']:
        ax1.spines[spine].set_visible(False)
    ax1.tick_params(axis='both', width=line_width, length=5, which='both', bottom=True, left=True)
    ax1.set_title(title, pad=25)

    # X-axis bins, only two bins
    max_x = max(x)
    x_limit = math.ceil(max_x)
    x_ticks = [0, x_limit]
    ax1.set_xlim(0, x_limit)
    ax1.set_xticks(x_ticks)

    # TODO: Grid only for the Y axis
    ax1.grid(axis='y')

    if top_limit is None:
        ax1.set_ylim(bottom=0.0)
    else:
        ax1.set_ylim(bottom=0.0, top=top_limit)

    ax1.set_xlabel(x_label)
    ax1.set_ylabel(label, labelpad=padding)

    # Right box plot (ax2)
    bp = ax2.boxplot(data, showfliers=True,
                     flierprops=dict(marker='o', markersize=5, alpha=0.5,
                                     markerfacecolor=color, markeredgecolor=color))

    # No visible spines
    for spine in ['left', 'right', 'top', 'bottom']:
        ax2.spines[spine].set_visible(False)

    # Adjust the box-plot styles
    for box in bp['boxes']:
        box.set(color=color, linewidth=line_width * 0.6)
    for whisker in bp['whiskers']:
        whisker.set(color=color, linewidth=line_width * 0.5)
    for cap in bp['caps']:
        cap.set(color=color, linewidth=line_width * 0.65, xdata=cap.get_xdata() + (-0.01, 0.01))
    for median in bp['medians']:
        median.set(color='k', linewidth=line_width * 0.65)

    # Shift the position of the box plot for compacting the figure
    bp_position = ax2.get_position()
    bp_position.x0 = bp_position.x0 - 0.1
    bp_position.x1 = bp_position.x1 - 0.1
    ax2.set_position(bp_position)

    # Set its transparency to zero
    ax2.patch.set_alpha(0.0)
    ax2.tick_params(axis='both', which='both', left=False, bottom=False, labelbottom=False)
    ax2.grid(False)

    # Save PNG by default, PDF and SVG if needed
    pyplot.savefig('%s/%s.png' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True)
    pyplot.savefig('%s/%s.pdf' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True) if save_pdf else None
    pyplot.savefig('%s/%s.svg' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True) if save_svg else None

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()


def plot_scatter(xdata, ydata,
                 xlabel, ylabel, title,
                 output_directory, output_prefix,
                 top_limit=None, figure_width=5, figure_height=10, spines_shift=10,
                 bins=50, color='r', font_size=30, line_width=1, padding=0, x_label='Count',
                 dpi=300, save_pdf=False, save_svg=False):

    # Set the default styles
    set_styles(font_size=font_size, axes_linewidth=line_width)

    # Create a new figure and adjust its size
    fig, ax1 = pyplot.subplots(1, 1)
    fig.set_size_inches(figure_width, figure_height)

    # Plot
    ax1.scatter(xdata, ydata, marker='+', color=color)

    # Adjust the spine parameters
    for spine in ['left', 'bottom']:
        ax1.spines[spine].set_position(('outward', spines_shift))
        ax1.spines[spine].set_color('black')
        ax1.spines[spine].set_linewidth(line_width)
    for spine in ['right', 'top']:
        ax1.spines[spine].set_visible(False)
    ax1.tick_params(axis='both', width=line_width, length=5, which='both', bottom=True,
                    left=True)
    ax1.grid(False)
    ax1.grid(axis='y')
    ax1.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title(title, pad=25)

    # X-axis bins, only two bins
    x_ticks = [math.floor(min(xdata)), math.ceil(max(xdata))]
    ax1.set_xlim(0, math.ceil(max(xdata)))
    ax1.set_xticks(x_ticks)

    if int(math.ceil(min(ydata))) == 0:
        ax1.set_ylim(bottom=0)

    # Save PNG by default, PDF and SVG if needed
    pyplot.savefig('%s/%s.png' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True)
    pyplot.savefig('%s/%s.pdf' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True) if save_pdf else None
    pyplot.savefig('%s/%s.svg' % (output_directory, output_prefix),
                   dpi=dpi, bbox_inches='tight', transparent=True) if save_svg else None

    # Close figure to reset
    pyplot.clf()
    pyplot.cla()
    pyplot.close()
