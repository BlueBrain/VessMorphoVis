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
import numpy
import pandas
import matplotlib.pyplot as pyplot

# Internal imports
import vmv.utilities
import vmv.consts
from vmv.consts import Keys, Prefix
import vmv.analysis.plotting as vmv_plotting


def plot_radius_analysisss_statistics(morphology, output_directory):

    return
    # Number of Samples per section histogram
    vmv.analysis.plot_histogram(
        data_frame=data_frame,
        data_key=[Keys.NUMBER_OF_SAMPLES],
        title='# Samples per Section\n Histogram',
        label='# Samples / Section',
        figure_width=6, figure_height=10,
        output_prefix='number-samples-per-section',
        output_directory=output_directory,
        color=vmv.consts.Color.CM_RED_DARK)



    data_frame = vmv.analysis.analyse_per_section_radius(morphology.sections_list)

    vmv.plot_range_data_closeups(df=data_frame,
                                 data_key=Keys.SECTION_INDEX,
                                 min_keyword=Keys.SECTION_MIN_RADIUS,
                                 mean_keyword=Keys.SECTION_MEAN_RADIUS,
                                 max_keyword=Keys.SECTION_MAX_RADIUS,
                                 label='Section Index',
                                 output_prefix='section-radius-analysis',
                                 output_directory=output_directory,
                                 light_color=o_light,
                                 dark_color=o_dark)

    vmv.plot_range_data_closeups(df=data_frame,
                                 data_key=Keys.X,
                                 min_keyword=Keys.SECTION_MIN_RADIUS,
                                 mean_keyword=Keys.SECTION_MEAN_RADIUS,
                                 max_keyword=Keys.SECTION_MAX_RADIUS,
                                 label=r'Distance along Z-axis ($\mu$m)',
                                 output_prefix='section-radius-analysis-x',
                                 output_directory=output_directory,
                                 light_color=r_light,
                                 dark_color=r_dark)

    vmv.plot_range_data_closeups(df=data_frame,
                                 data_key=Keys.Y,
                                 min_keyword=Keys.SECTION_MIN_RADIUS,
                                 mean_keyword=Keys.SECTION_MEAN_RADIUS,
                                 max_keyword=Keys.SECTION_MAX_RADIUS,
                                 label=r'Distance along Y-axis ($\mu$m)',
                                 output_prefix='section-radius-analysis-y',
                                 output_directory=output_directory,
                                 light_color=g_light,
                                 dark_color=g_dark)

    vmv.plot_range_data_closeups(df=data_frame,
                                 data_key=Keys.Z,
                                 min_keyword=Keys.SECTION_MIN_RADIUS,
                                 mean_keyword=Keys.SECTION_MEAN_RADIUS,
                                 max_keyword=Keys.SECTION_MAX_RADIUS,
                                 label=r'Distance along Z-axis ($\mu$m)',
                                 output_prefix='section-radius-analysis-z',
                                 output_directory=output_directory,
                                 light_color=b_light,
                                 dark_color=b_dark)

    # vmv.plot_range_data_xyz_with_closeups(
    #    df=per_section_radius_data, min_keyword='Vessel Min Radius',
    #    mean_keyword='Vessel Mean Radius',
    #    max_keyword='Vessel Max Radius',
    #    label='Distance', output_prefix='vessel-xx', output_directory=output_directory)


####################################################################################################
# @export_analysis_results
####################################################################################################
def export_analysis_results(morphology,
                            output_directory):

    vmv_plotting.plot_structure_analysis_statistics(morphology, output_directory)

    #vmv_plotting.plot_radius_analysis_statistics(morphology, output_directory)

    #vmv_plotting.plot_length_analysis_statistics(morphology, output_directory)

    #vmv_plotting.plot_surface_area_analysis_statistics(morphology, output_directory)


    # vmv_plotting.plot_volume_analysis_statistics(morphology, output_directory)


####################################################################################################
# @sample_range
####################################################################################################
def compute_average_profile_from_arranged_data(x,
                                               y,
                                               bins=25):
    """Assuming that the independent variable ix X and the dependent variable is Y, compute the
    average profile from an input list of arranged data.

    :param x:
    :type x:
    :param y:
    :type y:
    :param bins:
    :type bins:
    :return:
    :rtype:
    """

    # Compute the new X-axis range (number of elements) based on the given number of bins
    x_range = vmv.utilities.sample_range(min(x), max(x), bins)

    # Compute the number of elements per bin
    bin_size = int((len(y) / bins))

    # y_average is a list, each element has the average value of the samples located in a single bin
    y_average = list()

    # y_range is a list, each element is a list of minimum and maximum value is a single bin
    y_range = list()

    # y_samples is a list of lists containing all the samples located in a single bin
    y_samples = list()

    # Calculate the Y data
    for i in range(bins):

        # Initially, the average value per bin is Zero
        bin_average_value = 0

        # Other lists
        bin_samples = list()

        # An index to compute the number of elements in bin
        elements_in_bin = 0

        # Per bin
        for j in range(bin_size):

            # Compute the Y-index
            y_index = i * bin_size + j

            # Ensure that the current index the array contains the data
            if y_index < len(y):

                # Increase the elements count
                elements_in_bin += 1

                # Get the value, and update the lists
                bin_average_value += y[y_index]

                # Add the sample to the bin_samples list
                bin_samples.append(y[y_index])

        # Compute the average data per bin
        if elements_in_bin > 0:
            bin_average_value /= elements_in_bin
            y_average.append(bin_average_value)

            y_range.append([min(bin_samples), max(bin_samples)])
            y_samples.append(bin_samples)

    return x_range, numpy.array(y_average), numpy.array(y_range), y_samples


