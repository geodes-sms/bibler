'''
BiBler - A software to manage references of scientific articles using BibTeX.
Copyright (C) 2018  Eugene Syriani

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

"""
.. moduleauthor:: Eugene Syriani

.. versionadded:: 1.4.4

Created on Aug 27, 2022

This module represents the report generator
"""

from app.field_name import FieldName
from utils import settings, utils
from utils.settings import Preferences
import os.path


class ReportGenerator(object):
    """
    The abstract class for importing or exporting.
    Every Impex has a C{path} to the database file and a C{database} file handler.
    """
    def __init__(self, entries):
        """
        @type path: L{List<entry.Entry>}
        @param path: The list of entries.
        """
        self.entries = entries
    
    def generate(self, validation=None):
        """
        Generates the report
        @type validation: L{dict}
        @param validation: The dictionary of the validation results (optional).
        """
        #TODO: write the report generation code here
        for entry in self.entries:
            pass
        return 'Nada'