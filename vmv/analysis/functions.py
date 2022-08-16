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
import matplotlib.pyplot as pyplot

# Internal imports
import vmv.utilities


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


####################################################################################################
# @export_analysis_results
####################################################################################################
def export_analysis_results(morphology,
                            output_directory):
    """Exports the analysis results to files.

    :param morphology:
        Input morphology.
    :param output_directory:
        The directory where all the results will be written.
    """

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
         'Sample\nMean Radius (μm)',
         'sample-average-radius',
         'Radius'],

        [vmv.analysis.compute_segment_length_distribution_along_axes,
         'Segment\nMean Length (μm)',
         'segment-average-length',
         'Length'],

        [vmv.analysis.compute_segment_surface_area_distribution_along_axes,
         'Segment\nMean Surface Area (μm²)',
         'segment-average-surface-area',
         'Area'],

        [vmv.analysis.compute_segment_volume_distribution_along_axes,
         'Segment\nMean Volume (μm³)',
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



