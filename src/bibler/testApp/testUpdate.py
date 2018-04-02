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

This module tests the L{app.BiBlerApp.updateEntry} method.
'''
import unittest
from . import oracle
from app.user_interface import BiBlerApp
from gui.app_interface import EntryListColumn
from utils import settings


class TestUpdate(unittest.TestCase):
    def setUp(self):
        self.ui = BiBlerApp()
        self._ids = []
        for e in oracle.all_entries_all_fields:
            self._ids.append(self.ui.addEntry(e.getBibTeX()))
        self.total = len(oracle.all_entries_all_fields)
        settings.Preferences().overrideKeyGeneration = True

    def tearDown(self):
        pass
    
    def testUpdateAllFields(self):
        for i in self._ids:
            expected_entry = self.ui.getEntry(i)
            for col in list(expected_entry.keys()):
                if col in [EntryListColumn.Entrytype, EntryListColumn.Entrykey, EntryListColumn.Id,
                           EntryListColumn.Valid, EntryListColumn.Message]:  # tested in other test cases
                    continue
                expected_entry[col] = 'Abc'
            if expected_entry[EntryListColumn.Entrytype].lower() == 'book':
                del expected_entry[EntryListColumn.Author]
                expected_entry['number'] = ''
            bib = expected_entry.toBibTeX()
            result = self.ui.updateEntry(i, bib)
            if not result:
                pass
            self.assertTrue(result, 'entry not updated.')
            self.assertEqual(self.ui.getEntryCount(), self.total, 'number of entries wrongly changed.')
            observed_entry = self.ui.getEntry(i)
            for col in list(observed_entry.keys()):
                if col == 'message':
                    pass
                if col == EntryListColumn.Entrykey:
                    continue
                self.assertEqual(observed_entry[col], expected_entry[col], 'field %s not updated.' % col)
    
    def testUpdateAuthorYear(self):
        suffix = ''
        for ix in range(len(self._ids)):
            i = self._ids[ix]
            expected_entry = self.ui.getEntry(i)
            if oracle.all_entries_all_fields[ix] == oracle.valid_book_all_fields_editor:
                expected_entry['editor'] = 'Xyz'
            else:
                expected_entry[EntryListColumn.Author] = 'Xyz'
            expected_entry[EntryListColumn.Year] = '0000'
            bib = expected_entry.toBibTeX()
            result = self.ui.updateEntry(i, bib)
            self.assertTrue(result, 'entry not updated to %s.' % expected_entry)
            observed_entry = self.ui.getEntry(i)
            self.assertEqual(observed_entry[EntryListColumn.Entrykey], 'Xyz0000' + suffix, 'key not correctly updated.')
            self.assertEqual(self.ui.getEntryCount(), self.total, 'number of entries wrongly changed.')
            if suffix == '':
                suffix = 'a'
            elif suffix == 'z':
                break
            else:
                suffix = chr(ord(suffix) + 1)
    
    def testUpdateType(self):
        for i in self._ids:
            expected_entry = oracle.valid_article_all_fields
            if self.ui.getEntry(i)[EntryListColumn.Entrytype].lower() == 'article':
                expected_entry = oracle.valid_inproceedings_all_fields
            result = self.ui.updateEntry(i, expected_entry.getBibTeX())
            self.assertTrue(result, 'entry not updated to %s.' % expected_entry)
            self.assertEqual(self.ui.getEntryCount(), self.total, 'number of entries wrongly changed.')
 
    def testUpdateNonExistingEntry(self):
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        result = self.ui.updateEntry(_id + 10, oracle.valid_entry_full.getBibTeX())
        self.assertFalse(result, 'non-existing entry wrongly updated.')
 
    def testUpdateMissingRequiredFields(self):
        for i in self._ids:
            for e in oracle.all_invalid_entry_types_no_req:
                self.assertRaises(Exception, lambda: self.ui.updateEntry(i, e.getBibTeX()), 'entry updated to %s.' % e)
                self.assertEqual(self.ui.getEntryCount(), self.total, 'number of entries wrongly changed.')
     
    def testUpdateUpdateSanity(self):
        for i in self._ids:
            old_entry = self.ui.getEntry(i)
            new_entry = oracle.valid_entry_full
            result1 = self.ui.updateEntry(i, new_entry.getBibTeX())
            result2 = self.ui.updateEntry(i, old_entry.toBibTeX())
            self.assertTrue(result1 and result2, 'modifying %s back to itself did not retain changes.' % old_entry)
            self.assertEqual(self.ui.getEntryCount(), self.total, 'number of entries wrongly changed.')


if __name__ == "__main__":
    unittest.main()