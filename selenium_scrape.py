from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv


class Posting:

    def __init__(self, _company, _position, _link):
        self._company = _company
        self._position = _position
        self._link = _link

    @property
    def company(self):
        return self._company

    @property
    def position(self):
        return self._position

    @property
    def link(self):
        return self._link


def inner_html(obj):
    string = obj.encode_contents().decode('utf-8').strip()
    return string


def output_to_csv(file_name, postings):
    with open(file_name, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['Company', 'Position', 'Link'])
        for posting in postings:
            writer.writerow([posting.company, posting.position, posting.link])
    out.close()


def main():
    url = 'https://www.eranyc.com/jobs/'

    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(url)

    soup_page = BeautifulSoup(driver.page_source, 'html.parser')

    regex = re.compile(r'Page 1 of (\d+)')
    page_text = inner_html(soup_page.find('span', {'class': ['page-numbers', 'page-num']}))
    match = regex.match(page_text)
    pages = int(match.group(1))
    page_counter = 1
    postings = []

    while True:
        articles = soup_page.find_all('article', class_='jobs-item')
        for article in articles:
            company = inner_html(article.find('span', class_='jobs-item__meta'))
            position = inner_html(article.find('h2', class_='jobs-item__heading'))
            anchor = article.find('a', class_='jobs-item__link')['href']
            print(company, position, anchor)
            postings.append(Posting(company, position, anchor))
        page_counter += 1
        if page_counter > pages:
            break
        next_link = 'https://www.eranyc.com/jobs/page/{}'.format(page_counter)
        driver.get(next_link)
        soup_page = BeautifulSoup(driver.page_source, 'html.parser')

    output_to_csv('postings.csv', postings)


if __name__ == '__main__':
    main()
