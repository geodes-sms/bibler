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

This module is responsible for managing all resources of BiBler.
'''

from utils import utils
import os

class ResourceManager(object, metaclass=utils.Singleton):
    """
    Give access to the resource files.
    @sort: _*, get*
    """
    def __init__(self):
        self.pdfImagePath = os.path.join('utils', 'resources', 'pdf.png')
        self.aboutHTMLPath = os.path.join('utils', 'resources', 'about.html')
        self.usermanualHTMLPath = os.path.join('utils', 'resources', 'manual.html')
        self.docsHTMLPath = os.path.join('docs', 'index.html')
        self.iconPath = os.path.join('utils', 'resources', 'bibler.ico')
        self.nlp_modelPath = os.path.join('utils', 'resources', 'en_core_web_trf-3.4.0', 'en_core_web_trf', 'en_core_web_trf-3.4.0')
    
    def getAboutHTML(self):
        """
        Get the path to the web page for the L{AboutBox<gui.gui.HTMLDialog>}.
        """
        return self.__getPath(self.aboutHTMLPath)
    
    def getUserManualHTML(self):
        """
        Get the path to the web page for the L{UserManualWindow<gui.gui.HTMLWindow>}.
        """
        return self.__getPath(self.usermanualHTMLPath)
    
    def getPaperImagePath(self):
        """
        Get the path to image for entries with papers.
        """
        return self.__getPath(self.pdfImagePath)
    
    def getIconPath(self):
        """
        Get the path to the icon of BiBler.
        """
        return self.__getPath(self.iconPath)
    
    #def getNLPModelPath(self):
    #    """
    #    Get the path to the NLP model.
    #    """
    #    return self.__getPath(self.nlp_modelPath)
    
    def __getPath(self, path):
        """
        Validates that a path exists.
        @type path: L{str}
        @param path: The path.
        @rtype: L{str}
        @return: The validated path.
        @raise Exception: if the resource file was not found.
        """
        if os.path.exists(path):
            return path
        else:
            raise Exception('Resource file ' + path + ' is missing.')
