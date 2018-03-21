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
Created on Jan 13, 2014
.. moduleauthor:: Eugene Syriani

.. versionadded:: 1.0

This module tests the L{app.BiBlerApp.search} method.
'''
import unittest
from . import oracle
from app.user_interface import BiBlerApp
from utils.settings import Preferences


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.ui = BiBlerApp()

    def tearDown(self):
        pass

    def testSearchRegexInEmptyDB(self):
        Preferences().searchRegex = True
        total = self.ui.search('syriani')
        self.assertTrue(total >= 0, 'search failed.')
        self.assertEqual(len(self.ui.getSearchResult()), 0, 'entries wrongly found.')

    def testSearchRegexInSingletonDB(self):
        Preferences().searchRegex = True
        query = 'landin'
        self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        total = self.ui.search(query)
        self.assertTrue(total >= 0, 'search failed.')
        self.assertEqual(len(self.ui.getSearchResult()), 1, 'entry not found.')

    def testSearchRegexMatchingQuery(self):
        Preferences().searchRegex = True
        for e in oracle.all_entries_all_fields:
            self.ui.addEntry(e.getBibTeX())
        searchResults = oracle.search_all_entries_all_fields
        for query in oracle.search_all_entries_all_fields:
            total = self.ui.search(query)
            self.assertTrue(total >= 0, 'search failed.')
            self.assertEqual(len(self.ui.getSearchResult()), searchResults[query], 'incorrect number of entries found.')

    def testSearchRegexAll(self):
        Preferences().searchRegex = True
        for e in oracle.all_entries_all_fields:
            self.ui.addEntry(e.getBibTeX())
        total = self.ui.search('')
        self.assertTrue(total >= 0, 'search failed.')
        self.assertEqual(len(self.ui.getSearchResult()), self.ui.getEntryCount(), 'incorrect number of entries found.')

    def testSearchExactInEmptyDB(self):
        Preferences().searchRegex = False
        total = self.ui.search('syriani')
        self.assertTrue(total >= 0, 'search failed.')
        self.assertEqual(len(self.ui.getSearchResult()), 0, 'entries wrongly found.')

    def testSearchExactInSingletonDB(self):
        Preferences().searchRegex = False
        query = 'landin'
        self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        total = self.ui.search(query)
        self.assertTrue(total >= 0, 'search failed.')
        self.assertEqual(len(self.ui.getSearchResult()), 1, 'entry not found.')

    def testSearchExactMatchingQuery(self):
        Preferences().searchRegex = False
        for e in oracle.all_entries_all_fields:
            self.ui.addEntry(e.getBibTeX())
        searchResults = oracle.search_all_entries_all_fields
        for query in oracle.search_all_entries_all_fields:
            total = self.ui.search(query)
            self.assertTrue(total >= 0, 'search failed.')
            self.assertEqual(len(self.ui.getSearchResult()), searchResults[query], 'incorrect number of entries found.')

    def testSearchExactAll(self):
        Preferences().searchRegex = False
        for e in oracle.all_entries_all_fields:
            self.ui.addEntry(e.getBibTeX())
        total = self.ui.search('')
        self.assertTrue(total >= 0, 'search failed.')
        self.assertEqual(len(self.ui.getSearchResult()), self.ui.getEntryCount(), 'incorrect number of entries found.')


if __name__ == "__main__":
    unittest.main()