def draw_scatter_plots_index_x_y_z(data_frame,
                                   x_key,
                                   title,
                                   x_axis_label, 
                                   output_prefix,
                                   output_directory,
                                   show_closeup=False):

    # Number of samples per section w.r.t index and XYZ
    for i in ['section-index', 'x', 'y', 'z']:
        if i == 'section-index':
            y_key = Keys.SECTION_INDEX
            y_axis_label = 'Section Index'
            fig_title = '%s\nDistribution w.r.t Section Index' % title
            prefix = '%s-section-index' % output_prefix
            color = vmv.consts.Color.CM_ORANGE_DARK
        elif i == 'x':
            y_key = Keys.X
            y_axis_label = r'Distance along X-axis ($\mu$m)'
            fig_title = '%s\nDistribution w.r.t X-axis' % title
            prefix = '%s-x' % output_prefix
            color = vmv.consts.Color.CM_RED_DARK
        elif i == 'y':
            y_key = Keys.Y
            y_axis_label = r'Distance along Y-axis ($\mu$m)'
            fig_title = '%s\nDistribution w.r.t Y-axis' % title
            prefix = '%s-y' % output_prefix
            color = vmv.consts.Color.CM_GREEN_DARK
        elif i == 'z':
            y_key = Keys.Z
            y_axis_label = r'Distance along Z-axis ($\mu$m)'
            fig_title = '%s\nDistribution w.r.t Z-axis' % title
            prefix = '%s-z' % output_prefix
            color = vmv.consts.Color.CM_BLUE_DARK

        if show_closeup:
            vmv.plot_scatter_data_with_closeups(df=data_frame,
                                                idep_axis_label=y_axis_label,
                                                dep_axis_label=x_axis_label,
                                                idep_keyword=y_key,
                                                dep_keyword=x_key,
                                                figure_width=6, figure_height=10,
                                                output_prefix=prefix,
                                                output_directory=output_directory,
                                                light_color=color)
        else:
            vmv.analysis.plot_scatter(xdata=data_frame[x_key],
                                      ydata=data_frame[y_key],
                                      title=title,
                                      xlabel=x_axis_label,
                                      ylabel=y_axis_label,
                                      figure_width=6, figure_height=10,
                                      output_prefix=prefix,
                                      output_directory=output_directory,
                                      color=color)


####################################################################################################
# @apply_analysis_kernel
####################################################################################################
def apply_analysis_kernel(morphology,
                          function,
                          title,
                          label,
                          color,
                          output_directory):
    """Apply a given analysis function on the entire morphology.

    :param morphology:
        Input morphology.
    :param function:
        Analysis function.
    :param title:
        Figure title.
    :param label:
        Figure label.
    :param color:
        Figure color.
    :param output_directory:
        The directory where the results will be written.
    """

    # Apply the function to the morphology object
    distribution = function(morphology)

    # Write the distribution to a text file
    file_path = '%s/%s.dist' % (output_directory, label)
    vmv.file.write_distribution_to_file(distribution=distribution, file_path=file_path)

    # Plot the distribution
    vmv.analysis.plot_normalized_histogram(
        data=distribution, output_directory=output_directory, output_prefix=label,
        title=title, color=color)

    # Plot the range
    vmv.analysis.plot_range(
        avg_value=sum(distribution) / len(distribution),
        min_value=min(distribution), max_value=max(distribution),
        title=title, label=label, color=color, output_directory=output_directory)


####################################################################################################
# @apply_analysis_kernel
####################################################################################################
def apply_xyz_analysis_kernel(morphology,
                              function,
                              title,
                              label,
                              keyword,
                              output_directory):
    """Apply a given analysis function along the XYZ axes.

    :param morphology:
        Input morphology.
    :param function:
        Analysis function.
    :param title:
        Figure title.
    :param label:
        Figure label.
    :param keyword:
        Keyword used to plot the data from the resulting dataframe.
    :type keyword:
    :param output_directory:
        The directory where the results will be written.
    """

    # Apply the kernel to the morphology and compute the dataframe
    df = function(morphology)

    # Plot the profile
    vmv.analysis.plot_average_profile(df=df, title=title, label=label, df_keyword=keyword,
                                      output_directory=output_directory)


def apply_section_distribution_analysis_kernel(morphology,
                                               function,
                                               title,
                                               label,
                                               df_sorting_keyword,
                                               df_average_keyword,
                                               df_minimum_keyword,
                                               df_maximum_keyword,
                                               output_directory):

    # Apply the kernel to the morphology and compute the dataframe
    df = function(morphology)

    # Plot the profile
    vmv.analysis.plot_distribution_with_range(
        df=df, title=title, label=label,
        df_sorting_keyword=df_sorting_keyword, df_average_keyword=df_average_keyword,
        df_minimum_keyword=df_minimum_keyword, df_maximum_keyword=df_maximum_keyword,
        output_directory=output_directory)




####################################################################################################
# @analyze_morphology
####################################################################################################
def analyze_morphology(morphology_object):
    """Analyze a given morphology.

    :param morphology_object:
        Input morphology object.
    """

    import time
    analysis_stated = time.time()

    import vmv.analysis

    # Analysis string

    # Morphology total length
    morphology_total_length = vmv.analysis.compute_total_morphology_length(
        morphology_object.sections_list)

    # Total number of samples
    vmv.logger.info('Samples')
    total_number_samples = vmv.analysis.compute_total_of_number_samples_from_sections_list(
        morphology_object.sections_list)


