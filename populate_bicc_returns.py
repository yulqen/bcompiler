# -*- coding: utf-8 -*-
"""
    bicc_excel.populate_bicc_returns
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Populate blank BICC Return forms from a master xlsx template.

    :copyright: (c) 2016 by Matthew Lemon.
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    
"""

from openpyxl import load_workbook, Workbook
import re


cell_regex = re.compile('[A-Z]+[0-9]+')

SOURCE_MASTER = 'q2_source_files/master_test.xlsx'

def get_sheet_names(source_file):
    wb = load_workbook(source_file, read_only=True)
    return wb.get_sheet_names()


def get_sheet_data(source_file):
    wb = load_workbook(source_file, read_only=True)
    ws = wb['GMPP Return - DfT']

    for row in ws.rows:
        for cell in row:
            if cell.value != None:
                print(cell.value)


