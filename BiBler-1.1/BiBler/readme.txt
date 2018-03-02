BiBler version 1.0
By Eugene Syriani 15 Aug 2016
Updated by Florin Oncica 15 Dec 2016
==============================================================

This distribution contains the following files and folders:
- bibler.exe: starts the application in windows mode
- examples: contains some sample bibtex files
- docs: the source code documentation
- win_dll: Windows VisualStudio 12.0 graphic dll's.
- external: contains files for third-party compatibility
    - BiBler Export.ens: to export an EndNote library to bibtex compatible with BiBler

To compile the source code, you need the following dependencies:
- Python 3.5.2 or later
- wxPython_Phoenix 3.0.3 or later to run in GUI mode
- Sphinx 1.5.1 or later to generate the documentation
- py2exe 0.9.2.2 (requires Python 3.4 and wxPython_Phoenix for 3.4) to create the executable distribution

==============================================================

*** Version 1.0 (15 Dec 2016)
- Migrated from Python 2.7 to Python 3.5.2
- Installation kit was done using py2exe library (the source code must be compiled with 3.4 interpreter - py2exe not yet suported by 3.5.2).
- Documentation with Sphinx:
	- docstrings changed with md.sh (unix script).
	- rst files for each class made with CreateRSTfile.bat and CreateRSTfile.py
- Added tabs for grouping fields in Editor.

*** Version 0.8.5 (17 Aug 2016)
- Clicking a second time on a column will sort in decreasing order
- Fixed sort issue on column #
- Ctrl+Z now only undoes in editor

*** Version 0.8 (15 Aug 2016)
- Added a default HTML style (no more IEEE)
- Added an export to MySQL script
- Added option to not override bibtex key if provided
- Added function to generate bibtex key of all entries, even if overriding is disabled
- Wrote user manual

*** Version 0.7 (14 Jan 2014)
- First distribution of BiBler