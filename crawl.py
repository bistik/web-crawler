from typing import TypedDict
from urllib.parse import urljoin, urlsplit

import requests
from bs4 import BeautifulSoup


class PageData(TypedDict):
    url: str
    heading: str
    first_paragraph: str
    outgoing_links: list[str]
    image_urls: list[str]

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

def extract_page_data(html: str, page_url: str):
    page_data: PageData = {}
    page_data["url"] = page_url
    page_data["heading"] = get_heading_from_html(html)
    page_data['first_paragraph'] = get_first_paragraph_from_html(html)
    page_data["outgoing_links"] = get_urls_from_html(html, page_url)
    page_data["image_urls"] = get_images_from_html(html, page_url)
    return page_data

def get_html(url: str):
    r = requests.get(url, headers={"User-Agent": "BootCrawler/1.0"})
    if r.status_code >= 400:
        raise Exception("Error in fetching page")
    elif 'text/html' not in r.headers.get('content-type'):
        raise Exception('Invalid content-type {}'.format(r.headers.get('content-type')))
    return r.text

def crawl_page(base_url, current_url=None, page_data=None):
    if current_url is None:
        current_url = base_url
    normal_current_url = normalize_url(current_url)
    if not normal_current_url.startswith(normalize_url(base_url)):
        return
    if page_data is None:
        page_data = {}
    if normal_current_url in page_data:
        print(f"Already visited {normal_current_url}, skipping"),
        return
    print("Grabbing html...")
    html = get_html(current_url)
    single_pd = extract_page_data(html, current_url)
    page_data[normal_current_url] = single_pd
    print(f"Added page_data with key '{normal_current_url}'")
    for url in single_pd["outgoing_links"]:
        print(f"crawling '{url}' ...")
        crawl_page(base_url, current_url=url, page_data=page_data)
