import unittest
from crawl import get_heading_from_html, get_first_paragraph_from_html

class TestGetText(unittest.TestCase):
    def test_get_heading_from_h1(self):
        input_html = """<html>
            <body>test<h1>Heading1</h1></body>
        </html>"""
        actual = get_heading_from_html(input_html)
        expected = "Heading1"
        self.assertEqual(actual, expected)

    def test_get_heading_from_h2(self):
        input_html = """<html>
            <body>test<h2>Heading2</h2></body>
        </html>"""
        actual = get_heading_from_html(input_html)
        expected = "Heading2"
        self.assertEqual(actual, expected)

    def test_get_heading_from_no_heading(self):
        input_html = """<html>
            <body>test<p>Heading2</p></body>
        </html>"""
        actual = get_heading_from_html(input_html)
        expected = ""
        self.assertEqual(actual, expected)

    def test_get_multiple_paragraph(self):
        input_html = f"""<html>
            <body>
                <p>Paragraph1</p>
                <p>Paragraph2</p>
            </body>
        </html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = 'Paragraph1'
        self.assertEqual(actual, expected)
 
    def test_get_no_paragraph(self):
        input_html = f"""<html>
            <body>
                <div>Div text</div>
                <a href=\"http://example.com\">link</a>
            </body>
        </html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = ''
        self.assertEqual(actual, expected)

    def test_get_single_paragraph(self):
        input_html = f"""<html>
            <body>
                <P>Paragraph text</P>
                <a href=\"http://example.com\">link</a>
            </body>
        </html>"""
        actual = get_first_paragraph_from_html(input_html)
        expected = 'Paragraph text'
        self.assertEqual(actual, expected)

if __name__ == "__main__":
    unittest.main()