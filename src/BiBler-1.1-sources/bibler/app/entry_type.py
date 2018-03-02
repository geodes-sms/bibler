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
        for type in EntryType.__all_types: yield type
        
    @staticmethod   
    def creatEntry(entryType):
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