def plot_analysis_samples_per_section(morphology,
                                      output_directory):

    # Analyze and get the data-frame
    data_frame = vmv.analysis.analyze_samples_per_section(sections=morphology.sections_list)

    from matplotlib.colors import BoundaryNorm
    from matplotlib.ticker import MaxNLocator
    import numpy
    cmap = pyplot.colormaps['PiYG']
    
    
    Z, xedges, yedges = numpy.histogram2d(x=data_frame[Keys.X], y=data_frame[Keys.Y], 
        weights=data_frame[Keys.NUMBER_OF_SAMPLES], bins=[25, 25])
    levels = MaxNLocator(nbins=15).tick_values(Z.min(), Z.max())
    norm = BoundaryNorm(levels, ncolors=cmap.N, clip=True)
    fig = pyplot.figure(figsize=(9,10))
    ax1 = fig.add_subplot(111)
    im = ax1.pcolormesh(xedges, yedges, Z.T, cmap=cmap)
    fig.colorbar(im, ax=ax1)
    fig.savefig('%s/example.png' % output_directory)

    # Number of Samples per section histogram
    vmv.analysis.plot_histogram(
        data_frame=data_frame,
        data_key=[Keys.NUMBER_OF_SAMPLES],
        title='# Samples per Section\n Histogram',
        label='# Samples / Section',
        figure_width=6, figure_height=10,
        output_prefix='number-samples-per-section',
        output_directory=output_directory,
        color=vmv.consts.Color.CM_RED_DARK)

    # Number of samples per section w.r.t index and XYZ
    for i in ['section-index', 'x', 'y', 'z']:
        if i == 'section-index':
            y_key = Keys.SECTION_INDEX
            y_axis_label = 'Section Index'
            title = '# Samples per Section\nDistribution w.r.t Section Index'
            color = vmv.consts.Color.CM_ORANGE_DARK
        elif i == 'x':
            y_key = Keys.X
            y_axis_label = r'Distance along X-axis ($\mu$m)'
            title = '# Samples per Section\nDistribution w.r.t X-axis'
            color = vmv.consts.Color.CM_RED_DARK
        elif i == 'y':
            y_key = Keys.Y
            y_axis_label = r'Distance along Y-axis ($\mu$m)'
            title = '# Samples per Section\nDistribution w.r.t Y-axis'
            color = vmv.consts.Color.CM_GREEN_DARK
        elif i == 'z':
            y_key = Keys.Z
            y_axis_label = r'Distance along Z-axis ($\mu$m)'
            title = '# Samples per Section\nDistribution w.r.t Z-axis'
            color = vmv.consts.Color.CM_BLUE_DARK

        vmv.analysis.plot_scatter(xdata=data_frame[Keys.NUMBER_OF_SAMPLES],
                                  ydata=data_frame[y_key],
                                  xlabel='# Samples / Section',
                                  ylabel=y_axis_label,
                                  title=title,
                                  figure_width=6, figure_height=10,
                                  output_prefix='number-samples-per-section-%s' % i,
                                  output_directory=output_directory,
                                  color=color)

    return 
    two_samples_data = list()
    for index, row in data_frame.iterrows():
        if row[Keys.NUMBER_OF_SAMPLES] == 2:
            two_samples_data.append(row)

    two_samples_data_frame = pandas.DataFrame(two_samples_data,
                                              columns=[Keys.SECTION_INDEX, Keys.NUMBER_OF_SAMPLES,
                                                       Keys.X, Keys.Y, Keys.Z])

    vmv.analysis.plot_histogram(data_frame=two_samples_data_frame,
                                data_key=[Keys.X],
                                title='Sections with 2 Samples',
                                label=r'Distance along X-axis ($\mu$m)',
                                figure_width=5, figure_height=10,
                                output_prefix='sections-with-2-samples-x',
                                output_directory=output_directory,
                                color=r_dark)

    vmv.analysis.plot_histogram(data_frame=two_samples_data_frame,
                                data_key=[Keys.Y],
                                title='Sections with 2 Samples',
                                label=r'Distance along Y-axis ($\mu$m)',
                                figure_width=5, figure_height=10,
                                output_prefix='sections-with-2-samples-y',
                                output_directory=output_directory,
                                color=g_dark)

    vmv.analysis.plot_histogram(data_frame=two_samples_data_frame,
                                data_key=[Keys.Z],
                                title='Sections with 2 Samples',
                                label=r'Distance along Z-axis ($\mu$m)',
                                figure_width=5, figure_height=10,
                                output_prefix='sections-with-2-samples-z',
                                output_directory=output_directory,
                                color=b_dark)

    # Samples density w.r.t X-axis
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.X,
                       label='Samples Density along X-axis',
                       title='Samples Density',
                       output_prefix='samples-density-x',
                       output_directory=output_directory,
                       color=r_dark)

    # Samples density w.r.t Y-axis
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.Y,
                       label='Samples Density along Y-axis',
                       title='Samples Density',
                       output_prefix='samples-density-y',
                       output_directory=output_directory,
                       color=g_dark)

    # Samples density w.r.t Z-axis
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.Z,
                       label='Samples Density along Z-axis',
                       title='Samples Density',
                       output_prefix='samples-density-z',
                       output_directory=output_directory,
                       color=b_dark)







