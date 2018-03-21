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

This module declares the oracles for the test cases
'''

# Some additional examples can be found at https://verbosus.com/bibtex-style-examples.html

class Oracle(object):
    def __init__(self, test_case, bibtex):
        self.test_case = test_case
        self.bibtex = bibtex
    
    def getBibTeX(self):
        return self.bibtex
    
    def __str__(self):
        return self.test_case

class Valid(Oracle):
    def __init__(self, test_case, bibtex, acm_html, default_html):
        super(Valid, self).__init__(test_case, bibtex)
        self.acm_html = acm_html
        self.default_html = default_html
    
    def getACM_HTML(self):
        return self.acm_html
    
    def getDefault_HTML(self):
        return self.default_html

class Invalid(Oracle):
    def __init__(self, test_case, bibtex):
        super(Invalid, self).__init__(test_case, bibtex)

class ValidArticle(Valid):
    def __init__(self, test_case, bibtex, acm_html, ieeeTrans_html):
        super(ValidArticle, self).__init__(test_case, bibtex, acm_html, ieeeTrans_html)

class InvalidArticle(Invalid):
    def __init__(self, test_case, bibtex):
        super(InvalidArticle, self).__init__(test_case, bibtex)

class ValidInProceedings(Valid):
    def __init__(self, test_case, bibtex, acm_html, ieeeTrans_html):
        super(ValidInProceedings, self).__init__(test_case, bibtex, acm_html, ieeeTrans_html)

class InvalidInProceedings(Invalid):
    def __init__(self, test_case, bibtex):
        super(InvalidInProceedings, self).__init__(test_case, bibtex)

class ValidBook(Valid):
    def __init__(self, test_case, bibtex, acm_html, ieeeTrans_html):
        super(ValidBook, self).__init__(test_case, bibtex, acm_html, ieeeTrans_html)

class InvalidBook(Invalid):
    def __init__(self, test_case, bibtex):
        super(InvalidBook, self).__init__(test_case, bibtex)

class ValidTechReport(Valid):
    def __init__(self, test_case, bibtex, acm_html, ieeeTrans_html):
        super(ValidTechReport, self).__init__(test_case, bibtex, acm_html, ieeeTrans_html)

class InvalidTechReport(Invalid):
    def __init__(self, test_case, bibtex):
        super(InvalidTechReport, self).__init__(test_case, bibtex)

class ValidPhdThesis(Valid):
    def __init__(self, test_case, bibtex, acm_html, ieeeTrans_html):
        super(ValidPhdThesis, self).__init__(test_case, bibtex, acm_html, ieeeTrans_html)

class InvalidPhdThesis(Invalid):
    def __init__(self, test_case, bibtex):
        super(InvalidPhdThesis, self).__init__(test_case, bibtex)

# Entries
empty_entry1 = Valid('empty entry', None, '', '')

empty_entry2 = Valid('empty entry', None, '', '')

invalid_entry1 = Invalid('invalid entry',
'''@{,
}''')

invalid_entry3 = Invalid('invalid entry', '@')

invalid_entry4 = Invalid('invalid entry', '@{}')

invalid_entry5 = Invalid('invalid entry', '@article{y}')

invalid_entry6 = Invalid('invalid entry', '@article{y,}')

invalid_entry7 = Invalid('invalid entry', '''@article{
x = {}
}''')

invalid_entry8 = Invalid('invalid entry', '''@article{y,
author = {}
}''')

valid_entry_spaces = Valid('valid entry with spaces and new lines around fields',
'''   
 @ARTICLE{
    Landin1966  ,
    
    
  author={{L}andin, {P}eter {J}.},

title =  {{T}he next 700 programming languages},
       journal = {{C}ommunications of {ACM}},
  year   =    {1966}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966e)</b></font></p>
<p><span style="font-variant:small-caps">Landin, P.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

invalid_entry_no_author = Invalid('invalid entry with no year',
'''@ARTICLE{Landin1966,
  title = {{A} {T}heory of {T}imed {A}utomata},
  journal = {{T}heoretical {C}omputer {S}cience {J}ournal},
  volume = {126},
  pages = {183--235}
  paper = {Alur1994.pdf}
}''')

