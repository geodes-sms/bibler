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
from utils.utils import Utils
from datetime import datetime
from string import Template
from io import StringIO

"""
Template strings for the report
"""
TMPL_SEPARATOR = '''-----------------------
'''
TMPL_HEADER = Template('''
BiBler Report on $today for file
$file_name
''')
TMPL_FOOTER = '''
Report complete.
'''
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
TMPL_CONTRIB_FREQ = Template('''$contributor\t$frequency
''')
TMPL_ENTRYTYPE_HEADER = '''
Number of references per entry type
'''
TMPL_ENTRYTYPE_COUNT = Template('''$entry_type\t$count
''')
TMPL_YEAR_HEADER = '''
Number of references per year
'''
TMPL_YEAR_COUNT = Template('''$year\t$count
''')
TMPL_KEYWORD_HEADER = '''
Frequency of keywords (title and abstract)
'''
TMPL_KEYWORD_FREQ = Template('''$keyword\t$frequency
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
    
    def generate(self, total=None, validation=None, path=None):
        """
        Generates the report
        @type total: L{int}
        @param total: The total number of entries.
        @type validation: L{dict}
        @param validation: The dictionary of the validation results (optional).
        @type path: L{str}
        @param path: The path of the BibTeX file.
        """
        buffer = StringIO()
        buffer.write(TMPL_HEADER.substitute(today=datetime.now().strftime('%d/%m/%Y %H:%M:%S'),file_name=path))
        buffer.write(TMPL_SEPARATOR)
        if total:
            buffer.write(TMPL_TOTAL.substitute(total=total))
            buffer.write(TMPL_SEPARATOR)
        if validation:
            buffer.write(TMPL_VALIDATION.substitute(success=validation['success'],warning=validation['warning'],error=validation['error']))
            buffer.write(TMPL_SEPARATOR)
        year_freq = {}
        contributor_count = 0
        contributor_freq = {}
        entry_type_count = {}
        keyword_freq = {}
        for entry in self.entries:
            #TODO: build the dictionaries
            # use Utils().tex2simple(tex_value)
            year = entry.getFieldValue(FieldName.Year)
            year_freq[year] = (year_freq[year] + 1 if year in year_freq else 1)
            entry_type = entry.getEntryType()
            entry_type_count[entry_type] = (entry_type_count[entry_type] + 1 if entry_type in entry_type_count else 1)
        buffer.write(TMPL_CONTRIBUTORS.substitute(contributors=contributor_count,unique_contributors=len(contributor_freq)))
        for item in Utils().sort_dict_by_value(contributor_freq, False):
            cont,freq=item
            buffer.write(TMPL_CONTRIB_FREQ.substitute(contributor=cont,frequency=freq))
        buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_ENTRYTYPE_HEADER)
        for item in Utils().sort_dict_by_value(entry_type_count, False):
            entry_type,count = item
            buffer.write(TMPL_ENTRYTYPE_COUNT.substitute(entry_type=entry_type,count=count))
        buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_YEAR_HEADER)
        for year in Utils().sort_dict_by_key(year_freq):
            buffer.write(TMPL_YEAR_COUNT.substitute(year=year,count=year_freq[year]))
        buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_KEYWORD_HEADER)
        for item in Utils().sort_dict_by_value(keyword_freq, False):
            keyword,freq = item
            buffer.write(TMPL_KEYWORD_FREQ.substitute(keyword=keyword,frequency=freq))
        buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_FOOTER)
        return buffer.getvalue()