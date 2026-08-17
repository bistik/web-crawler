import asyncio
from typing import TypedDict
from urllib.parse import urljoin, urlparse, urlsplit

import aiohttp
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

async def crawl_site_async(base_url):
    async with AsyncCrawler(base_url, max_concurrency=5) as crawler:
        return await crawler.crawl()

class AsyncCrawler:
    def __init__(self, base_url, max_concurrency=3) -> None:
        self.base_url = base_url
        self.base_domain = urlparse(base_url).netloc
        self.page_data = {}
        self.max_concurrency = max_concurrency
        self.lock = asyncio.Lock()
        self.semaphore = asyncio.Semaphore(max_concurrency)
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def add_page_visit(self, normalized_url):
        async with self.lock:
            return normalized_url not in self.page_data

    async def get_html(self, url: str):
        if self.session is None:
            return
        async with self.session.get(url, headers={"User-Agent": "BootCrawler/1.0"}) as r:
            if r.status >= 400:
                raise Exception("Error in fetching page")
            elif 'text/html' not in r.headers.get('content-type'):
                raise Exception('Invalid content-type {}'.format(r.headers.get('content-type')))
            return await r.text()

    async def crawl_page(self, url):
        current_url_obj = urlsplit(url)
        if current_url_obj.netloc != self.base_domain:
            return
        normalized_url = normalize_url(url)
        first_time = await self.add_page_visit(normalized_url)
        if not first_time:
            return

        async with self.semaphore:
            html = await self.get_html(url)
            if html is None:
                return

            async with self.lock:
                self.page_data[normalized_url] = extract_page_data(html, url)
            urls = get_urls_from_html(html, url)

        tasks = []
        for u in urls:
            task = asyncio.create_task(self.crawl_page(u))
            tasks.append(task)
        if tasks:
            await asyncio.gather(*tasks)

    async def crawl(self):
        await self.crawl_page(self.base_url)
        return self.page_data
