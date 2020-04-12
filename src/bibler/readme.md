# Source code

The source code is licensed under a [GNU GENERAL PUBLIC LICENSE 3](https://www.gnu.org/copyleft/gpl.html) ![GNU GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)

## Dependencies
To compile the source code, you need the following dependencies:
- [Python](https://www.python.org/) 3.7 or later
- [wxPython](https://wxpython.org/) 4.0 or later to run in GUI mode
- [Sphinx](https://www.sphinx-doc.org/) 1.5 or later to generate the documentation
- [PyInstaller](https://www.pyinstaller.org/) 3.6 or later create the executable distribution

# Change log

## Version 1.5
#### 12 Apr 2020
- Ignores lines starting with '%' in a BibTeX file
- Open/Import errors now give the line number where the error happened
- Removed multiple error popups when an error opening a file occurs


## Version 1.4
#### 12 Apr 2020 (updated)
- Minor code refactorings: unit tests are working again
- Now using PyInstaller to create a build distribution

## Version 1.3
#### 16 Jan 2019
- Minor fixes of HTML output

## Version 1.2
#### 3 Apr 2018
- Bug fixes on the GUI and on integration with ReLiS

## Version 1.1
#### By Felix Belanger-Robillard (9 Apr 2017)
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

## Version 0.7 (14 Jan 2014)
- First distribution of BiBler