valid_entry_von_Last_Jr_First = Valid('valid entry with author name von Last Jr First',
'''@ARTICLE{,
  author = {von Last, Jr, First},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Last1966)</b></font></p>
<p><span style="font-variant:small-caps">von Last, F. Jr.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

valid_entry_von_Last_Jr_First_parenthesis = Valid('valid entry with author name von Last Jr First with parenthesis',
'''@ARTICLE{,
  author = {von {L}ast, {J}r, {F}irst},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1967}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Last1967)</b></font></p>
<p><span style="font-variant:small-caps">von Last, F. Jr.</span> The next 700 programming languages. <i>Communications of ACM</i> (1967).</p>
<p><center></center></p>"""
, '')

valid_entry_Last_Jr_First = Valid('valid entry with author name Last Jr First',
'''@ARTICLE{,
  author = {Last, Jr, First},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1968}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Last1968)</b></font></p>
<p><span style="font-variant:small-caps">Last, F. Jr.</span> The next 700 programming languages. <i>Communications of ACM</i> (1968).</p>
<p><center></center></p>"""
, '')

valid_entry_Last_First = Valid('valid entry with author name Last First',
'''@ARTICLE{,
  author = {Last, First},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1969}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Last1969)</b></font></p>
<p><span style="font-variant:small-caps">Last, F.</span> The next 700 programming languages. <i>Communications of ACM</i> (1969).</p>
<p><center></center></p>"""
, '')

valid_entry_von_Last_First = Valid('valid entry with author name von Last First',
'''@ARTICLE{,
  author = {von Last, First},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1970}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Last1970)</b></font></p>
<p><span style="font-variant:small-caps">von Last, F.</span> The next 700 programming languages. <i>Communications of ACM</i> (1970).</p>
<p><center></center></p>"""
, '')

valid_entry_First_von_Last = Valid('valid entry with author name First von Last',
'''@ARTICLE{,
  author = {First von Last},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1971}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Last1971)</b></font></p>
<p><span style="font-variant:small-caps">von Last, F.</span> The next 700 programming languages. <i>Communications of ACM</i> (1971).</p>
<p><center></center></p>"""
, '')

valid_entry_CLXJdlVP = Valid('valid entry with author name Charles Louis Xavier Joseph de la Vallee Poussin',
'''@ARTICLE{,
  author = {Charles Louis Xavier Joseph de la Vall{\\'e}e Poussin},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(ValleePoussin1966)</b></font></p>
<p><span style="font-variant:small-caps">de la Vall&eacute;e Poussin, C. L. X. J.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

valid_entry_First_Last = Valid('valid entry with author name First Last',
'''@ARTICLE{,
  author = {First Last},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1972}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Last1972)</b></font></p>
<p><span style="font-variant:small-caps">Last, F.</span> The next 700 programming languages. <i>Communications of ACM</i> (1972).</p>
<p><center></center></p>"""
, '')

valid_entry_Last = Valid('valid entry with author name Last',
'''@ARTICLE{,
  author = {Last},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1973}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Last1973)</b></font></p>
<p><span style="font-variant:small-caps">Last.</span> The next 700 programming languages. <i>Communications of ACM</i> (1973).</p>
<p><center></center></p>"""
, '')

