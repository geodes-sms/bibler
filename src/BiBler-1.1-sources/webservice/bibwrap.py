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

'''
:Author: Felix Belanger Robillard
'''
#-*- coding: utf-8 -*-
#import sys, os
#abspath = os.path.dirname("/var/www/ift3150/app/")
#sys.path.append(abspath)
#os.chdir(abspath)
from app.user_interface import BiBlerApp
from gui.app_interface import EntryListColumn
import tempfile


class BiBlerWrapper(object):
    @staticmethod
    def addEntry(self, bibtex):
        '''

        Takes a BibTeX string and outputs the corresponding EntryDict
        
        :param str bibtex: The BibTeX string to be processed.
        :return: The written Entry from the BibTeX
        :rtype: EntryDict
        '''
        biblerapp=BiBlerWrapper.__getBiblerApp()
        biblerapp.addEntry(bibtex)
        return biblerapp.iterAllEntries()

    @staticmethod
    def getBibTeX(self, bibtex):
        '''

        Takes a BibTeX string and outputs the corresponding corrected BibTeX string
        
        :param str bibtex: The BibTeX string to be processed.
        :return: The corrected BibTeX including overriden key
        :rtype: str
        '''
        biblerapp=BiBlerWrapper.__getBiblerApp()
        b = biblerapp.addEntry(bibtex)
        return biblerapp.getBibTeX(b)


    @staticmethod
    def exportString(self, bibtex, exportFormat):
        '''

        Takes a BibTeX string and outputs a string to the specified format
        
        :param str bibtex: The BibTeX string to be processed.
        :return: String to specified format
        :rtype: string
        '''
        biblerapp=BiBlerWrapper.__getBiblerApp()
        biblerapp.addEntry(bibtex)
        return biblerapp.exportString(exportFormat)
         
    @staticmethod
    def previewEntry(self,bibtex):
        '''

        Takes a BibTeX string and outputs an HTML preview
        
        :param str bibtex: The BibTeX string to be processed.
        :return: HTML preview for the entry
        :rtype: str
        '''
        biblerapp=BiBlerWrapper.__getBiblerApp()
        entryid = biblerapp.addEntry(bibtex)
        return biblerapp.previewEntry(entryid)

    @staticmethod
    def validateEntry(self, bibtex):
        '''

        Takes a BibTeX string and outputs 1 if the entry is valid or 0 if it's not

        :param str bibtex: The BibTeX string to be processed.
        :return: Number of valid entries, which will be 0 or 1
        :rtype: int
        '''
        biblerapp=BiBlerWrapper.__getBiblerApp()
        biblerapp.addEntry(bibtex)
        return biblerapp.validateAllEntries()
 

    @staticmethod
    def formatBibtex(self, bibtex):
        '''

        Takes a BibTeX string and outputs a formatted BibTeX

        :param str bibtex: The BibTeX string to be processed.
        :return: BibTeX entry
        :rtype: str
        '''
        return BiBlerApp.formatBibTeX(self, bibtex)

    # Added by Eugene Syriani on 18/10/2017 for ReLiS integration
    @staticmethod
    def createEntryForReLiS(self, bibtex):
        '''

        Takes a BibTeX string and outputs a JSON object with the parsed result: validation code and message, the EntryDict, the HTML preview, the BibTeX, the authors, the year, and the venue.
        
        :param str bibtex: The BibTeX string to be processed.
        :return: The result as a dictionary
        :rtype: dict
        '''
        biblerapp=BiBlerWrapper.__getBiblerApp()
        entryId = biblerapp.addEntry(bibtex)
        entry = biblerapp.getEntry(entryId)
        return BiBlerWrapper.__entryToJSON(entry)

    # Added by Eugene Syriani on 1/02/2018 for ReLiS integration
    @staticmethod
    def importStringForReLiS(self, data, format):
        '''

        Takes a BibTeX string and outputs a JSON object with the parsed result: validation code and message, the EntryDict, the HTML preview, the BibTeX, the authors, the year, and the venue.
        
        :param str data: The BibTeX string of all entries to be processed.
        :param str format: The format of the entries.
        :return: The result as a dictionary
        :rtype: dict
        '''
        biblerapp=BiBlerWrapper.__getBiblerApp()
        json = {'error' : '', 'total' : 0}
        try:
          total = biblerapp.importString(bibtex_data, format)
          json['total'] = total
          i = 1
          for entry in biblerapp.iterAllEntries():
            json[i] = BiBlerWrapper.__entryToJSON(entry)
            i += 1
          return str(json)
        except Exception as e:
          json['error'] = str(e)
    
    # Added by Eugene Syriani on 1/02/2018 for ReLiS integration
    @staticmethod
    def __entryToJSON(entry):
        '''

        Convert an entry into JSON.
        :param Entry entry: The entry.
        :return: The result as a dictionary.
        :rtype: dict
        '''
        json = {}
        json['result_code'] = int(entry[EntryListColumn.Valid])
        json['result_msg'] = entry[EntryListColumn.Message]
        json['entry'] = entry
        json['preview'] = biblerapp.previewEntry(entryId)
        json['bibtex'] = biblerapp.getBibTeX(entryId)
        authors = []
        for c in biblerapp.getContributors(entryId):
          a = {}
          a['first_name'] = c.first_name
          a['last_name'] = c.last_name
          a['preposition'] = c.preposition
          a['suffix'] = c.suffix
          authors.append(a)
        json['authors'] = authors
        json['venue_full'] = biblerapp.getVenue(entryId)
        return str(json)


    @staticmethod
    def __getBiblerApp():
        '''

        Returns an instance of BiblerApp.

        :return: Bibler's API instance
        :rtype: BiblerApp
        '''
        biblerapp=BiBlerApp()
        biblerapp.preferences.overrideKeyGeneration = True
        return biblerapp
