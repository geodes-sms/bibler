# -*- coding: utf-8 -*-
"""
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
"""
"""
:Author: Gauransh Kumar

:module: FastAPI version of Bbibler Web Service

"""

import json
import os
import sys
import tempfile
import time
import urllib.parse

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

from app.user_interface import BiBlerApp
from gui.app_interface import EntryListColumn
from utils.settings import ExportFormat, ImportFormat


def getBiblerApp():
    """
    Returns a BiBlerApp instance
    """
    biblerapp = BiBlerApp()
    biblerapp.preferences.overrideKeyGeneration = True
    return biblerapp


def entryToJSON(entry, biblerapp):
    """
    Convert an entry into JSON.
    :param Entry entry: The entry.
    :return: The result as a dictionary.
    :rtype: dict
    """
    json = {}
    json["result_code"] = int(entry[EntryListColumn.Valid])
    json["result_msg"] = entry[EntryListColumn.Message]
    json["entry"] = entry
    json["preview"] = biblerapp.previewEntry(entry[EntryListColumn.Id])
    json["bibtex"] = biblerapp.getBibTeX(entry[EntryListColumn.Id])
    authors = []
    for c in biblerapp.getContributors(entry[EntryListColumn.Id]):
        a = {}
        a["first_name"] = c.first_name
        a["last_name"] = c.last_name
        a["preposition"] = c.preposition
        a["suffix"] = c.suffix
        authors.append(a)
    json["authors"] = authors
    json["venue_full"] = biblerapp.getVenue(entry[EntryListColumn.Id])
    return json


# Pydantic models
class Data(BaseModel):
    bibtex: str


# Initialize FastAPI app
app = FastAPI()


@app.get("/")
def read_root():
    """Project Root return null"""
    return None


@app.post("/formatbibtex/")
async def formatbibtex(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    return biblerapp.formatBibTeX(self, bibtex)


@app.post("/addentry/")
async def addentry(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    biblerapp.addEntry(bibtex)
    return biblerapp.iterAllEntries()


@app.post("/getbibtex/")
async def getbibtex(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    b = biblerapp.addEntry(bibtex)
    return biblerapp.getBibTeX(b)


@app.post("/bibtextosql/")
async def bibtextosql(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    biblerapp.addEntry(bibtex)
    return biblerapp.exportString(ExportFormat.SQL)


@app.post("/bibtextocsv/")
async def bibtextocsv(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    biblerapp.addEntry(bibtex)
    return biblerapp.exportString(ExportFormat.CSV)


@app.post("/bibtextohtml/")
async def bibtextohtml(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    biblerapp.addEntry(bibtex)
    return biblerapp.exportString(ExportFormat.HTML)


@app.post("/bibtextobibtex/")
async def bibtextobibtex(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    biblerapp.addEntry(bibtex)
    return biblerapp.exportString(ExportFormat.BIBTEX)


@app.post("/previewentry/")
async def previewentry(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    entryid = biblerapp.addEntry(bibtex)
    return biblerapp.previewEntry(entryid)


@app.post("/validateentry/")
async def validateentry(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    entryId = biblerapp.addEntry(bibtex)
    return int(biblerapp.validateEntry(entryId).isValid())


@app.post("/createentryforrelis/")
async def createentryforrelis(data: Data):
    json_res = {}
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    entryId = biblerapp.addEntry(bibtex)
    entry = biblerapp.getEntry(entryId)
    json_res = json.dumps(entry)
    return jsonable_encoder(obj=json_res)


@app.post("/importbibtexstringforrelis/")
async def importbibtexstringforrelis(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    json_res = {"error": "", "total": 0}
    try:
        total = biblerapp.importString(bibtex, ImportFormat.BIBTEX)
        json_res["total"] = total
        i = 1
        papers = []
        for entry in biblerapp.iterAllEntries():
            paper = entryToJSON(entry, biblerapp)
            papers.append(paper)
            i += 1
        json_res["papers"] = papers
    except Exception as e:
        json_res["error"] = str(e)
    return jsonable_encoder(obj=json_res)


@app.post("/importendnotestringforrelis/")
async def importendnotestringforrelis(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    json_res = {"error": "", "total": 0}
    try:
        total = biblerapp.importString(bibtex, ImportFormat.ENDNOTE)
        json_res["total"] = total
        i = 1
        papers = []
        for entry in biblerapp.iterAllEntries():
            paper = entryToJSON(entry, biblerapp)
            papers.append(paper)
            i += 1
        json_res["papers"] = papers
    except Exception as e:
        json_res["error"] = str(e)
    # using jsonable_encoder to convert dict object to standard json
    return jsonable_encoder(obj=json_res)


@app.post("/generateReport/")
async def generateReport(data: Data):
    bibtex = urllib.parse.unquote_plus(data.bibtex)
    biblerapp = getBiblerApp()
    biblerapp.importString(bibtex, ImportFormat.BIBTEX)
    report = biblerapp.generateReport("", False)
    json_res = json.dumps(report)
    return jsonable_encoder(obj=json_res)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=80, log_level="info")
