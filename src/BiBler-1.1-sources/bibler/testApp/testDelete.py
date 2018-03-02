'''
Created on Jan 13, 2014
.. moduleauthor:: Eugene Syriani

.. versionadded:: 1.0

This module tests the L{app.BiBlerApp.deleteEntry} method.
'''
import unittest
from . import oracle
from app.user_interface import BiBlerApp
from gui.app_interface import EntryListColumn


class TestDelete(unittest.TestCase):
    def setUp(self):
        self.ui = BiBlerApp()

    def tearDown(self):
        pass

    def testDeleteInSingletonDB(self):
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        result = self.ui.deleteEntry(_id)
        self.assertTrue(result, '%s not deleted.' % oracle.valid_entry_full)
        self.assertEqual(self.ui.getEntryCount(), 0, '%s not deleted.' % oracle.valid_entry_full)

    def testDeleteInNonEmptyDB(self):
        for e in oracle.all_entry_types:
            self.ui.addEntry(e.getBibTeX())
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        result = self.ui.deleteEntry(_id)
        self.assertTrue(result, '%s not deleted.' % oracle.valid_entry_full)
        self.assertEqual(self.ui.getEntryCount(), len(oracle.all_entry_types), '%s not deleted.' % oracle.valid_entry_full)

    def testDeleteInEmptyDB(self):
        result = self.ui.deleteEntry(0)
        self.assertFalse(result, 'non-existing entry wrongly deleted.')

    def testDeleteNonExistingEntry(self):
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        result = self.ui.deleteEntry(_id + 1)
        self.assertFalse(result, 'non-existing entry wrongly deleted.')
    
    def testDeleteAddSanity(self):
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        self.ui.deleteEntry(_id)
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        e = self.ui.getEntry(_id)
        self.assertEqual(self.ui.getEntryCount(), 1, 'deleting an entry then adding it back did not undo the deletion.')
        self.assertTrue(e[EntryListColumn.Entrykey].endswith(e[EntryListColumn.Year]), 'deleting an entry then adding it back generated an incorrect key.')


if __name__ == "__main__":
    unittest.main()