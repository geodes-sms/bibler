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

This module tests the L{app.BiBlerApp.addEntry} method.
'''
import unittest
from testApp import oracle
from app.user_interface import BiBlerApp
from gui.app_interface import EntryListColumn


class TestSort(unittest.TestCase):
    def setUp(self):
        self.ui = BiBlerApp()
        c = 'z'
        for e in oracle.all_entries:
            _id = self.ui.addEntry(e.getBibTeX())
            entry = self.ui.getEntry(_id)
            for field in EntryListColumn.list():
                entry[field] = c + str(entry[field])
            result = self.ui.updateEntry(_id, entry.toBibTeX())
            if not result:
                raise Exception('Something went wrong when setting up the test cases.')
            c = chr(ord(c) - 1)

    def tearDown(self):
        pass

    def testSortEveryColumn(self):
        for col in EntryListColumn.list():
            result = self.ui.sort(col)
            self.assertTrue(result, 'Sorting failed on column %s.' % col)
            self.assertEqual(self.ui.getEntryCount(), len(oracle.all_entries), 'The number of entries was not preserved.')

    def testSortInvalidColumn(self):
        result = self.ui.sort('xyz')
        self.assertTrue(result, 'Sorted an invalid column.')
        self.assertEqual(self.ui.getEntryCount(), len(oracle.all_entries), 'The number of entries was not preserved.')

    def testSortSanity(self):
        for col in EntryListColumn.list():
            result = self.ui.sort(col)
            result = result and self.ui.sort(col)
            self.assertTrue(result, 'Sorting failed on column %s.' % col)
            self.assertEqual(self.ui.getEntryCount(), len(oracle.all_entries), 'The number of entries was not preserved.')


if __name__ == "__main__":
    unittest.main()