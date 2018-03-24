# BiBler ![logo](https://raw.githubusercontent.com/esyriani/bibler/master/src/BiBler-1.1-sources/bibler/utils/resources/bibler.png)
BiBler is a software for managing references to scientific articles using BibTeX. Not only is it a fully functional software, the tool has been entirely modeled and synthesized in Python. It is used for educational purposes in order to understand how to generate a complete application from UML models in an agile and test-driven environment.

## Features

- Graphical user interface for Windows
![gui_screenshot](https://a.fsdn.com/con/app/proj/bibler/screenshots/screenshot.png/1)
- Python library to integrate programmatically
![console_screenshot](https://a.fsdn.com/con/app/proj/bibler/screenshots/library.png/1)
- Web service to deploy online
- Validation against BibTeX standard
- Import from BibTeX, CSV, or EndNote
- Export to CSV, HTML, or SQL

# Installation
If you want to use the graphical user interface, simply download [BiBler](BiBler-1.1/BiBler) as a zip and run [bibler.exe](BiBler-1.1/BiBler/bibler.exe).

The [user manual](BiBler-1.1/BiBler/utils/resources/manual.html) is available from the help menu of the tool.


# Distribution
This distribution contains the following files and folders:
- bibler.exe: starts the application in windows mode
- examples: contains some sample BibTeX files
- docs: the source code documentation
- external: contains files for third-party compatibility
    - BiBler Export.ens: to export an EndNote library to bibtex compatible with BiBler

BiBler software is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0)
![CC-BY-NC-SA](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)

# Source code
To compile the source code, you need the following dependencies:
- Python 3.5.2 or later
- wxPython_Phoenix 3.0.3 or later to run in GUI mode
- Sphinx 1.5.1 or later to generate the documentation
- py2exe 0.9.2.2 (requires Python 3.4 and wxPython_Phoenix for 3.4) to create the executable distribution

The source code is licensed under a [GNU GENERAL PUBLIC LICENSE 3](https://www.gnu.org/copyleft/gpl.html) ![GNU GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)

# Change log
## Version BiBler version 1.1
#### By Félix Bélanger-Robillard (9 Apr 2017)
#### Updated by Eugene Syriani (20 Feb 2018)
- BiBler is now available as a web service
- Added functionalities to integrate BiBler web service in ReLiS

## Version 1.0
#### By Eugene Syriani (15 Aug 2016)
#### Updated by Florin Oncica (15 Dec 2016)
- Migrated from Python 2.7 to Python 3.5.2
- Installation kit was done using py2exe library (the source code must be compiled with 3.4 interpreter - py2exe not yet suported by 3.5.2)
- Documentation with Sphinx:
   - docstrings changed with md.sh (unix script)
   - rst files for each class made with CreateRSTfile.bat and CreateRSTfile.py
- Added tabs for grouping fields in Editor

## Version 0.8.5 (17 Aug 2016)
- Clicking a second time on a column will sort in decreasing order
- Fixed sort issue on column #
- Ctrl+Z now only undoes in editor

## Version 0.8 (15 Aug 2016)
- Added a default HTML style (no more IEEE)
- Added an export to MySQL script
- Added option to not override bibtex key if provided
- Added function to generate bibtex key of all entries, even if overriding is disabled
- Wrote user manual

## Version 0.7 (14 Jan 2014) - First distribution of BiBler


# Web service
To deploy this webservice, you need the current directory files and the BiBler source files.
In the application.py file, you will find two commented lines for which you must replace the
paths before uncommenting.
These paths are needed for the dependencies. First, you need to put the path to the web.py
framework directory.
```python
abspath = os.path.dirname("Path to directory where web is located")
```
The second path is for the location of the BiBler source files. Beware, the webservice needs
BiBler-1.1 source files to work properly.
```python
#abspath = os.path.dirname("Path to Bibler src")
```
The webservice, Bibler source files and the web.py folder are packaged together.

Once this setup is complete, you will need to deploy on an Apache 2.4 server. The server needs
mod_wsgi, a python module, to work properly. You are encouraged to read further on their
website: https://modwsgi.readthedocs.io/en/develop

The current Python version used is Python 3.6, make sure your python path pis properly setup
with your Apache's config.
Once the webservice is up and running, you can make http Post requests to the webservice. We
encourage you tu use the php library located in the proxy folder in the current directory. 
This library encapsulates the queries to the webservice. You have to get an instance of the
BiBlerProxy class and use setURL to your webservice's deployment address. After that, you 
may use the other methods contained in BiBlerProxy to make queries by passing the data you
want to be processed. The data expected is a String containing a single BibTeX entry.