def plot_length_analysis_statistics(morphology,
                                    output_directory,
                                    sections_centers=None):

    data_frame = vmv.analysis.perform_length_analysis(sections=morphology.sections_list,
                                                      sections_centers=sections_centers)
    # Number of Samples per section histogram
    vmv.analysis.plot_histogram(
        data_frame=data_frame,
        data_key=[Keys.SECTION_LENGTH],
        title='Section Length\nHistogram',
        label=r'Section Length ($\mu$m)',
        figure_width=6, figure_height=10,
        output_prefix='section-length',
        output_directory=output_directory,
        color=vmv.consts.Color.CM_RED_DARK)

    vmv.analysis.plot_histogram(
        data_frame=data_frame,
        data_key=[Keys.SEGMENT_MEAN_LENGTH],
        title='Segments Mean Length\nHistogram (per Section)',
        label=r'Segments Mean Length ($\mu$m)',
        figure_width=6, figure_height=10,
        output_prefix='segment-mean-length',
        output_directory=output_directory,
        color=vmv.consts.Color.CM_RED_DARK)

    vmv.analysis.plot_histogram(
        data_frame=data_frame,
        data_key=Keys.SEGMENT_LENGTH_RATIO,
        title='Segment Length Ratio\nHistogram (per Section)',
        label='Segment Length Ratio',
        output_prefix='segments-length-ratio',
        output_directory=output_directory,
        color=vmv.consts.Color.CM_RED_DARK)

    # Number of samples per section w.r.t index and XYZ
    for i in ['section-index', 'x', 'y', 'z']:
        if i == 'section-index':
            y_key = Keys.SECTION_INDEX
            y_axis_label = 'Section Index'
            title = 'Segment Length Ratio\nDistribution w.r.t Section Index'
            color = vmv.consts.Color.CM_ORANGE_DARK
        elif i == 'x':
            y_key = Keys.X
            y_axis_label = r'Distance along X-axis ($\mu$m)'
            title = 'Segment Length Ratio\nDistribution w.r.t X-axis'
            color = vmv.consts.Color.CM_RED_DARK
        elif i == 'y':
            y_key = Keys.Y
            y_axis_label = r'Distance along Y-axis ($\mu$m)'
            title = 'Segment Length Ratio\nDistribution w.r.t Y-axis'
            color = vmv.consts.Color.CM_GREEN_DARK
        elif i == 'z':
            y_key = Keys.Z
            y_axis_label = r'Distance along Z-axis ($\mu$m)'
            title = 'Segment Length Ratio\nDistribution w.r.t Z-axis'
            color = vmv.consts.Color.CM_BLUE_DARK

        # Number of Samples per section w.r.t the Section Index
        vmv.analysis.plot_scatter(xdata=data_frame[Keys.SEGMENT_LENGTH_RATIO],
                                  ydata=data_frame[y_key],
                                  xlabel='Segment Length Ratio',
                                  ylabel=y_axis_label,
                                  title=title,
                                  figure_width=6, figure_height=10,
                                  output_prefix='segment-length-ratio-%s' % i,
                                  output_directory=output_directory,
                                  color=color)

    ################################################################################
    # Sampling density per section 
    ################################################################################
    vmv.analysis.plot_histogram(
        data_frame=data_frame,
        data_key=[Keys.SECTION_SAMPLING_DENSITY],
        title='Sampling Density',
        label=r'Section Sampling Density ($\mu$m$^{\mathrm{-1}}$)',
        figure_width=6, figure_height=10,
        output_prefix='section-sampling-density',
        output_directory=output_directory,
        color=vmv.consts.Color.CM_RED_DARK)

    # Number of samples per section w.r.t index and XYZ
    for i in ['section-index', 'x', 'y', 'z']:
        if i == 'section-index':
            y_key = Keys.SECTION_INDEX
            y_axis_label = 'Section Index'
            title = 'Sampling Density\nDistribution w.r.t Section Index'
            color = vmv.consts.Color.CM_ORANGE_DARK
        elif i == 'x':
            y_key = Keys.X
            y_axis_label = r'Distance along X-axis ($\mu$m)'
            title = 'Sampling Density\nDistribution w.r.t X-axis'
            color = vmv.consts.Color.CM_RED_DARK
        elif i == 'y':
            y_key = Keys.Y
            y_axis_label = r'Distance along Y-axis ($\mu$m)'
            title = 'Sampling Density\nDistribution w.r.t Y-axis'
            color = vmv.consts.Color.CM_GREEN_DARK
        elif i == 'z':
            y_key = Keys.Z
            y_axis_label = r'Distance along Z-axis ($\mu$m)'
            title = 'Sampling Density\nDistribution w.r.t Z-axis'
            color = vmv.consts.Color.CM_BLUE_DARK

        # Number of Samples per section w.r.t the Section Index
        vmv.analysis.plot_scatter(xdata=data_frame[Keys.SEGMENT_LENGTH_RATIO],
                                  ydata=data_frame[y_key],
                                  xlabel=r'Section Sampling Density ($\mu$m$^{\mathrm{-1}}$)',
                                  ylabel=y_axis_label,
                                  title=title,
                                  figure_width=6, figure_height=10,
                                  output_prefix='section-sampling-density-%s' % i,
                                  output_directory=output_directory,
                                  color=color)

    return
    vmv.plot_range_data_closeups(df=length_df,
                                 data_key=Keys.SECTION_INDEX,
                                 min_keyword=Keys.SEGMENT_MIN_LENGTH,
                                 mean_keyword=Keys.SEGMENT_MEAN_LENGTH,
                                 max_keyword=Keys.SEGMENT_MAX_LENGTH,
                                 label='Section Index',
                                 output_prefix='section-length-analysis',
                                 output_directory=output_directory,
                                 light_color=o_light,
                                 dark_color=o_dark)

    vmv.plot_range_data_closeups(df=length_df,
                                 data_key=Keys.X,
                                 min_keyword=Keys.SEGMENT_MIN_LENGTH,
                                 mean_keyword=Keys.SEGMENT_MEAN_LENGTH,
                                 max_keyword=Keys.SEGMENT_MAX_LENGTH,
                                 label=r'Distance along X-axis ($\mu$m)',
                                 output_prefix='section-length-analysis-x',
                                 output_directory=output_directory,
                                 light_color=r_light,
                                 dark_color=r_dark)

    vmv.plot_range_data_closeups(df=length_df,
                                 data_key=Keys.Y,
                                 min_keyword=Keys.SEGMENT_MIN_LENGTH,
                                 mean_keyword=Keys.SEGMENT_MEAN_LENGTH,
                                 max_keyword=Keys.SEGMENT_MAX_LENGTH,
                                 label=r'Distance along Y-axis ($\mu$m)',
                                 output_prefix='section-length-analysis-y',
                                 output_directory=output_directory,
                                 light_color=g_light,
                                 dark_color=g_dark)

    vmv.plot_range_data_closeups(df=length_df,
                                 data_key=Keys.Z,
                                 min_keyword=Keys.SEGMENT_MIN_LENGTH,
                                 mean_keyword=Keys.SEGMENT_MEAN_LENGTH,
                                 max_keyword=Keys.SEGMENT_MAX_LENGTH,
                                 label=r'Distance along Z-axis ($\mu$m)',
                                 output_prefix='section-length-analysis-z',
                                 output_directory=output_directory,
                                 light_color=b_light,
                                 dark_color=b_dark)

    vmv.plot_histogram(df=length_df,
                       data_key=Keys.SEGMENT_LENGTH_RATIO,
                       label='Segment Length Ratio (per Section)',
                       title='Segment Length Ratio Histogram',
                       output_prefix='segments-length-ratio',
                       output_directory=output_directory,
                       color=o_dark)

    # Number of Samples per section w.r.t the Section Index
    vmv.analysis.plot_scatter(xdata=length_df[Keys.SEGMENT_LENGTH_RATIO],
                              ydata=length_df[Keys.SECTION_INDEX],
                              xlabel='Segment Length Ratio',
                              ylabel='Section Index',
                              figure_width=5, figure_height=10,
                              output_prefix='segment-length-ratio-by-section',
                              output_directory=output_directory,
                              color=o_dark)

    # Number of samples per section w.r.t the X-axis
    vmv.analysis.plot_scatter(xdata=length_df[Keys.SEGMENT_LENGTH_RATIO],
                              ydata=length_df[Keys.X],
                              xlabel='Segment Length Ratio',
                              ylabel=r'Distance along X-axis ($\mu$m)',
                              figure_width=5, figure_height=10,
                              output_prefix='segment-length-ratio-x',
                              output_directory=output_directory,
                              color=r_dark)

    # Number of samples per section w.r.t the X-axis
    vmv.analysis.plot_scatter(xdata=length_df[Keys.SEGMENT_LENGTH_RATIO],
                              ydata=length_df[Keys.Y],
                              xlabel='Segment Length Ratio',
                              ylabel=r'Distance along Y-axis ($\mu$m)',
                              figure_width=5, figure_height=10,
                              output_prefix='segment-length-ratio-y',
                              output_directory=output_directory,
                              color=g_dark)

    # Number of samples per section w.r.t the Z-axis
    vmv.analysis.plot_scatter(xdata=length_df[Keys.SEGMENT_LENGTH_RATIO],
                              ydata=length_df[Keys.Z],
                              xlabel='Segment Length Ratio',
                              ylabel=r'Distance along Z-axis ($\mu$m)',
                              figure_width=5, figure_height=10,
                              output_prefix='segment-length-ratio-z',
                              output_directory=output_directory,
                              color=b_dark)

    vmv.plot_histogram(df=length_df,
                       data_key=Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO,
                       label='Thickness to Length (per Section)',
                       title='Thickness to Length Histogram',
                       output_prefix='section-thickness-to-length-ratio',
                       output_directory=output_directory,
                       color=o_dark)

    # Number of samples per section w.r.t the X-axis
    vmv.analysis.plot_scatter(xdata=length_df[Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO],
                              ydata=length_df[Keys.SECTION_INDEX],
                              xlabel='Thickness to Length (per Section)',
                              ylabel='Section Index',
                              figure_width=5, figure_height=10,
                              output_prefix='section-thickness-to-length-by-index',
                              output_directory=output_directory,
                              color=o_dark)

    # Number of samples per section w.r.t the X-axis
    vmv.analysis.plot_scatter(xdata=length_df[Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO],
                              ydata=length_df[Keys.X],
                              xlabel='Thickness to Length (per Section)',
                              ylabel=r'Distance along X-axis ($\mu$m)',
                              figure_width=5, figure_height=10,
                              output_prefix='section-thickness-to-length-ratio-x',
                              output_directory=output_directory,
                              color=r_dark)

    # Number of samples per section w.r.t the X-axis
    vmv.analysis.plot_scatter(xdata=length_df[Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO],
                              ydata=length_df[Keys.Y],
                              xlabel='Thickness to Length (per Section)',
                              ylabel=r'Distance along Y-axis ($\mu$m)',
                              figure_width=5, figure_height=10,
                              output_prefix='section-thickness-to-length-ratio-y',
                              output_directory=output_directory,
                              color=g_dark)

    # Number of samples per section w.r.t the X-axis
    vmv.analysis.plot_scatter(xdata=length_df[Keys.SECTION_TERMINALS_THICKNESS_TO_LENGTH_RATIO],
                              ydata=length_df[Keys.Z],
                              xlabel='Thickness to Length (per Section)',
                              ylabel=r'Distance along Z-axis ($\mu$m)',
                              figure_width=5, figure_height=10,
                              output_prefix='section-thickness-to-length-ratio-z',
                              output_directory=output_directory,
                              color=b_dark)


