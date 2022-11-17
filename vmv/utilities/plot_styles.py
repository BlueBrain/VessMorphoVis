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

####################################################################################################
# @PlotStyle
####################################################################################################
class PlotStyle:
    """Styles used for plotting the analysis figures.
    """
    ################################################################################################
    # @__int__
    ################################################################################################
    def __init__(self,
                 axes_grid=False,
                 title_pad=25,
                 font_type='Arial',
                 font_weight='regular',
                 font_size=30,
                 line_style='-',
                 line_width=2,
                 tick_length=5,
                 spines_shift=10,
                 box_plot_marker='o',
                 box_plot_marker_size=5,
                 box_plot_alpha=0.5,
                 scatter_plot_marker='x'):

        self.axes_grid = axes_grid
        self.title_pad = title_pad
        self.font_type = font_type
        self.font_weight = font_weight
        self.font_size = font_size
        self.line_style = line_style
        self.line_width = line_width
        self.tick_length = tick_length
        self.spines_shift = spines_shift
        self.box_plot_marker = box_plot_marker
        self.box_plot_marker_size = box_plot_marker_size
        self.box_plot_alpha = box_plot_alpha
        self.scatter_plot_marker = scatter_plot_marker
