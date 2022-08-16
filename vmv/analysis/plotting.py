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

# Internal imports
import vmv.consts
import vmv.utilities


####################################################################################################
# @verify_plotting_packages
####################################################################################################
def verify_plotting_packages():
    """Verifies the paths of the fonts that are used for plotting the figures.
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

    verify_plotting_packages()

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
                         bins=25):
    """Plot average profile of a given data frame with respect X, Y and Z axes.

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

        # Get the data
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
