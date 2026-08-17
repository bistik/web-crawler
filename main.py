import sys

from aiohttp.cookiejar import asyncio

from crawl import crawl_site_async


async def main():
    base_url: str = ""
    if len(sys.argv) < 2:
        print("no website provided")
        sys.exit(1)
    elif len(sys.argv) > 2:
        print("too many arguments provided")
        sys.exit(1)
    else:
        base_url = sys.argv[1]
        print(f"starting crawl of: {base_url}")
        page_data = await crawl_site_async(base_url)
        for pd in page_data.values():
            print(pd)
        # crawl_page("https://learnwebscraping.dev", current_url="https://learnwebscraping.dev/practice/ecommerce/")

if __name__ == "__main__":
    asyncio.run(main())
