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

.. versionadded:: 1.0

Created on Nov 09, 2016

This module represents the importers and exporters.
"""

from app.field_name import FieldName
from utils import settings, utils
from utils.settings import Preferences
import os.path


class ImpEx(object):
    """
    The abstract class for importing or exporting.
    Every Impex has a C{path} to the database file and a C{database} file handler.
    """
    def __init__(self, path):
        """
        @type path: L{str}
        @param path: The path to a file.
        """
        self.path = path
        self.database = None
    
    def openDB(self, mode):
        """
        Open the database in a specific mode.
        @type mode: L{str}
        @param mode: Any mode support by python U{open<https://docs.python.org/3.5/library/functions.html#open>}.
        """
        try:
            self.database = open(self.path, mode, encoding='utf8')
        except:
            raise Exception('Cannot open the requested file.')
    
    def closeDB(self):
        """
        Close the database.
        """
        self.database.close()



class Exporter(ImpEx):
    """
    Export a list of L{Entries<app.entry.Entry>} to a specified format.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(Exporter, self).__init__(path)
        self.entries = entries
    
    def export(self):
        """
        The export process.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        total = 0
        try:
            self.openDB('w')
            self._preprocess()
            for entry in self.entries:
                output = self._exportEntry(entry)
                self.write(output)
                total += 1
            self._postprocess()
        except:
            raise
        finally:
            self.closeDB()
        return total

    def write(self, output):
        self.database.write(output + '\n')
    
    def _exportEntry(self):
        pass
    
    def _preprocess(self):
        pass
    
    def _postprocess(self):
        pass
        
class BibTeXExporter(Exporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to a BibTeX file.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(BibTeXExporter, self).__init__(path, entries)
    
    def _exportEntry(self, entry):
        """
        Export to BibTeX.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        return entry.toBibTeX(ignoreEmptyField=True)
    
    
class CSVExporter(Exporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to a CSV (tabs) file.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(CSVExporter, self).__init__(path, entries)
    
    def _exportEntry(self, entry):
        """
        Export to CSV (tabs). The first row consists of the field names for each column.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        return entry.toCSV()
    
    def _preprocess(self):
        self.database.write('entrytype\t' + '\t'.join(FieldName.iterAllFieldNames()) + '\n')    # headers
    
    
class HTMLExporter(Exporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to an HTML file in the default style.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(HTMLExporter, self).__init__(path, entries)
    
    def _exportEntry(self, entry):
        """
        Export to HTML following the default style.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        txt = '<li>'
        if Preferences().bibStyle == settings.BibStyle.ACM:
            txt += entry.toHtmlACM()
        else:
            txt += entry.toHtmlDefault()
        paper = entry.getField(FieldName.Paper).getValue()
        if paper:
            txt += '<a href="%s" class="pdfLink">&nbsp;&nbsp;</a></li>' % paper
        return txt + '</li>'
    
    def _preprocess(self):
        self.database.write('<html><head><style>ol.ref{ list-style-type: none; counter-reset: refCounter; margin-top: 0px; padding: .495% 0 0 0;}ol.ref li:before{ content: "[" counter(refCounter, decimal) "] "; counter-increment: refCounter;}ol.ref li{ display: block; padding-top: .99%;}a.pdfLink{ background: url("http://image.chromefans.org/fileicons/format/pdf.png") center right no-repeat; padding-right: 1.48515%; margin-right: .297%; text-decoration: none;}</style></head><body><ol class="ref">\n')
    
    def _postprocess(self):
        self.database.write('</ol></body></html>')
    
    
class MySQLExporter(Exporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to a MySQL database script.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(MySQLExporter, self).__init__(path, entries)
        ext = os.path.splitext(path)[1]
        self.papersPath = path
        self.authorsPath = os.path.join(os.path.dirname(path), os.path.basename(path)[:-len(ext)] + '_authors' + ext)
        self.assignmentsPath = os.path.join(os.path.dirname(path), os.path.basename(path)[:-len(ext)] + '_assignments' + ext)
        self.unique_contributors = {}
    
    def exportPapers(self):
        papers = 0
        unique_authors = 0
        try:
            self.path = self.papersPath
            self.openDB('w')
            self._preprocess()
            for entry in self.entries:
                output = self._exportEntry(entry)
                self.database.write(output + '\n')
                papers += 1
                for contributor in entry.getContributors():
                    contributor = str(contributor)
                    for uc in self.unique_contributors.keys():
                        if contributor.lower() == uc.lower():
                            self.unique_contributors[uc][1].append(papers)
                            break
                    else:
                        unique_authors += 1
                        self.unique_contributors[contributor] = [unique_authors,[papers]]
            self._postprocess()
        except:
            raise
        finally:
            self.closeDB()
        return papers
    
    def exportAuthors(self):
        total = 0
        try:
            self.path = self.authorsPath
            self.openDB('w')
            for c in self.unique_contributors.keys():
                self.database.write('''INSERT INTO Author (id, name) VALUES (%d, N'%s');\n''' % (self.unique_contributors[c][0], utils.escapeSQLCharacters(c)))
                total += 1
        except:
            raise
        finally:
            self.closeDB()
        return total
    
    def exportAssignments(self):
        total = 0
        try:
            self.path = self.assignmentsPath
            self.openDB('w')
            for c in self.unique_contributors.keys():
                for p in self.unique_contributors[c][1]:
                    self.database.write('''INSERT INTO PaperAuthor (paperId,authorId) VALUES (%d, %d);\n''' % (p, self.unique_contributors[c][0]))
                    total += 1
        except:
            raise
        finally:
            self.closeDB()
        return total
    
    def export(self):
        """
        The export process. It outputs 3 files:
            * one for the database tables and the INSERT statements of the papers,
            * a second one for the authors,
            * and a last one for the paper author assignments.
            
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        papers = self.exportPapers()
        authors = self.exportAuthors()
        assignments = self.exportAssignments()
        if papers > 0 and authors > 0 and assignments > 0:
            return papers
        else:
            return 0
    
    def _exportEntry(self, entry):
        """
        Export to a MySQL database script.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        return entry.toSQL()
    
    def _preprocess(self):
        # create the database tables
        self.database.write('''
-- Table for Papers
DROP TABLE IF EXISTS Paper;
CREATE TABLE IF NOT EXISTS Paper (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    bibtexKey VARCHAR(100) NOT NULL UNIQUE KEY,
    title VARCHAR(200) DEFAULT NULL,
    doi VARCHAR(200) DEFAULT NULL,
    bibtex longtext NOT NULL,
    preview longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Table for Authors
DROP TABLE IF EXISTS Author;
CREATE TABLE IF NOT EXISTS Author (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Table for paper author assignments
DROP TABLE IF EXISTS PaperAuthor;
CREATE TABLE IF NOT EXISTS PaperAuthor (
    paperId INT(11) NOT NULL,
    authorId INT(11) NOT NULL,
    PRIMARY KEY (paperId, authorId),
    KEY FK_Paper (paperId),
    KEY FK_Author (authorId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE PaperAuthor
    ADD CONSTRAINT FK_Author FOREIGN KEY (authorId) REFERENCES Author (id),
    ADD CONSTRAINT FK_Paper FOREIGN KEY (paperId) REFERENCES Paper (id);

''')   

class StringExporter(Exporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to a specified format in a string.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(Exporter, self).__init__(path)
        self.database = ""
        self.entries = entries 

    def openDB(self, mode):
        """
        Open the database in a specific mode.
        @type mode: L{str}
        @param mode: Any mode support by python U{open<https://docs.python.org/3.5/library/functions.html#open>}.
        """
        pass
    
    def closeDB(self):
        """
        Close the database.
        """
        pass

    def write(self, output):
        self.database+=output + '\n'

    def export(self):
        """
        The export process.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        total = 0
        try:
            self.openDB('w')
            self._preprocess()
            for entry in self.entries:
                output = self._exportEntry(entry)
                self.write(output)
                total += 1
            self._postprocess()
        except:
            raise
        finally:
            self.closeDB()
        return self.database

        
class BibTeXStringExporter(StringExporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to a BibTeX file.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(BibTeXStringExporter, self).__init__(path, entries)
    
    def _exportEntry(self, entry):
        """
        Export to BibTeX.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        return entry.toBibTeX(ignoreEmptyField=True)
    

class CSVStringExporter(StringExporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to a CSV formatted String.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(CSVStringExporter, self).__init__(path, entries)
    
    def _exportEntry(self, entry):
        """
        Export to CSV (tabs). The first row consists of the field names for each column.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        return entry.toCSV()
    
    def _preprocess(self):
        self.write('entrytype\t' + '\t'.join(FieldName.iterAllFieldNames()) + '\n')    # headers
    
    
class HTMLStringExporter(StringExporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to an HTML file in the default style as a String.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(HTMLStringExporter, self).__init__(path, entries)
    
    def _exportEntry(self, entry):
        """
        Export to HTML following the default style.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        txt = '<li>'
        if Preferences().bibStyle == settings.BibStyle.ACM:
            txt += entry.toHtmlACM()
        else:
            txt += entry.toHtmlDefault()
        paper = entry.getField(FieldName.Paper).getValue()
        if paper:
            txt += '<a href="%s" class="pdfLink">&nbsp;&nbsp;</a></li>' % paper
        return txt + '</li>'
    
    def _preprocess(self):
        self.write('<html><head><style>ol.ref{ list-style-type: none; counter-reset: refCounter; margin-top: 0px; padding: .495% 0 0 0;}ol.ref li:before{ content: "[" counter(refCounter, decimal) "] "; counter-increment: refCounter;}ol.ref li{ display: block; padding-top: .99%;}a.pdfLink{ background: url("http://image.chromefans.org/fileicons/format/pdf.png") center right no-repeat; padding-right: 1.48515%; margin-right: .297%; text-decoration: none;}</style></head><body><ol class="ref">\n')
    
    def _postprocess(self):
        self.write('</ol></body></html>')
    
    
class MySQLStringExporter(StringExporter):
    """
    Export a list of L{Entries<app.entry.Entry>} to a MySQL database script as String.
    """
    def __init__(self, path, entries):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type entries: list of L{app.entry.Entry}
        @param entries: The list of entries to export.
        """
        super(MySQLStringExporter, self).__init__(path, entries)
        ext = os.path.splitext(path)[1]
        self.papersPath = path
        self.authorsPath = os.path.join(os.path.dirname(path), os.path.basename(path)[:-len(ext)] + '_authors' + ext)
        self.assignmentsPath = os.path.join(os.path.dirname(path), os.path.basename(path)[:-len(ext)] + '_assignments' + ext)
        self.unique_contributors = {}
        
    def exportPapers(self):
        papers = 0
        unique_authors = 0
        try:
            self.path = self.papersPath
            self.openDB('w')
            self._preprocess()
            for entry in self.entries:
                output = self._exportEntry(entry)
                self.write(output + '\n')
                papers += 1
                for contributor in entry.getContributors():
                    contributor = str(contributor)
                    for uc in self.unique_contributors.keys():
                        if contributor.lower() == uc.lower():
                            self.unique_contributors[uc][1].append(papers)
                            break
                    else:
                        unique_authors += 1
                        self.unique_contributors[contributor] = [unique_authors,[papers]]
            self._postprocess()
        except:
            raise
        finally:
            self.closeDB()
        return papers
    
    def exportAuthors(self):
        total = 0
        try:
            self.path = self.authorsPath
            self.openDB('w')
            for c in self.unique_contributors.keys():
                self.write('''INSERT INTO Author (id, name) VALUES (%d, N'%s');\n''' % (self.unique_contributors[c][0], utils.escapeSQLCharacters(c)))
                total += 1
        except:
            raise
        finally:
            self.closeDB()
        return total
    
    def exportAssignments(self):
        total = 0
        try:
            self.path = self.assignmentsPath
            self.openDB('w')
            for c in self.unique_contributors.keys():
                for p in self.unique_contributors[c][1]:
                    self.write('''INSERT INTO PaperAuthor (paperId,authorId) VALUES (%d, %d);\n''' % (p, self.unique_contributors[c][0]))
                    total += 1
        except:
            raise
        finally:
            self.closeDB()
        return total
    
    def export(self):
        """
        The export process. It outputs 3 files:
            * one for the database tables and the INSERT statements of the papers,
            * a second one for the authors,
            * and a last one for the paper author assignments.
            
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        papers = self.exportPapers()
        authors = self.exportAuthors()
        assignments = self.exportAssignments()
        if papers > 0 and authors > 0 and assignments > 0:
            return self.database
        else:
            return 0
    
    def _exportEntry(self, entry):
        """
        Export to a MySQL database script.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        return entry.toSQL()
    
    def _preprocess(self):
        # create the database tables
        self.write('''
-- Table for Papers
DROP TABLE IF EXISTS Paper;
CREATE TABLE IF NOT EXISTS Paper (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    bibtexKey VARCHAR(100) NOT NULL UNIQUE KEY,
    title VARCHAR(200) DEFAULT NULL,
    doi VARCHAR(200) DEFAULT NULL,
    bibtex longtext NOT NULL,
    preview longtext
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Table for Authors
DROP TABLE IF EXISTS Author;
CREATE TABLE IF NOT EXISTS Author (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(200) NOT NULL UNIQUE KEY
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- Table for paper author assignments
DROP TABLE IF EXISTS PaperAuthor;
CREATE TABLE IF NOT EXISTS PaperAuthor (
    paperId INT(11) NOT NULL,
    authorId INT(11) NOT NULL,
    PRIMARY KEY (paperId, authorId),
    KEY FK_Paper (paperId),
    KEY FK_Author (authorId)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
ALTER TABLE PaperAuthor
    ADD CONSTRAINT FK_Author FOREIGN KEY (authorId) REFERENCES Author (id),
    ADD CONSTRAINT FK_Paper FOREIGN KEY (paperId) REFERENCES Paper (id);

''')   


    

class Importer(ImpEx):
    """
    Import entries L{Entries<app.entry.Entry>} from a specified format.
    """
    def __init__(self, path, manager):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type manager: list of L{app.manager.ReferenceManager}
        @param manager: The reference manager that will hold the entry list.
        """
        super(Importer, self).__init__(path)
        self.manager = manager
        
    def importFile(self):
        """
        Import from a specific file format.
        """        
        pass
        
    def add(self, entry):
        """
        Adds an entry if it is not empty.
        """        
        result = self.manager.add(entry, ignoreIfEmpty=True)
        if result is None:
            result = 0
        return int(result > 0)
    
    def remove_empty_entry(self):
        pass
    
    
class BibTeXImporter(Importer):
    """
    Import entries L{Entries<app.entry.Entry>} from a BibTeX file.
    """
    def __init__(self, path, manager):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type manager: list of L{app.manager.ReferenceManager}
        @param manager: The reference manager that will hold the entry list.
        """
        super(BibTeXImporter, self).__init__(path, manager)
    
    def importFile(self):
        """
        Import from a BibTeX file.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        self.openDB('r')
        total = 0
        line_number = 1
        try:
            line = self.database.readline()
            entry = ''
            while line:
                if line.strip().startswith('@'):
                    if entry:
                        total += self.add(entry)
                    entry = line
                elif not line.strip().startswith('%'):
                    entry += line
                line = self.database.readline()
                line_number += 1
            if entry:
                total += self.add(entry)
        except Exception as ex:
            raise Exception('%s (while reading line %d of the file)' % (str(ex), line_number)) from ex
        finally:
            self.closeDB()
        
        return total

class EndNoteImporter(Importer):
    """
    Import entries L{Entries<app.entry.Entry>} from a BibTeX file exported from EndNote using the BiBler exporter.
    """
    def __init__(self, path, manager):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type manager: list of L{app.manager.ReferenceManager}
        @param manager: The reference manager that will hold the entry list.
        """
        super(EndNoteImporter, self).__init__(path, manager)
    
    def importFile(self):
        """
        Import from a BibTeX file exported from EndNote using the BiBler exporter.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        
        self.openDB('r')
        total = 0
        line_number = 1
        try:
            line = self.database.readline()
            entry = ''
            while line:
                if line.startswith('@'):
                    if entry:
                        total += self.add(entry)
                    entry = line
                else:
                    entry += line
                line = self.database.readline()
                line_number += 1
            if entry:
                total += self.add(entry)
        except Exception as ex:
            raise Exception('%s (while reading line %d of the file)' % (str(ex), line_number)) from ex
        finally:
            self.closeDB()
        return total
        
    def add(self, entry):
        """
        Shorthand to remove code duplication
        """
        entry = self.__cleanEndNoteEntry(entry)
        result = self.manager.add(entry)
        return int(result > 0)
    
    def __cleanEndNoteEntry(self, entry):
        """
        This is a patch when data comes from EndNote.
        Sometimes, the journal of the article is in the tertiary title field.
        Sometimes, the book title of the inproceedings is in the series field.
        @type entry: L{str}
        @param entry: The BibTeX string.
        """
        #entry = entry.decode('utf-8','replace').encode('ascii','ignore')
        # Rename url field to paper
        entry = entry.replace('url = {', 'paper = {')
        
        # Articles may have the journal in the tertiary title
        if entry.startswith('article',1) or entry.startswith('Article',1) or entry.startswith('ARTICLE',1):
            i = entry.find('journal')
            if i == -1:
                j = entry.find('tertiaryTitle')
                if j != -1:
                    entry = entry[0:j] + entry[j:].replace('tertiaryTitle', 'journal', 1)
            # In which case, remove the leading JO - mark
            k = entry.find('{JO')
            if k != -1:
                entry = entry[0:k] + entry[k:].replace('{JO - ', '{', 1)
        # Inproceedings may have the booktitle in the series
        elif entry.startswith('inproceedings', 1) or entry.startswith('Inproceedings', 1) or entry.startswith('INPROCEEDINGS', 1):
            i = entry.find('booktitle')
            if i == -1:
                j = entry.find('series')
                if j != -1:
                    entry = entry[0:j] + entry[j:].replace('series', 'booktitle', 1)
        # Inbooks who have an author should not have an editor
        elif entry.startswith('inbook', 1) or entry.startswith('Inbook', 1) or entry.startswith('INBOOK', 1):
            i = entry.find('author')
            if i != -1:
                j = entry.find('editor')
                if j != -1:
                    k = entry[j:].find('}')
                    entry = entry[0:j] + entry[j+k+2:]
        return entry

    
class CSVImporter(Importer):
    """
    Import entries L{Entries<app.entry.Entry>} from a CSV (tabs) file. The first row must consist of the field names for each column.
    This operation is meant to be the inverse for the L{CSVExporter}.
    """
    def __init__(self, path, manager):
        """
        @type path: L{str}
        @param path: The path to a file.
        @type manager: list of L{app.manager.ReferenceManager}
        @param manager: The reference manager that will hold the entry list.
        """
        super(CSVImporter, self).__init__(path, manager)
    
    def importFile(self):
        """
        Import from a CSV (tabs) file.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        self.openDB('r')
        total = 0
        allFields = FieldName.getAllFieldNames()
        
        try:
            line = self.database.readline() # skip header line
            line = self.database.readline()
            line_number = 2
            while line:
                line = line.split('\t')
                if len(line) != len(allFields) + 1:
                    raise Exception('CSV file on line %d has incorrect fields.' % total)
                entry = {'entrytype': line[0]}
                for i in range(len(allFields)):
                    value = line[i + 1]
                    if value.startswith('"'):
                        value = value[1:]
                    if value.endswith('"'):
                        value = value[:-1]
                    elif value.endswith('"\n'):
                        value = value[:-2]
                    entry[allFields[i]] = value
                # Convert to BibTeX
                bibtex = '@%s{' % entry['entrytype'] # key will be auto generated
                for field in entry.keys():
                    bibtex += ',\n  %s = {%s}' % (field, entry[field])
                bibtex += '\n}'
                total += self.add(bibtex)
                line = self.database.readline()
                line_number += 1
        except Exception as ex:
            raise Exception('%s (while reading line %d of the file)' % (str(ex), line_number)) from ex
        finally:
            self.closeDB()
        return total


class BibTeXStringImporter(BibTeXImporter):
    """
    Import entries L{Entries<app.entry.Entry>} from a string.
    """
    def __init__(self, data, manager):
        """
        @type data: L{str}
        @param data: The data containing the bibtex.
        @type manager: list of L{app.manager.ReferenceManager}
        @param manager: The reference manager that will hold the entry list.
        """
        super(BibTeXImporter, self).__init__(None, manager)
        self.data = data
    
    def importFile(self):
        """
        Import from a string of multi.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        total = 0
        try:
            self.data = self.data.split('\n')
            entry = ''
            for line in self.data:
                if line.startswith('@'):
                    if entry:
                        total += self.add(entry)
                    entry = line
                else:
                    entry += line
            if entry:
                total += self.add(entry)
        except:
            raise
        
        return total

class EndNoteStringImporter(EndNoteImporter):
    """
    Import entries L{Entries<app.entry.Entry>} from a BibTeX string exported from EndNote using the BiBler exporter.
    """
    def __init__(self, data, manager):
        """
        @type data: L{str}
        @param data: The data containing the bibtex.
        @type manager: list of L{app.manager.ReferenceManager}
        @param manager: The reference manager that will hold the entry list.
        """
        super(EndNoteImporter, self).__init__(None, manager)
        self.data = data
    
    def importFile(self):
        """
        Import from a BibTeX file exported from EndNote using the BiBler exporter.
        @rtype: L{int}
        @return: The total number of entries successfully exported.
        @raise Exception: If an error occurred during the export process.
        """
        total = 0
        try:
            self.data = self.data.split('\n')
            entry = ''
            for line in self.data:
                if line.startswith('@'):
                    if entry:
                        total += self.add(entry)
                    entry = line
                else:
                    entry += line
            if entry:
                total += self.add(entry)
        except:
            raise
        
        return total