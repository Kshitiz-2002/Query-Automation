from bs4 import BeautifulSoup
import requests

class ScrapeJobDetails:
    def __init__(self, urls: list):

        self.url_list = urls

    def _fetchUrlData(self, url: str):

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }

        return requests.get(url, headers=headers).text

    def _parseHtml(self, html_content):

        soup = BeautifulSoup(html_content, 'lxml')

        tags_to_extract = ['p', 'li', 'ul']

        extracted_text = []
        for tag in tags_to_extract:
            for element in soup.find_all(tag):
                extracted_text.append(element.get_text(strip=True))  

        return "\n".join(extracted_text)


    def _run(self):

        result_dict = {}

        for url in self.url_list:

            html_data = self._fetchUrlData(url)

            result_dict[url] = self._parseHtml(html_data)

        return result_dict