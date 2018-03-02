'''
Created on Jan 13, 2014
.. moduleauthor:: Eugene Syriani

.. versionadded:: 1.0

This module tests the L{app.BiBlerApp.previewEntry} method.
'''
import unittest
from . import oracle
from app.user_interface import BiBlerApp
from utils.settings import Preferences, BibStyle


class TestPreview(unittest.TestCase):
    def setUp(self):
        self.ui = BiBlerApp()

    def tearDown(self):
        pass

    def testPreviewACMAllFields(self):
        Preferences().bibStyle = BibStyle.ACM
        for entry in oracle.all_entries_all_fields:
            _id = self.ui.addEntry(entry.getBibTeX())
            if _id:
                html = self.ui.previewEntry(_id)
                self.assertEqual(html, entry.getACM_HTML(), '%s was not previewed correctly.' % entry)

    def testPreviewACMMissingOptionalFields(self):
        Preferences().bibStyle = BibStyle.ACM
        for entry in oracle.all_entry_types:
            _id = self.ui.addEntry(entry.getBibTeX())
            if _id:
                html = self.ui.previewEntry(_id)
                self.assertEqual(html, entry.getACM_HTML(), '%s was not previewed correctly.' % entry)

    def testPreviewACMNonExistingEntry(self):
        Preferences().bibStyle = BibStyle.ACM
        _id = self.ui.addEntry(oracle.valid_entry_full.getBibTeX())
        self.assertRaises(Exception, self.ui.previewEntry, _id + 1)
    
    def testPreviewACMAuthorVariants(self):
        Preferences().bibStyle = BibStyle.ACM
        for entry in oracle.valid_authors:
            _id = self.ui.addEntry(entry.getBibTeX())
            if _id:
                html = self.ui.previewEntry(_id)
                self.assertEqual(html, entry.getACM_HTML(), '%s was not previewed correctly.' % entry)


if __name__ == "__main__":
    unittest.main()