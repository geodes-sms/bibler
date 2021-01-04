# Source code

The source code is licensed under a [GNU GENERAL PUBLIC LICENSE 3](https://www.gnu.org/copyleft/gpl.html) ![GNU GPL v3](https://img.shields.io/badge/license-GPLv3-blue.svg)


## Dependencies
To compile the source code, you need the following dependencies:
- [Python](https://www.python.org/) 3.7 or later
- [wxPython](https://wxpython.org/) 4.0 or later to run in GUI mode
- [Sphinx](https://www.sphinx-doc.org/) 3.0.1 or later to generate the documentation
- [PyInstaller](https://www.pyinstaller.org/) 3.6 or later to create the executable distribution

## Usage

#### Running BiBler

To run the application with the GUI, simply run the `bibler` module from the command line like so.
It requires wxPython.
```console
python src/bibler/__init__.py
```

To run in head-less mode, simply import the `bibler` module and use the `bibler` object.
The main file is [`__init__.py`](__init__.py).
The available functions are listed in the [documentation](../../docs/index.html) of the `IApplication` interface in the `App_Interface` module.
```python
from bibler import bibler
bibler.start()      # starts the BiBler
bibler.addEntry('') # adds an empty entry
bibler.exit()       # closes BiBler
```

You can set the options of BiBler via the `Preferences` object.
```python
from bibler import *
Preferences.overrideKeyGeneration = True	# Generates a key for entries even if one is already provided
Preferences.bibStyle = BibStyle.DEFAULT		# Sets the bibliography style
```

#### Testing BiBler

All unit tests are available in the [`testApp`](testApp) module.
It requires PyUnit.
To run the tests, simply run:
```console
python testApp.py
```

To test open and import, you can use the sample BibTeX files in the [examples](../../examples) folder.

#### Building a distribution

BiBler is built and distributed as a executable package.
All the releases are available in the [build](../../build) folder.
To create a new release, open the [build.py](build.py) module and set `VERSION` to the version number.
Then, simply run:
```console
python build.py
```
It requires PyInstaller.
This will override the latest build in the [build/bibler](../../build/bibler) folder.
Finally, create a zip file of the build and deploy it as a new release.

#### Generating the source code documentation

It requires Sphinx.

TODO

# Change log

## Version 1.4.3 (dev)
#### 4 Jan 2021
- Small bug fixes

## Version 1.4.2 (dev)
#### 27 May 2020
- Properly handles curly brackets in year and doi
- Improved validation result to show more information
- Added tests for open, import and validate all
- Added more example files
- Bug fix for HTML characters

## Version 1.4.1
#### 12 Apr 2020
- Ignores lines starting with '%' in a BibTeX file
- Open/Import errors now give the line number where the error happened
- Removed multiple error popups when an error opening a file occurs
- Removed comment field, use the standard annote field instead. Moved abstract field to additional
- Added endnote example for testing
- Updated user manual
- Minor code refactoring


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
