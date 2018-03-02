'''
Created on Jan 13, 2014
@author: Eugene Syriani
@version: 0.7

This module contains utility classes and functions. 
'''

from . import utils
import re


class Encoder(type, metaclass=utils.Singleton):
    """
    The abstract class representing character encoders.
    """
    def __init__(self):
        self.TeX = TeXEncoder()
        self.Codes = []
    
    def isLowerCase(self, c):
        raise NotImplementedError()
    
    def isUpperCase(self, c):
        raise NotImplementedError()
    
    def isLetter(self, c):
        raise NotImplementedError()


class TeXEncoder(Encoder):
    """
    Utility handling TeX special characters.
    """
    def __init__(self):
        super().__init__(self)
        self.TeXCodes = ['\\\'{A}', '\\\'{a}', '\`{A}', '\`{a}', '\^{A}', '\^{a}', '\\"{A}', '\\"{a}', '\~{A}',
                     '\~{a}', '\AA', '\\aa', '\AE', '\\ae', '\c{C}', '\c{c}', '\DJ', '\dj', '\\\'{E}',
                     '\\\'{e}', '\`{E}', '\`{e}', '\^{E}', '\^{e}', '\\"{E}', '\\"{e}', '\\\'{I}', '\\\'{i}', '\`{I}',
                     '\`{i}', '\^{I}', '\^{i}', '\\"{I}', '\\"{i}', '\~{N}', '\~{n}', '\\\'{O}', '\\\'{o}', '\`{O}',
                     '\`{o}', '\^{O}', '\^{o}', '\\"{O}', '\\"{o}', '\~{O}', '\~{o}', '\O', '\o', '\ss',
                     '\\textThorn', '\\textthorn', '\\\'{U}', '\\\'{u}', '\`{U}', '\`{u}', '\^{U}', '\^{u}', '\\"{U}', '\\"{u}',
                     '\`{Y}', '\`{y}', '\\"{y}', '\copyright', '\\textregistered', '\\texttrademark', '\euro{}', '\cent', '\pounds', '`',
                     '\'', '``', '\'\'', '<<', '>>', '\emdash', '\endash', '\degree', '\pm', '\\textonequarter',
                     '\\textonehalf', '\\textthreequarters', '$\\times$', '$\div$', '$\\alpha$', '$\\beta$', '$\infty$']
        """
        TeX codes for special characters.
        """
    
    def isLowerCase(self, c):
        """
        Checks if the TeX code is a lower case letter.
        @type s: L{str}
        @param s: The code to check.
        @return: L{bool}.
        """
        try:
            re.finditer('[a-z]', c)
            return True
        except StopIteration:
            return False
    
    def isUpperCase(self, c):
        """
        Checks if the TeX code is an upper case letter.
        @type s: L{str}
        @param s: The code to check.
        @return: L{bool}.
        """
        try:
            re.finditer('[A-Z]', c)
            return True
        except StopIteration:
            return False
    
    def isLetter(self, c):
        """
        Checks if the TeX code is a letter.
        @type s: L{str}
        @param s: The code to check.
        @return: L{bool}.
        """
        try:
            re.finditer('[A-Z]', c, flag=re.IGNORECASE)
            return True
        except StopIteration:
            return False


class Converter(Encoder):
    """
    The abstract class representing entries.
    Convert TeX special characters.
    """
    def __init__(self):
        self.TeX = TeXEncoder()
        self.Codes = []

    def toTeX(self, s):
        """
        Converts encoded characters in a string into their TeX code.
        @type s: L{str}
        @param s: The string to encode in TeX.
        @return: The string encoded in TeX.
        """
        for c in self.Codes:
            s = s.replace(c, self.TeX.TeXCodes[c])
        return s
    
    def fromTeX(self, s):
        """
        Converts TeX codes in a string into their corresponding encoded characters.
        @type s: L{str}
        @param s: The string to encode.
        @return: The string encoded in Unicode.
        """
        for c in self.TeX.TeXCodes:
            s = s.replace(c, self.Codes[c])
        return s
    
    def isLowerCase(self, c):
        """
        Checks if the encoded character is a lower case letter.
        @type s: L{str}
        @param s: The character to check.
        @return: L{bool}.
        """
        return self.isTeXCodeLowerCase(self.toTeX(c))
    
    def isUnicodeUpperCase(self, c):
        """
        Checks if the encoded character is an upper case letter.
        @type s: L{str}
        @param s: The character to check.
        @return: L{bool}.
        """
        return self.isTeXCodeUpperCase(self.unicode2TeX(c))
    
    def isUnicodeLetter(self, c):
        """
        Checks if the encoded character is a letter.
        @type s: L{str}
        @param s: The character to check.
        @return: L{bool}.
        """
        return self.isTeXCodeUpperCase(self.unicode2TeX(c))
    

