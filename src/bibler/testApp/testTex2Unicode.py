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
This module tests the LaTeX-to-Unicode conversion fix introduced for
ReLiS issue #23: "Importing bibtex strips latex commands for accented
characters".

Before the fix, BiBler returned BibTeX entries with raw LaTeX commands
(e.g., "Pr{\\'e}server") in the JSON sent to ReLiS, which then displayed
them as broken strings ("Preserver"). The fix introduces Utils.tex2unicode()
and applies it to the relevant text fields in web.entryToJSON().
'''

import unittest

from utils.utils import Utils


class TestTex2Unicode(unittest.TestCase):
    """
    Unit tests for the new Utils.tex2unicode() function.

    These tests verify that LaTeX-encoded accented characters in BibTeX
    fields are correctly decoded into their Unicode equivalents, which is
    what consumers of the BiBler web service (such as ReLiS) expect.

    Each test follows the Arrange-Act-Assert pattern and documents the
    LaTeX construct it covers.
    """

    def setUp(self):
        """Create a fresh Utils instance for each test."""
        self.utils = Utils()


    # 1.  Acute accent: \'e -> é
    def test_acute_accent_lowercase(self):
        """Acute accent on a lowercase letter is decoded to é."""
        self.assertEqual(
            self.utils.tex2unicode("Caf{\\'e}"),
            "Café",
        )

    def test_acute_accent_uppercase(self):
        """Acute accent on an uppercase letter is decoded to É."""
        self.assertEqual(
            self.utils.tex2unicode("{\\'E}cole"),
            "École",
        )

    # 2. Grave accent: \`e -> è
    def test_grave_accent_lowercase(self):
        """Grave accent on a lowercase letter is decoded to è."""
        self.assertEqual(
            self.utils.tex2unicode("p{\\`e}re"),
            "père",
        )

    #  3. Circumflex accent: \^o -> ô
    def test_circumflex_accent(self):
        """Circumflex accent is decoded properly."""
        self.assertEqual(
            self.utils.tex2unicode("C{\\^o}te d'Azur"),
            "Côte d'Azur",
        )

    #  4. Diaeresis / umlaut: \"u -> ü
    def test_umlaut_accent(self):
        """Diaeresis (umlaut) is decoded properly."""
        self.assertEqual(
            self.utils.tex2unicode('M{\\"u}ller'),
            "Müller",
        )

    #  5. Tilde: \~n -> ñ
    def test_tilde_accent(self):
        """Tilde is decoded properly."""
        self.assertEqual(
            self.utils.tex2unicode("Ni{\\~n}o"),
            "Niño",
        )

    #  6. Cedilla: \c{c} -> ç
    def test_cedilla_accent(self):
        """Cedilla is decoded properly."""
        self.assertEqual(
            self.utils.tex2unicode("Fran{\\c{c}}ois"),
            "François",
        )

    #  7. Special letters (no accent argument)
    def test_ss_ligature(self):
        """The German sharp s ligature (\\ss) is decoded to ß."""
        self.assertEqual(
            self.utils.tex2unicode("Stra{\\ss}e"),
            "Straße",
        )

    def test_o_slash(self):
        """The Scandinavian \\o is decoded to ø."""
        self.assertEqual(
            self.utils.tex2unicode("S{\\o}ren"),
            "Søren",
        )

    #  8. Real-world BibTeX entry from the bug report
    def test_full_title_from_issue_23(self):
        """
        Full title from the bug report (issue #23) is decoded correctly.
        """
        latex = (
            "Pr{\\'e}server la S{\\'e}paration des Pr{\\'e}occupations "
            "durant l'Int{\\'e}gration de Domaines H{\\'e}t{\\'e}rog{\\`e}nes "
            "dans les Syst{\\`e}mes Logiciels"
        )
        expected = (
            "Préserver la Séparation des Préoccupations "
            "durant l'Intégration de Domaines Hétérogènes "
            "dans les Systèmes Logiciels"
        )
        self.assertEqual(self.utils.tex2unicode(latex), expected)

    def test_school_field_from_issue_23(self):
        """The school field from the bug report is decoded correctly."""
        self.assertEqual(
            self.utils.tex2unicode("University of C{\\^o}te d'Azur, France"),
            "University of Côte d'Azur, France",
        )

    #  9. Multiple accents in a single string
    def test_multiple_accents_in_one_string(self):
        """Several different accents in the same string are all decoded."""
        self.assertEqual(
            self.utils.tex2unicode("Ren{\\'e} Ch{\\^a}teau {\\`a} Z{\\\"u}rich"),
            "René Château à Zürich",
        )

    # 10. Edge cases: empty strings and ASCII
    def test_empty_string(self):
        """An empty string is returned unchanged."""
        self.assertEqual(self.utils.tex2unicode(""), "")

    def test_plain_ascii_unchanged(self):
        """A string with no LaTeX commands is returned unchanged."""
        self.assertEqual(
            self.utils.tex2unicode("Plain ASCII text 123"),
            "Plain ASCII text 123",
        )

    def test_already_unicode_unchanged(self):
        """A string already containing Unicode characters is preserved."""
        self.assertEqual(
            self.utils.tex2unicode("Déjà décodé"),
            "Déjà décodé",
        )

    # 11. Round-trip property: unicode -> tex -> unicode
    def test_round_trip_unicode_to_tex_to_unicode(self):
        """
        Encoding to TeX then decoding back returns the original string.
        This ensures unicode2Tex() and tex2unicode() are proper inverses
        for the supported character set.
        """
        original = "Café Crème Brûlée"
        encoded = self.utils.unicode2Tex(original)
        decoded = self.utils.tex2unicode(encoded)
        self.assertEqual(decoded, original)

    def test_hungarian_double_acute(self):
        """Double acute (Hungarian umlaut) is decoded properly."""
        self.assertEqual(
            self.utils.tex2unicode("Erd{\\H{o}}s"),
            "Erdős",
        )

    def test_ae_ligature(self):
        """AE ligature is decoded properly."""
        self.assertEqual(
            self.utils.tex2unicode("{\\AE}gean Sea"),
            "Ægean Sea",
        )

    def test_dotless_i(self):
        """Dotless i with accent is decoded properly."""
        self.assertEqual(
            self.utils.tex2unicode("Mart{\\'\\i}nez"),
            "Martínez",
        )

    # 12. Alternative valid BibTeX form: \'{e}
    def test_accent_braces_around_letter_only(self):
        """Alternative valid BibTeX form \\'{e} is decoded to é."""
        self.assertEqual(
            self.utils.tex2unicode("Eug\\'{e}ne"),
            "Eugéne",
        )

    def test_accent_braces_around_letter_only2(self):
        """Alternative valid BibTeX form \\'{e} is decoded to è."""
        self.assertEqual(
            self.utils.tex2unicode("Eug\\`{e}ne"),
            "Eugène",
        )
if __name__ == "__main__":
    unittest.main(verbosity=2)