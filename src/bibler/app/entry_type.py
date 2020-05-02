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
.. moduleauthor:: Florin Oncica 

.. versionadded:: 1.0

Created on Dec 6, 2016

This module represents the entry types.
"""
from app.entry import Article, Book, Inproceedings, Phdthesis, Techreport, Booklet, Inbook, Incollection, \
                    Conference, Manual, Mastersthesis, Misc, Proceedings, Unpublished, EmptyEntry
                    
class EntryType:
    """
    Enum that contains all entry types used in BiBler including the empty entry.
    """
    Article = 'Article'
    Book =  'Book'
    Booklet = 'Booklet'
    EmptyEntry = 'EmptyEntry'
    Inbook = 'Inbook'
    Incollection = 'Incollection'
    Inproceedings = 'Inproceedings'
    Conference = 'Conference'
    Manual = 'Manual'
    Misc = 'Misc'
    Phdthesis = 'Phdthesis'
    Mastersthesis = 'Mastersthesis'
    Proceedings = 'Proceedings'
    Techreport = 'Techreport'
    Unpublished = 'Unpublished'
    
    __all_types = sorted(
                        [Article, Book, Booklet, EmptyEntry, Inbook,
                        Incollection, Inproceedings, Conference, Manual, Misc,
                        Phdthesis, Mastersthesis, Proceedings, Techreport, Unpublished]
                        )
    
    @staticmethod
    def getAllEntryTypes():
        """
        Get all entry types sorted in alphabetical order.
        @rtype: list of L{EntryType}
        @return: The list of entry types.
        """
        return EntryType.__all_types
    
    @staticmethod
    def iterAllEntryTypes():
        """
        Iterator over the list of all field names sorted in alphabetical order.
        @rtype: C{generator} of L{FieldName}
        @return: The list of field names.
        """
        for t in EntryType.__all_types:
            yield t
        
    @staticmethod   
    def createEntry(entryType):
        if not entryType:
            return None
        elif entryType.lower() == Article.getEntryType():
            return Article()
        elif entryType.lower() == Book.getEntryType():
            return Book()
        elif entryType.lower() == Inproceedings.getEntryType():
            return Inproceedings()
        elif entryType.lower() == Phdthesis.getEntryType():
            return Phdthesis()
        elif entryType.lower() == Techreport.getEntryType():
            return Techreport()
        elif entryType.lower() == Booklet.getEntryType():
            return Booklet()
        elif entryType.lower() == Inbook.getEntryType():
            return Inbook()
        elif entryType.lower() == Incollection.getEntryType():
            return Incollection()
        elif entryType.lower() == Conference.getEntryType():
            return Conference()
        elif entryType.lower() == Manual.getEntryType():
            return Manual()
        elif entryType.lower() == Mastersthesis.getEntryType():
            return Mastersthesis()
        elif entryType.lower() == Misc.getEntryType():
            return Misc()
        elif entryType.lower() == Proceedings.getEntryType():
            return Proceedings()
        elif entryType.lower() == Unpublished.getEntryType():
            return Unpublished()
        else:
            return EmptyEntry()

