'''
Created on Jan 13, 2014
@author: Eugene Syriani
@version: 0.7

This is module represents the settings for BiBler.
@group Enumerations: BibStyle, ExportFormat, ImportFormat
'''

import os
from . import utils

class ImportFormat:
    """
    Enumerates the allowed import formats.
    """
    BIBTEX = 'bib'
    """
    .bib extension representing a BibTeX file.
    """
    CSV = 'csv'
    """
    .csv extension representing a Comma-Separated Values file.
    """
    ENDNOTE = 'endnote'
    """
    .bib extension representing a BibTeX file exported from EndNote using the BiBlerExporter for EndNote.
    """

class ExportFormat:
    """
    Enumerates the allowed export formats.
    """
    BIBTEX = 'bib'
    """
    .bib extension representing a BibTeX file.
    """
    CSV = 'csv'
    """
    .csv extension representing a Comma-Separated Values file.
    """
    HTML = 'html'
    """
    .html extension representing a web page.
    """
    SQL = 'sql'
    """
    .sql extension representing a MySQL database.
    """

class BibStyle:
    """
    Enumerates the possible bibliography styles.
    """
    ACM = 'acm'
    DEFAULT = 'default'
    
    @staticmethod
    def getAllStyles():
        return sorted([BibStyle.ACM, BibStyle.DEFAULT])

class Preferences(object, metaclass=utils.Singleton):
    """
    Holds the preferences of this BiBler instance, such as:
    the bibliography style and the default directory.
    """
    def __init__(self):
        self.bibStyle = BibStyle.DEFAULT
        """
        The bibliography style of BiBler.
        """
        self.defaultDir = os.path.pardir
        """
        The default directory to use for I/O.
        """
        self.allowInvalidEntries = True
        """
        Enforces to only add valid well-formed entries with respect to their BibTeX representation and ignore others.
        """
        self.allowNonStandardFields = False
        """
        Enforces to only retain standard BibTeX fields in each entry.
        """
        self.overrideKeyGeneration = False
        """
        Enforces to only add valid well-formed entries with respect to their BibTeX representation and ignore others.
        """
        self.searchRegex = False
        """
        Allows regular expressions in search query.
        """