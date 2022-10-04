# BiBler ![logo](https://raw.githubusercontent.com/esyriani/bibler/master/src/bibler/utils/resources/bibler.png)
BiBler is a simple software for managing references of scientific articles using BibTeX.
It follows rigorously the validation rules of BibTeX as stated [in the standard](http://www.openoffice.org/bibliographic/bibtex-defs.html).

BiBler is a open-source and cross-platform compatible. 
Not only is it a fully functional software, the tool has been entirely modeled and synthesized in Python.
It is used for educational purposes in order to understand how to generate a complete application from UML models in an agile and test-driven environment.

You can interact with BiBler via its GUI, its API, or as a web service.

![gui_screenshot](https://a.fsdn.com/con/app/proj/bibler/screenshots/screenshot.png/1)
<!--![console_screenshot](https://a.fsdn.com/con/app/proj/bibler/screenshots/library.png/1)-->

## Features
- Graphical user interface to manage a BibTeX bibliography
- Add, updated, delete references
- Search through the library
- Saves as simple BibTeX file
- Validation against BibTeX standard
- Import from BibTeX, CSV, or EndNote
- Export to CSV, HTML, or SQL
- Python module and API to integrate programmatically
- Web service to deploy online as a service

## Installation and usage

### With the graphical user interface

The latest version is pre-built and available under the [build/bibler](build/bibler) directory.
You can also download the latest zip file from the [build](build) directory.
Simply run [bibler.exe](build/bibler/bibler.exe).

The [user manual](src/bibler/utils/resources/manual.md) is available from the help menu of the tool.


### Programming with the API

To run BiBler from Python code, the main file is [`src/bibler/__init__.py`](src/bibler/__init__.py).
You can use BiBler programmatically like so:
```python
from bibler import bibler 
bibler.start()      # starts the BiBler
bibler.addEntry('') # adds an empty entry
bibler.exit()       # closes BiBler
```

Go to [src/bibler](src/bibler) for more information.

### Web service

1. Using Docker
   1. `docker build src/bibler -t bibler:latest`
   2. `docker run -p <port-on-your-system>:8000 bibler:latest`

   > To run Production Server use this command

   3. `docker run -e ENV=prod -p <port-on-your-system>:80 bibler:latest`
   > Also, if you want to use our prebuilt docker image skip building on Step 1. and replace image name `bibler:latest` with `relis/bibler:latest` in the commands.


2. Using local installation
   1. Install the Dependencies with this command `pip install -r src/bibler/requirements-web.txt`
   2. Run command `python src/bibler/web.py`
   > To Run Production Server set Environment Variable ENV=prod or use command `ENV=prod python src/bibler/web.py`


## Distribution

This distribution contains the following files and folders:
- `src/__init__.py` and `bibler.exe`: starts the application in windowed mode
- `examples/`: contains some sample BibTeX files and references
- `docs/`: contains the documentation of the source code
- `external/`: contains files for third-party compatibility
    - `BiBler Export.ens`: is an export style for EndNote to export a library to a BibTeX file compatible with BiBler

BiBler software is licensed under a [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-nc-sa/4.0)

![CC-BY-NC-SA](https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png)