def plot_surface_area_analysis_statistics(morphology,
                                          output_directory,
                                          sections_centers=None):

    # Collect the volume data frame
    data_frame = vmv.analysis.perform_surface_area_analysis(sections=morphology.sections_list,
                                                            sections_centers=sections_centers)

    # Section volume histogram
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.SECTION_SURFACE_AREA,
                       label=r'Section Surface Area ($\mu$m²)',
                       title='Histogram',
                       output_prefix='section-surface-area',
                       output_directory=output_directory,
                       color=vmv.consts.Color.CM_RED_DARK)

    # Section volume
    draw_scatter_plots_index_x_y_z(data_frame=data_frame,
                                   x_key=Keys.SECTION_SURFACE_AREA,
                                   title='Section Surface Area',
                                   x_axis_label=r'Section Surface Area ($\mu$m)²',
                                   output_prefix='section-surface-area',
                                   output_directory=output_directory,
                                   show_closeup=True)

    # Segment mean volume histogram
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.SEGMENT_MEAN_SURFACE_AREA,
                       label=r'Segment Mean Surface Area ($\mu$m²)',
                       title='Histogram',
                       output_prefix='segment-mean-surface-area',
                       output_directory=output_directory,
                       color=vmv.consts.Color.CM_RED_DARK)

    # Segment mean volume distribution
    draw_scatter_plots_index_x_y_z(data_frame=data_frame,
                                   x_key=Keys.SEGMENT_MEAN_SURFACE_AREA,
                                   title='Segment Mean Surface Area',
                                   x_axis_label=r'Segment Mean Surface Area ($\mu$m²)',
                                   output_prefix='segment-mean-surface-area',
                                   output_directory=output_directory,
                                   show_closeup=True)

    # Segment volume ratio histogram, per section
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.SEGMENT_SURFACE_AREA_RATIO,
                       label='Segment Surface Area Ratio',
                       title='Histogram',
                       output_prefix='segment-surface-area-ratio',
                       output_directory=output_directory,
                       color=vmv.consts.Color.CM_RED_DARK)

    # Segment volume ratio distribution, per section
    draw_scatter_plots_index_x_y_z(data_frame=data_frame,
                                   x_key=Keys.SEGMENT_SURFACE_AREA_RATIO,
                                   title='Segment Surface Area Ratio',
                                   x_axis_label='Segment Surface Area Ratio',
                                   output_prefix='segment-surface-area-ratio',
                                   output_directory=output_directory,
                                   show_closeup=False)


