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
.. moduleauthor:: Florin Oncica 

.. versionadded:: 1.0

Created on Nov 09, 2016

This module represents the BiTeX parser.
"""

import re
#import unicodedata
from app.entry import EmptyEntry
from app.entry_type import EntryType
from app.field_name import FieldName
from app.field import Field
from utils.settings import Preferences
from utils.utils import Utils
#from docutils.parsers.rst.directives import encoding


class BibTeXParserWithStdFields(object):
    """
    Same as :class:`BibTeXParser <app.bibtex_parser.BibTeXParser>` but only looks at standard fields in the BibTeX entry.
    """
    def __init__(self, bibtex):
        """
        (Constructor)
           
        :param bibtex: The BibTeX string.
        :type bibtex: str.
        """
        #bibtex = bibtex.decode('utf-8','replace')           # make sure the text is in utf-8 encoding
        bibtex = bibtex.replace('{\n', '{stubKey,\n')       # if key is missing
        bibtex = Utils().unicode2Tex(bibtex)                  # replace unicode characters to TeX equivalent
        #bibtex = unicodedata.normalize('NFKD', bibtex).encode(encoding='ascii', errors='ignore')  # replace unicode characters with their ASCII approximation
        bibtex = bibtex.strip()                             # remove all leading and trailing spaces
        self.bibtex = self.remove_comments(bibtex)          # remove all comments
        self.bibtex = self.bibtex.replace('\n', ' ')        # remove all new lines
        self.bibtex = re.sub('=\s*\"', '= {', self.bibtex)  # replace all double quotes that delimit the beginning of a field value
        self.bibtex = re.sub('\"\s*,', '},', self.bibtex)   # replace all double quotes that delimit the end of a field value
        self.re_header = re.compile("""\s*@(\w+)\s*[({]\s*([\w-]*)\s*""", re.RegexFlag.DOTALL)
        self.entry = None
    
    def remove_comments(self, bibtex):
        """
        Removes all the comments (starting with %) in the BibTeX string
        :param bibtex: The BibTeX string.
        :type field: str
        :return: str -- The uncommented BibTeX string.
        """
        bibtex = bibtex.splitlines()
        new_bibtex = ''
        for i in range(len(bibtex)):
            comment_position = bibtex[i].find('%')
            if comment_position >= 0:
                if bibtex[i][comment_position-1] != '\\':
                    # in a line, ignore everything after %, except if it is escaped \%
                    new_bibtex += bibtex[i][:comment_position]
                else:
                    # It was escaped so keep the text after \%
                    new_bibtex += bibtex[i]
            else:
                # no comments on this line, so keep it
                new_bibtex += bibtex[i]
        return new_bibtex

    def parse(self):
        """
        Parses the string into an :class:`Entry <app.entry.Entry>`
        
        :returns: :class:`Entry <app.entry.Entry>`
        The entry object corresponding to its type. The default is :class:`EmptyEntry <app.entry.EmptyEntry>`
        """
        self.parseEntryHeader()
        self.parseFields()
        return self.entry
    
    def parseEntryHeader(self):
        """
        Parse the type of the entry and its key.
        """
        # 1. Get the type of entry
        if not self.bibtex:
            self.entry = EmptyEntry()
            return
        header = self.re_header.match(self.bibtex)
        if not header:
            raise Exception('Invalid BibTeX.')
        entryType = header.group(1)
        self.entry = EntryType.createEntry(entryType)
        if not isinstance(self.entry, EmptyEntry):            
            # 2. Get the key
            self.entry.setKey(header.group(2))
    
    def parseFields(self):
        """
        Parse all the fields of the entry.
        """
        for field in self.entry.iterAllFields():
            value = self.findField(field.getName()).strip()
            self.entry.setField(field.getName(), value)
            self.entry.formatField(field.getName())
        
    def findField(self, field):
        """
        Finds the value of a field.
             
        :param field: The field.
        :type field: str
        :return: str -- The value.
        """
        sep = '{'
        inv_sep = '}'
        result = re.findall(""",\s*(""" + field + """)\s*=\s*\{\s*(.*)\s*\}\s*,?""", self.bibtex, re.RegexFlag.DOTALL|re.RegexFlag.IGNORECASE)
        if len(result) == 0 or len(result[0]) != 2:
            return ''
        value = self.__parseNested(sep + result[0][1] + inv_sep, sep, inv_sep, 0)
        if not value:
            return ''
        value = re.sub("""\s+""", ' ', value).strip()
        if value.endswith('"'):
            value = value[:-1]
        return value
    
    def __parseNested(self, s, separator, inv_separator, level):
        """
        Finds the string delimited within separators, even if the same separators are used inside the string.
        
        :param s: The string.
        :type s: str
        
        :param separator: The opening separator.
        :type separator: str
        
        :type inv_separator: str
        :param inv_separator: The closing separator.
        
        :type level: str
        :param level: The level of nesting for finding the string to return.
        
        :returns: str -- The result.
        """
        stack = []
        for i,_ in enumerate(s):
            if s[i:i+len(separator)] == separator and not (s[i:i+len(inv_separator)] == inv_separator):
                stack.append(i)
            elif s[i:i+len(inv_separator)] == inv_separator and stack:
                start = stack.pop()
                if len(stack) == level:
                    return s[start + 1: i]

class BibTeXParserWithNonStdFields(BibTeXParserWithStdFields):
    """
    Same as :class:`BibTeXParser <app.bibtex_parser.BibTeXParser>` but allows for additional non-standard fields in the BibTeX entry.
    """
    def __init__(self, bibtex):
        """
        (Constructor)
           
        :param bibtex: The BibTeX string.
        :type bibtex: str.
        """
        super(BibTeXParserWithNonStdFields, self).__init__(bibtex)
        self.re_field_name = re.compile("""},\s*(.*?)\s*=\s*\{""", re.RegexFlag.DOTALL)
    
    def parseFields(self):
        """
        Parse all the fields of the entry.
        """
        for field in re.findall(self.re_field_name, self.bibtex):
            value = self.findField(field).strip()
            if field in FieldName.iterAllFieldNames():
                self.entry.setField(field, value)
            else:
                self.entry.additionalFields[field] = Field(field, value)
            self.entry.formatField(field)

class BibTeXParser(object):
    """
    Class responsible for parsing a string written in BibTeX.
    The accepted input formats are:
        * spaces outside field values are ignored
        * key is optional
        * field value delimiters can be {} or "
        * entry delimiter can be {} or ()
        * unicode characters are supported
        * in one line:
                @TYPE{KEY,field1 = {value1},field2 = {value2}}
        * with new lines:
                @TYPE{KEY,
                    field1 = {value1},
                    field2 = {value2}
                    }
        * with multiline values:
                @TYPE{KEY,
                    field1 = {value11
                    value12
                    value13},
                    field2 = {value2}
                    }
        * with nested value delimiters ({} or "):
                @TYPE{KEY,field1 = {val{u}e1},field2 = "val"u"e2"}
    """
    def __init__(self, bibtex):
        """
        (Constructor)
           
        :param bibtex: The BibTeX string.
        :type bibtex: str.
        """
        if Preferences().allowNonStandardFields:
            self.parser = BibTeXParserWithNonStdFields(bibtex)
        else:
            self.parser = BibTeXParserWithStdFields(bibtex)
    
    def parse(self):
        return self.parser.parse()