valid_entry_full = Valid('valid entry with all fields',
'''@ARTICLE{Landin1966,
  author = {{L}andin, {P}eter {J}.},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966},
  paper = {www.google.com},
  note = {Some note}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966e)</b></font></p>
<p><span style="font-variant:small-caps">Landin, P.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

valid_entry_no_key = Valid('valid entry without key',
'''@ARTICLE{,
  author = {{L}andin, {P}eter {J}.},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966d)</b></font></p>
<p><span style="font-variant:small-caps">Landin, P.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

valid_entry_wrong_key = Valid('valid entry with a wrong key',
'''@ARTICLE{abc,
  author = {{L}andin, {P}eter {J}.},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966)</b></font></p>
<p><span style="font-variant:small-caps">Landin, P.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

valid_entry_quote = Valid('valid entry with quotes as field delimiter',
'''@ARTICLE{Landin1966,
  author = "{L}and{\\"i}n, {P}eter {J}.",
  title = "{T}he next 700 programming languages",
  journal = "{C}ommunications of {ACM}",
  year = "1966",
  paper = "www.google.com",
  note = "Some note"
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966e)</b></font></p>
<p><span style="font-variant:small-caps">Land&iuml;n, P.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

valid_entry_bracket = Valid('valid entry brackets as field delimiter',
'''@ARTICLE{Landin1966,
  author = {{L}and{\\"i}n, {P}eter {J}.},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966},
  paper = {www.google.com},
  note = {Some note}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966e)</b></font></p>
<p><span style="font-variant:small-caps">Land&iuml;n, P.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

valid_entry_multiline = Valid('valid entry with multiple lines in fields',
'''@ARTICLE{Landin1966,
  author = {{L}andin, {P}eter {J}.},
  title = {{T}he next 700
  programming languages},
  journal = {{C}ommunications of
      {ACM}},
  year = {1966},
  paper = {www.google.com},
  note = {Some
note}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966e)</b></font></p>
<p><span style="font-variant:small-caps">Landin, P.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

# Articles
valid_article_single_author = ValidArticle('valid article with a single author',
'''@ARTICLE{Landin1966,
  author = {{L}andin, {P}eter {J}.},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966},
  number = {3},
  pages = {157--166},
  month = {mar}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966)</b></font></p>
<p><span style="font-variant:small-caps">Landin, P. J.</span> The next 700 programming languages. <i>Communications of ACM</i>, 3 (mar 1966), 157&#8211;166.</p>
<p><center></center></p>"""
, '')

valid_article_multi_author = ValidArticle('valid article with multiple author',
'''@ARTICLE{Alur1994,
  author = {{A}lur, {R}ajeev and {D}ill, {D}avid {L}.},
  title = {{A} {T}heory of {T}imed {A}utomata},
  journal = {{T}heoretical {C}omputer {S}cience {J}ournal},
  year = {1994},
  volume = {126},
  pages = {183--235}
  paper = {Alur1994.pdf}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Alur1994)</b></font></p>
<p><span style="font-variant:small-caps">Alur, R. and Dill, D. L.</span> A Theory of Timed Automata. <i>Theoretical Computer Science Journal</i> <i>126</i> (1994), 183&#8211;235.</p>
<p><center></center></p>"""
, '')

valid_article_all_fields = ValidArticle('valid article with all fields',
'''@ARTICLE{Landin1966,
  author = {{L}andin, {P}eter {J}.},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966},
  volume = {9},
  number = {3},
  pages = {157--166},
  month = {mar}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966)</b></font></p>
<p><span style="font-variant:small-caps">Landin, P. J.</span> The next 700 programming languages. <i>Communications of ACM</i> <i>9</i>, 3 (mar 1966), 157&#8211;166.</p>
<p><center></center></p>"""
, '')

valid_article_req_fields = ValidArticle('valid article with required fields only',
'''@ARTICLE{Landin1966,
  author = {{L}andin, {P}eter {J}.},
  title = {{T}he next 700 programming languages},
  journal = {{C}ommunications of {ACM}},
  year = {1966}
}''', """<p><font face="verdana"><b><i>ARTICLE</i>(Landin1966b)</b></font></p>
<p><span style="font-variant:small-caps">Landin, P. J.</span> The next 700 programming languages. <i>Communications of ACM</i> (1966).</p>
<p><center></center></p>"""
, '')

invalid_article_no_req_fields = InvalidArticle('invalid article with no required fields',
'''@ARTICLE{Alur1994,
  volume = {126},
  pages = {183--235}
  paper = {Alur1994.pdf}
}''')

invalid_article_author_year_no_req_fields = InvalidArticle('invalid article with author and year but no other required fields',
'''@ARTICLE{Landin1966,
  author = {{L}andin, {P}eter {J}.},
  year = {1966},
  volume = {9},
  number = {3},
  pages = {157--166},
  month = {mar}
}''')

# Books
valid_book_no_key = ValidBook('valid book without key',
'''@BOOK{,
  title = {{MDA} {E}xplained. {T}he {M}odel {D}riven {A}rchitecture: {P}ractice {A}nd {P}romise},
  publisher = {Addison-Wesley},
  year = {2003},
  author = {{K}leppe, {A}nneke {G}. and {W}armer, {J}os and {B}ast, {W}im}
}
''', """<p><font face="verdana"><b><i>BOOK</i>(Kleppe2003)</b></font></p>
<p><span style="font-variant:small-caps">Kleppe, A., Warmer, J., and Bast, W.</span> <i>MDA Explained. The Model Driven Architecture: Practice And Promise</i>. Addison-Wesley, 2003.</p>
<p><center></center></p>"""
, '')

valid_book_single_author = ValidBook('valid book with a single author',
'''@BOOK{Lyu1995,
  publisher = {John Wiley \\& Sons},
  title = {{S}oftware {F}ault {T}olerance},
  year = {1995},
  author = {{L}yu, {M}ichael {R}},
}''', """<p><font face="verdana"><b><i>BOOK</i>(Lyu1995)</b></font></p>
<p><span style="font-variant:small-caps">Lyu, M. R.</span> <i>Software Fault Tolerance</i>. John Wiley & Sons, 1995.</p>
<p><center></center></p>"""
, '')

valid_book_multi_author = ValidBook('valid book with multiple author',
'''@BOOK{Kleppe2003,
  title = {{MDA} {E}xplained. {T}he {M}odel {D}riven {A}rchitecture: {P}ractice {A}nd {P}romise},
  publisher = {Addison-Wesley},
  year = {2003},
  author = {{K}leppe, {A}nneke {G}. and {W}armer, {J}os and {B}ast, {W}im}
}''', """<p><font face="verdana"><b><i>BOOK</i>(Kleppe2003)</b></font></p>
<p><span style="font-variant:small-caps">Kleppe, A. G., Warmer, J., and Bast, W.</span> <i>MDA Explained. The Model Driven Architecture: Practice And Promise</i>. Addison-Wesley, 2003.</p>
<p><center></center></p>"""
, '')

valid_book_editor = ValidBook('valid book with editor',
'''@BOOK{Kleppe2003,
  title = {{MDA} {E}xplained. {T}he {M}odel {D}riven {A}rchitecture: {P}ractice {A}nd {P}romise},
  publisher = {Addison-Wesley},
  year = {2003},
  editor = {{K}leppe, {A}nneke {G}. and {W}armer, {J}os and {B}ast, {W}im}
}''', """<p><font face="verdana"><b><i>BOOK</i>(Kleppe2003a)</b></font></p>
<p><span style="font-variant:small-caps">Kleppe, A. G., Warmer, J., and Bast, W.</span> <i>MDA Explained. The Model Driven Architecture: Practice And Promise</i>. Addison-Wesley, 2003.</p>
<p><center></center></p>"""
, '')

valid_book_all_fields_author = ValidBook('valid book with all fields with authors',
'''@BOOK{Mehlhorn1984,
  title = {{G}raph {A}lgorithms and {NP}-{C}ompleteness},
  publisher = {Springer-Verlag},
  year = {1984},
  author = {{M}ehlhorn, {K}urt},
  volume = {2},
  series = {EATCS Monographs in Theoretical Computer Science},
  address = {New York, NY, USA},
  edition = {1},
  month = {jan}
}''', """<p><font face="verdana"><b><i>BOOK</i>(Mehlhorn1984)</b></font></p>
<p><span style="font-variant:small-caps">Mehlhorn, K.</span> <i>Graph Algorithms and NP-Completeness</i>, 1 ed., vol. 2 of <i>EATCS Monographs in Theoretical Computer Science</i>. Springer-Verlag, New York, NY, USA, jan 1984.</p>
<p><center></center></p>"""
, '')

valid_book_all_fields_editor = ValidBook('valid book with all fields with editors',
'''@BOOK{Mehlhorn1984,
  title = {{G}raph {A}lgorithms and {NP}-{C}ompleteness},
  publisher = {Springer-Verlag},
  year = {1984},
  editor = {{B}ast, {W}im},
  volume = {2},
  series = {EATCS Monographs in Theoretical Computer Science},
  address = {New York, NY, USA},
  edition = {1},
  month = {jan}
}''', """<p><font face="verdana"><b><i>BOOK</i>(Bast1984)</b></font></p>
<p><span style="font-variant:small-caps">Bast, W.</span> <i>Graph Algorithms and NP-Completeness</i>, 1 ed., vol. 2 of <i>EATCS Monographs in Theoretical Computer Science</i>. Springer-Verlag, New York, NY, USA, jan 1984.</p>
<p><center></center></p>"""
, '')

valid_book_req_fields = ValidBook('valid book with required fields only',
'''@BOOK{Lyu1995,
  publisher = {John Wiley \\& Sons},
  title = {{S}oftware {F}ault {T}olerance},
  year = {1995},
  author = {{L}yu, {M}ichael {R},
}''', """<p><font face="verdana"><b><i>BOOK</i>(Lyu1995)</b></font></p>
<p><span style="font-variant:small-caps">Lyu, M.</span> <i>Software Fault Tolerance</i>. John Wiley & Sons,  1995.</p>
<p><center></center></p>"""
, '')

invalid_book_no_req_fields = InvalidBook('invalid book with no required fields',
'''@BOOK{Mehlhorn1984,
  volume = {2},
  series = {EATCS Monographs in Theoretical Computer Science},
  address = {New York, NY, USA},
  edition = {1},
  month = {jan}
}''')

invalid_book_author_editor = InvalidBook('invalid book with both author and editor',
'''@BOOK{Kleppe2003,
  title = {{MDA} {E}xplained. {T}he {M}odel {D}riven {A}rchitecture: {P}ractice {A}nd {P}romise},
  publisher = {Addison-Wesley},
  year = {2003},
  author = {{K}leppe, {A}nneke {G}. and {W}armer, {J}os and {B}ast, {W}im},
  editor = {{K}leppe, {A}nneke {G}. and {W}armer, {J}os and {B}ast, {W}im}
}''')

invalid_book_author_year_no_req_fields = InvalidBook('invalid book with author and year but no other required fields',
'''@BOOK{Mehlhorn1984,
  year = {1984},
  author = {{M}ehlhorn, {K}urt},
  volume = {2},
  series = {EATCS Monographs in Theoretical Computer Science},
  address = {New York, NY, USA},
  edition = {1},
  month = {jan}
}''')

# InProceedings
valid_inproceedings_single_author = ValidInProceedings('valid inproceedings with a single author',
'''@INPROCEEDINGS{Dony1990,
  author = {{D}ony, {C}hristophe},
  title = {{E}xception {H}andling and {O}bject-{O}riented {P}rogramming: {T}owards a {S}ynthesis},
  booktitle = {{E}uropean {C}onference on {O}bject-{O}riented {P}rogramming},
  year = {1990},
  editor = {Meyrowitz, Norman},
  volume = {25},
  series = {ACM SIGPLAN Notices},
  pages = {322--330},
  publisher = {ACM Press}
}''', """<p><font face="verdana"><b><i>INPROCEEDINGS</i>(Dony1990)</b></font></p>
<p><span style="font-variant:small-caps">Dony, C.</span> Exception Handling and Object-Oriented Programming: Towards a Synthesis. In <i>European Conference on Object-Oriented Programming</i> (1990), Meyrowitz, N., Ed., vol. 25 of <i>ACM SIGPLAN Notices</i>, ACM Press, pp. 322&#8211;330.</p>
<p><center></center></p>"""
, '')

valid_inproceedings_multi_author = ValidInProceedings('valid inproceedings with multiple author',
'''@INPROCEEDINGS{Kiczales1997,
  author = {{K}iczales, {G}regor and {L}amping, {J}ohn and {M}endhekar, {A}nurag and {M}aeda, {C}hris and {V}ideira-{L}opes, {C}ristina and {L}oingtier, {J}ean-{M}arc and {I}rwin, {J}ohn},
  title = {{A}spect-{O}riented {P}rogramming},
  booktitle = {ECOOP},
  year = {1997},
  editor = {{A}skit, {M}ehmet and {M}atsuoka, {S}atoshi},
  volume = {1241},
  series = {LNCS},
  pages = {220--242},
  month = {jun},
  address = {Jyv{\\"a}skyl{\\"a}},
  publisher = {Springer-Verlag}
}''', """<p><font face="verdana"><b><i>INPROCEEDINGS</i>(Kiczales1997)</b></font></p>
<p><span style="font-variant:small-caps">Kiczales, G., Lamping, J., Mendhekar, A., Maeda, C., Videira-Lopes, C., Loingtier, J., and Irwin, J.</span> Aspect-Oriented Programming. In <i>ECOOP</i> (Jyv&auml;skyl&auml;, jun 1997), Askit, M. and Matsuoka, S., Eds., vol. 1241 of <i>LNCS</i>, Springer-Verlag, pp. 220&#8211;242.</p>
<p><center></center></p>"""
, '')

valid_inproceedings_all_fields = ValidInProceedings('valid inproceedings with all fields',
'''@INPROCEEDINGS{Kiczales1997,
  author = {{K}iczales, {G}regor and {L}amping, {J}ohn and {M}endhekar, {A}nurag and {M}aeda, {C}hris and {V}ideira-{L}opes, {C}ristina and {L}oingtier, {J}ean-{M}arc and {I}rwin, {J}ohn},
  title = {{A}spect-{O}riented {P}rogramming},
  booktitle = {ECOOP},
  year = {1997},
  editor = {{A}skit, {M}ehmet and {M}atsuoka, {S}atoshi},
  volume = {1241},
  number = {1},
  organization = {Org},
  series = {LNCS},
  pages = {220--242},
  month = {jun},
  address = {Jyv{\\"a}skyl{\\"a}},
  publisher = {Springer-Verlag}
}''', """<p><font face="verdana"><b><i>INPROCEEDINGS</i>(Kiczales1997)</b></font></p>
<p><span style="font-variant:small-caps">Kiczales, G., Lamping, J., Mendhekar, A., Maeda, C., Videira-Lopes, C., Loingtier, J., and Irwin, J.</span> Aspect-Oriented Programming. In <i>ECOOP</i> (Jyv&auml;skyl&auml;, jun 1997), Askit, M. and Matsuoka, S., Eds., vol. 1241 of <i>LNCS</i>, Org, Springer-Verlag, pp. 220&#8211;242.</p>
<p><center></center></p>"""
, '')

valid_inproceedings_req_fields = ValidInProceedings('valid inproceedings with required fields only',
'''@INPROCEEDINGS{Dony1990,
  author = {{D}ony, {C}hristophe},
  title = {{E}xception {H}andling and {O}bject-{O}riented {P}rogramming: {T}owards a {S}ynthesis},
  booktitle = {{E}uropean {C}onference on {O}bject-{O}riented {P}rogramming},
  year = {1990}
}''', """<p><font face="verdana"><b><i>INPROCEEDINGS</i>(Dony1990a)</b></font></p>
<p><span style="font-variant:small-caps">Dony, C.</span> Exception Handling and Object-Oriented Programming: Towards a Synthesis. In <i>European Conference on Object-Oriented Programming</i> (1990).</p>
<p><center></center></p>"""
, '')

invalid_inproceedings_no_req_fields = InvalidInProceedings('invalid inproceedings with no required fields',
'''@INPROCEEDINGS{Dony1990,
  editor = {Meyrowitz, Norman},
  volume = {25},
  series = {ACM SIGPLAN Notices},
  pages = {322--330},
  publisher = {ACM Press}
}''')

invalid_inproceedings_author_year_no_req_fields = InvalidInProceedings('invalid inproceedings with author and year but no other required fields',
'''@INPROCEEDINGS{Dony1990,
  author = {{D}ony, {C}hristophe},
  year = {1990},
  editor = {Meyrowitz, Norman},
  volume = {25},
  series = {ACM SIGPLAN Notices},
  pages = {322--330},
  publisher = {ACM Press}
}''')

# TechReports
valid_techreport_single_author = ValidTechReport('valid techreport with a single author',
'''@TECHREPORT{Batz2006,
  author = {{B}atz, {G}ernot {V}eit},
  title = {{A}n {O}ptimization {T}echnique for {S}ubgraph {M}atching {S}trategies},
  institution = {Universit{\\"a}t Karlsruhe, IPD Goos},
  year = {2006},
  number = {2006-7},
  month = {apr}
}''', """<p><font face="verdana"><b><i>TECHREPORT</i>(Batz2006)</b></font></p>
<p><span style="font-variant:small-caps">Batz, G. V.</span> An Optimization Technique for Subgraph Matching Strategies. 2006-7, Universit&auml;t Karlsruhe, IPD Goos, apr 2006.</p>
<p><center></center></p>"""
, '')

valid_techreport_multi_author = ValidTechReport('valid techreport with multiple author',
'''@TECHREPORT{Harel2000,
  author = {{H}arel, {D}avid and {R}umpe, {B}ernhard},
  title = {{M}odeling {L}anguages: {S}yntax, {S}emantics and {A}ll {T}hat {S}tuff, {P}art {I}: {T}he {B}asic {S}tuff},
  institution = {Weizmann Institute Of Sience},
  year = {2000},
  publisher = {Weizmann Science Press of Israel}
}''', """<p><font face="verdana"><b><i>TECHREPORT</i>(Harel2000)</b></font></p>
<p><span style="font-variant:small-caps">Harel, D. and Rumpe, B.</span> Modeling Languages: Syntax, Semantics and All That Stuff, Part I: The Basic Stuff. Weizmann Institute Of Sience, 2000.</p>
<p><center></center></p>"""
, '')

valid_techreport_all_fields = ValidTechReport('valid techreport with all fields',
'''@TECHREPORT{Syriani2009,
  author = {{S}yriani, {E}ugene and {V}angheluwe, {H}ans},
  title = {{M}atters of model transformation},
  institution = {McGill University},
  year = {2009},
  type = {Tech. rep.},
  number = {SOCS-TR-2009.2},
  address = {School of Computer Science},
  month = {mar}
}''', """<p><font face="verdana"><b><i>TECHREPORT</i>(Syriani2009)</b></font></p>
<p><span style="font-variant:small-caps">Syriani, E. and Vangheluwe, H.</span> Matters of model transformation. Tech. rep., SOCS-TR-2009.2, McGill University, School of Computer Science, mar 2009.</p>
<p><center></center></p>"""
, '')

valid_techreport_req_fields = ValidTechReport('valid techreport with required fields only',
'''@TECHREPORT{Syriani2009,
  author = {{S}yriani, {E}ugene and {V}angheluwe, {H}ans},
  title = {{M}atters of model transformation},
  institution = {McGill University},
  year = {2009}
}''', """<p><font face="verdana"><b><i>TECHREPORT</i>(Syriani2009)</b></font></p>
<p><span style="font-variant:small-caps">Syriani, E. and Vangheluwe, H.</span> Matters of model transformation. McGill University, 2009.</p>
<p><center></center></p>"""
, '')

invalid_techreport_no_req_fields = InvalidTechReport('invalid techreport with no required fields',
'''@TECHREPORT{Syriani2009,
  type = {Tech. rep.}
  number = {SOCS-TR-2009.2},
  address = {School of Computer Science},
  month = {mar}
}''')

invalid_techreport_author_year_no_req_fields = InvalidTechReport('invalid techreport with author and year but no other required fields',
'''@TECHREPORT{Syriani2009,
  author = {{S}yriani, {E}ugene and {V}angheluwe, {H}ans},
  year = {2009},
  type = {Tech. rep.}
  number = {SOCS-TR-2009.2},
  address = {School of Computer Science},
  month = {mar}
}''')

# PhdThesis
valid_phdthesis_single_author = ValidPhdThesis('valid phdthesis with a single author',
'''@PHDTHESIS{Syriani2011a,
  author = {{S}yriani, {E}ugene},
  title = {{A} {M}ulti-{P}aradigm {F}oundation for {M}odel {T}ransformation {L}anguage {E}ngineering},
  school = {McGill University},
  year = {2011},
  type = {Ph.D. Thesis},
  month = {feb}
}''', """<p><font face="verdana"><b><i>PHDTHESIS</i>(Syriani2011)</b></font></p>
<p><span style="font-variant:small-caps">Syriani, E.</span> <i>A Multi-Paradigm Foundation for Model Transformation Language Engineering</i>. Ph.D. Thesis, McGill University, feb 2011.</p>
<p><center></center></p>"""
, '')

valid_phdthesis_all_fields = ValidPhdThesis('valid phdthesis with all fields',
'''@PHDTHESIS{Syriani2011a,
  author = {{S}yriani, {E}ugene},
  title = {{A} {M}ulti-{P}aradigm {F}oundation for {M}odel {T}ransformation {L}anguage {E}ngineering},
  school = {McGill University},
  address = {Montreal},
  year = {2011},
  type = {Ph.D. Thesis},
  month = {feb}
}''', """<p><font face="verdana"><b><i>PHDTHESIS</i>(Syriani2011)</b></font></p>
<p><span style="font-variant:small-caps">Syriani, E.</span> <i>A Multi-Paradigm Foundation for Model Transformation Language Engineering</i>. Ph.D. Thesis, McGill University, Montreal, feb 2011.</p>
<p><center></center></p>"""
, '')

valid_phdthesis_req_fields = ValidPhdThesis('valid phdthesis with required fields only',
'''@PHDTHESIS{Syriani2011a,
  author = {{S}yriani, {E}ugene},
  title = {{A} {M}ulti-{P}aradigm {F}oundation for {M}odel {T}ransformation {L}anguage {E}ngineering},
  school = {McGill University},
  year = {2011}
}''', """<p><font face="verdana"><b><i>PHDTHESIS</i>(Syriani2011)</b></font></p>
<p><span style="font-variant:small-caps">Syriani, E.</span> <i>A Multi-Paradigm Foundation for Model Transformation Language Engineering</i>. McGill University 2011.</p>
<p><center></center></p>"""
, '')

invalid_phdthesis_no_req_fields = InvalidPhdThesis('invalid phdthesis with no required fields',
'''@PHDTHESIS{Syriani2011a,
  address = {Montreal},
  type = {Ph.D. Thesis},
  month = {feb}
}''')

invalid_phdthesis_author_year_no_req_fields = InvalidPhdThesis('invalid phdthesis with author and year but no other required fields',
'''@PHDTHESIS{Syriani2011a,
  author = {{S}yriani, {E}ugene},
  address = {Montreal},
  year = {2011},
  type = {Ph.D. Thesis},
  month = {feb}
}''')

# Lists
all_entry_types = [valid_article_multi_author, valid_article_single_author, valid_book_multi_author,
                   valid_book_single_author, valid_inproceedings_multi_author, valid_inproceedings_single_author,
                   valid_phdthesis_single_author, valid_techreport_multi_author, valid_techreport_single_author]

all_entries = all_entry_types + [valid_entry_full]

all_entries_all_fields = [valid_article_all_fields, valid_book_all_fields_author, valid_book_all_fields_editor,
                          valid_inproceedings_all_fields, valid_phdthesis_all_fields, valid_techreport_all_fields]

all_invalid_entry_types_no_req = [invalid_article_author_year_no_req_fields, invalid_article_no_req_fields,
                              invalid_book_author_year_no_req_fields, invalid_book_no_req_fields,
                              invalid_inproceedings_author_year_no_req_fields, invalid_inproceedings_no_req_fields,
                              invalid_phdthesis_author_year_no_req_fields, invalid_phdthesis_no_req_fields,
                              invalid_techreport_author_year_no_req_fields, invalid_techreport_no_req_fields]

all_invalid_entry_types = all_invalid_entry_types_no_req + \
                            [invalid_entry1, invalid_entry3, invalid_entry4,
                             invalid_entry5, invalid_entry6, invalid_entry7, invalid_entry8]

valid_bibtex_variants = [valid_entry_spaces, valid_entry_full, valid_entry_quote, valid_entry_multiline]

search_all_entries_all_fields = {'landin': 1, 'graph': 2, '4': 3, '19': 4, 'ne': 5, 'm': 6}

valid_authors =  [valid_entry_CLXJdlVP, valid_entry_First_Last, valid_entry_First_von_Last, valid_entry_Last_First,
                  valid_entry_Last_Jr_First, valid_entry_von_Last_First, valid_entry_von_Last_Jr_First,
                  valid_entry_von_Last_Jr_First_parenthesis, valid_entry_Last]
