'''
Created on Jan 13, 2014
@author: Eugene Syriani
@version: 0.7

This module contains utility classes and functions. 
'''

class Singleton(type):
    """
    Meta-class to turn a class into a singleton.
    """
    def __init__(self, name, bases, _dict):
        super(Singleton, self).__init__(name, bases, _dict)
        self.instance = None
    
    def __call__(self, *args, **kw):
        # called whenever a function (or class) is called
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kw)
        return self.instance
    
    
def escapeSQLCharacters(s):
    return s.replace("'","''").replace("\\","\\\\")