####################################################################################################
# plot_volume_analysis_statistics
####################################################################################################
def plot_volume_analysis_statistics(morphology,
                                    output_directory,
                                    sections_centers=None):

    # Collect the volume data frame
    data_frame = vmv.analysis.perform_volume_analysis(sections=morphology.sections_list,
                                                      sections_centers=sections_centers)

    # Section volume histogram
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.SECTION_VOLUME,
                       label=r'Section Volume ($\mu$m³)',
                       title='Histogram',
                       output_prefix='section-volume',
                       output_directory=output_directory,
                       color=vmv.consts.Color.CM_RED_DARK)

    # Section volume
    draw_scatter_plots_index_x_y_z(data_frame=data_frame,
                                   x_key=Keys.SECTION_VOLUME,
                                   title='Section Volume',
                                   x_axis_label=r'Section Volume ($\mu$m³)',
                                   output_prefix='section-volume',
                                   output_directory=output_directory,
                                   show_closeup=True)

    # Segment mean volume histogram
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.SEGMENT_MEAN_VOLUME,
                       label=r'Segment Mean Volume ($\mu$m³)',
                       title='Histogram',
                       output_prefix='segment-mean-volume',
                       output_directory=output_directory,
                       color=vmv.consts.Color.CM_RED_DARK)

    # Segment mean volume distribution
    draw_scatter_plots_index_x_y_z(data_frame=data_frame,
                                   x_key=Keys.SEGMENT_MEAN_VOLUME,
                                   title='Segment Mean Volume',
                                   x_axis_label=r'Segment Mean Volume ($\mu$m³)',
                                   output_prefix='segment-mean-volume',
                                   output_directory=output_directory,
                                   show_closeup=True)

    # Segment volume ratio histogram, per section
    vmv.plot_histogram(data_frame=data_frame,
                       data_key=Keys.SEGMENT_VOLUME_RATIO,
                       label='Segment Volume Ratio',
                       title='Histogram',
                       output_prefix='segments-volume-ratio',
                       output_directory=output_directory,
                       color=vmv.consts.Color.CM_RED_DARK)

    # Segment volume ratio distribution, per section
    draw_scatter_plots_index_x_y_z(data_frame=data_frame,
                                   x_key=Keys.SEGMENT_VOLUME_RATIO,
                                   title='Segment Volume Ratio',
                                   x_axis_label='Segment Volume Ratio',
                                   output_prefix='segment-volume-ratio',
                                   output_directory=output_directory,
                                   show_closeup=False)



def plot_analysis_angles():
    pass

def plot_analysis_branching():
    pass 

