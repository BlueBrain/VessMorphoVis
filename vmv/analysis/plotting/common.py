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
import matplotlib.pyplot as pyplot


####################################################################################################
# @set_plotting_styles
####################################################################################################
def set_plotting_styles(plot_styles):

    pyplot.rcParams['axes.grid'] = plot_styles.axes_grid
    pyplot.rcParams['grid.linestyle'] = plot_styles.line_style
    pyplot.rcParams['font.family'] = plot_styles.font_type
    pyplot.rcParams['axes.labelweight'] = plot_styles.font_weight
    pyplot.rcParams['axes.linewidth'] = plot_styles.line_width
    pyplot.rcParams['axes.labelsize'] = plot_styles.font_size
    pyplot.rcParams['xtick.labelsize'] = plot_styles.font_size
    pyplot.rcParams['ytick.labelsize'] = plot_styles.font_size
    pyplot.rcParams['legend.fontsize'] = plot_styles.font_size
    pyplot.rcParams['axes.titlesize'] = plot_styles.font_size
    pyplot.rcParams['axes.autolimit_mode'] = 'round_numbers'
    pyplot.rcParams['axes.autolimit_mode'] = 'round_numbers'


####################################################################################################
# @add_default_axis_styles
####################################################################################################
def add_default_axis_styles(ax,
                            plot_styles):

    for spine in ['left', 'bottom']:
        ax.spines[spine].set_position(('outward', plot_styles.spines_shift))
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(plot_styles.line_width)
    for spine in ['right', 'top']:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis='both', which='both', bottom=True, left=True,
                   width=plot_styles.line_width, length=plot_styles.tick_length)
    ax.grid(axis='y')


####################################################################################################
# @add_patch_styles
####################################################################################################
def add_patch_styles(ax,
                     plot_styles):

    # Adjust the spine parameters
    for spine in ['left', 'bottom']:
        ax.spines[spine].set_position(('outward', plot_styles.spines_shift))
        ax.spines[spine].set_color('black')
        ax.spines[spine].set_linewidth(2)
    for spine in ['left', 'top', 'right']:
        ax.spines[spine].set_visible(False)
    ax.tick_params(axis='both', which='both', bottom=True, left=False,
                   width=plot_styles.line_width, length=plot_styles.tick_length)
    ax.set_xlim(left=0, right=1)
    ax.axes.get_yaxis().set_visible(False)
    ax.grid(False)


####################################################################################################
# save_figure
####################################################################################################
def save_figure(output_prefix,
                output_directory,
                dpi=300,
                svg=False,
                pdf=False):

    # Save PNG by default, PDF and SVG if needed
    file_path = '%s/%s' % (output_directory, output_prefix)
    pyplot.savefig('%s.png' % file_path, dpi=dpi, bbox_inches='tight', transparent=True)
    if svg:
        pyplot.savefig('%s.svg' % file_path, dpi=dpi, bbox_inches='tight', transparent=True)
    if pdf:
        pyplot.savefig('%s.pdf' % file_path, dpi=dpi, bbox_inches='tight', transparent=True)


####################################################################################################
# reset_matplotlib
####################################################################################################
def reset_matplotlib():
    pyplot.clf()
    pyplot.cla()
    pyplot.close()
