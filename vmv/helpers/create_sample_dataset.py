####################################################################################################
# Copyright (c) 2019, EPFL / Blue Brain Project
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

import math 

class Point:
	def __init__(x=0.0, y=0.0, z=0.0, r=0.1, index=-1):
		self.x = x
		self.y = y
		self.z = z
		self.r = r
		self.index = index
		
def create_stright_line(p0, p1, number_points, starting_index=0):
	
	d = Point()
	d.x = p0.x - p1.x
	d.y = p0.y - p1.y
	d.z = p0.z - p1.z
	distance = math.sqrt(d.x * d.x + d.y * d.y + d.z * d.z)
	step = distance / number_points
	
	points = list()
	for i in range(steps):
		p = Point()
		p.x = p0.x + step * i
		p.y = p0.y + step * i
		p.z = p0.z + step * i
		p.index = starting_index + i
		points.append(p)
	return points
	

	
