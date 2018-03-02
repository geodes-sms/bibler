'''
Created on Jan 13, 2014
.. moduleauthor:: Eugene Syriani

.. versionadded:: 1.0

This module tests the L{app.BiBlerApp.duplicateEntry} method.
'''
import unittest
from . import oracle
from app.user_interface import BiBlerApp
from gui.app_interface import EntryListColumn
from utils import settings


class TestDuplicate(unittest.TestCase):
    def setUp(self):
        self.ui = BiBlerApp()
        settings.Preferences().overrideKeyGeneration = True

    def tearDown(self):
        pass

    def testDuplicateExistingEntry(self):
        for entry in oracle.all_entries_all_fields:
            first_id = self.ui.addEntry(entry.getBibTeX())
            first_entry = self.ui.getEntry(first_id)
            for i in range(27):
                _id = self.ui.duplicateEntry(first_id)
                self.assertIsNotNone(_id, '%s not duplicated.' % entry)
                e = self.ui.getEntry(_id)
                self.assertEqual(e[EntryListColumn.Entrykey], first_entry[EntryListColumn.Entrykey] + chr(ord('a') + i), 'incorrect key in duplicate of %s.' % entry)

    def testDuplicateNonExistingEntry(self):
        _id = 0
        for entry in oracle.all_entries_all_fields:
            _id = self.ui.addEntry(entry.getBibTeX())
        _id = self.ui.duplicateEntry(_id + 1)
        self.assertIsNone(_id, 'non-existing entry wrongly duplicated.')


if __name__ == "__main__":
    unittest.main()