'''
Created on March 10, 2017
@author: Félix Bélanger-Robillard
'''
import sys, os
abspath = os.path.dirname("/var/www/html/ift3150/")
sys.path.append(abspath)
os.chdir(abspath)

import unittest
import oracle
from bibwrap import BiBlerWrapper


class TestAddEntry(unittest.TestCase):
    def setUp(self):
        #self.ui = BiBlerWrapper
        pass
    
    def tearDown(self):
        pass

    def testAddEmptyEntryFromNone(self):
        _id = BiBlerWrapper.addEntry(None)
        self.assertIsNotNone(_id, 'empty entry not added.')
        self.assertEqual(self.ui.getEntryCount(), 1, 'empty entry not added.')

    def testAddEmptyEntryFromEmptyString(self):
        _id = BiBlerWrapper.addEntry('')
        self.assertIsNotNone(_id, 'empty entry not added.')
        self.assertEqual(self.ui.getEntryCount(), 1, 'empty entry not added.')
        
    def testAddValidBibTeX(self):
        for e in oracle.valid_bibtex_variants:
            _id = BiBlerWrapper.addEntry(e.getBibTeX())
            self.assertIsNotNone(_id, '%s not added.' % e)

    def testAddInvalidBibTeX(self):
        for e in oracle.all_invalid_entry_types:
            _id = BiBlerWrapper.addEntry(e.getBibTeX())
            self.assertIsNone(_id, '%s was wrongly added.' % e)
            self.assertEqual(self.ui.getEntryCount(), 0, '%s wrongly added.' % e)
    
    def testAddWithQuotes(self):
        settings.Preferences().overrideKeyGeneration = False
        _id = BiBlerWrapper.addEntry(oracle.valid_entry_bracket.getBibTeX())
        bibtex_bracket = self.ui.getBibTeX(_id)
        _id = BiBlerWrapper.addEntry(oracle.valid_entry_quote.getBibTeX())
        bibtex_quote = self.ui.getBibTeX(_id)
        self.assertEqual(bibtex_bracket, bibtex_quote, 'adding an entry in quotes does not parse correctly')


if __name__ == "__main__":
    unittest.main()