####################################################################################################
# @export_analysis_results
####################################################################################################
def export_analysis_results_(morphology,
                            output_directory):
    """Exports the analysis results to files.

    :param morphology:
        Input morphology.
    :param output_directory:
        The directory where all the results will be written.
    """

    plot_radius_analysis_statistics(morphology, output_directory)

    # plot_analysis_samples_per_section(morphology, output_directory)
    


    # plot_length_analysis_statistics(morphology, output_directory)
    #plot_surface_area_analysis_statistics(morphology, output_directory)
    #plot_volume_analysis_statistics(morphology, output_directory)
    exit(0)








    # Radius
    # Compute a data-frame for the vessel radii
    # Radius, X, Y, Z

    from matplotlib import cm
    cmap = cm.get_cmap('viridis', 20)
    cmap2 = cm.get_cmap('Set1')

    # Radius Distribution (Radius Vs Count)
    rxyz_data = vmv.VesselRadiusAnalysis.rxyz_data(morphology.sections_list)

    # Vessel radius histogram
    vmv.plot_histogram(df=rxyz_data,
                       data_key='Vessel Radius',
                       label=r'Vessel Radius ($\mu$m)',
                       title='Vessel Radius Histogram',
                       output_prefix='vessel-radius',
                       output_directory=output_directory,
                       color=cmap.colors[0])

    

    # Vessel Mean Radius
    per_section_radius_data = vmv.VesselRadiusAnalysis.analyse_per_section_radius(
        morphology.sections_list)

    # Vessel radius histogram
    vmv.plot_histogram(df=per_section_radius_data,
                       data_key='Vessel Mean Radius',
                       label=r'Vessel Radius ($\mu$m)',
                       title='Vessel Mean Radius',
                       output_prefix='vessel-xx',
                       output_directory=output_directory,
                       color=cmap.colors[3])

    vmv.plot_range_data_closeups(df=per_section_radius_data,
                                 data_key='Section Index',
                                 min_keyword='Vessel Min Radius',
                                 mean_keyword='Vessel Mean Radius',
                                 max_keyword='Vessel Max Radius',
                                 label='Section Index',
                                 output_prefix='vessel-xx',
                                 output_directory=output_directory)

    vmv.plot_range_data_xyz_with_closeups(
        df=per_section_radius_data, min_keyword='Vessel Min Radius',
        mean_keyword='Vessel Mean Radius',
        max_keyword='Vessel Max Radius',
        label='Distance', output_prefix='vessel-xx', output_directory=output_directory)

    # Samples density
    vmv.plot_histogram(df=per_section_radius_data,
                       data_key='Section Radius Ratio',
                       label='Section Radius Ratio',
                       title='Radius Ratio',
                       output_prefix='segment-radius-ratio',
                       output_directory=output_directory,
                       color=cmap2.colors[1])

    samples_per_section = vmv.VesselRadiusAnalysis.samples_per_section(morphology.sections_list)


    # Samples number samples
    vmv.plot_scatter(xdata=samples_per_section['Number Samples'],
                     ydata=samples_per_section['Section Index'],
                     xlabel='Number of Samples',
                     ylabel='Section Index',
                     output_prefix='samples-per-section-index',
                     output_directory=output_directory,
                     color=cmap2.colors[4])

    # Samples number samples
    vmv.plot_scatter(xdata=samples_per_section['Number Samples'],
                     ydata=samples_per_section['X'],
                     xlabel='Number of Samples',
                     ylabel=r'Distance along X-axis ($\mu$m)',
                     figure_width=5, figure_height=10,
                     output_prefix='samples-per-section-x',
                     output_directory=output_directory,
                     color=cmap2.colors[0])

    # Samples number samples
    vmv.plot_scatter(xdata=samples_per_section['Number Samples'],
                     xlabel='Number of Samples',
                     ylabel=r'Distance along Y-axis ($\mu$m)',
                     figure_width=5, figure_height=10,
                     ydata=samples_per_section['Y'],
                     output_prefix='samples-per-section-y',
                     output_directory=output_directory,
                     color=cmap2.colors[2])
    # Samples number samples
    vmv.plot_scatter(xdata=samples_per_section['Number Samples'],
                     xlabel='Number of Samples',
                     ylabel=r'Distance along Z-axis ($\mu$m)',
                     ydata=samples_per_section['Z'],
                     figure_width=5, figure_height=10,
                     output_prefix='samples-per-section-z',
                     output_directory=output_directory,
                     color=cmap2.colors[1])




    vmv.analysis.plot_histogram(
        df=samples_per_section, data_key=['Number Samples'], title='# Samples / Section Hist',
        label='Number Samples',
        output_directory=output_directory, output_prefix='number-samples-histo',
        save_svg=False)

    for axis in ['X', 'Y', 'Z']:
        vmv.analysis.plot_histogram(
            df=samples_per_section, data_key=[axis], title='# Samples / Section Hist',
            label=axis,
            output_directory=output_directory, output_prefix='number-samples-histo-%s' % axis,
            save_svg=False)

    vmv.analysis.plot_histogram(
        df=samples_per_section, data_key=['Number Samples'], title='# Samples / Section Hist',
        label='Number Samples',
        output_directory=output_directory, output_prefix='number-samples-histo',
        save_svg=False)


    two_samples_per_section = list()
    for index, row in samples_per_section.iterrows():
        if row['Number Samples'] == 2:
            two_samples_per_section.append(row)

    import pandas
    two_samples_per_section = pandas.DataFrame(
        two_samples_per_section, columns=['Section Index', 'Number Samples', 'X', 'Y', 'Z'])

    # Samples number samples
    vmv.plot_scatter(xdata=two_samples_per_section['Number Samples'],
                     ydata=two_samples_per_section['X'],
                     xlabel='Number of Samples',
                     ylabel=r'Distance along X-axis ($\mu$m)',
                     figure_width=5, figure_height=10,
                     output_prefix='2-samples-per-section-x',
                     output_directory=output_directory,
                     color=cmap2.colors[0])

    vmv.analysis.plot_histogram(
        df=two_samples_per_section, data_key=['X'], title='2 Samples', label='X axis',
        output_directory=output_directory, output_prefix='2-samples-per-section-x',
        save_svg=False)



    import matplotlib
    pastel1 = matplotlib.cm.get_cmap('Set1')
    light_colors = [pastel1.colors[0], pastel1.colors[2], pastel1.colors[1]]

    vmv.plot_scatter_data_with_closeups(df=rxyz_data,
                                        idep_axis_label=r'Distance along X-axis ($\mu$m)',
                                        dep_axis_label=r'Sample Radius ($\mu$m)',
                                        idep_keyword='X',
                                        dep_keyword='Vessel Radius',
                                        output_prefix='segment-radius-x',
                                        light_color=light_colors[0],
                                        output_directory=output_directory)

    vmv.plot_scatter_data_with_closeups(df=rxyz_data,
                                        idep_keyword='Y',
                                        idep_axis_label=r'Distance along Y-axis ($\mu$m)',
                                        dep_axis_label=r'Sample Radius ($\mu$m)',
                                        dep_keyword='Vessel Radius',
                                        output_prefix='segment-radius-y',
                                        light_color=light_colors[2],
                                        output_directory=output_directory)

    vmv.plot_scatter_data_with_closeups(df=rxyz_data,
                                        idep_keyword='Z',
                                        idep_axis_label=r'Distance along Z-axis ($\mu$m)',
                                        dep_axis_label=r'Sample Radius ($\mu$m)',
                                        dep_keyword='Vessel Radius',
                                        output_prefix='segment-radius-z',
                                        light_color=light_colors[1],
                                        output_directory=output_directory)



    analysis_items = [

        [vmv.analysis.compute_number_of_samples_per_section_distribution,
         'Number of Samples / Section',
         'number-samples-per-section'],

        [vmv.analysis.compute_sample_radius_distribution,
         'Sample Radius (μm)',
         'samples-radius'],

        [vmv.analysis.compute_sections_average_radius_distributions,
         'Section Average Radius (μm)',
         'section-average-radius'],

        [vmv.analysis.compute_segments_length_distributions,
         'Segment Length (μm)',
         'segments-length'],

        [vmv.analysis.compute_sections_length_distributions,
         'Section Length (μm)',
         'section-length'],

        [vmv.analysis.compute_segments_surface_area_distribution,
         'Segment Surface Area (μm²)',
         'segments-surface-area'],

        [vmv.analysis.compute_sections_surface_area_distribution,
         'Section Surface Area (μm²)',
         'section-surface-area'],

        [vmv.analysis.compute_segments_volume_distribution,
         'Segment Volume (μm³)',
         'segments-volume'],

        [vmv.analysis.compute_sections_volume_distribution,
         'Section Volume (μm³)',
         'section-volume'],
    ]

    palette = pyplot.get_cmap('tab20')
    palette = palette(numpy.linspace(0, 1.0, len(analysis_items) + 1))

    for i, analysis_item in enumerate(analysis_items):
        print('\t *%s' % analysis_item[1])
        apply_analysis_kernel(morphology=morphology,
                              function=analysis_item[0],
                              title=analysis_item[1],
                              label='%s-%s' % (morphology.name, analysis_item[2]),
                              color=palette[i],
                              output_directory=output_directory)

    # Spatial distributions
    xyz_distributions = [

        [vmv.analysis.compute_sample_radius_distribution_along_axes,
         'Sample Mean Radius (μm)',
         'sample-average-radius',
         'Radius'],

        [vmv.analysis.compute_segment_length_distribution_along_axes,
         'Segment Mean Length (μm)',
         'segment-average-length',
         'Length'],

        [vmv.analysis.compute_segment_surface_area_distribution_along_axes,
         'Segment Mean Surface Area (μm²)',
         'segment-average-surface-area',
         'Area'],

        [vmv.analysis.compute_segment_volume_distribution_along_axes,
         'Segment Mean Volume (μm³)',
         'segment-average-volume',
         'Volume'],
    ]

    for i, analysis_item in enumerate(xyz_distributions):
        print('\t *%s' % analysis_item[1])
        apply_xyz_analysis_kernel(morphology=morphology,
                                  function=analysis_item[0],
                                  title=analysis_item[1],
                                  label='%s-%s' % (morphology.name, analysis_item[2]),
                                  keyword=analysis_item[3],
                                  output_directory=output_directory)

    section_distributions = [
        [vmv.analysis.compute_section_radius_distribution,
         'Section Radius Distribution (μm)',
         'section-radius-distribution',
         'Section Index',
         'Mean Sample Radius',
         'Min. Sample Radius',
         'Max. Sample Radius'],
    ]

    for i, analysis_item in enumerate(section_distributions):
        print('\t *%s' % analysis_item[1])
        apply_section_distribution_analysis_kernel(
            morphology=morphology, function=analysis_item[0], title=analysis_item[1],
            label='%s-%s' % (morphology.name, analysis_item[2]),
            df_sorting_keyword=analysis_item[3],
            df_average_keyword=analysis_item[4],
            df_minimum_keyword=analysis_item[5],
            df_maximum_keyword=analysis_item[6],
            output_directory=output_directory)

    # Histograms
    histograms = [
        [vmv.analysis.compute_section_radius_ratio_distribution,
         'Radius Ratio Histogram',
         'Radius Ratio',
         'Radius Ratio',
         'section-radius-ratio-distribution'],

        [vmv.analysis.compute_segment_length_ratio_distribution,
         'Segment Length Ratio Histogram',
         'Length Ratio',
         'Length Ratio',
         'segment-length-ratio-distribution'],

        [vmv.analysis.compute_number_of_samples_per_section_distribution_,
         'Number of Samples / Section',
         'Number of Samples / Section',
         'Number Samples',
         'number-samples-per-section-distribution'],

        [vmv.analysis.compute_samples_density,
         'Density',
         'Density',
         'X',
         'density-x'],

        [vmv.analysis.compute_samples_density,
         'Density',
         'Density',
         'Y',
         'density-y']

    ]

    for element in histograms:

        # Apply the kernel to the morphology and compute the dataframe
        function = element[0]
        title = element[1]
        label = element[2]
        data_key = element[3]
        output_prefix = element[4]

        # Apply the function to the morphology and return the data frame
        df = function(morphology)


        # Plot the profile
        vmv.analysis.plot_histogram(
            df=df, data_key=data_key, title=title, label=label,
            output_directory=output_directory, output_prefix=output_prefix, save_svg=False)
        if ('Density' in title):
            w = morphology.bounding_box.bounds[0]
            h = morphology.bounding_box.bounds[1]

            w_r = 1.0 * 10
            h_r = (1.0 * h / w) * 10
            vmv.analysis.plot_scatter(df=df, x_keyword='X', y_keyword='Y',
                                      figure_width=w_r, figure_height=h_r)

    # Density






