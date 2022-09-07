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
:Author: Felix Belanger Robillard

:module: The following classes are used to handle the different URLs


Pour utiliser l'ensemble de ces classes, on s'attend à ce que l'utilisateur 
cree passe par une requête http POST pour soumettre une reference BibTeX sous 
forme de string au webservice. Cette reference est ensuite ajoutee à une instance
locale de BiBler et sera ensuite traitee selon la methode appelee.

On ne peut appeler l'ensemble des methodes de l'API BiBler, les methodes pouvant être
appelees sont celles qui possèdent une classe equivalente au sein de ce module. Celles
qui ne sont pas disponibles sont celles qui necessitaient un identifiant pour
selectionner une entree en particulier, ce qui est caduque dans le format
actuel.
'''
#-*- coding: utf-8 -*-
import sys, os
import urllib.parse
import time
#abspath = os.path.dirname("Path to bibler source")
abspath = os.path.dirname("/u/relis/public_html/bibler/")
sys.path.append(abspath)
os.chdir(abspath)
import web
from bibler.utils.settings import ExportFormat, ImportFormat
#abspath = os.path.dirname("Path to webservice")
abspath = os.path.dirname("/u/relis/public_html/bibler/webservice/")
sys.path.append(abspath)
os.chdir(abspath)
from bibwrap import BiBlerWrapper

urls = (
    '/formatbibtex/(.*)', 'FormatBibTeX',
    '/addentry/(.*)', 'AddEntry',
    '/getbibtex/(.*)', 'GetBibTeX',
    '/bibtextosql/(.*)', 'BibTeXtoSQL',
    '/bibtextocsv/(.*)', 'BibTeXtoCSV',
    '/bibtextohtml/(.*)', 'BibTeXtoHTML',
    '/bibtextobibtex/(.*)', 'BibTeXtoBibTeX',
    '/previewentry/(.*)', 'PreviewEntry',
    '/validateentry/(.*)', 'ValidateEntry',
    '/createentryforrelis/(.*)', 'CreateEntryForReLiS',
    '/importbibtexstringforrelis/(.*)', 'ImportBibTeXStringForReLiS',
    '/importendnotestringforrelis/(.*)', 'ImportEndNoteStringForReLiS',
    '/generateReport/(.*)', 'GenerateReport',
    '/', 'index'
)
class index:
    def GET(self):
        return None

class FormatBibTeX:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.formatBibtex(self,data)

class AddEntry:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.addEntry(self, data)

class GetBibTeX:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.getBibTeX(self, data)

class BibTeXtoSQL:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.exportString(self, data, ExportFormat.SQL)

class BibTeXtoCSV:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.exportString(self, data, ExportFormat.CSV)

class BibTeXtoHTML:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.exportString(self, data, ExportFormat.HTML)

class BibTeXtoBibTeX:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode('utf-8'))
        return BiBlerWrapper.exportString(self, data, ExportFormat.BIBTEX)

class PreviewEntry:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.previewEntry(self, data)

class ValidateEntry:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.validateEntry(self, data)
        
# Added by Eugene Syriani on 18/10/2017 for ReLiS integration
class CreateEntryForReLiS:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.createEntryForReLiS(self, data)
        
# Added by Eugene Syriani on 1/02/2018 for ReLiS integration
class ImportBibTeXStringForReLiS:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.importStringForReLiS(self, data, ImportFormat.BIBTEX)
        
# Added by Eugene Syriani on 1/02/2018 for ReLiS integration
class ImportEndNoteStringForReLiS:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.importStringForReLiS(self, data, ImportFormat.ENDNOTE)
        
# Added by Eugene Syriani on 2/09/2022 for ReLiS integration
class GenerateReport:
    def POST(self,code):
        data = urllib.parse.unquote_plus(web.data().decode())
        return BiBlerWrapper.generateReport(self, data, ImportFormat.BIBTEX)
        
web.config.debug = True

app = web.application(urls, globals(), autoreload=False)
application = app.wsgifunc()
if __name__ == '__main__': app.run()