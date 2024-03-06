import requests  
from bs4 import BeautifulSoup
from collections import defaultdict
from urllib.parse import urljoin, urlparse

class WebCrawler:
    def __init__(self):
        self.index = defaultdict(list)
        self.visited = set()

    def crawl(self, url, base_url=None):
        if url in self.visited:
            return 
        self.visited.add(url)

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            self.index[url] = soup.get_text()

            for link in soup.find_all('a'):
                href = link.get('href')
                if href:
                    if urlparse(href).scheme in ('http', 'https'):
                        if not urlparse(href).netloc:
                            href = urljoin(base_url or url, href)
                        if href  in self.visited: #remove "not" to stop infite loop
                            self.crawl(href, base_url=base_url or url)
        except Exception as e:
            print(f"Error crawling {url}: {e}")

    def search(self, keyword):
        results = []
        for url, text in self.index.items():
            if keyword.lower() in text.lower(): #we remove not to show "No found" if search result not match
                results.append(url)
        return results

    def print_results(self, results):
        if results:
            print("Search results:")
            for result in results:
                print(f"- {result}")# Fixed undefined_variable to result
        else:
            print("No results found.")

def main():
    crawler = WebCrawler()
    start_url = "https://example.com"
    crawler.crawl(start_url) # Fixed method name from 'craw' to 'crawl'

    keyword = "test"
    results = crawler.search(keyword)
    crawler.print_results(results)

if __name__ == "__main__":
    main()