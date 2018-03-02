"""
.. moduleauthor:: Eugene Syriani
.. moduleauthor:: Florin Oncica 

.. versionadded:: 1.0

Created on Nov 09, 2016

This module represents the BiTeX parser.
"""

import re
import unicodedata
from app.entry import EmptyEntry
from app.entry_type import EntryType
from app.field_name import FieldName
from app.field import Field
from utils.settings import Preferences
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
        #bibtex = bibtex.decode('utf-8','replace')   # make sure the text is in utf-8 encoding
        bibtex = bibtex.replace('{\n', '{stubKey,\n')   # if key is missing
        bibtex = bibtex.replace('\xdf', '{\ss}')   # unicodedata ignores \ss
        bibtex = bibtex.replace('\xf8', '\\o')     # unicodedata ignores \\o
        bibtex = self.__unicodeToTex(bibtex)
        #bibtex = unicodedata.normalize('NFKD', bibtex).encode(encoding='ascii', errors='ignore')  # replace unicode characters with their ASCII approximation
        self.bibtex = bibtex.strip().replace('\n', ' ')         # remove all spaces and new lines
        self.bibtex = re.sub('=\s*\"', '= {', self.bibtex)      # replace all double quotes that delimit the beginning of a field value
        self.bibtex = re.sub('\"\s*,', '},', self.bibtex)       # replace all double quotes that delimit the end of a field value
        self.re_header = re.compile("""\s*@(\w+)\s*[({]\s*(\w*)\s*""", re.DOTALL)
        self.entry = None

    def __unicodeToTex(self,bibtex):
        """   
        :param bibtex: The BibTeX string.
        :type bibtex: str
        :returns: str -- The transformed BibTeX string.
        """
        chars = dict()
        funnychars = ['\xc1','\xe1','\xc0','\xe0','\xc2','\xe2','\xc4','\xe4','\xc3',
                      '\xe3','\xc5','\xe5','\xc6','\xe6','\xc7','\xe7','\xd0','\xf0','\xc9',
                      '\xe9','\xc8','\xe8','\xca','\xea','\xcb','\xeb','\xcd','\xed','\xcc',
                      '\xec','\xce','\xee','\xcf','\xef','\xd1','\xf1','\xd3','\xf3','\xd2',
                      '\xf2','\xd4','\xf4','\xd6','\xf6','\xd5','\xf5','\xd8','\xf8','\xdf',
                      '\xde','\xfe','\xda','\xfa','\xd9','\xf9','\xdb','\xfb','\xdc','\xfc',
                      '\xdd','\xfd','\xff','\xa9','\xae','\u2122','\u20ac','\xa2','\xa3','\u2018',
                      '\u2019','\u201c','\u201d','\xab','\xbb','\u2014','\u2013','\xb0','\xb1','\xbc',
                      '\xbd','\xbe','\xd7','\xf7','\u03b1','\u03b2','\u221e']
        bibtexcodes = ['\\\'{A}', '\\\'{a}', '\`{A}', '\`{a}', '\^{A}', '\^{a}', '\\"{A}', '\\"{a}', '\~{A}',
                     '\~{a}', '\AA', '\\aa', '\AE', '\\ae', '\c{C}', '\c{c}', '\DJ', '\dj', '\\\'{E}',
                     '\\\'{e}', '\`{E}', '\`{e}', '\^{E}', '\^{e}', '\\"{E}', '\\"{e}', '\\\'{I}', '\\\'{i}', '\`{I}',
                     '\`{i}', '\^{I}', '\^{i}', '\\"{I}', '\\"{i}', '\~{N}', '\~{n}', '\\\'{O}', '\\\'{o}', '\`{O}',
                     '\`{o}', '\^{O}', '\^{o}', '\\"{O}', '\\"{o}', '\~{O}', '\~{o}', '\O', '\o', '\ss',
                     '\\textThorn', '\\textthorn', '\\\'{U}', '\\\'{u}', '\`{U}', '\`{u}', '\^{U}', '\^{u}', '\\"{U}', '\\"{u}',
                     '\`{Y}', '\`{y}', '\\"{y}', '\copyright', '\\textregistered', '\\texttrademark', '\euro{}', '\cent', '\pounds', '`',
                     '\'', '``', '\'\'', '<<', '>>', '\emdash', '\endash', '\degree', '\pm', '\\textonequarter',
                     '\\textonehalf', '\\textthreequarters', '$\\times$', '$\div$', '$\\alpha$', '$\\beta$', '$\infty$']

        for i in range(len(bibtexcodes)):
            chars[funnychars[i]] = bibtexcodes[i]
        for c in list(chars.keys()):
            bibtex = bibtex.replace(c, chars[c])

        return bibtex


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
        self.entry = EntryType.creatEntry(entryType)
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
        result = re.findall(""",\s*(""" + field + """)\s*=\s*\{\s*(.*)\s*\}\s*,?""", self.bibtex, re.DOTALL|re.IGNORECASE)
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
        self.re_field_name = re.compile("""},\s*(.*?)\s*=\s*\{""", re.DOTALL)
    
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