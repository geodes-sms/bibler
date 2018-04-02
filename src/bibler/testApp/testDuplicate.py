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