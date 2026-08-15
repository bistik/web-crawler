import unittest
from crawl import get_images_from_html

class TestGetImageFromHtml(unittest.TestCase):
    def test_get_images_from_html_relative(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <img src="/logo.png" alt="Logo">
        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_absolute(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <img src="/logo.png" alt="Logo">
        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png"]
        self.assertEqual(actual, expected)

    def test_get_images_from_html_multiple(self):
        input_url = "https://crawler-test.com"
        input_body = """<html><body>
        <img src="/logo.png" alt="Logo">
        <img src="https://example.com/smiley.png" alt="Smiley">
        <img alt="what is this?">
        </body></html>"""
        actual = get_images_from_html(input_body, input_url)
        expected = ["https://crawler-test.com/logo.png", "https://example.com/smiley.png"]
        self.assertEqual(actual, expected)