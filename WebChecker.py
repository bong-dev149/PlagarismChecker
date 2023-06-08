import urllib.request
from bs4 import BeautifulSoup
from googlesearch import search
import numpy as np
import os
from LocalFileChecker import LocalFileChecker

# class for web based plagiarism checking
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"


class WebBasedChecking:
    url_list = []
    text_content = []

    def __init__(self):
        self.url_list = []
        self.text_content = []

    @classmethod
    #     method for creating url list from topics
    def create_url_list(self, topic):
        for link in search(topic, 'com', 'en', num=10, stop=10, pause=4):
            self.url_list.append(link)
        return self.url_list
        # print(self.url_list)

    #     method for gathering textual data from the url links
    def gather_data(self, url_list):
        count = 0
        for url in url_list:
            count += 1
            # print(url)

            opener = AppURLopener()
            html = opener.open(url)

            # html = urlopen().read()
            soup = BeautifulSoup(html, features="html.parser")

            # kill all script and style elements
            for script in soup(["script", "style"]):
                script.extract()  # rip it out

            # get text
            text = soup.get_text()
            # print(text)
            # break into lines and remove leading and trailing space on each
            lines = (line.strip() for line in text.splitlines())
            # break multi-headlines into a line each
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            # drop blank lines
            text = '\n'.join(chunk for chunk in chunks if chunk)
            self.text_content.append(text)
            with open(f'./web_results/{count}.txt', 'w', encoding="utf-8") as f:
                f.writelines(self.text_content)


if __name__ == '__main__':
    obj = WebBasedChecking()
    obj.url_list = obj.create_url_list('psychology')
    # print(obj.url_list)
    obj.gather_data(obj.url_list)
    file_path = './hello.txt'
    web_files = [doc for doc in os.listdir('./web_results') if doc.endswith('.txt')]
    lfc = LocalFileChecker(file_path,web_files)
    lfc.check_plagiarism()
    lfc.show_result()
