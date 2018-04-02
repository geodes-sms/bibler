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

This module represents the entries.
"""

from gui.app_interface import EntryDict, EntryListColumn
from .field_name import FieldName
from .field import Author, Editor, Field, Organization, Pages, Year
from utils import utils
import re

class EntryIdGenerator(object, metaclass=utils.Singleton):
    def __init__(self):
        self.lastId = 0
    
    def getLastId(self):
        """
        Get the last id issued.
        """
        return self.lastId
    
    def getNewId(self):
        """
        Generate the next available id. 
        """
        self.lastId += 1
        return self.lastId
    
    def reset(self):
        """
        Reset the id increment back to its initial value.
        """
        self.lastId = 0


class ValidationResult(object):
    SUCCESS = 1
    ERROR = 2
    WARNING = 3
    """
    The result of the validation of an :class:`app.entry.Entry`.
    """
    def __init__(self, val, field='', msg=''):
        """
        :type val: :class:`SUCCESS<app.entry.ValidationResult.SUCCESS>`, :class:`ERROR<app.entry.ValidationResult.ERROR>`, or :class:`WARNING<app.entry.ValidationResult.WARNING>`
        :param val: The value of the validation.
        :type field: :class:`str`
        :param field: An optional :class:`app.entry.FieldName`.
        :type msg: :class:`str`
        :param msg: An optional error or warning message.
        """
        self.value = val
        self.field = field
        if field and not msg:
            msg = '%s is missing.' % (field)
        self.message = msg
    
    def isValid(self):
        """
        :rtype: :class:`bool`
        :return: Whether the value is valid.
        """
        return self.value is not ValidationResult.ERROR
    
    def getValue(self):
        """
        :rtype: :class:`SUCCESS<app.entry.ValidationResult.SUCCESS>`, :class:`ERROR<app.entry.ValidationResult.ERROR>`, or :class:`WARNING<app.entry.ValidationResult.WARNING>`
        :return: The value of the validation.
        """
        return self.value is not ValidationResult.ERROR
    
    def getMessage(self):
        """
        :rtype: :class:`str`
        :return: A message if not :class:`SUCCESS<app.entry.ValidationResult.SUCCESS>`.
        """
        return self.message


class Entry(object):
    """
    The abstract class representing entries.	
    Every entry has an :class:`_id`, a :class:`key`, and dictionaries for :class:`requiredFields`, :class:`optionalFields`, and :class:`additionalFields`
    as defined in `BibTeX <http://www.openoffice.org/bibliographic/bibtex-defs.html>`_.
    :class:`importantFields` are usually required from the optional ones, but if missing the entry is still valid.
    """
    def __init__(self):
        self._id = None
        self.key = ''
        self.requiredFields = dict()
        self.optionalFields = {FieldName.Annote: Field(FieldName.Annote),
                               FieldName.Crossref: Field(FieldName.Crossref),
                               FieldName.Key: Field(FieldName.Key)}
        self.additionalFields = {FieldName.DOI: Field(FieldName.DOI),
                                 FieldName.Paper: Field(FieldName.Paper),
                                 FieldName.Comment: Field(FieldName.Comment),
                                 FieldName.Note: Field(FieldName.Note)}
        self.importantFields = []   # contains keys from optionalFields
        
    def getId(self):
        """
        Get the id of this entry.
        
        :rtype: :class:`int`
        :return: The id of the entry.
        """
        return self._id
    
    def setId(self, _id):
        """
        Set the id for this entry.
        
        :type _id: :class:`int`
        :param _id: The id of the entry.
        """
        self._id = _id
    
    def generateId(self):
        """
        Assign the next available id to the entry. 
        """
        self._id = EntryIdGenerator().getNewId()
        
    def getKey(self):
        """
        Get the key of this entry.
        
        :rtype: :class:`str`
        :return: The key of the entry.
        """
        return self.key
    
    def setKey(self, key):
        """
        Set the key for this entry.
        
        :type key: :class:`str`
        :param key: The key of the entry.
        """
        self.key = key
    
    def generateKey(self):
        """
        Generates the unique key for this entry. 
        """
        key = self.getField(FieldName.Key)
        if not key.isEmpty():
            key = Field.simplify(key.getValue())
        else:
            # First author's last name (no {}, no spaces) concatenated with year
            author = self.getField(FieldName.Author)
            if not author.isEmpty():
                key = Field.simplify(author.getFirstLastName())
            else:
                key = ''
        return key + self.getField(FieldName.Year).getYear()
        
    def getField(self, field):
        """
        Get a field object of this entry.
        
        :type field: :class:`str`
        :param field: The name of the field requested.
        :rtype: :class:`Field<app.field.Field>`
        :return: The field of the entry.
        :raises Exception: If the field does not exist in this entry.
        """
        if field in self.requiredFields:
            return self.requiredFields[field]
        elif field in self.optionalFields:
            return self.optionalFields[field]
        elif field in self.additionalFields:
            return self.additionalFields[field]
        else:
            raise Exception('Invalid field requested.')
        
    def getFieldValue(self, field):
        """
        Get the value of a field of this entry.
        
        :type field: :class:`str`
        :param field: The name of the field requested.
        :rtype: :class:`str`
        :return: The value of the field.
        :raises Exception: If the field does not exist in this entry.
        """
        return self.getField(field).getValue()
    
    def getContributors(self):
        """
        Get the contributors of an entry.
        
        :rtype: list of :class:`Contributor<app.field.Contributor>`
        :return: The contributors.
        """
        return []
    
    def getVenue(self):
        """
        Get the venue of an entry. This corresponds to where the renference was published. For example, the name of the journal or proceedings.
        
        :rtype: :class:`str`
        :return: The venue name.
        """
        return ''
        
    def setField(self, field, value):
        """
        Set a field for this entry.
        
        :type field: :class:`str`
        :param field: The name of the field.
        :type value: :class:`str`
        :param value: The value of the field.
        :raises Exception: If the field does not exist in this entry.
        """
        if field in self.requiredFields:
            self.requiredFields[field].setValue(value)
        elif field in self.optionalFields:
            self.optionalFields[field].setValue(value)
        elif field in self.additionalFields:
            self.additionalFields[field].setValue(value)
        else:
            raise Exception('Field %s not found.' % field)
    
    def formatField(self, field):
        """
        Correctly format a field inplace.
        
        :type field: :class:`str`
        :param field: The name of the field.
        """
        self.getField(field).format()
        
    def iterAllFields(self):
        """
        Iterator over the list of all fields of this entry.
        
        :rtype: ``generator`` of :class:`Field<app.field.Field>`
        :return: The list of fields.
        """
        # Sorted deterministic list of fields: first required then optional then additional
        for field in self.iterRequiredFields():
            yield field
        for field in self.iterOptionalFields():
            yield field
        for field in self.iterAdditionalFields():
            yield field
        
    def __iterAllFieldsUnsorted(self):
        """
        Iterator over the list of all fields of this entry.
        
        :rtype: ``generator`` of :class:`Field<app.field.Field>`
        :return: The list of fields.
        """
        # Sorted deterministic list of fields: first required then optional then additional
        for field in self.requiredFields.values():
            yield field
        for field in self.optionalFields.values():
            yield field
        for field in self.additionalFields.values():
            yield field
        
    def iterRequiredFields(self):
        """
        Iterator over the list of all required fields of this entry.
        
        :rtype: ``generator`` of :class:`Field<app.field.Field>`
        :return: The list of fields.
        """
        # Sorted deterministic list
        for field in sorted(iter(self.requiredFields.values()), key=lambda x:x.getName()):
            yield field
        
    def iterOptionalFields(self):
        """
        Iterator over the list of all optional fields of this entry.
        
        :rtype: ``generator`` of :class:`Field<app.field.Field>`
        :return: The list of fields.
        """
        # Sorted deterministic list
        for field in sorted(iter(self.optionalFields.values()), key=lambda x:x.getName()):
            yield field
        
    def iterAdditionalFields(self):
        """
        Iterator over the list of all additional fields of this entry.
        
        :rtype: ``generator`` of :class:`Field<app.field.Field>`
        :return: The list of fields.
        """
        # Sorted deterministic list
        for field in sorted(self.additionalFields.values(), key=lambda x:x.getName()):
            yield field
        
    def validate(self):
        """
        Verify that the entry is valid by checking that all required fields are not empty.
        
        :rtype: :class:`bool`
        :return: :class:`True` if valid, :class:`False` otherwise.
        """
        for field in self.requiredFields:
            if self.requiredFields[field].isEmpty():
                return ValidationResult(ValidationResult.ERROR, field)
        for field in self.importantFields:
            if self.optionalFields[field].isEmpty():
                return ValidationResult(ValidationResult.WARNING, field)
        return ValidationResult(ValidationResult.SUCCESS)
        
    def matchesRegex(self, query):
        """
        Check if any field value matches the query. 
        
        :type query: :class:`str`
        :param query: A regular expression to find.
        :rtype: :class:`bool`
        :return: :class:`True` if query matched, :class:`False` otherwise.
        """
        for value in self.__iterAllFieldsUnsorted():
            if re.search(query, Field.simplify(value.getValue())):
                return True
        return False
        
    def matchesExact(self, query):
        """
        Check if any field value matches the query.
        
        :type query: :class:`str`
        :param query: A substring to find.
        :rtype: :class:`bool`
        :return: :class:`True` if query matched, :class:`False` otherwise.
        """
        query = query.lower()
        simplify = Field.simplify
        for value in self.__iterAllFieldsUnsorted():
            if query in simplify(value.getValue()).lower():
                return True
        return False
    
    def __str__(self):
        return self.toBibTeX()
    
    def toEntryDict(self):
        """
        Convert the entry into an :class:`EntryDict<gui.app_interface.EntryDict>`.
        
        :rtype: :class:`gui.app_interface.EntryDict`
        :return: The entry in dictionary format.
        """
        e = EntryDict()
        e[EntryListColumn.Id] = self.getId()
        e[EntryListColumn.Entrytype] = self.getEntryType().upper()
        e[EntryListColumn.Entrykey] = self.getKey()
        v = self.validate()
        e[EntryListColumn.Valid] = v.isValid()
        e[EntryListColumn.Message] = v.getMessage()
        for field in self.iterRequiredFields():
            col = FieldName.toEntryListColumn(field.getName())
            e[col] = field.getValue()
        for field in self.iterOptionalFields():
            col = FieldName.toEntryListColumn(field.getName())
            e[col] = field.getValue()
        for field in self.iterAdditionalFields():
            col = FieldName.toEntryListColumn(field.getName())
            e[col] = field.getValue()
        return e
        
    def toBibTeX(self, ignoreEmptyField=False):
        """
        Convert the entry into its BibTeX reference.
        
        :param ignoreEmptyField: If :class:`True` ignores empty fields.
        :type ignoreEmptyField: ``bool``
        :rtype: :class:`str`
        :return: The BibTeX reference.
        
        .. note:: The BibTeX format is:
            @TYPE{KEY,
              FIELD1 = {VALUE1},
              FIELD2 = {VALUE2}
            }
        """
        try:
            bibtex = '@%s{%s' % (self.getEntryType().upper(), self.getKey())
            for field in self.iterAllFields():
                value = self.getFieldValue(field.getName())
                if not value:
                    continue
                # This part is to put {} around capital letters if they aren't already
                v = ''
                for i in range(len(value)):
                    if value[i].isupper():
                        if 0 < i < len(value) - 1 and value[i-1] != '{' and value[i+1] != '}':
                            v += '{%s}' % value[i]
                    else:
                        v += value[i]
                bibtex += ',\n  %s = {%s}' % (field.getName(), value)
            bibtex += '\n}'
            return bibtex
        except:
            return ''
        
    def toCSV(self):
        """
        Convert the entry into a tabified sequence of its fields.
        The order of the fields is always the same for any entry type.
                
        :rtype: :class:`str`
        :return: The row of all its values.
        
        .. note::  The row format is:  "VALUE1"   "VALUE2"
        """
        #"VALUE1"\t"VALUE2"
        # Where the order is determined by FieldName.iterAllFieldNames()
        try:
            csv = self.getEntryType()   # the first column is the entrytype
            for field in FieldName.iterAllFieldNames():
                csv += '\t'
                try:
                    csv += '"' + self.getFieldValue(field) + '"'
                except:
                    continue    # the field is not in this entrytype
            return csv
        except:
            return ''
        
    def __toHtml(self, styleWriter):
        """
        Convert this entry into HTML.
        
        :rtype: :class:`str`
        :return: The HTML code within <p></p>.
        """
        if self.isEmpty():
            html = '''<p><font face="verdana"><b><i>%s</i>(%s)</b></font></p>
<p>''' % (self.getEntryType().upper(), self.getKey())
        else:
            html = '''<p><font face="verdana"><b><i>%s</i>(%s)</b></font></p>
<p>''' % (self.getEntryType().upper(), self.getKey())
            html += styleWriter()
            html += '''</p>
<p><center>'''
        html += self.getField(FieldName.Annote).getHTMLValue()
        html += '</center></p>'
        return html
        
    def toHtmlACM(self):
        """
        Convert this entry into HTML following the ACM style.
        
        :rtype: :class:`str`
        :return: The HTML code.
        """
        raise NotImplementedError()
        
    def toCompleteHtmlACM(self):
        """
        Convert this entry into HTML following the ACM style.
        
        :rtype: :class:`str`
        :return: The HTML code within <p></p>.
        """
        return self.__toHtml(self.toHtmlACM)
        
    def toHtmlDefault(self):
        """
        Convert this entry into HTML following the default style.
        
        :rtype: :class:`str`
        :return: The HTML code within.
        """
        raise NotImplementedError()
        
    def toCompleteHtmlDefault(self):
        """
        Convert this entry into HTML following the default style.
        
        :rtype: :class:`str`
        :return: The HTML code within <p></p>.
        """
        return self.__toHtml(self.toHtmlDefault)
        
    def toSQL(self):
        """
        Convert the entry into an SQL INSERT statement.
        
        :rtype: :class:`str`
        :return: The INSERT statement.
        """
        try:
            key = utils.escapeSQLCharacters(self.getKey())
            title = utils.escapeSQLCharacters(self.getField(FieldName.Title).getValue())
            bibtex = utils.escapeSQLCharacters(self.toBibTeX().replace('\n',''))
            preview = utils.escapeSQLCharacters(self.toHtmlDefault().replace('\n',''))
            url = self.getField(FieldName.Paper).getValue()
            if url and url != '' and not url.startswith('http://'):
                url = utils.escapeSQLCharacters('http://' + url)
            else:
                url = ''
            return '''INSERT INTO Paper (bibtexKey,title,doi,bibtex,preview) VALUES (N'%s', N'%s', N'%s', N'%s', N'%s');''' \
                % (key, title, url, bibtex, preview)
        except:
            return ''
    
    @staticmethod
    def getEntryType():
        """
        Get the type of this entry.
        
        :rtype: :class:`str`
        :return: The type of the entry.
        """
        raise NotImplementedError()
    
    def isEmpty(self):
        """
        Verify if an entry has all the fields empty 
        """
        for field in (self.iterRequiredFields()):
            if field.getValue() != "":
                return False
        for field in (self.iterOptionalFields()):
            if field.getValue() != "":
                return False
        
        return True


class EmptyEntry(Entry):
    """
    An entry with no type.
    """
    
    @staticmethod
    def getEntryType():
        return ''
        
    def __init__(self):
        super(EmptyEntry, self).__init__()
        self.entryType = ''
        self.requiredFields = dict()
        self.optionalFields = dict()
        self.additionalFields = {FieldName.DOI: Field(FieldName.DOI),
                                 FieldName.Paper: Field(FieldName.Paper),
                                 FieldName.Comment: Field(FieldName.Comment)}
    
    def generateKey(self):
        return ''
    
    def validate(self):
        # No field should exist
        if not list(self.requiredFields.keys()) and not list(self.optionalFields.keys()):
            return ValidationResult(ValidationResult.SUCCESS)
        return ValidationResult(ValidationResult.ERROR, msg='No field should be defined.')
        
    def toBibTeX(self):
        return ''
        
    def toCompleteHtmlDefault(self):
        return ''
    
    def toCompleteHtmlACM(self):
        return ''
   
class Article(Entry):
    """
    An article from a journal or magazine.
    """
    
    @staticmethod
    def getEntryType():
        return 'article'
    
    def __init__(self):
        super(Article, self).__init__()
        self.requiredFields = { FieldName.Author: Author(),
                                FieldName.Title: Field(FieldName.Title),
                                FieldName.Journal: Field(FieldName.Journal),
                                FieldName.Year: Year()}
        self.optionalFields.update({FieldName.Volume: Field(FieldName.Volume),
                                    FieldName.Number: Field(FieldName.Number),
                                    FieldName.Pages: Pages(),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note),
                                    FieldName.Abstract: Field(FieldName.Abstract)})
        self.importantFields = [FieldName.Volume, FieldName.Pages]
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
    
    def getVenue(self):
        return self.getField(FieldName.Journal).getValue()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            journal = self.getField(FieldName.Journal).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            volume = self.getField(FieldName.Volume).getACMValue()
            number = self.getField(FieldName.Number).getACMValue()
            pages = self.getField(FieldName.Pages).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''<span style="font-variant:small-caps">{0}</span> {1}. <i>{2}</i>'''.format(authors, title, journal)
            if volume:
                html += ''' <i>%s</i>''' % volume
            if number:
                html += ''', %s''' % number
            html += ''' ('''
            if month:
                html += '''%s ''' % month
            html += '''%s)''' % year
            if pages:
                html += ''', %s''' % pages
            html += '.'
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            journal = self.getField(FieldName.Journal).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            volume = self.getField(FieldName.Volume).getHtmlDefaultValue()
            number = self.getField(FieldName.Number).getHtmlDefaultValue()
            pages = self.getField(FieldName.Pages).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''{0} {1}. <i>{2}</i>'''.format(authors, title, journal)
            if volume:
                html += ''': %s''' % volume
            if number:
                html += '''(%s)''' % number
            if pages:
                html += ''', pp. %s''' % pages
            if month:
                html += ''', %s''' % month
            html += ''' (%s)''' % year
            html += '.'
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Book(Entry):
    """
    A book with an explicit publisher.
    """
    
    @staticmethod
    def getEntryType():
        return 'book'
    
    def __init__(self):
        super(Book, self).__init__()
        self.requiredFields = { FieldName.Author: Author(),
                                FieldName.Editor: Editor(),
                                FieldName.Title: Field(FieldName.Title),
                                FieldName.Publisher: Field(FieldName.Publisher),
                                FieldName.Year: Year()}
        self.optionalFields.update({FieldName.Volume: Field(FieldName.Volume),
                                    FieldName.Number: Field(FieldName.Number),
                                    FieldName.Series: Field(FieldName.Series),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Edition: Field(FieldName.Edition),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note),
                                    FieldName.Abstract: Field(FieldName.Abstract)})
    
    def getContributors(self):
        if not self.getField(FieldName.Author).isEmpty():
            return self.getField(FieldName.Author).getContributors()
        else:
            return self.getField(FieldName.Editor).getContributors()
    
    def generateKey(self):
        key = self.getField(FieldName.Key)
        if not key.isEmpty():
            key = Field.simplify(key.getValue())
        elif not self.getField(FieldName.Author).isEmpty():
            # First author's last name (no {}, no spaces) concatenated with year
            key = Field.simplify(self.getField(FieldName.Author).getFirstLastName())
        elif not self.getField(FieldName.Editor).isEmpty():
            # First author's last name (no {}, no spaces) concatenated with year
            key = Field.simplify(self.getField(FieldName.Editor).getFirstLastName())
        return key + self.getField(FieldName.Year).getYear()
        
    def validate(self):
        for field in [FieldName.Title, FieldName.Publisher, FieldName.Year]:
            if self.requiredFields[field].isEmpty():
                return ValidationResult(ValidationResult.ERROR, field)
        if not (self.requiredFields[FieldName.Author].isEmpty() ^ self.requiredFields[FieldName.Editor].isEmpty()):
            return ValidationResult(ValidationResult.ERROR, msg='use either %s or %s' % (FieldName.Author, FieldName.Editor))
        if not (self.optionalFields[FieldName.Volume].isEmpty() ^ self.optionalFields[FieldName.Number].isEmpty()):
            return ValidationResult(ValidationResult.WARNING, msg='use either %s or %s' % (FieldName.Volume, FieldName.Number))
        return ValidationResult(ValidationResult.SUCCESS)
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            editor = self.getField(FieldName.Editor).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            publisher = self.getField(FieldName.Publisher).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            volume = self.getField(FieldName.Volume).getACMValue()
            number = self.getField(FieldName.Number).getACMValue()
            series = self.getField(FieldName.Series).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            edition = self.getField(FieldName.Edition).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            contributor = authors
            if editor:
                contributor = editor
            if contributor:
                if not contributor.endswith('.'):
                    contributor += '.'
                html = '''<span style="font-variant:small-caps">%s</span>''' % contributor
            html += ''' <i>%s</i>''' % title
            if edition:
                html += ''', %s ed.''' % edition
            if volume:
                html += ''', vol. %s''' % volume
            elif number:
                html += ''', no. %s''' % number
            if series:
                html += ''' of <i>%s</i>''' % series
            html += '''. %s,''' % publisher
            if address:
                html += ''' %s,''' % address
            if month:
                html += ''' %s''' % month
            html += ''' %s.''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            editor = self.getField(FieldName.Editor).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            publisher = self.getField(FieldName.Publisher).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            volume = self.getField(FieldName.Volume).getHtmlDefaultValue()
            number = self.getField(FieldName.Number).getHtmlDefaultValue()
            series = self.getField(FieldName.Series).getHtmlDefaultValue()
            address = self.getField(FieldName.Address).getHtmlDefaultValue()
            edition = self.getField(FieldName.Edition).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            contributor = authors
            if editor:
                contributor = editor
            if contributor:
                if not contributor.endswith('.'):
                    contributor += '.'
                html = '''%s''' % contributor
            html += ''' <i>%s</i>''' % title
            if edition:
                html += ''', %s ed.''' % edition
            if not html.endswith('.'):
                html += '.'
            if series:
                html += ''' %s:''' % series
            if volume:
                html += ''' %s''' % volume
            elif number:
                html += ''' %s''' % number
            if not html.endswith('.'):
                html += '.'
            add_comma = False
            if publisher:
                html += ''' %s''' % publisher
                add_comma = True
            if address:
                if add_comma: html += ','
                html += ''' %s''' % address
            if month:
                if add_comma: html += ','
                html += ''' %s''' %  month
            html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Booklet(Entry):
    """
    A work that is printed and bound, but without a named publisher or sponsoring institution.
    """
    
    @staticmethod
    def getEntryType():
        return 'booklet'
    
    def __init__(self):
        super(Booklet, self).__init__()
        self.requiredFields = { FieldName.Title: Field(FieldName.Title)}
        self.optionalFields.update({FieldName.Author: Author(),
                                    FieldName.Howpublished: Field(FieldName.Howpublished),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Year: Year(),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note),
                                    FieldName.Abstract: Field(FieldName.Abstract)})
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            howpublished = self.getField(FieldName.Howpublished).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            html = ''
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
                html = '''<span style="font-variant:small-caps">%s</span>''' % authors
            html += '''%s.''' % title
            add_comma = False
            if howpublished:
                html += ''' %s''' % howpublished
                add_comma = True
            if address:
                if add_comma: html += ','
                html += ''' %s''' % address
            if month:
                if add_comma: html += ','
                html += ''' %s''' % month
            if year:
                if add_comma:
                    html += ','
                html += ''' %s''' % year
            html += '.'
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            howpublished = self.getField(FieldName.Howpublished).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            html = ''
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
                html += '''%s''' % authors
            html += ''' %s.''' % title
            if month:
                html += ''' %s''' % month
            if year:
                html += ''' (%s).''' % year
            if howpublished:
                html += ''' %s''' % howpublished
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Inbook(Book):
    """
    A part of a book, which may be a chapter (or section or whatever) and/or a range of pages.
    """
    
    @staticmethod
    def getEntryType():
        return 'inbook'
    
    def __init__(self):
        super(Inbook, self).__init__()
        self.requiredFields = { FieldName.Author: Author(),
                                FieldName.Editor: Editor(),
                                FieldName.Title: Field(FieldName.Title),
                                FieldName.Publisher: Field(FieldName.Publisher),
                                FieldName.Chapter: Field(FieldName.Chapter),
                                FieldName.Pages: Pages(),
                                FieldName.Year: Year()}
        self.optionalFields.update({FieldName.Volume: Field(FieldName.Volume),
                                    FieldName.Number: Field(FieldName.Number),
                                    FieldName.Series: Field(FieldName.Series),
                                    FieldName.Type: Field(FieldName.Type),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Edition: Field(FieldName.Edition),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note),
                                    FieldName.Abstract: Field(FieldName.Abstract)})
    
    def getContributors(self):
        if not self.getField(FieldName.Author).isEmpty():
            return self.getField(FieldName.Author).getContributors()
        else:
            return self.getField(FieldName.Editor).getContributors()
    
    def getVenue(self):
        return self.getField(FieldName.Title).getValue()
        
    def validate(self):
        if self.requiredFields[FieldName.Chapter].isEmpty() and self.requiredFields[FieldName.Pages].isEmpty():
            return ValidationResult(ValidationResult.ERROR, '%s or %s' % (FieldName.Chapter, FieldName.Pages))
        return super(Inbook, self).validate()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            editor = self.getField(FieldName.Editor).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            publisher = self.getField(FieldName.Publisher).getACMValue()
            chapter = self.getField(FieldName.Chapter).getACMValue()
            pages = self.getField(FieldName.Pages).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            volume = self.getField(FieldName.Volume).getACMValue()
            number = self.getField(FieldName.Number).getACMValue()
            series = self.getField(FieldName.Series).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            edition = self.getField(FieldName.Edition).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            contributor = authors
            if editor:
                contributor = editor
            if contributor:
                if not contributor.endswith('.'):
                    contributor += '.'
                html = '''<span style="font-variant:small-caps">%s</span>''' % contributor
            html += ''' <i>%s</i>''' % title
            if edition:
                html += ''', %s ed.''' % edition
            if volume:
                html += ''', vol. %s''' % volume
            elif number:
                html += ''', no. %s''' % number
            if series:
                html += ''' of <i>%s</i>''' % series
            html += '''. %s,''' % publisher
            if pages:
                html += ''' pp. %s,''' % pages
            if chapter:
                html += ''' ch. %s,''' % chapter
            if address:
                html += ''' %s,''' % address
            if month:
                html += ''' %s''' % month
            html += ''' %s.''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            editor = self.getField(FieldName.Editor).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            publisher = self.getField(FieldName.Publisher).getHtmlDefaultValue()
            chapter = self.getField(FieldName.Chapter).getHtmlDefaultValue()
            pages = self.getField(FieldName.Pages).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            volume = self.getField(FieldName.Volume).getHtmlDefaultValue()
            number = self.getField(FieldName.Number).getHtmlDefaultValue()
            series = self.getField(FieldName.Series).getHtmlDefaultValue()
            address = self.getField(FieldName.Address).getHtmlDefaultValue()
            edition = self.getField(FieldName.Edition).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            contributor = authors
            if editor:
                contributor = editor
            if contributor:
                if not contributor.endswith('.'):
                    contributor += '.'
                html = '''%s''' % contributor
            html += ''' <i>%s</i>''' % title
            if edition:
                html += ''', %s ed.''' % edition
            if not html.endswith('.'):
                html += '.'
            if series:
                html += ''' %s:''' % series
            if volume:
                html += ''' %s''' % volume
            elif number:
                html += ''' %s''' % number
            if pages:
                html += ''', pp. %s''' % pages
            if chapter:
                html += ''', ch. %s''' % chapter
            if not html.endswith('.'):
                html += '.'
            add_comma = False
            if publisher:
                html += ''' %s''' % publisher
                add_comma = True
            if address:
                if add_comma: html += ','
                html += ''' %s''' % address
            if month:
                if add_comma: html += ','
                html += ''' %s''' %  month
            html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Incollection(Entry):
    """
    A part of a book having its own title.
    """
    
    @staticmethod
    def getEntryType():
        return 'incollection'
    
    def __init__(self):
        super(Incollection, self).__init__()
        self.requiredFields = { FieldName.Author: Author(),
                                FieldName.Title: Field(FieldName.Title),
                                FieldName.BookTitle: Field(FieldName.BookTitle),
                                FieldName.Publisher: Field(FieldName.Publisher),
                                FieldName.Year: Year()}
        self.optionalFields.update({FieldName.Editor: Editor(),
                                    FieldName.Volume: Field(FieldName.Volume),
                                    FieldName.Number: Field(FieldName.Number),
                                    FieldName.Series: Field(FieldName.Series),
                                    FieldName.Type: Field(FieldName.Type),
                                    FieldName.Chapter: Field(FieldName.Chapter),
                                    FieldName.Pages: Pages(),
                                    FieldName.Edition: Field(FieldName.Edition),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note),
                                    FieldName.Abstract: Field(FieldName.Abstract)})
        self.importantFields = [FieldName.Pages]
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
    
    def getVenue(self):
        return self.getField(FieldName.BookTitle).getValue()
        
    def validate(self):
        if not (self.optionalFields[FieldName.Volume].isEmpty() ^ self.optionalFields[FieldName.Number].isEmpty()):
            return ValidationResult(ValidationResult.WARNING, msg='use either %s or %s' % (FieldName.Volume, FieldName.Number))
        return super(Incollection, self).validate()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            booktitle = self.getField(FieldName.BookTitle).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            editor = self.getField(FieldName.Editor).getACMValue()
            volume = self.getField(FieldName.Volume).getACMValue()
            number = self.getField(FieldName.Number).getACMValue()
            series = self.getField(FieldName.Series).getACMValue()
            #_type = self.getField(FieldName.Type).getACMValue()
            chapter = self.getField(FieldName.Chapter).getACMValue()
            pages = self.getField(FieldName.Pages).getACMValue()
            edition = self.getField(FieldName.Edition).getACMValue()
            publisher = self.getField(FieldName.Publisher).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''<span style="font-variant:small-caps">{0}</span> {1}. In <i>{2}</i>'''.format(authors, title, booktitle)
            if editor:
                html += ''', %s, Eds.''' %  editor
            if edition:
                html += ''', %s ed.''' % edition
            if volume:
                html += ''', vol. %s''' % volume
            elif number:
                html += ''', no. %s''' % number
            if series:
                html += ''' in %s''' % series
            html += '.'
            if publisher:
                html += ''' %s,''' % publisher
            if address:
                html += ''' %s,''' % address
            if month:
                html += ''' %s''' % month
            html += ''' %s''' % year
            if chapter:
                html += ''', ch. %s''' % chapter
            if pages:
                html += ''', pp. %s''' % pages
            html += '.'
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            booktitle = self.getField(FieldName.BookTitle).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            editor = self.getField(FieldName.Editor).getHtmlDefaultValue()
            volume = self.getField(FieldName.Volume).getHtmlDefaultValue()
            number = self.getField(FieldName.Number).getHtmlDefaultValue()
            series = self.getField(FieldName.Series).getHtmlDefaultValue()
            #_type = self.getField(FieldName.Type).getHtmlDefaultValue()
            chapter = self.getField(FieldName.Chapter).getHtmlDefaultValue()
            pages = self.getField(FieldName.Pages).getHtmlDefaultValue()
            edition = self.getField(FieldName.Edition).getHtmlDefaultValue()
            publisher = self.getField(FieldName.Publisher).getHtmlDefaultValue()
            address = self.getField(FieldName.Address).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''{0} {1}. '''.format(authors, title)
            if editor:
                if self.getField(FieldName.Editor).getContributorsCount() == 1:
                    html += '''In %s, Ed.: ''' %  editor
                else:
                    html += '''In %s, Eds.: ''' %  editor
            html += '''<i>%s</i>''' % booktitle
            if edition:
                html += ''', %s ed. ''' % edition
            if not html.endswith('. '):
                html += '. '
            add_comma = False
            if series:
                html += '''%s: ''' % series
            if volume:
                html += '''%s''' % volume
                add_comma = True
            elif number:
                html += '''%s''' % number
                add_comma = True
            if pages:
                if add_comma: html += ', '
                html += '''pp. %s''' % pages
            if chapter:
                if add_comma: html += ', '
                html += ''', ch. %s''' % chapter
            if not html.endswith('.'):
                html += '.'
            add_comma = False
            if publisher:
                html += ''' %s''' % publisher
                add_comma = True
            if address:
                if add_comma: html += ','
                html += ''' %s''' % address
            if month:
                if add_comma: html += ','
                html += ''' %s''' % month
            html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Inproceedings(Entry):
    """
    An article in a conference proceedings.
    """
    
    @staticmethod
    def getEntryType():
        return 'inproceedings'
    
    def __init__(self):
        super(Inproceedings, self).__init__()
        self.requiredFields = { FieldName.Author: Author(),
                                FieldName.Title: Field(FieldName.Title),
                                FieldName.BookTitle: Field(FieldName.BookTitle),
                                FieldName.Year: Year()}
        self.optionalFields.update({FieldName.Editor: Editor(),
                                    FieldName.Volume: Field(FieldName.Volume),
                                    FieldName.Number: Field(FieldName.Number),
                                    FieldName.Series: Field(FieldName.Series),
                                    FieldName.Pages: Pages(),
                                    FieldName.Organization: Organization(),
                                    FieldName.Publisher: Field(FieldName.Publisher),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note),
                                    FieldName.Abstract: Field(FieldName.Abstract)})
        self.importantFields = [FieldName.Volume, FieldName.Pages, FieldName.Publisher]
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
    
    def getVenue(self):
        return self.getField(FieldName.BookTitle).getValue()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            booktitle = self.getField(FieldName.BookTitle).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            editor = self.getField(FieldName.Editor).getACMValue()
            volume = self.getField(FieldName.Volume).getACMValue()
            number = self.getField(FieldName.Number).getACMValue()
            series = self.getField(FieldName.Series).getACMValue()
            pages = self.getField(FieldName.Pages).getACMValue()
            organization = self.getField(FieldName.Organization).getACMValue()
            publisher = self.getField(FieldName.Publisher).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''<span style="font-variant:small-caps">{0}</span> {1}. In <i>{2}</i>'''.format(authors, title, booktitle)
            html += ''' ('''
            if address:
                html += '''%s, ''' % address
            if month:
                html += '''%s ''' % month
            html += '''%s)''' % year
            if editor:
                if self.getField(FieldName.Editor).getContributorsCount() == 1:
                    html += ''', %s, Ed.''' %  editor
                else:
                    html += ''', %s, Eds.''' %  editor
            if volume:
                html += ''', vol. %s''' % volume
            elif number:
                html += ''', no. %s''' % number
            if series:
                html += ''' of <i>%s</i>''' % series
            if organization:
                html += ''', %s''' % organization
            if publisher:
                html += ''', %s''' % publisher
            if pages:
                html += ''', pp. %s''' % pages
            html += '.'
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            booktitle = self.getField(FieldName.BookTitle).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            editor = self.getField(FieldName.Editor).getHtmlDefaultValue()
            volume = self.getField(FieldName.Volume).getHtmlDefaultValue()
            number = self.getField(FieldName.Number).getHtmlDefaultValue()
            series = self.getField(FieldName.Series).getHtmlDefaultValue()
            pages = self.getField(FieldName.Pages).getHtmlDefaultValue()
            organization = self.getField(FieldName.Organization).getHtmlDefaultValue()
            publisher = self.getField(FieldName.Publisher).getHtmlDefaultValue()
            address = self.getField(FieldName.Address).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''{0} {1}. '''.format(authors, title)
            if editor:
                if self.getField(FieldName.Editor).getContributorsCount() == 1:
                    html += '''In %s, Ed.: ''' %  editor
                else:
                    html += '''In %s, Eds.: ''' %  editor
            html += '''<i>%s</i>. ''' % booktitle
            add_comma = False
            if series:
                html += '''%s: ''' % series
            if volume:
                html += '''%s''' % volume
                add_comma = True
            elif number:
                html += '''%s''' % number
                add_comma = True
            if pages:
                if add_comma: html += ', '
                html += '''pp. %s''' % pages
            if organization:
                html += ''', %s''' % organization
            if not html.endswith('.'):
                html += '.'
            add_comma = False
            if publisher:
                html += ''' %s''' % publisher
                add_comma = True
            if address:
                if add_comma: html += ','
                html += ''' %s''' % address
            if month:
                if add_comma: html += ','
                html += ''' %s''' % month
            html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Conference(Inproceedings):
    """
    An article in a conference proceedings.
	
    :deprecated: The same as INPROCEEDINGS, included for Scribe compatibility.
    """
    
    @staticmethod
    def getEntryType():
        return 'conference'
    
    def __init__(self):
        super(Conference, self).__init__()
        
    
class Manual(Entry):
    """
    Technical documentation.
    """
    
    @staticmethod
    def getEntryType():
        return 'manual'
    
    def __init__(self):
        super(Manual, self).__init__()
        self.requiredFields = { FieldName.Title: Field(FieldName.Title)}
        self.optionalFields.update({FieldName.Author: Author(),
                                    FieldName.Organization: Organization(),
                                    FieldName.Edition: Field(FieldName.Edition),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Year: Year(),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note),
                                    FieldName.Abstract: Field(FieldName.Abstract)})
        self.importantFields = [FieldName.Author, FieldName.Year]
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
    
    def generateKey(self):
        key = self.getField(FieldName.Key)
        key = Field.simplify(key.getValue())
        if not self.getField(FieldName.Author).isEmpty():
            key = Field.simplify(self.getField(FieldName.Author).getFirstLastName())
        elif not self.getField(FieldName.Organization).isEmpty():
            key = Field.simplify(self.getField(FieldName.Organization).getFirstWord())
        return key + self.getField(FieldName.Year).getYear()
    
    def validate(self):
        v = super(Manual, self).validate()
        if not v.isValid():
            return v
        if self.optionalFields[FieldName.Author].isEmpty() and self.optionalFields[FieldName.Organization].isEmpty():
            return ValidationResult(ValidationResult.WARNING, '%s or %s' % (FieldName.Author, FieldName.Organization))
        return ValidationResult(ValidationResult.SUCCESS)
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            organization = self.getField(FieldName.Organization).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            edition = self.getField(FieldName.Edition).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            contributor = authors
            if organization:
                contributor = organization
            if contributor:
                if not contributor.endswith('.'):
                    contributor += '.'
                html = '''<span style="font-variant:small-caps">%s</span>''' % contributor
            html += ''' <i>%s</i>''' % title
            if edition:
                html += ''', %s ed.''' % edition
            if address:
                html += ''' %s,''' % address
            if month:
                html += ''' %s''' % month
            if year:
                html += ''' %s.''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            organization = self.getField(FieldName.Organization).getACMValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            address = self.getField(FieldName.Address).getACMValue()
            edition = self.getField(FieldName.Edition).getACMValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            contributor = authors
            if organization:
                contributor = organization
            if contributor:
                if not contributor.endswith('.'):
                    contributor += '.'
                html = '''%s''' % contributor
            html += ''' <i>%s</i>''' % title
            if edition:
                html += ''', %s ed.''' % edition
            if not html.endswith('.'):
                html += '.'
            if address:
                html += ''' %s,''' % address
            if month:
                html += ''' %s''' % month
            if year:
                html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Misc(Entry):
    """
    Document of any other type.
    """
    
    @staticmethod
    def getEntryType():
        return 'misc'
    
    def __init__(self):
        super(Misc, self).__init__()
        self.optionalFields.update({FieldName.Author: Author(),
                                    FieldName.Title: Field(FieldName.Title),
                                    FieldName.Howpublished: Field(FieldName.Howpublished),
                                    FieldName.Year: Year(),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note),
                                    FieldName.Abstract: Field(FieldName.Abstract)})
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            howpublished = self.getField(FieldName.Howpublished).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            html = ''
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
                html += '''<span style="font-variant:small-caps">{0}</span>'''.format(authors)
            if title:
                html += ''' %s.''' % title
            if howpublished:
                html += ''' %s''' % howpublished
            if year or month:
                if not html.endswith('.'):
                    html += ', '
            if year:
                if month:
                    html += '''%s %s.''' % (month, year)
                else:
                    html += '''%s.''' % year
            elif month:
                html += '''%s.''' % month
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            howpublished = self.getField(FieldName.Howpublished).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            html = ''
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
                html += '''%s''' % authors
            if title:
                html += ''' %s.''' % title
            if month:
                html += ''' %s''' % month
            if year:
                html += ''' (%s).''' % year
            if howpublished:
                html += ''' %s''' % howpublished
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Phdthesis(Entry):
    """
    A Ph.D. thesis.
    """
    
    @staticmethod
    def getEntryType():
        return 'phdthesis'
    
    def __init__(self):
        super(Phdthesis, self).__init__()
        self.requiredFields = { FieldName.Author: Author(),
                                FieldName.Title: Field(FieldName.Title),
                                FieldName.School: Field(FieldName.School),
                                FieldName.Year: Year()}
        self.optionalFields.update({FieldName.Type: Field(FieldName.Type),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note)})
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            school = self.getField(FieldName.School).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            _type = self.getField(FieldName.Type).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''<span style="font-variant:small-caps">{0}</span> <i>{1}</i>. '''.format(authors, title)
            if _type:
                html += '''%s, ''' % _type
            html += '''%s''' % school
            if address:
                html += ''', %s''' % address
            if month:
                html += ''', %s''' % month
            html += ''' %s.''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            school = self.getField(FieldName.School).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            _type = self.getField(FieldName.Type).getHtmlDefaultValue()
            address = self.getField(FieldName.Address).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''{0} {1}. '''.format(authors, title)
            if _type:
                html += '''%s, ''' % _type
            html += '''<i>%s</i>''' % school
            if address:
                html += ''', %s''' % address
            if month:
                html += ''', %s''' % month
            html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
        
    
class Mastersthesis(Phdthesis):
    """
    A Master's thesis.
    """
    
    @staticmethod
    def getEntryType():
        return 'mastersthesis'
    
    def __init__(self):
        super(Mastersthesis, self).__init__()

    
class Proceedings(Entry):
    """
    The proceedings of a conference.
    """
    
    @staticmethod
    def getEntryType():
        return 'proceedings'
    
    def __init__(self):
        super(Proceedings, self).__init__()
        self.requiredFields = { FieldName.Title: Field(FieldName.Title),
                                FieldName.Year: Year()}
        self.optionalFields.update({FieldName.Editor: Editor(),
                                    FieldName.Volume: Field(FieldName.Volume),
                                    FieldName.Number: Field(FieldName.Number),
                                    FieldName.Series: Field(FieldName.Series),
                                    FieldName.Organization: Organization(),
                                    FieldName.Publisher: Field(FieldName.Publisher),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note)})
        self.importantFields = [FieldName.Editor, FieldName.Volume, FieldName.Publisher]
    
    def getContributors(self):
        return self.getField(FieldName.Editor).getContributors()
    
    def generateKey(self):
        key = self.getField(FieldName.Key)
        if not key.isEmpty():
            key = Field.simplify(key.getValue())
        elif not self.getField(FieldName.Editor).isEmpty():
            # First author's last name (no {}, no spaces) concatenated with year
            key = Field.simplify(self.getField(FieldName.Editor).getFirstLastName())
        elif not self.getField(FieldName.Organization).isEmpty():
            # First author's last name (no {}, no spaces) concatenated with year
            key = Field.simplify(self.getField(FieldName.Organization).getFirstWord())
        return key + self.getField(FieldName.Year).getYear()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            title = self.getField(FieldName.Title).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            editor = self.getField(FieldName.Editor).getACMValue()
            volume = self.getField(FieldName.Volume).getACMValue()
            number = self.getField(FieldName.Number).getACMValue()
            series = self.getField(FieldName.Series).getACMValue()
            organization = self.getField(FieldName.Organization).getACMValue()
            publisher = self.getField(FieldName.Publisher).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            html = ''
            if editor:
                if not editor.endswith('.'):
                    editor += '.'
                html = '''<span style="font-variant:small-caps">%s, Ed''' % editor
                if self.getField(FieldName.Editor).getContributorsCount() > 1:
                    html += 's'
                html += '. '
            html = '''<i>%s</i>''' % title
            html += ''' ('''
            if address:
                html += '''%s, ''' % address
            if month:
                html += '''%s ''' % month
            html += '''%s)''' % year
            if volume:
                html += ''', vol. %s''' % volume
            elif number:
                html += ''', no. %s''' % number
            if series:
                html += ''' of <i>%s</i>''' % series
            if organization:
                html += ''', %s''' % organization
            if publisher:
                html += ''', %s''' % publisher
            html += '.'
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            editor = self.getField(FieldName.Editor).getHtmlDefaultValue()
            volume = self.getField(FieldName.Volume).getHtmlDefaultValue()
            number = self.getField(FieldName.Number).getHtmlDefaultValue()
            series = self.getField(FieldName.Series).getHtmlDefaultValue()
            organization = self.getField(FieldName.Organization).getHtmlDefaultValue()
            publisher = self.getField(FieldName.Publisher).getHtmlDefaultValue()
            address = self.getField(FieldName.Address).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            html = ''
            if editor:
                if not editor.endswith('.'):
                    editor += '.'
                html = '''%s, Ed''' % editor
                if self.getField(FieldName.Editor).getContributorsCount() > 1:
                    html += 's'
                html += '. '
            html = '''<i>%s</i>. ''' % title
            if series:
                html += '''%s: ''' % series
            if volume:
                html += '''%s''' % volume
            elif number:
                html += '''%s''' % number
            if organization:
                html += ''', %s''' % organization
            if not html.endswith('.'):
                html += '.'
            add_comma = False
            if publisher:
                html += ''' %s''' % publisher
                add_comma = True
            if address:
                if add_comma: html += ','
                html += ''' %s''' % address
            if month:
                if add_comma: html += ','
                html += ''' %s''' % month
            html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')


class Techreport(Entry):
    """
    A report published by a school or other institution, usually numbered within a series.
    """
    
    @staticmethod
    def getEntryType():
        return 'techreport'
    
    def __init__(self):
        super(Techreport, self).__init__()
        self.requiredFields = { FieldName.Author: Author(),
                                FieldName.Title: Field(FieldName.Title),
                                FieldName.Institution: Field(FieldName.Institution),
                                FieldName.Year: Year()}
        self.optionalFields.update({FieldName.Type: Field(FieldName.Type),
                                    FieldName.Number: Field(FieldName.Number),
                                    FieldName.Address: Field(FieldName.Address),
                                    FieldName.Month: Field(FieldName.Month),
                                    FieldName.Note: Field(FieldName.Note)})
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            institution = self.getField(FieldName.Institution).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            _type = self.getField(FieldName.Type).getACMValue()
            number = self.getField(FieldName.Number).getACMValue()
            address = self.getField(FieldName.Address).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''<span style="font-variant:small-caps">{0}</span> {1}. '''.format(authors, title)
            if _type:
                html += '''%s, ''' % _type
            if number:
                html += '''%s, ''' % number
            html += '''%s, ''' % institution
            if address:
                html += '''%s, ''' % address
            if month:
                html += '''%s ''' % month
            html += '''%s.''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            institution = self.getField(FieldName.Institution).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            _type = self.getField(FieldName.Type).getHtmlDefaultValue()
            number = self.getField(FieldName.Number).getHtmlDefaultValue()
            address = self.getField(FieldName.Address).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
            html = '''{0} {1}. '''.format(authors, title)
            if _type:
                html += '''%s, ''' % _type
            html += '''<i>%s</i>''' % institution
            if number:
                html += ''': %s''' % number
            if address:
                html += ''', %s''' % address
            if month:
                html += ''', %s''' % month
            html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')

    
class Unpublished(Entry):
    """
    A report published by a school or other institution, usually numbered within a series.
    """
    
    @staticmethod
    def getEntryType():
        return 'unpublished'
    
    def __init__(self):
        super(Unpublished, self).__init__()
        self.requiredFields = { FieldName.Author: Author(),
                                FieldName.Title: Field(FieldName.Title),
                                FieldName.Note: Field(FieldName.Note)}
        self.optionalFields.update({FieldName.Year: Year(),
                                    FieldName.Month: Field(FieldName.Month)})
    
    def getContributors(self):
        return self.getField(FieldName.Author).getContributors()
        
    def toHtmlACM(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getACMValue()
            title = self.getField(FieldName.Title).getACMValue()
            year = self.getField(FieldName.Year).getACMValue()
            month = self.getField(FieldName.Month).getACMValue()
            note = self.getField(FieldName.Note).getACMValue()
            
            html = ''
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
                html += '''<span style="font-variant:small-caps">{0}</span>'''.format(authors)
            if title:
                html += ''' %s.''' % title
            html += ''' %s, ''' % note
            if year:
                if month:
                    html += '''%s %s.''' % (month, year)
                else:
                    html += '''%s.''' % year
            elif month:
                html += '''%s.''' % month
            return html
        except:
            raise Exception('Failed to generate ACM style.')
        
    def toHtmlDefault(self):
        # Capital letters are already between {}
        try:
            authors = self.getField(FieldName.Author).getHtmlDefaultValue()
            title = self.getField(FieldName.Title).getHtmlDefaultValue()
            year = self.getField(FieldName.Year).getHtmlDefaultValue()
            month = self.getField(FieldName.Month).getHtmlDefaultValue()
            note = self.getField(FieldName.Note).getHtmlDefaultValue()
            
            html = ''
            if authors:
                if not authors.endswith('.'):
                    authors += '.'
                html += '''%s''' % authors
            if title:
                html += ''' %s.''' % title
            if month:
                html += ''' %s''' % month
            if year:
                html += ''' (%s).''' % year
            if note:
                html += ''' %s.''' % note
            return html
        except:
            raise Exception('Failed to generate default style.')
