from urllib.parse import urlsplit, urljoin
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

def get_urls_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    a_tags = soup.find_all('a')
    urls = []
    for a_tag in a_tags:
        url = a_tag.get('href')
        if url:
            urls.append(urljoin(base_url, url))
    return urls

def get_images_from_html(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    img_tags = soup.find_all('img')
    urls = []
    for a_tag in img_tags:
        src = a_tag.get('src')
        if src:
            urls.append(urljoin(base_url, src))
    return urls