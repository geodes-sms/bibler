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

This module represents the API of the application.
"""

from gui.app_interface import IApplication
from .manager import ReferenceManager
from .command import AddCommand, CommandExecutor, DeleteCommand, DuplicateCommand, ExportCommand, GenerateAllKeysCommand, ImportCommand, OpenCommand, PreviewCommand, SearchCommand, SortCommand, UndoCommand, UpdateCommand, ValidateAllCommand, ExportStringCommand, ImportStringCommand
from .field_name import FieldName
from .bibtex_parser import BibTeXParser
from utils.settings import Preferences


class BiBlerApp(IApplication):
    """
    The main class that provides all the application functionalities.
    """
    def __init__(self):
        super(BiBlerApp, self).__init__()
        self.__manager = ReferenceManager()
        self.__executor = CommandExecutor()
        self.preferences = Preferences()
        
    def start(self):
        """
        @see: L{gui.app_interface.IApplication.start}.
        """
        pass
        
    def exit(self):
        """
        @see: L{gui.app_interface.IApplication.exit}.
        """
        pass
        
    def importFile(self, path, importFormat):
        """
        @see: L{gui.app_interface.IApplication.importFile}.
        """
        return self.__executor.execute(ImportCommand(self.__manager, path, importFormat))
        
    def importString(self, data, importFormat):
        """
        @see: L{gui.app_interface.IApplication.importFile}.
        """
        return self.__executor.execute(ImportStringCommand(self.__manager, path, importFormat))
        
    def exportFile(self, path, exportFormat):
        """
        @see: L{gui.app_interface.IApplication.exportFile}.
        """
        return self.__executor.execute(ExportCommand(self.__manager, path, exportFormat))
                
    def exportString(self, exportFormat):
        """
        @see: L{gui.app_interface.IApplication.exportFile}.
        """
        return self.__executor.execute(ExportStringCommand(self.__manager, exportFormat))
        
    def openFile(self, path, openFormat):
        """
        @see: L{gui.app_interface.IApplication.openFile}.
        """
        return self.__executor.execute(OpenCommand(self.__manager, path, openFormat))
        
    def addEntry(self, entryBibTeX, entryType = None):
        """
        @see: L{gui.app_interface.IApplication.addEntry}.
        """
        return self.__executor.execute(AddCommand(self.__manager, entryBibTeX, entryType))
        
    def duplicateEntry(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.duplicateEntry}.
        """
        return self.__executor.execute(DuplicateCommand(self.__manager, entryId))
        
    def updateEntry(self, entryId, entryBibTeX):
        """
        @see: L{gui.app_interface.IApplication.updateEntry}.
        """
        return self.__executor.execute(UpdateCommand(self.__manager, entryId, entryBibTeX))
    
    def updateEntryField(self, entryId, entryBibTeX, fieldName, fieldValue):
        """
        @see: L{gui.app_interface.IApplication.updateEntryField}.
        """
        return self.__executor.execute(UpdateCommand(self.__manager,entryId, entryBibTeX, fieldName, fieldValue))
    
    def deleteEntry(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.deleteEntry}.
        """
        return self.__executor.execute(DeleteCommand(self.__manager, entryId))
        
    def previewEntry(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.previewEntry}.
        """
        return self.__executor.execute(PreviewCommand(self.__manager, entryId))
        
    def generateAllKeys(self):
        """
        @see: L{gui.app_interface.IApplication.generateAllKeys}.
        """
        return self.__executor.execute(GenerateAllKeysCommand(self.__manager))
        
    def validateAllEntries(self):
        """
        @see: L{gui.app_interface.IApplication.validateAllEntries}.
        """
        return self.__executor.execute(ValidateAllCommand(self.__manager))
        
    def undo(self):
        """
        @see: L{gui.app_interface.IApplication.undo}.
        """
        return self.__executor.execute(UndoCommand(self.__executor))
    
    def hasUndoableActionLeft(self):
        """
        @see: L{gui.app_interface.IApplication.hasUndoableActionLeft}.
        """
        return self.__executor.canUndo()
    
    def getEntryPaperURL(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.getEntryPaperURL}.
        """
        entry = self.__manager.getEntry(entryId)
        if entry:
            return entry.getFieldValue(FieldName.Paper)
        raise Exception('entry not found.')
        
    def search(self, query):
        """
        @see: L{gui.app_interface.IApplication.search}.
        """
        return self.__executor.execute(SearchCommand(self.__manager, query))
        
    def sort(self, field, reverse=False):
        """
        @see: L{gui.app_interface.IApplication.sort}.
        """
        return self.__executor.execute(SortCommand(self.__manager, field, reverse))
        
    def getEntry(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.getEntry}.
        """
        entry = self.__manager.getEntry(entryId)
        if entry:
            return entry.toEntryDict()
        raise Exception('entry not found.')
        
    def getContributors(self, entryId):
        """
        Get the contributors of an entry.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{list} of L{app.field.Contributor}
        @return: The contributors.
        @raise Exception: If entry not found.
        @note: Contributors are not always the authors, they could be the editors or organizers.
        """
        entry = self.__manager.getEntry(entryId)
        if entry:
            return entry.getContributors()
        raise Exception('entry not found.')
        
    def getVenue(self, entryId):
        """
        Get the venue of an entry.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{str}
        @return: The name of the venue.
        @raise Exception: If entry not found.
        @note: This corresponds to where the renference was published. For example, the name of the journal or proceedings.
        """
        entry = self.__manager.getEntry(entryId)
        if entry:
            return entry.getVenue()
        raise Exception('entry not found.')
        
    def getBibTeX(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.getBibTeX}.
        """
        entry = self.__manager.getEntry(entryId)
        if entry:
            return entry.toBibTeX()
        raise Exception('entry not found.')
    
    def getEntryRequiredFields(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.getEntryRequiredFields}.
        """
        entry = self.__manager.getEntry(entryId)
        if entry:
            result=entry.iterRequiredFields()
            return result
        raise Exception('entry not found.')
    
    def getEntryOptionalFields(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.getEntryOptionalFields}.
        """
        entry = self.__manager.getEntry(entryId)
        if entry:
            result=entry.iterOptionalFields()
            return result
        raise Exception('entry not found.')
    
    def getEntryAdditionalFields(self, entryId):
        """
        @see: L{gui.app_interface.IApplication.getEntryAdditionalFields}.
        """
        entry = self.__manager.getEntry(entryId)
        if entry:
            result=entry.iterAdditionalFields()
            return result
        raise Exception('entry not found.')
        
    def getAllEntries(self):
        """
        @see: L{gui.app_interface.IApplication.getAllEntries}.
        """
        return [entry.toEntryDict() for entry in self.__manager.iterEntries()]
        
    def getEntryCount(self):
        """
        @see: L{gui.app_interface.IApplication.getEntryCount}.
        """
        return self.__manager.getEntryCount()
        
    def getSearchResult(self):
        """
        @see: L{gui.app_interface.IApplication.getSearchResult}.
        """
        return [entry.toEntryDict() for entry in self.__manager.iterSearchResult()]
        
    def getSearchResultCount(self):
        """
        @see: L{gui.app_interface.IApplication.getSearchResultCount}.
        """
        return self.__manager.getSearchResultCount()
        
    def iterAllEntries(self):
        """
        @see: L{gui.app_interface.IApplication.iterAllEntries}.
        """
        for entry in self.__manager.iterEntries():
            yield entry.toEntryDict()
        
    def iterSearchResult(self):
        """
        @see: L{gui.app_interface.IApplication.iterSearchResult}.
        """
        for entry in self.__manager.iterSearchResult():
            yield entry.toEntryDict()
    
    @staticmethod
    def formatBibTeX(self, bibtex):
        """
        Parses a BibTeX string, formats it according to the standard, and returns it.
        @type bibtex: L{str}
        @param bibtex: The BibTeX string.
        @rtype: L{str}
        @return: If parsed successfully, returns the formatted string, otherwise returns C{''}.
        @raise Exception: If the provided BibTeX is invalid.
        @see: L{BibTeXParser} for supported formats.
        """
        return BibTeXParser(bibtex).parse().toBibTeX()
