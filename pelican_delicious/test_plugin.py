# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import requests
from testfixtures import LogCapture
from httmock import all_requests, HTTMock
from mock import Mock
from .plugin import *
from pelican.generators import (Generator, ArticlesGenerator, PagesGenerator,
                                TemplatePagesGenerator)
from pelican.contents import Page
from pelican.tests.support import get_settings


class TestBookmark(unittest.TestCase):

    def test_title(self):
        self.assertEqual(Bookmark({"description": "desc"}).title, "desc")
        self.assertEqual(Bookmark({}).title, None)

    def test_description(self):
        self.assertEqual(Bookmark({"extended": "ext"}).description, "ext")
        self.assertEqual(Bookmark({}).title, None)

    def test_href(self):
        self.assertEqual(Bookmark({"href": "url"}).href, "url")
        self.assertEqual(Bookmark({}).title, None)

    def test_tags(self):
        self.assertEqual(
            Bookmark({"tag": "tag1 tag2"}).tags, set(["tag1", "tag2"]))
        self.assertEqual(Bookmark({}).tags, set())

    def test_cmp(self):
        self.assertEqual(Bookmark(), Bookmark())
        self.assertEqual(
            Bookmark({"description": "desc"}), Bookmark({"description": "desc"}))


class TestDelicious(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.b1 = Bookmark({
            'description': 'desc1',
            'extended': 'ext1',
            'href': 'url1',
            'tag': 'tag1 tag2'})
        self.b2 = Bookmark({
            'description': 'desc2',
            'extended': 'ext2',
            'href': 'url2',
            'tag': 'tag1 tag2'})
        self.b3 = Bookmark({
            'description': 'desc3',
            'extended': 'ext3',
            'href': 'url3',
            'tag': 'tag3'})

    def test_fetch_delicious(self):

        @all_requests
        def response_content(url, request):
            return {'status_code': 200,
                    'text': b''}

        with HTTMock(response_content):
            with LogCapture() as l:
                bookmarks = fetch_delicious("user", "pass")
                self.assertEqual(bookmarks, set())
                l.check(('pelican_delicious.plugin',
                         'ERROR',
                         'No bookmarks downloaded'))

        @all_requests
        def response_content(url, request):
            return {'status_code': 401,
                    'content': ''}

        with HTTMock(response_content):
            with LogCapture() as l:
                bookmarks = fetch_delicious("user", "pass")
                self.assertEqual(bookmarks, set())
                l.check(('pelican_delicious.plugin',
                         'ERROR',
                         'Wrong Delicious credentials'))

        @all_requests
        def response_content(url, request):
            return {'status_code': 200,
                    'content': b"""<posts tag="" total="2014" user="2xyo">\
<post description="desc1" extended="ext1" hash="hs" href="url1" private="yes" \
shared="no" tag="tag1 tag2" time="2013-09-21T14:05:23Z"/> \
<post description="desc2" extended="ext2" hash="hs" href="url2" private="no" \
shared="yes" tag="tag1 tag2" time="2013-09-21T14:05:23Z"/></posts>"""}

        with HTTMock(response_content):
            bookmarks = fetch_delicious("user", "pass")

            self.assertEqual(bookmarks, set([self.b1, self.b2]))

    def test_regex(self):

        tests = {"None": [],
                 "a [delicious a b c] z": ["a b c"],
                 "a [delicious a b c] [delicious d e f] z": ["a b c", "d e f"],
                 "a [delicious 8-ƃʇn sı sıɥʇ]": ["8-ƃʇn sı sıɥʇ"],
                 "a [delicious tag1 tag2]": ["tag1 tag2"]}

        for s, e in tests.items():
            match = [m for m in delicious_regex.findall(s)]
            self.assertEqual(match, e)

    def test_replace_delicious_tags(self):

        settings = get_settings(filenames={})
        settings['DEFAULT_CATEGORY'] = 'Default'
        settings['DEFAULT_DATE'] = (1970, 1, 1)
        settings['READERS'] = {'asc': None}

        generator = PagesGenerator(
            context=settings.copy(), settings=settings,
            path="/tmp", theme=settings['THEME'], output_path=None)
        generator.generate_context()

        d = {'DELICIOUS_TEMPLATE': delicious_default_template,
             'DELICIOUS_BOOKMARKS': set([self.b1, self.b2, self.b3])}

        generator.context.update(d)

        p1 = Page("a [delicious tag1] z")
        e1 = """a <div class="delicious">

    <dl>
        <dt>Title</dt>
        <dd>desc2</dd>
        <dt>Description</dt>
        <dd>ext2</dd>
        <dt>URL</dt>
        <dd><a href="url2">url2</a></dd>
    </dl>

    <dl>
        <dt>Title</dt>
        <dd>desc1</dd>
        <dt>Description</dt>
        <dd>ext1</dd>
        <dt>URL</dt>
        <dd><a href="url1">url1</a></dd>
    </dl>

</div> z"""

        p2 = Page("a [delicious tag1 tag2] z")
        e2 = e1

        p3 = Page("a [delicious tag3] z")
        e3 = """a <div class="delicious">

    <dl>
        <dt>Title</dt>
        <dd>desc3</dd>
        <dt>Description</dt>
        <dd>ext3</dd>
        <dt>URL</dt>
        <dd><a href="url3">url3</a></dd>
    </dl>

</div> z"""
        generator.pages = [p1, p2, p3]
        replace_delicious_tags(generator)

        self.assertEqual(generator.pages[0]._content, e1)
        self.assertEqual(generator.pages[1]._content, e2)
        self.assertEqual(generator.pages[2]._content, e3)
