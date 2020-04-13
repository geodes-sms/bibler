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
Created on Jan 13, 2014
.. moduleauthor:: Eugene Syriani
.. moduleauthor:: Florin Oncica 

.. versionadded:: 1.0

This module represents the interface that the L{app} module must conform to.
@group Interchange data-structures: EntryDict, EntryListColumn
@sort: EntryDict, EntryListColumn
"""

class EntryListColumn(object):
    """
    The columns of the entry list.
    """
    Author = 'author'
    Entrytype = 'entrytype'
    Entrykey = 'entrykey'
    Id = 'id'
    Message = 'message'
    Paper = 'paper'
    Title = 'title'
    Valid = 'valid'
    Year = 'year'
    
    @staticmethod
    def list():
        """
        @rtype: L{list}
        @return: A list of all the columns.
        """
        return [EntryListColumn.Author, EntryListColumn.Id, EntryListColumn.Entrykey, EntryListColumn.Paper,
                EntryListColumn.Title, EntryListColumn.Entrytype, EntryListColumn.Valid, EntryListColumn.Year, EntryListColumn.Message]

class EntryDict(dict):
    """
    The exchange format of entries.
    It is a dictionary where all L{EntryListColumn} fields are predefined keys that cannot be removed.
    
        >>> d = EntryDict()
        >>> print d
            {'id': '', ...}
        >>> del d[EntryListColumn.Id]
        >>> print d
            {'id': '', ...}
    """
    def __init__(self, *args):
        """
        All L{EntryListColumn} fields are predefined keys.
        """
        dict.__init__(self, args)
        for key in EntryListColumn.list():
            if key not in iter(self.keys()):
                if key == EntryListColumn.Id:
                    self[key] = 0
                else:
                    self[key] = ''
        
    def __delitem__(self, key):
        """
        Deleting a L{EntryListColumn} key will set its value to C{''}.
        """
        if key not in EntryListColumn.list():
            dict.__delitem__(key)
        elif key == EntryListColumn.Id:
            raise KeyError('Cannot delete key: ' + EntryListColumn.Id)
        else:
            self[key] = ''
        
    def toBibTeX(self):
        """
        Convert into a BibTeX reference.
        @rtype: L{str}
        @return: The BibTeX reference.
        @note: The BibTeX format is::
            @TYPE{KEY,
              FIELD1 = {VALUE1},
              FIELD2 = {VALUE2}
            }
        """
        try:
            bibtex = '@%s{%s' % (self[EntryListColumn.Entrytype].upper(), self[EntryListColumn.Entrykey])
            for field,value in self.items():
                if field == EntryListColumn.Id or field == EntryListColumn.Valid:
                    continue
                # This part is to put {} around capital letters if they aren't already
                v = ''
                for i in range(len(value)):
                    if value[i].isupper():
                        if 0 < i < len(value) - 1 and value[i-1] != '{' and value[i+1] != '}':
                            v += '{%s}' % value[i]
                    else:
                        v += value[i]
                bibtex += ',\n  %s = {%s}' % (field, value)
            bibtex += '\n}'
            return bibtex
        except:
            return ''
    
    @staticmethod
    def fromDict(d):
        """
        Convert a Python L{dict} into an L{EntryDict}.
        @type d: L{dict}
        @param d: The dictionary to convert.
        @rtype: L{EntryDict}
        @return: An L{EntryDict} with all the keys and values from C{d}.
        """
        ed = EntryDict()
        for k in d:
            ed[k] = d[k]
        return ed

class IApplication(object):
    """
    Interface that provides all the application functions required for the L{Controller<gui.controller.Controller>}.
    The meaning of every operation in the BiBler GUI is given by these functions.
    """
    
    def start(self):
        """
        Start the application.
        """
        raise NotImplementedError()
    
    def exit(self):
        """
        Close the application.
        """
        raise NotImplementedError()
    
    def importFile(self, path, importFormat):
        """
        Import a list of entries from a file in a given format.
        @type path: L{str}
        @param path: The path to a file.
        @type importFormat: L{utils.settings.ImportFormat}
        @param importFormat: The format of the file.
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def importString(self, data, importFormat):
        """
        Import a list of entries from a string in a given format.
        @type data: L{str}
        @param data: The string containing the data.
        @type importFormat: L{utils.settings.ImportFormat}
        @param importFormat: The format of the file.
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def exportFile(self, path, exportFormat):
        """
        Export the list of entries to a file in a given format.
        @type path: L{str}
        @param path: The path to a file.
        @type exportFormat: L{utils.settings.ExportFormat}
        @param exportFormat: The format of the file.
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def exportString(self, exportFormat):
        """
        Export the list of entries to a string in a given format.
        @type exportFormat: L{utils.settings.ExportFormat}
        @param exportFormat: The format of the file.
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def openFile(self, path, openFormat):
        """
        Import a list of entries from a BibTeX file in a given format and overwrites all existing entries.
        @type path: L{str}
        @param path: The path to a file.
        @type openFormat: L{utils.settings.ImportFormat}
        @param openFormat: The format of the file.
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def addEntry(self, entryBibTeX, entryType=None, ignoreIfEmpty=False):
        """
        Add a new entry. If C{entryBibTeX==Empty Entry}, an empty entry is created.
        @type entryBibTeX: L{str}
        @param entryBibTeX: The BibTeX reference of the entry.
        @type entryType: L{str}
        @param entryType: The type of the entry, if known in advance.
        @type ignoreIfEmpty: L{bool}
        @param ignoreIfEmpty: When True, does not add the entry if it is empty.
        @rtype: L{int}
        @return: The I{id} of the new entry. C{None} is returned if failed.
        """
        raise NotImplementedError()
    
    def duplicateEntry(self, entryId):
        """
        Create a copy of an existing entry.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry to copy.
        @rtype: L{int}
        @return: The I{id} of the new entry. C{None} is returned if failed.
        """
        raise NotImplementedError()
    
    def updateEntry(self, entryId, entryBibTeX):
        """
        Update an entry with a new BibTeX reference.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry to update. 
        @type entryBibTeX: L{str}
        @param entryBibTeX: The BibTeX reference. 
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def updateEntryField(self, entryId, fieldName, fieldValue):
        """
        Update an entry BibTeX reference field with a new value.
        
        @type entryId: L{int}
        @param entryId: The I{id} of the entry to update. 
        @type fieldName: L{str}
        @param fieldName: The field name.
        @type fieldValue: L{str}
        @param fieldValue: The field value.
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def deleteEntry(self, entryId):
        """
        Delete an entry.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry to delete. 
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def previewEntry(self, entryId):
        """
        Convert an entry into its HTML representation following the bibliography style specified in L{utils.settings.Preferences}.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry to preview. 
        @rtype: L{str}
        @return: The HTML representation of the entry.
        @raise Exception: If entry not found.
        """
        raise NotImplementedError()
        
    def generateAllKeys(self):
        """
        Generate the key of all entries.
        @rtype: L{bool}
        @return: C{True} if all keys were generated successfully, C{False} otherwise.
        """
        raise NotImplementedError()
        
    def validateAllEntries(self):
        """
        Validate all entries.
        """
        raise NotImplementedError()
    
    def undo(self):
        """
        Undo the last action performed. 
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def hasUndoableActionLeft(self):
        """
        Verify if there is any action to undo.
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()
    
    def getEntryPaperURL(self, entryId):
        """
        Get the URL of the paper of the selected entry.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{str}
        @return: The URL (or path) to the file.
        @raise Exception: If entry not found.
        """
        raise NotImplementedError()
    
    def search(self, query):
        """
        Search for entries that satisfy the query provided.
        @type query: L{str}
        @param query: The query to match.
        @rtype: L{int}
        @return: Number of matches if search succeeded, negative number otherwise.
        """
        raise NotImplementedError()
    
    def sort(self, field, reverse=False):
        """
        Inplace sort of in alphabetically increasing order all entries with respect to a field.
        @type field: L{EntryListColumn}
        @param field: The field to sort on.
        @type field: L{bool}
        @param reverse: Sort in decreasing order when C{True}.
        @rtype: L{bool}
        @return: C{True} if succeeded, C{False} otherwise.
        """
        raise NotImplementedError()

    def getEntry(self, entryId):
        """
        Convert an entry into an L{EntryDict}.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{list} of L{EntryDict}
        @return: The entry.
        @raise Exception: If entry not found.
        """
        raise NotImplementedError()

    def getBibTeX(self, entryId):
        """
        Convert an entry into its BibTeX reference.
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{str}
        @return: The BibTeX reference.
        @raise Exception: If entry not found.
        """
        raise NotImplementedError()
    
    def getEntryRequiredFields(self, entryId):
        """
        Get the required fields of an entry.
        
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{dict}
        @return: The dictionary of required fields.
        @raise Exception: If entry not found.
        """
        raise NotImplementedError()
    
    def getEntryOptionalFields(self,entryId):
        """
        Get the optional fields of an entry.
        
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{dict}
        @return: The dictionary of optional fields.
        @raise Exception: If entry not found.
        """
        raise NotImplementedError()
    
    def getEntryAdditionalFields(self,entryId):
        """
        Get the additional fields of an entry.
        
        @type entryId: L{int}
        @param entryId: The I{id} of the entry. 
        @rtype: L{dict}
        @return: The dictionary of additional fields.
        @raise Exception: If entry not found.
        """
        raise NotImplementedError()
    
    def getAllEntries(self):
        """
        Get the list of all entries.
        @rtype: L{list} of L{EntryDict}
        @return: The list of entries.
        """
        raise NotImplementedError()
    
    def getEntryCount(self):
        """
        Get the total number of entries.
        @rtype: L{int}
        @return: The total.
        """
        raise NotImplementedError()
    
    def getSearchResult(self):
        """
        Get the list of entries filtered by the search.
        @rtype: L{list} of L{EntryDict}
        @return: The list of entries.
        """
        raise NotImplementedError()
    
    def getSearchResultCount(self):
        """
        Get the total number of results from the search.
        @rtype: L{int}
        @return: The total.
        """
        raise NotImplementedError()
        
    def iterAllEntries(self):
        """
        Iterator over the list of all entries.
        @rtype: C{generator} of L{EntryDict}
        @return: The list of entries.
        """
        raise NotImplementedError()
        
    def iterSearchResult(self):
        """
        Get the list of entries filtered by the search.
        @rtype: C{generator} of L{EntryDict}
        @return: The list of entries.
        """
        raise NotImplementedError()
