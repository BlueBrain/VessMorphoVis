####################################################################################################
# Copyright (c) 2019 - 2023, EPFL / Blue Brain Project
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

# Internal imports
import vmv.geometry
import vmv.skeleton
import vmv.utilities


####################################################################################################
# @add_samples_at_terminals
####################################################################################################
def add_samples_at_terminals(section):
    """Adds duplicate samples at the terminals of the given section. Note that to perform any
    sample-related operation, re-re-indexing the samples of the entire morphology must be performed.

    :param section:
        A given section to add duplicate samples at its terminals.
    """

    # First terminal sample
    sample_1 = vmv.skeleton.Sample(
        point=section.samples[0].point, radius=section.samples[0].radius, index=-1)
    section.samples.insert(0, sample_1)

    # Last terminal sample
    sample_2 = vmv.skeleton.Sample(
        point=section.samples[-1].point, radius=section.samples[-1].radius, index=-1)
    section.samples.append(sample_2)


####################################################################################################
# @resample_section_at_fixed_step
####################################################################################################
def resample_section_at_fixed_step(section,
                                   sampling_step=1.0,
                                   resample_shorter_sections=True):
    """Resamples the section at a given sampling step. If the section has only two sample,
    it will never get resampled. If the section length is smaller than the sampling step, a
    convenient sampling step will be computed and used.

    :param section:
        A given section to resample.
    :param sampling_step:
        User-defined sampling step, by default 1.0 micron.
    :param resample_shorter_sections:
        If this flag is set to True, the short sections will be resampled.
    """

    # If the section has no samples, report this as an error and ignore this filter
    if len(section.samples) == 0:
        vmv.logger.error('Section [%s: %d] has NO samples, cannot be re-sampled' %
                         (section.get_type_string(), section.index))
        return

    # If the section has ONLY one sample, report this as an error and ignore this filter
    elif len(section.samples) == 1:
        vmv.logger.error('Section [%s: %d] has only ONE sample, cannot be re-sampled' %
                         (section.get_type_string(), section.index))
        return

    # If the section length is less than the sampling step, then adaptively resample it
    if vmv.skeleton.compute_section_length(section=section) < sampling_step:
        if resample_shorter_sections:

            # Get a good sampling step that would match this small section
            section_length = vmv.skeleton.compute_section_length(section=section)
            section_number_samples = len(section.samples)
            section_step = section_length / section_number_samples

            # Resample the section at this sampling step
            resample_section_at_fixed_step(section=section, sampling_step=section_step)
        return

    # Sample index
    i = 0

    # Just keep moving along the section till you hit the last section
    while True:

        # Break if we reach the last sample
        if i >= len(section.samples) - 1:
            break

        # Compute the distance between the current sample and the next one
        distance = (section.samples[i + 1].point - section.samples[i].point).length

        # If the distance is less than the resampling step, then remove this sample  at [i + 1]
        if distance < sampling_step:

            if i >= len(section.samples) - 2:
                break

            # Remove the sample
            section.samples.remove(section.samples[i + 1])

            # Proceed to the next sample
            continue

        # If the sample is at a greater step, then add a new sample exactly at the current step
        else:

            # Compute the auxiliary sample radius based on the previous and next samples
            radius = (section.samples[i + 1].radius + section.samples[i].radius) / 2.0

            # Compute the direction
            direction = (section.samples[i + 1].point - section.samples[i].point).normalized()

            # Compute the auxiliary sample point, use epsilon for floating point comparison
            point = section.samples[i].point + (direction * sampling_step)

            # Add the auxiliary sample, the index of the sample is set to -1 (auxiliary sample)
            auxiliary_sample = vmv.skeleton.Sample(
                point=point, radius=radius, index=-1)

            # Update the samples list
            section.samples.insert(i + 1, auxiliary_sample)

            # Move to the nex sample
            i += 1

            # Break if we reach the last sample
            if i >= len(section.samples) - 1:
                break


####################################################################################################
# @resample_samples_list_adaptively
####################################################################################################
def resample_samples_list_adaptively(samples):
    """Re-samples a list of samples adaptively.

    :param samples:
        A list of samples to be re-sampled.
    """

    # If the section has less then four samples, ignore this filter and return
    if len(samples) < 4:
        return

    # The section has more than three samples, then it can be re-sampled, but never remove
    # the first or the last samples

    i = 0
    while True:

        # Just keep the last sample of the branch just in case
        if i < len(samples) - 2:

            sample_1 = samples[i]
            sample_2 = samples[i + 1]

            # Segment length
            segment_length = (sample_2.point - sample_1.point).length

            # If the distance between the two samples if less than the radius of the first
            # sample remove the second sample
            if segment_length < sample_1.radius + sample_2.radius:
                samples.remove(samples[i + 1])
                i = 0
            else:
                i += 1

        # No more samples to process, break please
        else:
            break


####################################################################################################
# @resample_section_adaptively
####################################################################################################
def resample_section_adaptively(section):
    """Re-samples the sections adaptively based on the radii of each sample and the distance between
    each two consecutive samples.

    :param section:
        A given section to resample.
    """

    return resample_samples_list_adaptively(section.samples)