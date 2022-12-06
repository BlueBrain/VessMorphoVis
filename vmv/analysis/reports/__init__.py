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
from fpdf import FPDF

# Internal imports
import vmv.consts


####################################################################################################
# @PDFReport
####################################################################################################
class PDFReport(FPDF):

    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(30, 10, '', 0, 0, 'C')

    def footer(self):
        self.set_y(-8)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 8, 'This report is automatically generated with VessMorphoVis, Page ' + str(
            self.page_no()) + ' / {nb}', 0, 0, 'C',
                  link='https://github.com/BlueBrain/VessMorphoVis')

    def add_central_title(self, text, x_start=0, y_start=20):
        self.set_x(x_start)
        self.set_y(y_start)
        self.set_font('Arial', '', 15)
        self.cell(0, 0, text, border=0, align='C')

    def add_section_title(self, text, x_start=0, y_start=0):
        self.set_x(x_start)
        self.set_y(y_start)
        self.set_font('Arial', '', 10)
        self.cell(0, 0, text, border=0, align='L')

    def add_default_table_cell(self, quantity, value, y_start=0, x_margin=10,
                               cell_height=vmv.consts.Geometry.TABLE_CELL_HEIGHT):

        # Compute the width of the cells
        page_width = vmv.consts.Geometry.PDF_PAGE_WIDTH
        table_width = page_width - (x_margin * 2)
        quantity_cell_width = 0.7 * table_width
        value_cell_width = table_width - quantity_cell_width

        # Adjust the value format
        value_string = str(value)
        if isinstance(value, int):
            value_string = str(value)
        elif isinstance(value, float):
            if value < 1e-4:
                value_string = "{:.5e}".format(value)
            else:
                value_string = "{:.5f}".format(value)

        self.set_font('Arial', '', 9)
        self.set_fill_color(220, 220, 220)
        self.set_y(y_start)
        self.cell(quantity_cell_width, cell_height, str(quantity) + '  ',
                  border=0, align='R', fill=True)
        self.set_fill_color(235, 235, 235)
        self.cell(value_cell_width, cell_height, '  ' + value_string,
                  border=0, align='C', fill=True)

    def save_report(self, path):
        self.output(path + '.pdf', 'F')

