# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import unittest
import requests
from testfixtures import LogCapture
from httmock import all_requests, HTTMock
from .plugin import *


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


class TestDelicious(unittest.TestCase):

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

            b1 = Bookmark({
                'description': 'desc1',
                'extended': 'ext1',
                'href': 'url1',
                'tag': 'tag1 tag2'})
            b2 = Bookmark({
                'description': 'desc2',
                'extended': 'ext2',
                'href': 'url2',
                'tag': 'tag1 tag2'})

            self.assertEqual(bookmarks, set([b1, b2]))

    def test_regex(self):

        tests = {"None": [],
                 "a [delicious a b c] z": ["a b c"],
                 "a [delicious a b c] [delicious d e f] z": ["a b c", "d e f"],
                 "a [delicious 8-ƃʇn sı sıɥʇ]": ["8-ƃʇn sı sıɥʇ"]}

        for s, e in tests.items():
            match = [m for m in delicious_regex.findall(s)]
            self.assertEqual(match, e)

    def test_replace_delicious_tags(self):
        pass
