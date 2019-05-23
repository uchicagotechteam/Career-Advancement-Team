from bs4 import BeautifulSoup
from selenium import webdriver
import csv


class Company:

    def __init__(self, _name, _description, _link):
        self._name = _name
        self._description = _description
        self._link = _link

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


def output_to_csv(file_name, companies, city, incubator):
    with open(file_name, 'w') as out:
        writer = csv.writer(out)
        for company in companies:
            writer.writerow([city, incubator, company.name, company.description, company.link])
    out.close()


def main():
    initial_url = 'http://tritonventures.com/portfolio/'
    city = 'Austin'
    incubator = 'Triton Ventures'

    driver = webdriver.Firefox()
    driver.implicitly_wait(30)
    driver.get(initial_url)

    soup_page = BeautifulSoup(driver.page_source, 'html.parser')
    sp_containers = soup_page.find_all('div', {'class': 'sp'})
    anchor_container = sp_containers[1]  # second one has links
    anchors = anchor_container.find_all('a')

    company_list = []

    for anchor in anchors:
        relative_url = anchor['href']
        if '.html' in relative_url:
            company_name = inner_html(anchor)
            url = initial_url + relative_url
            driver.get(url)
            soup_page = BeautifulSoup(driver.page_source, 'html.parser')

            # get first one
            description_container = soup_page.find('div', {'class': 'sp'})
            paragraphs = description_container.find_all('p')
            description_paragraph = paragraphs[3]
            company_description = inner_html(description_paragraph)
            url_paragraph = paragraphs[4]
            company_anchor = url_paragraph.find('a')
            company_url = company_anchor['href']

            current_company = Company(company_name, company_description, company_url)
            company_list.append(current_company)

    if len(company_list) > 0:
        output_to_csv('companies.csv', company_list, city, incubator)
    driver.quit()


if __name__ == '__main__':
    main()