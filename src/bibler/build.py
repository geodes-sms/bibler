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

import os
import datetime
import PyInstaller.__main__

VERSION = '1.4.2'
DATE = datetime.date.today().strftime('%d %b %Y')

# First update the version and the date
####################

# In the __init__.py file
init = open('__init__.py','r+')
init_lines = init.readlines()
init.seek(0)
for line in init_lines:
    if line.startswith('.. versionadded:: '):
        line = '.. versionadded:: %s\n' % VERSION
    if line.startswith('__version__ = '):
        line = '__version__ = "%s"\n' % VERSION
    elif line.startswith('Created on '):
        line = 'Created on %s\n' % DATE
    init.write(line)
init.close()

# In the about.html file
about = open(os.path.join('utils', 'resources', 'about.html'),'r+')
about_lines = about.readlines()
about.seek(0)
for line in about_lines:
    if line.find('Version') >= 0:
        line = ' ' * 16
        line += '<font size="2">Version: %s -- %s</font><br />\n' % (VERSION, DATE)
    about.write(line)
about.close()

# Then build and package the code
####################

PyInstaller.__main__.run([
    '--name=%s' % 'bibler',
    '--distpath=%s' % '../../build',
    '--noconfirm',
    '--windowed',
    '--clean',
    #'--debug=all', # remove --windowed if debug is enabled
    '--add-binary=%s%s%s' % (os.path.join('utils', 'resources', '*.ico'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-binary=%s%s%s' % (os.path.join('utils', 'resources', '*.jpg'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-binary=%s%s%s' % (os.path.join('utils', 'resources', '*.png'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-data=%s%s%s' % (os.path.join('utils', 'resources', '*.html'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-data=%s%s%s' % (os.path.join('utils', 'resources', '*.md'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-data=%s%s%s' % (os.path.join('utils', 'resources', '*.pdf'), os.pathsep, os.path.join('utils', 'resources')),
    '--add-data=%s%s%s' % (os.path.join('external'), os.pathsep, os.path.join('external')),
    '--add-data=%s%s%s' % (os.path.join('..','..','examples'), os.pathsep, os.path.join('examples')),
    '--icon=%s' % os.path.join('utils', 'resources', 'bibler.ico'),
    os.path.join('__init__.py')
])
