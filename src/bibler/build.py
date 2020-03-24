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
This is the script that creates a distribution of BiBler as an executable.
"""

import os.path
import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=%s' % 'bibler',
    '--windowed',
    #'--debug=all', # remove --windowed if debug is enabled
    '--add-binary=%s%s%s' % (os.path.join('utils', 'resources', '*.ico'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-binary=%s%s%s' % (os.path.join('utils', 'resources', '*.jpg'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-binary=%s%s%s' % (os.path.join('utils', 'resources', '*.png'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-data=%s%s%s' % (os.path.join('utils', 'resources', '*.html'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-data=%s%s%s' % (os.path.join('utils', 'resources', '*.md'), os.pathsep, os.path.join('utils', 'resources')),
    '--icon=%s' % os.path.join('utils', 'resources', 'bibler.ico'),
    '__init__.py'
])