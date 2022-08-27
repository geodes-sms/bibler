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
from utils import utils
from datetime import date
from string import Template
from cStringIO import StringIO

"""
Template strings for the report
"""
SEPARATOR = '-----------------------'
TMPL_HEADER = Template('''
BiBler Report on $today
''')
TMPL_FOOTER = Template('''
Report complete.
''')
TMPL_TOTAL = Template('''
Total references: $total
''')
TMPL_VALIDATION = Template('''
$success correct references
$warning references with warnings
$error references with errors
''')
TMPL_CONTRIBUTORS = Template('''
$contributors authors/contributors
$unique_contributors unique authors/contributors
Frequency of contributors
''')
TMPL_CONTRIB_FREQ = Template('''
$contributor: $frequency
''')
TMPL_ENTRYTYPE_HEADER = Template('''
Number of references per entry type
''')
TMPL_ENTRYTYPE_COUNT = Template('''
$entry_type: $count
''')
TMPL_YEAR_HEADER = Template('''
Number of references per year
''')
TMPL_YEAR_COUNT = Template('''
$year: $count
''')
TMPL_KEYWORD_HEADER = Template('''
Frequency of keywords (title and abstract)
''')
TMPL_KEYWORD_FREQ = Template('''
$keyword: $frequency
''')

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
    
    def generate(self, total=None, validation=None):
        """
        Generates the report
        @type validation: L{dict}
        @param validation: The dictionary of the validation results (optional).
        """
        buffer = StringIO()
        buffer.write(TMPL_HEADER.substitute(today=date.now()))
        if total:
            buffer.write(TMPL_TOTAL.substitute(total=total))
        if validation:
            buffer.write(TMPL_VALIDATION.substitute(success=validation['success'],warning=validation['warning'],error=validation['error']))
        year_freq = {}
        contributor_count = 0
        contributor_freq = {}
        entry_type_count = {}
        keyword_freq = {}
        for entry in self.entries:
            #TODO: build the dictionaries
            # use utils.Util.tex2simple(tex_value)
            pass
        buffer.write(TMPL_CONTRIBUTORS.substitute(contributors=contributor_count,unique_contributors=len(contributor_freq)))
        for cont,freq in contributor_freq:
            buffer.write(TMPL_CONTRIB_FREQ.substitute(contributor=cont,frequency=freq))
        #TODO: continue buffers here. Add SEPARATOR
        return buffer.getValue()