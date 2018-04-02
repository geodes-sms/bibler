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

This module represents the management of entries.
"""

from .entry import EmptyEntry, EntryIdGenerator
from .bibtex_parser import BibTeXParser
from .field_name import FieldName
from .field import Field, Paper
from .entry_type import EntryType
from gui.app_interface import EntryListColumn
from utils import settings
from re import compile as re_compile, IGNORECASE as re_IGNORECASE
    
#TypedEmptyEntry

class ReferenceManager(object):
    """
    Manage the operations on entries.
    The reference manager holds the list of all the L{entries<app.entry.Entry>}.
    """
    def __init__(self):
        self.searchResult = list()
        self.entryList = list()
    
    def insertAt(self, index, entry):
        return self.entryList.insert(index, entry)
    
    def getIndex(self, entry):
        return self.entryList.index(entry)
    
    def __parseEntry(self, entryBibTeX):
        """
        Set DOI if not set and set URL if not set.
        """
        parser = BibTeXParser(entryBibTeX)
        entry = parser.parse()
        if settings.Preferences().overrideKeyGeneration or not entry.getKey():
            self.__setKey(entry)        
        paper = entry.additionalFields[FieldName.Paper]
        doi = entry.additionalFields[FieldName.DOI]
        if not doi.isEmpty() and paper.isEmpty():
            entry.additionalFields[FieldName.Paper] = Paper(doi=doi)
        validation = entry.validate()
        if settings.Preferences().allowInvalidEntries or validation.isValid():
            return True, entry
        return False, entry
        
    def add(self, entryBibTeX, entryType=None):
        """
        @see: L{app.user_interface.BiBlerApp.addEntry}.           
        """
        if entryBibTeX == None:
            if entryType == None:
                entry = EntryType.creatEntry(' ')
            else:
                entry = EntryType.creatEntry(entryType)
            entry.generateId()
            self.entryList.append(entry)
            return entry.getId()
        else:
            try:
                valid, entry = self.__parseEntry(entryBibTeX)
                if valid:
                    entry.generateId()
                    self.entryList.append(entry)
                    return entry.getId()
                else:
                    return None
            except Exception as ex:
                    return None
        
    def update(self, entryId, entryBibTeX):
        """
        @see: L{app.user_interface.BiBlerApp.updateEntry}.
        """
        entry = self.getEntry(entryId)
        if entry == None:
            return False
        valid, new_entry = self.__parseEntry(entryBibTeX)
        new_entry.setId(entryId)
        if valid:
            # Overwrite the entry in entryList
            self.entryList[self.entryList.index(entry)] = new_entry
            if settings.Preferences().overrideKeyGeneration:
                self.__setKey(self.entryList[self.entryList.index(new_entry)])
        else:
            return False
        return True
    
    def updateEntryField(self, entryId, fieldName, fieldValue):
        """
        @see: L{app.user_interface.BiBlerApp.updateEntryField}.
        """
        entry = self.getEntry(entryId)
        if entry == None:
            return False
        else:
            entry.setField(fieldName, fieldValue)
            entry.toBibTeX()
            return True
        return False
        
    def delete(self, entryId):
        """
        @see: L{app.user_interface.BiBlerApp.deleteEntry}.
        """
        entry = self.getEntry(entryId)
        if entry == None:
            return False
        self.entryList.remove(entry)
        if self.getEntryCount() == 0:
            EntryIdGenerator().reset()
        return True
        
    def deleteAll(self):
        """
        Delete all entries.
        """
        self.entryList = []
        self.searchResult = []
        EntryIdGenerator().reset()
        
    def duplicate(self, entryId):
        """
        @see: L{app.user_interface.BiBlerApp.duplicateEntry}.
        """
        entry = self.getEntry(entryId)
        if entry == None:
            return None
        return self.add(entry.toBibTeX())
        
    def search(self, query):
        """
        @see: L{app.user_interface.BiBlerApp.search}.
        """
        try:
            if settings.Preferences().searchRegex:
                query = re_compile(query, re_IGNORECASE)
                self.searchResult = [e for e in iter(self.entryList) if e.matchesRegex(query)]
            else:
                self.searchResult = [e for e in iter(self.entryList) if e.matchesExact(query)]
            return len(self.searchResult)
        except:
            return -1
    
    def sort(self, field, reverse=False):
        """
        @see: L{app.user_interface.BiBlerApp.sort}.
        """
        
        def getField(e, field):
            try:
                return e.getFieldValue(FieldName.fromEntryListColumn(field)).lower()
            except:
                return ''
        
        try:
            if field == EntryListColumn.Entrytype:
                self.entryList.sort(key=lambda e: e.getEntryType().lower(), reverse=reverse)
                self.searchResult.sort(key=lambda e: e.getEntryType().lower(), reverse=reverse)
            elif field == EntryListColumn.Id:
                self.entryList.sort(key=lambda e: e.getId(), reverse=reverse)
                self.searchResult.sort(key=lambda e: e.getId(), reverse=reverse)
            elif field == EntryListColumn.Entrykey:
                self.entryList.sort(key=lambda e: e.getKey().lower(), reverse=reverse)
                self.searchResult.sort(key=lambda e: e.getKey().lower(), reverse=reverse)
            else:
                self.entryList.sort(key=lambda e: getField(e, field).lower(), reverse=reverse)
                self.searchResult.sort(key=lambda e: getField(e, field).lower(), reverse=reverse)
            return True
        except:
            return False 
        
    def generateAllKeys(self):
        """
        @see: L{app.user_interface.BiBlerApp.generateAllKeys}.
        """
        try:
            for entry in self.entryList:
                self.__setKey(entry)
            return True
        except:
            return False
    
    def getEntry(self, entryId):
        """
        Get an entry given its id.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{app.entry.Entry}
        @return: The entry, L{None} if not found.
        """
        for e in self.entryList:
            if e.getId() == entryId:
                return e
        return None
        
    def iterEntries(self):
        """
        Iterator over the list of all entries.
        @rtype: C{generator} of L{app.entry.Entry}
        @return: The list of entries.
        """
        for entry in self.entryList:
            yield entry
        
    def getEntryCount(self):
        """
        @see: L{app.user_interface.BiBlerApp.getEntryCount}.
        """
        return len(self.entryList)
        
    def iterSearchResult(self):
        """
        Iterator over the list of entries filtered by the search.
        @rtype: C{generator} of L{app.entry.Entry}
        @return: The list of entries.
        """
        for entry in self.searchResult:
            yield entry
        
    def getSearchResultCount(self):
        """
        @see: L{app.user_interface.BiBlerApp.getSearchResultCount}.
        """
        return len(self.searchResult)
        
    def __setKey(self, entry):
        """
        Generate and set a unique key to the entry.
        @type entry: L{app.entry.Entry}
        @param entry: The entry.
        @raise Exception: If the first author of the entry published more than 27 on the entry's publication year.
        """
        key = entry.generateKey()
        if not key:
            return
            raise Exception('Cannot generate key because of missing fields.')
        duplicateKeys = [e.getKey() for e in [e for e in self.entryList if e.getId() != entry.getId() and e.getKey().startswith(key)]]
        if len(duplicateKeys) > 27:
            raise Exception('Too many entries with the same key.')
        elif not duplicateKeys:
            entry.setKey(key)
        else:
            suffix = ''
            for i in range(len(duplicateKeys) + 1):
                if key + suffix not in duplicateKeys:
                    entry.setKey(key + suffix)
                    break
                suffix = chr(ord('a') + i)
