from __future__ import absolute_import, unicode_literals
import unittest
import tempfile
import os
import codecs
from shutil import rmtree
from usfm_tools.transform import UsfmTransform
from bs4 import BeautifulSoup


class TestSinglehtmlRender(unittest.TestCase):

    resources_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="singlehtml-renderer-")

    def tearDown(self):
        rmtree(self.temp_dir)

    def test_quote_indents_of_large_book(self):
        usfm_dir = os.path.join(self.resources_dir, 'usfm_projects', 'numbers')
        html_dir = os.path.join(self.temp_dir, 'quote_indents_of_large_book')
        os.mkdir(html_dir)
        UsfmTransform.buildSingleHtml(usfm_dir, html_dir, 'bible')
        html_file = os.path.join(html_dir, 'bible.html')
        self.assertTrue(os.path.exists(html_file))
        with codecs.open(html_file, 'r', 'utf-8-sig') as f:
            converted_html = f.read()
        soup = BeautifulSoup(converted_html, 'html.parser')
        indent_count = len(soup.select("p[class^=indent-]"))
        self.assertEqual(indent_count, 190)

    def test_quote_indents_of_large_book_with_illegal_usfm(self):
        usfm_dir = os.path.join(self.resources_dir, 'usfm_projects', 'matthew')
        html_dir = os.path.join(self.temp_dir, 'quote_indents_of_large_book')
        os.mkdir(html_dir)
        UsfmTransform.buildSingleHtml(usfm_dir, html_dir, 'bible')
        html_file = os.path.join(html_dir, 'bible.html')
        self.assertTrue(os.path.exists(html_file))
        with codecs.open(html_file, 'r', 'utf-8-sig') as f:
            converted_html = f.read()
        soup = BeautifulSoup(converted_html, 'html.parser')
        verse_count = len(soup.select("span[class^=v-num]"))
        self.assertEqual(verse_count, 315)
        nbsp = converted_html.find('\xa0')
        self.assertTrue(nbsp < 0,"'\\xa0' should not be in text")

    def test_footnotes_in_ruth(self):
        usfm_dir = os.path.join(self.resources_dir, 'usfm_projects', 'ruth')
        html_dir = os.path.join(self.temp_dir, 'footnotes_in_ruth')
        os.mkdir(html_dir)
        UsfmTransform.buildSingleHtml(usfm_dir, html_dir, 'bible')
        html_file = os.path.join(html_dir, 'bible.html')
        self.assertTrue(os.path.exists(html_file))
        with codecs.open(html_file, 'r', 'utf-8-sig') as f:
            converted_html = f.read()
        soup = BeautifulSoup(converted_html, 'html.parser')
        chapter_count = len(soup.select("h2[class^=c-num]"))
        self.assertEqual(chapter_count, 4)
        verse_count = len(soup.select("span[class^=v-num]"))
        self.assertEqual(verse_count, 85)
        footnote_count = len(soup.select("div[class^=footnote]"))
        self.assertEqual(footnote_count, 4)

    def test_footnotes_in_1samuel(self):
        usfm_dir = os.path.join(self.resources_dir, 'usfm_projects', '1samuel')
        html_dir = os.path.join(self.temp_dir, 'footnotes_in_1samuel')
        os.mkdir(html_dir)
        UsfmTransform.buildSingleHtml(usfm_dir, html_dir, 'bible')
        html_file = os.path.join(html_dir, 'bible.html')
        self.assertTrue(os.path.exists(html_file))
        with codecs.open(html_file, 'r', 'utf-8-sig') as f:
            converted_html = f.read()
        soup = BeautifulSoup(converted_html, 'html.parser')
        chapter_count = len(soup.select("h2[class^=c-num]"))
        self.assertEqual(chapter_count, 31)
        verse_count = len(soup.select("span[class^=v-num]"))
        self.assertEqual(verse_count, 810)
        footnote_count = len(soup.select("div[class=footnote]"))
        self.assertEqual(footnote_count, 9)

    def test_sections_in_song_of_solomon(self):
        usfm_dir = os.path.join(self.resources_dir, 'usfm_projects', 'song_of_solomon')
        html_dir = os.path.join(self.temp_dir, 'section_person_in_song_of_solomon')
        os.mkdir(html_dir)

        UsfmTransform.buildSingleHtml(usfm_dir, html_dir, 'bible')
        html_file = os.path.join(html_dir, 'bible.html')
        self.assertTrue(os.path.exists(html_file))
        with codecs.open(html_file, 'r', 'utf-8-sig') as f:
            converted_html = f.read()
        soup = BeautifulSoup(converted_html, 'html.parser')
        chapter_count = len(soup.select("h2[class^=c-num]"))
        self.assertEqual(chapter_count, 8)
        verse_count = len(soup.select("span[class^=v-num]"))
        self.assertEqual(verse_count, 117)
        # check for \sp
        section_who_count = len(soup.select("p[class=s-who]"))
        self.assertEqual(section_who_count, 51)

if __name__ == "__main__":
    unittest.main()
