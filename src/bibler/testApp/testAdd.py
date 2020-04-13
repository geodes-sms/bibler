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
.. moduleauthor:: Florin Oncica 

.. versionadded:: 1.0

This module tests the L{app.BiBlerApp.addEntry} method.
'''
import unittest
from testApp import oracle
from app.user_interface import BiBlerApp
from gui.app_interface import EntryListColumn
from app.entry_type import EntryType
from utils import settings


class TestAdd(unittest.TestCase):
    def setUp(self):
        self.ui = BiBlerApp()
        settings.Preferences().allowInvalidEntries = False
        settings.Preferences().overrideKeyGeneration = True

    def tearDown(self):
        pass

    def testAddEmptyEntryFromNone(self):
        _id = self.ui.addEntry(None)
        self.assertIsNotNone(_id, 'empty entry not added.')
        self.assertEqual(self.ui.getEntryCount(), 1, 'empty entry not added.')

    def testAddEmptyEntryFromEmptyString(self):
        _id = self.ui.addEntry('')
        self.assertIsNotNone(_id, 'empty entry not added.')
        self.assertEqual(self.ui.getEntryCount(), 1, 'empty entry not added.')
        
    def testAddInEmptyEntryWithType(self):
        for t in EntryType.getAllEntryTypes():
            _id = self.ui.addEntry(None, t.lower())
            self.assertIsNotNone(_id, 'empty %s entry not added.' % t)

    def testAddInEmptyDB(self):
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        self.assertIsNotNone(_id, '%s not added.' % oracle.valid_entry_full)
        self.assertEqual(self.ui.getEntryCount(), 1, '%s not added.' % oracle.valid_entry_full)
    
    def testAddValidBibTeX(self):
        for e in oracle.all_entries:
            _id = self.ui.addEntry(e.getBibTeX())
            self.assertIsNotNone(_id, '%s not added.' % e)
    
    def testAddValidBibTeXVariants(self):
        for e in oracle.valid_bibtex_variants:
            _id = self.ui.addEntry(e.getBibTeX())
            self.assertIsNotNone(_id, '%s not added.' % e)

    def testAddInNonEmptyDB(self):
        for e in oracle.all_entry_types:
            self.ui.addEntry(e.getBibTeX())
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        self.assertIsNotNone(_id, '%s not added.' % oracle.valid_entry_full)
        self.assertEqual(self.ui.getEntryCount(), len(oracle.all_entry_types) + 1, '%s not added.' % oracle.valid_entry_full)

    def testAddExistingEntry(self):
        entry = oracle.valid_entry_full
        self.ui.addEntry(entry.getBibTeX())
        _id = self.ui.addEntry(entry.getBibTeX())
        self.assertIsNotNone(_id, 'entry not added.')
        self.assertTrue(self.ui.getEntry(_id)[EntryListColumn.Entrykey].endswith('a'), 'incorrect key in duplicate of %s.' % entry)
        self.assertEqual(self.ui.getEntryCount(), 2, '%s not added.' % oracle.valid_entry_full)

    def testAddMissingRequiredField(self):
        for e in oracle.all_invalid_entry_types_no_req:
            _id = self.ui.addEntry(e.getBibTeX())
            self.assertIsNone(_id, '%s wrongly added.' % e)
            self.assertEqual(self.ui.getEntryCount(), 0, '%s wrongly added.' % e)

    def testAddInvalidBibTeX(self):
        for e in oracle.all_invalid_entries:
            _id = self.ui.addEntry(e.getBibTeX())
            self.assertIsNone(_id, '%s was wrongly added.' % e)
            self.assertEqual(self.ui.getEntryCount(), 0, '%s wrongly added.' % e)

    def testAddErroneousBibTeX(self):
        for e in oracle.all_erroneous_entries:
            self.assertRaises(Exception, self.ui.addEntry, e.getBibTeX())
            self.assertEqual(self.ui.getEntryCount(), 0, '%s wrongly added.' % e)
    
    def testAddDeleteSanity(self):
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        self.ui.deleteEntry(_id)
        self.assertEqual(self.ui.getEntryCount(), 0, 'adding an entry then deleting it did not undo the addition.')
    
    def testAddWithQuotes(self):
        settings.Preferences().overrideKeyGeneration = False
        _id = self.ui.addEntry(oracle.valid_entry_bracket.getBibTeX())
        bibtex_bracket = self.ui.getBibTeX(_id)
        _id = self.ui.addEntry(oracle.valid_entry_quote.getBibTeX())
        bibtex_quote = self.ui.getBibTeX(_id)
        self.assertEqual(bibtex_bracket, bibtex_quote, 'adding an entry in quotes does not parse correctly')


if __name__ == "__main__":
    unittest.main()