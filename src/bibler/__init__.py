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

"""
.. moduleauthor:: Eugene Syriani
.. versionadded:: 1.4.2

Created on 15 Apr 2020



This is the main BiBler module.
Execute this module from the command line to start the application with a graphical user interface.
You can also interact with BiBler programmatically through its API as follows:

    >>> from BiBler import BiBler 
    >>> BiBler.start()    # starts the BiBler
    >>> BiBler.add('')    # adds an empty entry
    1 
    >>> BiBler.exit()    # closes BiBler
    
.. note:: You may also want to import Preferences (if you need to change the default settings) or Fields (to access a specific field of an entry)

.. attention:: This module assumes that the :ref:`gui` has a L{statechart.BiBler_Statechart} class and the :ref:`app` has a :ref:`Class BiBlerApp` that implements L{gui.app_interface.IApplication}.

G{packagetree app, gui, utils}
"""
__version__ = "1.4.2"

import sys
sys.path.insert(0, 'BiBler')

import wx
from gui.gui import BiBlerGUI 
from gui.controller import Controller
from app.user_interface import BiBlerApp
from gui.app_interface import EntryListColumn
from app.field_name import FieldName
from utils import settings

__all__ = ['BiBler', 'FieldNames', 'Preferences']

class FieldNames(EntryListColumn, FieldName):
    """
    The name of all possible entry fields.
    It is the union of the two enumerations L{gui.app_interface.EntryListColumn} and L{app.field_name.FieldName}.
    """
    pass

class BiBler:
    """
    The application launcher.
    """
    def __init__(self):
        """
        (Constructor)
        """
        self.app = BiBlerApp()
        self.control = None
        self.gui = None
    
    def start(self):
        """
        Starts the BiBler application head-less. 
        """
        self.app.start()
    
    def startGUI(self):
        """
        Starts the BiBler application with the GUI. 
        """
        app = wx.App(False)
        self.control = Controller()
        self.gui = BiBlerGUI(self.control)
        self.control.bindGUI(self.gui)
        self.control.bindApp(self.app)
        self.control.start()
        app.MainLoop()

# The built-in variables
__b = BiBler()
bibler = __b.app
"""
The application in head-less mode.
"""
Preferences = settings.Preferences()
"""
The preferences from L{utils.settings.Preferences}.
"""


if __name__ == '__main__':
    __b.startGUI()


