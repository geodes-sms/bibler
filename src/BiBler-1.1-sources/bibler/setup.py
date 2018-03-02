"""
This is the script that creates a distribution of BiBler as a Windows executable.
Follow these instructions when packaging a new distribution:
. Install py2exe from http://www.py2exe.org/ (only needed once)
. Copy __init__.py to a new file bibler.py
. Run 'python setup.py py2exe'
. Delete build/
. Copy utils/resources/ to dist/utils/resources/
. Copy readme.txt to dist/readme.txt
. Rename dist/ to BiBler/
. Create a zip of BiBler/ and distribute it
"""


from distutils.core import setup
import py2exe
from glob import glob
import sys
import re

sys.path.append("dist\\Microsoft.VC140.CRT")    # make sure this is where you have the MSVCR90.dll file
data_files = [("Microsoft.VC140.CRT", glob(r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\redist\x86\Microsoft.VC140.CRT\*.*'))]

VERSIONFILE = "__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
version = "0.0.0"
if mo:
    version = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setup(
    version = version,
    name = "BiBler",
    data_files = data_files,
    windows = [ {
        "script": "bibler.py",
        "icon_resources": [(1, "utils\\resources\\bibler.ico")]
    }]
)