class TeXUnicodeConverter(TeXEncoder):
    """
    Convert between TeX and Unicode special characters.
    """
    def __init__(self):
        super().__init__(self)
        self.Codes = ['\xc1','\xe1','\xc0','\xe0','\xc2','\xe2','\xc4','\xe4','\xc3',
                      '\xe3','\xc5','\xe5','\xc6','\xe6','\xc7','\xe7','\xd0','\xf0','\xc9',
                      '\xe9','\xc8','\xe8','\xca','\xea','\xcb','\xeb','\xcd','\xed','\xcc',
                      '\xec','\xce','\xee','\xcf','\xef','\xd1','\xf1','\xd3','\xf3','\xd2',
                      '\xf2','\xd4','\xf4','\xd6','\xf6','\xd5','\xf5','\xd8','\xf8','\xdf',
                      '\xde','\xfe','\xda','\xfa','\xd9','\xf9','\xdb','\xfb','\xdc','\xfc',
                      '\xdd','\xfd','\xff','\xa9','\xae','\u2122','\u20ac','\xa2','\xa3','\u2018',
                      '\u2019','\u201c','\u201d','\xab','\xbb','\u2014','\u2013','\xb0','\xb1','\xbc',
                      '\xbd','\xbe','\xd7','\xf7','\u03b1','\u03b2','\u221e']
        self.TeXCodeUnicode = dict()
        for i in range(self.TeX.TeXCodes):
            self.TeXCodeUnicode[self.TeX.TeXCodes[i]] = self.Codes[i]


class TeXAsciiEncoder(TeXEncoder):
    def __init__(self):
        super().__init__(self)
        self.TeXCodeASCII = dict()
        """
        TeX codes and ASCII characters mapping.
        """
        for i in list(range(ord('A'), ord('Z'))) + list(range(ord('a'), ord('z'))):
            self.TeXCodeASCII["{\\c%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["{\\r%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["{\\'%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["{\\`%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["{\\\"%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["{\\^%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["{\\~%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["\\c{%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["\\r{%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["\\'{%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["\\`{%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["\\\"{%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["\\^{%s}" % chr(i)] = '%s' % chr(i)
            self.TeXCodeASCII["\\~{%s}" % chr(i)] = '%s' % chr(i)

    def toTeX(self, s):
        """
        Returns the same string.
        """
        return s
    
    def fromTeX(self, s):
        """
        Converts TeX codes in a string into their corresponding encoded characters.
        @type s: L{str}
        @param s: The string to encode.
        @return: The string encoded in ASCII.
        """
        for c in self.TeXCode2ASCII.keys():
            s = s.replace(c, self.TeXCode2ASCII[c])
        return s

    def teX2Ascii(self, s):
        """
        Converts TeX codes in a string into their ASCII characters.
        @type s: L{str}
        @param s: The string to convert.
        @return: The string in ASCII.
        """

class TeXHTMLEncoder(TeXEncoder):
    def __init__(self):
        super().__init__(self)
        self.TeXCodesHTML = dict()
        """
        TeX codes and HTML characters mapping.
        """
        self.TeXCodesHTML["{\\ss}"] = '&szlig;'
        self.TeXCodesHTML["\\ss"] = '&szlig;'
        self.TeXCodesHTML["\\&"] = '&'
        self.TeXCodesHTML["{\\&}"] = '&'
        self.TeXCodesHTML["\\o"] = '&oslash;'
        self.TeXCodesHTML["\\O"] = '&Oslash;'
        for i in list(range(ord('A'), ord('Z'))) + list(range(ord('a'), ord('z'))):
            self.TeXCodesHTML["{\\c%s}" % chr(i)] = '&%scedil;' % chr(i)
            self.TeXCodesHTML["{\\r%s}" % chr(i)] = '&%sring;' % chr(i)
            self.TeXCodesHTML["{\\'%s}" % chr(i)] = '&%sacute;' % chr(i)
            self.TeXCodesHTML["{\\`%s}" % chr(i)] = '&%sgrave;' % chr(i)
            self.TeXCodesHTML["{\\\"%s}" % chr(i)] = '&%suml;' % chr(i)
            self.TeXCodesHTML["{\\^%s}" % chr(i)] = '&%scirc;' % chr(i)
            self.TeXCodesHTML["{\\~%s}" % chr(i)] = '&%stilde;' % chr(i)
            self.TeXCodesHTML["{\\%s}" % chr(i)] = '&%sslash;' % chr(i)
            self.TeXCodesHTML["\\c{%s}" % chr(i)] = '&%scedil;' % chr(i)
            self.TeXCodesHTML["\\r{%s}" % chr(i)] = '&%sring;' % chr(i)
            self.TeXCodesHTML["\\'{%s}" % chr(i)] = '&%sacute;' % chr(i)
            self.TeXCodesHTML["\\`{%s}" % chr(i)] = '&%sgrave;' % chr(i)
            self.TeXCodesHTML["\\\"{%s}" % chr(i)] = '&%suml;' % chr(i)
            self.TeXCodesHTML["\\^{%s}" % chr(i)] = '&%scirc;' % chr(i)
            self.TeXCodesHTML["\\~{%s}" % chr(i)] = '&%stilde;' % chr(i)

    def teX2Ascii(self, s):
        """
        Converts TeX codes in a string into their ASCII characters.
        @type s: L{str}
        @param s: The string to convert.
        @return: The string in ASCII.
        """
        for c in self.TeXCode2ASCII.keys():
            s = s.replace(c, self.TeXCode2ASCII[c])