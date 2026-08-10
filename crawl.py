from urllib.parse import urlsplit
from bs4 import BeautifulSoup, Tag

def normalize_url(url_str: str) -> str:
    url = urlsplit(url_str)
    return url.netloc + url.path.rstrip('/')

def get_heading_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.h1:
        return soup.h1.get_text(strip=True)
    if soup.h2:
        return soup.h2.get_text(strip=True)
    return ''

def get_first_paragraph_from_html(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    p_tag = soup.find('p')
    if p_tag is not None:
        return p_tag.get_text(strip=True)
    return ''