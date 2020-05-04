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
Created on May 05, 2020
.. moduleauthor:: Eugene Syriani

.. versionadded:: 1.4.2

This module tests the L{app.BiBlerApp.impex} method.
'''
import unittest
from testApp import oracle
from app.user_interface import BiBlerApp
from app.entry import ValidationResult
from utils import settings


class TestOpenImportValidateAll(unittest.TestCase):
    def setUp(self):
        self.ui = BiBlerApp()
        settings.Preferences().allowInvalidEntries = True
        settings.Preferences().overrideKeyGeneration = True

    def tearDown(self):
        pass

    def testOpenBibTeXFileAndValidate(self):
        for bib_file in oracle.bibtex_files:
            result = self.ui.openFile(bib_file.getPath(), settings.ImportFormat.BIBTEX)
            self.assertTrue(result, 'opening %s failed.' % oracle.warn_bibtex_file)
            self.assertEqual(self.ui.getEntryCount(), bib_file.getTotal(), 'incorrect number of imported entries.')
            validation = self.ui.validateAllEntries()
            self.assertEqual(validation['success'], bib_file.getValidNumber(), 'incorrect number of valid entries.')
            self.assertEqual(validation['warning'], bib_file.getWarningNumber(), 'incorrect number of entries with warnings.')
            self.assertEqual(validation['error'], bib_file.getErrorNumber(), 'incorrect number of entries with errors.')

    def testOpenEndNoteFileAndValidate(self):
        result = self.ui.openFile(oracle.warn_error_endnote_file.getPath(), settings.ImportFormat.ENDNOTE)
        self.assertTrue(result, 'opening %s failed.' % oracle.warn_bibtex_file)
        self.assertEqual(self.ui.getEntryCount(), oracle.warn_error_endnote_file.getTotal(), 'incorrect number of imported entries.')
        validation = self.ui.validateAllEntries()
        self.assertEqual(validation['success'], oracle.warn_error_endnote_file.getValidNumber(), 'incorrect number of valid entries.')
        self.assertEqual(validation['warning'], oracle.warn_error_endnote_file.getWarningNumber(), 'incorrect number of entries with warnings.')
        self.assertEqual(validation['error'], oracle.warn_error_endnote_file.getErrorNumber(), 'incorrect number of entries with errors.')
    
    def testImportFile(self):
        self.ui.openFile(oracle.warn_bibtex_file.getPath(), settings.ImportFormat.BIBTEX)
        result = self.ui.importFile(oracle.warn_bibtex_file.getPath(), settings.ImportFormat.BIBTEX)
        self.assertTrue(result, 'importing %s failed.' % oracle.warn_bibtex_file)
        self.assertEqual(self.ui.getEntryCount(), oracle.warn_bibtex_file.getTotal() * 2, 'incorrect number of imported entries.')
        validation = self.ui.validateAllEntries()
        self.assertEqual(validation['success'], oracle.warn_bibtex_file.getValidNumber() * 2, 'incorrect number of valid entries.')
        self.assertEqual(validation['warning'], oracle.warn_bibtex_file.getWarningNumber() * 2, 'incorrect number of entries with warnings.')
        self.assertEqual(validation['error'], oracle.warn_bibtex_file.getErrorNumber() * 2, 'incorrect number of entries with errors.')
        

    #TODO: test other import formats


if __name__ == "__main__":
    unittest.main()