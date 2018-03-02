'''
Created on March 12, 2017
@author: Félix Bélanger-Robillard
'''
import unittest
from testAddEntry import TestAddEntry

def testApp():
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAddEntry))
    return suite  


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(testApp())