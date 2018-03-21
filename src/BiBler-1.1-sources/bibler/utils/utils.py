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