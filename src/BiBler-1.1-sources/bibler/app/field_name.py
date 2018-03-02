"""
.. moduleauthor:: Eugene Syriani

.. versionadded:: 1.0

Created on Nov 09, 2016

This module represents the field names.
"""

from gui.app_interface import EntryListColumn

class FieldName:
    """
    Enum that contains all standard field names as well as additional ones used in BiBler.
    """
    Address = 'address'
    Annote = 'annote'
    Author = 'author'
    BookTitle = 'booktitle'
    Chapter = 'chapter'
    Crossref = 'crossref'
    DOI = 'doi' 
    Edition = 'edition'
    Editor = 'editor'
    Howpublished = 'howpublished'
    Institution = 'institution'
    Journal = 'journal'
    Key = 'key'
    Month = 'month'
    Note = 'note'
    Number = 'number'
    Organization = 'organization'
    Pages = 'pages'
    Publisher = 'publisher'
    School = 'school'
    Series = 'series'
    Title = 'title'
    Type = 'type'
    Volume = 'volume'
    Year = 'year'
    Paper = 'paper'     # not part of the BibTeX standard
    Comment = 'comment' # not part of the BibTeX standard
    Abstract= 'abstract' # not part of the BibTeX standard
    
    __all_names = sorted(
            [Abstract, Address, Annote, Author, BookTitle, Crossref,
             Chapter, Edition, Editor, Howpublished, Institution,
             Journal, Key, Month, Note, Number,
             Organization, Pages, Publisher, School, Series,
             Title, Type, Volume, Year, Paper, Comment])
    
    @staticmethod
    def toEntryListColumn(field):
        """
        Convert a field name into an entry list column name.
        @type field: L{FieldName}
        @param field: A field name.
        @rtype: L{gui.app_interface.EntryListColumn}
        @return: The corresponding L{EntryListColumn<gui.app_interface.EntryListColumn>} name.
                 The same name is returned if it is not a valid EntryListColumn name.
        """
        if field == FieldName.Author: return EntryListColumn.Author
        elif field == FieldName.Paper: return EntryListColumn.Paper
        elif field == FieldName.Title: return EntryListColumn.Title
        elif field == FieldName.Year: return EntryListColumn.Year
        else:
            return field
    
    @staticmethod
    def fromEntryListColumn(column):
        """
        Convert a  entry list column name into a field name.
        @type column: L{gui.app_interface.EntryListColumn}
        @param column: A EntryListColumn name.
        @rtype: L{FieldName}
        @return: The corresponding L{FieldName} name.
                 The same name is returned if it is not a valid L{FieldName} name.
        """
        if column == EntryListColumn.Author: return FieldName.Author
        elif column == EntryListColumn.Paper: return FieldName.Paper
        elif column == EntryListColumn.Title: return FieldName.Title
        elif column == EntryListColumn.Year: return FieldName.Year
        else:
            raise Exception('The column is not an EntryColumnList.')
    
    @staticmethod
    def getAllFieldNames():
        """
        Get all field names sorted in alphabetical order.
        @rtype: list of L{FieldName}
        @return: The list of field names.
        """
        return FieldName.__all_names
    
    @staticmethod
    def iterAllFieldNames():
        """
        Iterator over the list of all field names sorted in alphabetical order.
        @rtype: C{generator} of L{FieldName}
        @return: The list of field names.
        """
        for name in FieldName.__all_names: yield name
