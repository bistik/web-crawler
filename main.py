import sys

from crawl import crawl_page


def main():
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
        crawl_page("https://learnwebscraping.dev", current_url="https://learnwebscraping.dev/practice/ecommerce/")

if __name__ == "__main__":
    main()
