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

# System imports
import time


####################################################################################################
# @Timer
####################################################################################################
class Timer:

    ################################################################################################
    # @__init__
    ################################################################################################
    def __init__(self):
        """Constructor
        """

        # Starting time
        self.starting_time = 0.0

        # Ending time
        self.ending_time = 0.0

    ################################################################################################
    # @start
    ################################################################################################
    def start(self):
        """Start the timer.
        """

        # Start the timer
        self.starting_time = time.time()

    ################################################################################################
    # @end
    ################################################################################################
    def end(self):
        """End the timer.
        """

        # End the timer
        self.ending_time = time.time()

    ################################################################################################
    # @duration
    ################################################################################################
    def duration(self):
        """Get the duration of the timer in milliseconds.
        """

        # Return the duration in milliseconds.
        return self.ending_time - self.starting_time
