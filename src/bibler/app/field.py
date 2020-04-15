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

.. versionadded:: 1.0

Created on Nov 09, 2016

This module represents the fields of each entry.
"""

import re
from app.field_name import FieldName
from utils.utils import Utils

class Field(object):
    """
    The generic class representing any field of an entry.
    Every field has a C{name} and a C{value}.
    """
    def __init__(self, name, value=''):
        """
        @type name: L{str}
        @param name: The name of the field.
        @type value: L{str}
        @param value: The value of the field.
        """
        self.name = name
        self.value = value
    
    def isEmpty(self):
        """
        Verfies if the field does not have a value.
        @rtype: L{bool}
        @return: L{True} if the value is empty, L{False} otherwise.
        """
        return self.value == ''
        
    def getName(self):
        """
        Get the name of this field.
        @rtype: L{str}
        @return: The name of the field.
        """
        return self.name
        
    def getValue(self):
        """
        Get the value of this field.
        @rtype: L{str}
        @return: The value of the field.
        """
        return self.value
        
    def setValue(self, value):
        """
        Set the value for this field.
        @type value: L{str}
        @param value: The value of the field.
        """
        self.value = value
        
    def format(self):
        """
        Correctly format the value of this field according to the BibTeX standard.
        """
        pass
        
    def getHTMLValue(self):
        """
        Get the value of this field in HTML format.
        @see: L{toHTML}.
        @return: The value in HTML encoding.
        """
        return Field.toHTML(self.value)
        
    def getACMValue(self):
        """
        Get the value of this field in HTML format following the ACM style.
        @see: L{toHTML}.
        @return: The value in HTML encoding.
        """
        return self.getHTMLValue()
        
    def getHtmlDefaultValue(self):
        """
        Get the value of this field in HTML format following the default style.
        @see: L{toHTML}.
        @return: The value in HTML encoding.
        """
        return self.getHTMLValue()
    
    @staticmethod
    def simplify(value):
        """
        Strip all special characters in a string.
        For example:: a{\'a}a or a\'{a}a -> aaa
        @type value: L{str}
        @param value: The string to simplify.
        @rtype: L{str}
        @return: The simplified value.
        """
        value = Utils().tex2simple(value)
        return Field.__clean(value)
        
    @staticmethod
    def toHTML(value):
        """
        Convert all BibTeX special commands into HTML encodings.
        For example:: {\'e} -> &eacute; or \'{e} -> &eacute;
        @type value: L{str}
        @param value: The string to convert.
        @rtype: L{str}
        @return: The value in HTML encoding.
        """
        value = Utils().tex2html(value)
        return Field.__clean(value)
    
    @staticmethod
    def __clean(value):
        """
        Remove all E{lb},E{rb},[,], and other BibTeX commands.
        For example:: {\'e} -> &eacute;
        @type value: L{str}
        @param value: The string to convert.
        @rtype: L{str}
        @return: The cleaned value.
        """
        value = value.replace('{','').replace('}','').replace('[','').replace(']','')
        value = value.replace('\\em', '').replace('\\it', '').replace('\\url', '')
        return value

class Contributor(object):
    """
    Contributor of an article such asE{:} an author, an editor, etc.
    """
    def __init__(self, last, first='', von='', jr=''):
        """
        @type last: L{str}
        @param last: The last name.
        @type first: L{str}
        @param first: The first name.
        @type von: L{str}
        @param von: The preposition before the last name like 'de la' in 'Eugene de la Croix'.
        @type jr: L{str}
        @param jr: The suffix at the end of the name like 'Jr.' in 'Martin Luther King Jr.'.
        """
        if first is None: first = ''
        if last is None: last = ''
        if von is None: von = ''
        if jr is None: jr = ''
        self.first_name = first.strip()
        self.last_name = last.strip()
        self.preposition = von.strip()
        self.suffix = jr.strip()
    
    def __str__(self):
        s = ''
        if self.preposition:
            s += self.preposition + ' '
        if self.last_name:
            s += self.last_name
        if self.suffix:
            s += ', ' + self.suffix
        if self.first_name:
            s += ', ' + self.first_name
        return s

class ContributorField(Field):
    """
    The field for contributors. Multiple contributors must be separated by ' and '.
    The supported formats for individual names are defined in U{BibTeX<http://www.openoffice.org/bibliographic/bibtex-defs.html>}:
        - Last
        - First Last
        - Last, First
        - First von Last
        - von Last, First
        - von Last, Jr, First 
    """
    ET_AL = ('et al.', 'and others')
    SPLIT = ' and '
    
    def __init__(self, name, value=''):
        super(ContributorField, self).__init__(name, value)
        self.contributors = []
        self.hasEtal = False
        von = """(?P<von>([a-z]+)|(\\\\\{.[a-z]+\})|(\{\\\\.[a-z]+\})|(\\\\.\{[a-z]+\})|(\\\\[^{][a-z]+))?"""
        self.re_von_Last_Jr_First = re.compile(von + """\s*(?P<last>[^,]+)\s*,\s*(?P<jr>[^,]*)\s*,\s*(?P<first>.*)""", re.RegexFlag.DOTALL)
        self.re_von_Last_First = re.compile(von + """\s*(?P<last>[^,]+)\s*,\s*(?P<first>.*)""", re.RegexFlag.DOTALL)
    
    def getContributors(self):
        """
        Get the list of contributors.
        @rtype: list of L{Contributor}
        @return: The list of contributors.
        """
        return self.contributors
    
    def getContributorsCount(self):
        """
        Get the number of contributors.
        @rtype: L{int}
        @return: The number of contributors.
        """
        return len(self.contributors)
        
    def format(self):
        people = self.value
        if not people:
            return
        for etal in ContributorField.ET_AL:
            etal_ix = people.find(etal)
            if etal_ix >= 0:
                self.hasEtal = True
                people = people[:etal_ix] # removes ET_AL and everything after 
                break
        people = people.split(ContributorField.SPLIT)
        for person in people:
            name = self.re_von_Last_Jr_First.match(person)
            if name:
                # von Last, Jr, First
                self.contributors.append(Contributor(last=name.group('last'), first=name.group('first'), von=name.group('von'), jr=name.group('jr')))
            else:
                name = self.re_von_Last_First.match(person)
                if name:
                    # von Last, First
                    self.contributors.append(Contributor(last=name.group('last'), first=name.group('first'), von=name.group('von')))
                else:
                    person = person.split()
                    vonIx = -1
                    for i,name in enumerate(person):
                        if name[0].islower():
                            vonIx = i
                            break
                    if vonIx < 0:
                        # First Last 
                        self.contributors.append(Contributor(last=person[-1], first=' '.join(person[:-1])))
                    elif vonIx == len(person) - 1:
                        raise Exception('Incorrect author name: missing last name.')
                    else:
                        # First von Last 
                        lastIx = vonIx
                        for i,name in enumerate(person[vonIx + 1:]):
                            if name[0].isupper():
                                lastIx = i + vonIx + 1
                                break
                        self.contributors.append(Contributor(last=' '.join(person[lastIx:]), first=' '.join(person[:vonIx]), von=' '.join(person[vonIx:lastIx])))
        self.value = ContributorField.SPLIT.join([str(c) for c in self.contributors])
        if self.hasEtal:
            self.value += ' ' + ContributorField.ET_AL[0]
    
    def getFirstNameFirst(self, contributor):
            person = ''
            suffix = False
            if contributor.first_name:
                first = contributor.first_name.split()
                for f in first:
                    person += Field.toHTML(f)[0] + '. '
                if contributor.suffix:
                    suffix = True
            if contributor.preposition:
                person += contributor.preposition + ' '
            if contributor.last_name:
                person += contributor.last_name
            if suffix:
                person += ' ' + contributor.suffix
            return person
    
    def getFirstNameLast(self, contributor):
            person = ''
            if contributor.preposition:
                person += contributor.preposition + ' '
            if contributor.last_name:
                person += contributor.last_name
            if contributor.first_name:
                first = contributor.first_name.split()
                person += ','
                for f in first:
                    person += ' ' + Field.toHTML(f)[0] + '.'
                if contributor.suffix:
                    person += ' ' + contributor.suffix
            return person
    
    def getHTMLValue(self, firstNameOrder):
        """
        Get the names of the contributors in HTML.
        @rtype: L{str}
        @return: The contributors in HTML.
        @raise Exception: If a name is not in a legal format.
        """
        try:
            value = ''
            people = []
            for contributor in self.contributors:
                person = firstNameOrder(contributor)
                people.append(person)
            if len(people) > 1:
                _and = ContributorField.SPLIT
                if len(people) > 2:
                    _and = ',' + _and
                value = ', '.join(people[:-1]) + _and + people[-1]
            elif len(people) == 1:
                value = people[0]
            else:
                value = ''
            if self.hasEtal:
                value += ContributorField.ET_AL[0]
            return Field.toHTML(value)
        except Exception as ex:
            raise Exception('Invalid %s names.' % self.name)
    
    def getACMValue(self):
        """
        Get the names of the contributors in HTML following the ACM style.
        @rtype: L{str}
        @return: The contributors in HTML.
        @raise Exception: If a name is not in a legal format.
        """
        return self.getHTMLValue(self.getFirstNameLast)
    
    def getHtmlDefaultValue(self):
        """
        Get the names of the contributors in HTML following the default style.
        @rtype: L{str}
        @return: The contributors in HTML.
        @raise Exception: If a name is not in a legal format.
        """
        return self.getHTMLValue(self.getFirstNameFirst)
    
    def getFirstLastName(self):
        """
        Get the last name of the first contributor.
        @rtype: L{str}
        @return: The last name of the first contributor.
        """
        if not self.contributors:
            raise Exception('No author or editor name found.')
        return self.contributors[0].last_name.replace(' ', '')
        
    
class Author(ContributorField):
    """
    The field for authors.
    """
    def __init__(self, value = ''):
        super(Author, self).__init__(FieldName.Author, value)
        
    
class Editor(ContributorField):
    """
    The field for editors.
    """
    def __init__(self, value = ''):
        super(Editor, self).__init__(FieldName.Editor, value)
        
    
class Title(Field):
    """
    The field for title.
    """
    def __init__(self, value = ''):
        super(Title, self).__init__(FieldName.Title, value)
        
    def getHtmlDefaultValue(self):
        return '''<span style="font-weight: 600; color: #3F3F3F;">%s</span>''' % super(Title, self).getHtmlDefaultValue()
        
    
class Chapter(Title):
    """
    The field for chapter.
    """
    def __init__(self, value = ''):
        super(Chapter, self).__init__(value)
        self.name = FieldName.Chapter
        
    
class Organization(Field):
    """
    The field for the organization.
    """
    def __init__(self, value = ''):
        super(Organization, self).__init__(FieldName.Organization, value)
    
    def getFirstWord(self):
        """
        Get the first word of the organization name.
        @rtype: L{str}
        @return: The first word.
        """
        if len(self.value) == 0:
            return ''
        return self.value.split()[0]
        
    
class Pages(Field):
    """
    The field for pages.
    """
    def __init__(self, value = ''):
        super(Pages, self).__init__(FieldName.Pages, value)
        self.re_dashes = re.compile("""-+""")
        
    def format(self):
        self.value = self.value.replace(' ', '')
        self.value = self.re_dashes.sub('--', self.value)


class Year(Field):
    """
    The field for year.
    """
    def __init__(self, value = ''):
        super(Year, self).__init__(FieldName.Year, value)
    
    def getYear(self):
        """
        Get the year part.
        @rtype: L{str}
        @return: The last four-digits of the value, or C{''} if they are not present.
        """
        if len(self.value) >= 4:
            return self.value[-4:]
        else:
            return ''


class DOI(Field):
    """
    The field for DOI.
    """
    def __init__(self, value = ''):
        super(DOI, self).__init__(FieldName.DOI, value)
        
    def format(self):
        self.value = self.value.replace(' ', '')


class Paper(Field):
    """
    The field for paper.
    """
    def __init__(self, value = '', doi = None):
        """
        @type value: L{str}
        @param value: The value of the field.
        @type doi: L{DOI}
        @param doi: The DOI field form which the paper field will get its value.
        """
        super(Paper, self).__init__(FieldName.Paper, value)
        if doi:
            doi.format()
            doi = doi.getValue()
            if doi != '':
                if not doi.startswith('http'):
                    doi = 'https://dx.doi.org/' + doi
                self.value = doi
