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