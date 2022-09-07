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
from app.field import Field
#from utils import resourcemgr
from utils.utils import Utils
from datetime import datetime
from string import Template
from io import StringIO
import spacy

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
TMPL_KEYWORD_HEADER = Template('''
Frequency of keywords (title and abstract)
$keyword_count unique keywords
''')
TMPL_KEYWORD_FREQ = Template('''$keyword\t$frequency
''')

#resMgr = resourcemgr.ResourceManager()
#"""
#Load the resource manager.
#"""

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
        
        # Initialize spacy 'en_core_web_trf' model, keeping only tagger component needed for lemmatization
        #self.nlp = spacy.load(resMgr.getNLPModelPath(), disable=['parser', 'ner'])
        self.nlp = spacy.load('en_core_web_trf', disable=['parser', 'ner'])
        self.stop_words = self.nlp.Defaults.stop_words
        #stop_words |= {' ', '.', ':', '(', ')', ',', "'", }
    
    def __getToday(self):
        return datetime.now().strftime('%d/%m/%Y %H:%M:%S')
    
    def __genYearFrequency(self):
        year_freq = {}
        for entry in self.entries:
            year = entry.getFieldValue(FieldName.Year)
            year_freq[year] = (year_freq[year] + 1 if year in year_freq else 1)
        for year in Utils().sort_dict_by_key(year_freq):
            yield (year, year_freq[year])
    
    def __getTotalContributors(self):
        contributor_count = 0
        for entry in self.entries:
            contributor_count += len(entry.getContributors())
        return contributor_count
    
    def __genContributorFrequency(self):
        contributor_freq = {}
        for entry in self.entries:
            contributors = entry.getContributors()
            for cont in contributors:
                cont = Field.simplify(str(cont))
                contributor_freq[cont] = (contributor_freq[cont] + 1 if cont in contributor_freq else 1)
        for cont, freq in Utils().sort_dict_by_value(contributor_freq, False):
            yield (cont, freq)
    
    def __genEntryTypeCount(self):
        entry_type_count = {}
        for entry in self.entries:
            entry_type = entry.getEntryType()
            entry_type_count[entry_type] = (entry_type_count[entry_type] + 1 if entry_type in entry_type_count else 1)
        for entry_type, count in Utils().sort_dict_by_value(entry_type_count, False):
            yield (entry_type, count)
    
    def __genKeywordFrequency(self):
        keyword_freq = {}
        keywords = ' '
        for entry in self.entries:
            keywords = '. '.join([keywords, entry.getFieldValue(FieldName.Title), entry.getFieldValue(FieldName.Abstract)])
        for keyword in self.lemmatize(keywords):
            k = Field.simplify(keyword)
            keyword_freq[k] = (keyword_freq[k] + 1 if k in keyword_freq else 1)
        for keyword,freq in Utils().sort_dict_by_value(keyword_freq, False):
            yield (keyword, freq)
    
    def lemmatize(self, text):
        """
        Generator that tokenizes a text by stemming each word ignoring stop words.
        @type text: L{str}
        @param total: The text to lemmatize.
        @rtype: L{str}
        @return: All the unique words.
        """
        # Parse the text
        doc = self.nlp(text)
        # Extract the lemma for each token and join
        for token in doc:
            if not token.lemma_ in self.stop_words and not token.is_punct and not token.is_digit:
                yield token.lemma_
    
    def generate(self, total=None, validation=None, path=None):
        """
        Generates the report as a dictionary object
        @type total: L{int}
        @param total: The total number of entries.
        @type validation: L{dict}
        @param validation: The dictionary of the validation results (optional).
        @type path: L{str}
        @param path: The path of the BibTeX file.
        @rtype: L{dict}
        @return: Dictionary of the report
        """
        report = {}
        report['datetime'] = self.__getToday()
        report['filename'] = path
        report['total_entries'] = total
        report['validation'] = { 'success': validation['success'],'warning': validation['warning'],'error': validation['error'] }
        report['year_frequency'] = [i for i in self.__genYearFrequency()]
        report['total_contributor'] = self.__getTotalContributors()
        report['contributor_frequency'] = [i for i in self.__genContributorFrequency()]
        report['unique_contributors'] =  len(report['contributor_frequency'])
        report['entry_type_count'] = [i for i in self.__genEntryTypeCount()]
        report['keyword_frequency'] = [i for i in self.__genKeywordFrequency()]
        report['total_keyword'] = len(report['keyword_frequency'])
        return report
    
    def generateText(self, total=None, validation=None, path=None):
        """
        Generates the report as text
        @type total: L{int}
        @param total: The total number of entries.
        @type validation: L{dict}
        @param validation: The dictionary of the validation results (optional).
        @type path: L{str}
        @param path: The path of the BibTeX file.
        """
        report = self.generate(total, validation, path)
        buffer = StringIO()
        buffer.write(TMPL_HEADER.substitute(today=report['datetime'], file_name=report['filename']))
        buffer.write(TMPL_SEPARATOR)
        if total:
            buffer.write(TMPL_TOTAL.substitute(total=report['total_entries']))
            buffer.write(TMPL_SEPARATOR)
        if validation:
            buffer.write(TMPL_VALIDATION.substitute(
                success=report['validation']['success'], warning=report['validation']['warning'], error=report['validation']['error']))
            buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_CONTRIBUTORS.substitute(contributors=report['total_contributor'], unique_contributors=report['unique_contributors']))
        for cont,freq in report['contributor_frequency']:
            buffer.write(TMPL_CONTRIB_FREQ.substitute(contributor=cont,frequency=freq))
        buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_ENTRYTYPE_HEADER)
        for entry_type,count in report['entry_type_count']:
            buffer.write(TMPL_ENTRYTYPE_COUNT.substitute(entry_type=entry_type,count=count))
        buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_YEAR_HEADER)
        for year,freq in report['year_frequency']:
            buffer.write(TMPL_YEAR_COUNT.substitute(year=year,count=freq))
        buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_KEYWORD_HEADER.substitute(keyword_count=report['total_keyword']))
        for keyword,freq in report['keyword_frequency']:
            buffer.write(TMPL_KEYWORD_FREQ.substitute(keyword=keyword,frequency=freq))
        buffer.write(TMPL_SEPARATOR)
        buffer.write(TMPL_FOOTER)
        return buffer.getvalue()