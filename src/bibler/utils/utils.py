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
Created on Jan 13, 2014
@author: Eugene Syriani
@version: 0.7

This module contains utility classes and functions. 
'''

class Singleton(type):
    """
    Meta-class to turn a class into a singleton.
    """
    def __init__(self, name, bases, _dict):
        super(Singleton, self).__init__(name, bases, _dict)
        self.instance = None
    
    def __call__(self, *args, **kw):
        # called whenever a function (or class) is called
        if self.instance is None:
            self.instance = super(Singleton, self).__call__(*args, **kw)
        return self.instance

class Utils(object, metaclass=Singleton):
    """
    Utility class offering helpful functions.
    """
    
    def __init__(self):
        self.funnychars_to_latex = {
            '\xc1':    '\\\'{A}',
            '\xe1':    '\\\'{a}',
            '\xc0':    '\`{A}',
            '\xe0':    '\`{a}',
            '\xc2':    '\^{A}',
            '\xe2':    '\^{a}',
            '\xc4':    '\\"{A}',
            '\xe4':    '\\"{a}',
            '\xc3':    '\~{A}',
            '\xe3':    '\~{a}',
            '\xc5':    '\AA',
            '\xe5':    '\\aa',
            '\xc6':    '\AE',
            '\xe6':    '\\ae',
            '\xc7':    '\c{C}',
            '\xe7':    '\c{c}',
            '\xd0':    '\DJ',
            '\xf0':    '\dj',
            '\xc9':    '\\\'{E}',
            '\xe9':    '\\\'{e}',
            '\xc8':    '\`{E}',
            '\xe8':    '\`{e}',
            '\xca':    '\^{E}',
            '\xea':    '\^{e}',
            '\xcb':    '\\"{E}',
            '\xeb':    '\\"{e}',
            '\xcd':    '\\\'{I}',
            '\xed':    '\\\'{i}',
            '\xcc':    '\`{I}',
            '\xec':    '\`{i}',
            '\xce':    '\^{I}',
            '\xee':    '\^{i}',
            '\xcf':    '\\"{I}',
            '\xef':    '\\"{i}',
            '\xd1':    '\~{N}',
            '\xf1':    '\~{n}',
            '\xd3':    '\\\'{O}',
            '\xf3':    '\\\'{o}',
            '\xd2':    '\`{O}',
            '\xf2':    '\`{o}',
            '\xd4':    '\^{O}',
            '\xf4':    '\^{o}',
            '\xd6':    '\\"{O}',
            '\xf6':    '\\"{o}',
            '\xd5':    '\~{O}',
            '\xf5':    '\~{o}',
            '\xd8':    '{\O}',
            '\xf8':    '{\o}',
            '\xdf':    '{\ss}',
            '\xde':    '\\textThorn',
            '\xfe':    '\\textthorn',
            '\xda':    '\\\'{U}',
            '\xfa':    '\\\'{u}',
            '\xd9':    '\`{U}',
            '\xf9':    '\`{u}',
            '\xdb':    '\^{U}',
            '\xfb':    '\^{u}',
            '\xdc':    '\\"{U}',
            '\xfc':    '\\"{u}',
            '\xdd':    '\`{Y}',
            '\xfd':    '\`{y}',
            '\xff':    '\\"{y}',
            '\xa9':    '\copyright',
            '\xae':    '\\textregistered',
            '\u2122':  '\\texttrademark',
            '\u20ac':  '{\euro}',
            '\xa2':    '{\cent}',
            '\xa3':    '{\pounds}',
            '\u2018':  '`',
            '\u2019':  '\'',
            '\u201c':  '``',
            '\u201d':  '\'\'',
            '\xab':    '<<',
            '\xbb':    '>>',
            '\u2014':  '\emdash',
            '\u2013':  '\endash',
            '\xb0':    '\degree',
            '\xb1':    '\pm',
            '\xbc':    '\\textonequarter',
            '\xbd':    '\\textonehalf',
            '\xbe':    '\\textthreequarters',
            '\xd7':    '$\\times$',
            '\xf7':    '$\div$',
            '\u03b1':  '$\\alpha$',
            '\u03b2':  '$\\beta$',
            '\u221e':  '$\infty$'
        }
    
        self.tex_chars = ["{\\c%s}","{\\r%s}","{\\'%s}","{\\`%s}","{\\\"%s}","{\\^%s}","{\\~%s}",
                          "\\c{%s}","\\r{%s}","\\'{%s}","\\`{%s}","\\\"{%s}","\\^{%s}","\\~{%s}"]
        self.html_chars = ['&%scedil;','&%sring;','&%sacute;','&%sgrave;','&%suml;','&%scirc;',
                           '&%stilde;'] * 2  # corresponds to tex_chars
        self.tex_to_simple = {}
        self.tex_to_simple["{\\ss}"] = 'ss'
        self.tex_to_simple["\\o"] = 'o'
        for i in self.alphabet_ordinals():
            for c in self.tex_chars:
                self.tex_to_simple[c % chr(i)] = '%s' % chr(i)
        
        self.tex_to_html = {}
        self.tex_to_html["{\\ss}"] = '&szlig;'
        self.tex_to_html["\\ss"] = '&szlig;'
        self.tex_to_html["\\&"] = '&'
        self.tex_to_html["{\\&}"] = '&'
        self.tex_to_html["\\o"] = '&oslash;'
        self.tex_to_html["\\O"] = '&Oslash;'
        self.tex_to_html['--'] = '&#8211;'
        for i in self.alphabet_ordinals():
            for c in range(len(self.tex_chars)):
                self.tex_to_html[self.tex_chars[c] % chr(i)] = self.html_chars[c] % chr(i)
    
    def alphabet_ordinals(self):
        """
        Generator producing the ordinal of every character in the alphabet [A-Za-z].
        """
        for A in range(ord('A'), ord('Z') + 1): yield A
        for a in range(ord('a'), ord('z') + 1): yield a
    
    def escapeSQLCharacters(self, s):
        """
        Returns a copy of a string by escaping SQL strings.
        :param s: A string.
        :type s: str
        :returns: str -- The converted string.
        """
        return s.replace("'","''").replace("\\","\\\\")
    
    def unicode2Tex(self, s):
        """
        Returns a copy of a string with all unicode characters replaced by their TeX equivalent.
        :param s: A string.
        :type s: str
        :returns: str -- The converted string.
        """
        return s.translate(str.maketrans(self.funnychars_to_latex))
    
    def tex2simple(self, s):
        """
        Returns a copy of a string with all TeX symbols simplified.
        :param s: A string.
        :type s: str
        :returns: str -- The converted string.
        """
        for tex in self.tex_to_simple:
            s = s.replace(tex, self.tex_to_simple[tex])
        s.replace('^','').replace('$','').replace('_','')
        return s
    
    def tex2html(self, s):
        """
        Returns a copy of a string with all TeX symbols simplified.
        :param s: A string.
        :type s: str
        :returns: str -- The converted string.
        """
        for tex in self.tex_to_html:
            s = s.replace(tex, self.tex_to_html[tex])
        return s
    
    def sort_dict_by_key(self, d, ascending=True):
        """
        Returns a copy of the dictionary sorted by ascending order of its keys.
        :param d: A dictionary.
        :type d: dict
        :param ascending: If True, ascending order, else descending order
        :type ascending: int
        :returns: list -- The list of the items in sorted order.
        """
        return list(sorted(d, reverse=not ascending))
    
    def sort_dict_by_value(self, d, ascending=True):
        """
        Returns a copy of the dictionary sorted by ascending order of its values.
        :param d: A dictionary.
        :type d: dict
        :param ascending: If True, ascending order, else descending order
        :type ascending: int
        :returns: list -- The list of the items in sorted order.
        """
        return list(sorted(d.items(), key=lambda item: item[1], reverse=not ascending))