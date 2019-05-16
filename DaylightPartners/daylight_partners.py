from bs4 import BeautifulSoup
from selenium import webdriver
import csv


class Company:

    def __init__(self, _name, _description, _link, _city):
        self._name = _name
        self._description = _description
        self._link = _link
        self._city = _city

    @property
    def name(self):
        return self._name

    @property
    def description(self):
        return self._description

    @property
    def link(self):
        return self._link


def inner_html(obj):
    string = obj.encode_contents().decode('utf-8').strip()
    return string


def output_to_csv(file_name, companies):
    with open(file_name, 'w') as out:
        writer = csv.writer(out)
        writer.writerow(['Company', 'Description', 'Company Link'])
        for company in companies:
            writer.writerow([company.name, company.description, company.link])
    out.close()


def main():
    initial_url = 'http://daylightpartners.com/portfolio/'
    city = 'Austin, TX'

    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(initial_url)

    soup_page = BeautifulSoup(driver.page_source, 'html.parser')

    list_container = soup_page.find('div', {'class': 'entry'})
    anchors = list_container.find_all('a')

    company_list = []
    base_url = 'http://daylightpartners.com'

    for anchor in anchors:
        url = base_url + anchor['href']
        driver.get(url)
        soup_page = BeautifulSoup(driver.page_source, 'html.parser')

        description_container = soup_page.find('div', {'class': 'post'})
        company_name = inner_html(description_container.find('h1'))
        paragraph_tags = description_container.find_all('p')
        paragraphs = []
        company_url = ''

        for index, paragraph in enumerate(paragraph_tags):
            if index == 0:
                image = paragraph.find('img')
                if image is not None:
                    image.extract()
            if index == len(paragraph_tags) - 1:
                company_anchor = paragraph.find('a')
                if company_anchor is not None:
                    company_url = company_anchor['href']
            else:
                paragraphs.append(inner_html(paragraph))
        company_description = '\n'.join(paragraphs)
        current_company = Company(company_name, company_description, company_url, city)
        company_list.append(current_company)

    output_to_csv('companies.csv', company_list)
    driver.quit()  # close the browser(s) in session


if __name__ == '__main__':
    main()

