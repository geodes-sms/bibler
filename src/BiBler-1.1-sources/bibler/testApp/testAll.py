'''
Created on Jan 13, 2014
.. moduleauthor:: Eugene Syriani

.. versionadded:: 1.0

This package contains the modules to unit test the L{app.UserInterface.UserInterface} class.
'''
import unittest
from .testAdd import TestAdd
from .testDelete import TestDelete
from .testUpdate import TestUpdate
from .testDuplicate import TestDuplicate
from .testPreview import TestPreview
from .testSearch import TestSearch
from .testSort import TestSort

def testApp():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAdd))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDelete))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestUpdate))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDuplicate))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestPreview))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSearch))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSort))
    return suite  


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testApp())