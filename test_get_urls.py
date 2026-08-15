import unittest
from crawl import get_urls_from_html

class TestGetUrls(unittest.TestCase):
    def test_get_urls_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="https://crawler-test.com"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = '<html><body><a href="/bootdev"><span>Boot.dev</span></a></body></html>'
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/bootdev"]
        self.assertEqual(actual, expected)

    def test_get_urls_from_html_multiple_urls(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
            <a href="/bootdev"><span>Boot.dev</span></a>
            <a href="https://example.com"><span>example.com</span></a>
            <a>No link</a>
        </body></html>"""
        actual = get_urls_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/bootdev", "https://example.com"]
        self.assertEqual(actual, expected)