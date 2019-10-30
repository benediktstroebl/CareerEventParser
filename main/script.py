import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import re
from urllib.parse import urljoin

output = []


def remove_space_control_characters(string):
    s = str(string).replace('\n', '')
    s = s.replace('\t', '')
    s = s.replace('\r', '')
    s = s.strip()
    s = re.sub(' +', ' ', s)  # replaces 2 or more spaces with a single space
    s = s.replace('\xa0', '')
    return s


def bcg_parser():
    print('BCG Parser started! ')
    root_url = "https://www.bcg.com/careers/recruiting-events/default.aspx"
    local_page = requests.get(root_url)
    local_soup = BeautifulSoup(local_page.content, 'html.parser')
    location_URLs = []

    url_section = local_soup.find_all('div', {"class": "grid-column"})

    for a in url_section[2].find_all('a'):
        location_URLs.append(a['href'])

    for a in url_section[3].find_all('a'):
        location_URLs.append(a['href'])

    for location in location_URLs:
        location_page = requests.get(location)
        location_soup = BeautifulSoup(location_page.content, 'html.parser')

        text_section = location_soup.find_all('section', {"class": "text"})
        for section in text_section:
            if section is not None:  # no events at all in a location
                item = {}
                itemTitle = section.find('h3')
                if itemTitle is not None:
                    item['title'] = remove_space_control_characters(itemTitle.contents[0])
                else:
                    item['title'] = '-'

                itemDate = section.find('span', {"class": "date"})
                if itemDate is not None:
                    item['date'] = remove_space_control_characters(itemDate.contents[0])
                else:
                    item['date'] = '-'

                itemPlace = section.find('span', {"class": "place"})
                if itemPlace is not None:
                    item['place'] = remove_space_control_characters(itemPlace.contents[0])
                else:
                    item['place'] = '-'

                item['url'] = location
                item['company'] = 'Boston Consulting Group'

            print(item)
            output.append(item)
    print('BCG parser finished! ')


def mck_parser():
    pass


def bane_parser():
    print('Bane Parser started! ')
    root_url = "https://careers.bain.com/recruits/events"
    local_page = requests.get(root_url)
    local_soup = BeautifulSoup(local_page.content, 'html.parser')
    pagination_urls = [root_url]

    while len(pagination_urls) > 0:
        page_url = pagination_urls.pop(0)
        page_page = requests.get(page_url)
        page_soup = BeautifulSoup(page_page.content, 'html.parser')
        next_url = page_soup.find('div', {"class": "listPagination"}).find_all('a')
        if next_url is not None:
            if next_url[len(next_url) - 1].contents[0] == 'Next >>':
                pagination_urls.append(next_url[len(next_url) - 1].get('href'))

        list_items = page_soup.find_all('li', {"class": "listSingleColumnItem autoClearer"})
        for list_item in list_items:
            item = {}
            itemDate = list_item.find('div', {"class": "box-list box-date"})
            if itemDate is not None:
                item['date'] = remove_space_control_characters(itemDate.contents[0])

            itemTitle = list_item.find('h3', {"class": "listSingleColumnItemTitle"}).find('a')
            if itemTitle is not None:
                item['title'] = remove_space_control_characters(itemTitle.contents[0])
                item['url'] = itemTitle['href']

            itemPlace = list_item.find_all('span', {"class": "listSingleColumnItemMiscDataItem"})
            if len(itemPlace) > 0:
                item['place'] = remove_space_control_characters(itemPlace[1].find('span', {"class": None}).contents[0])

            item['company'] = 'Bane & Company'
            print(item)
            output.append(item)
    print('Bane Parser done!')


def jp_morgan_parser():
    print('JP Morgan Parser started! ')
    root_url = 'https://careers.jpmorgan.com/us/en/students/events'
    driver = webdriver.Chrome()
    page_page = requests.get(root_url)
    driver.get(root_url)
    html = driver.page_source
    page_soup = BeautifulSoup(html, 'html.parser')
    driver.close()

    event_container = page_soup.find_all('div', {"class": "filter-display-card events active"})

    for container in event_container:
        item = {}
        item['company'] = 'JP Morgan'

        itemDateDay = container.find('p', {"class": "date-start-day"})
        itemDateMonth = container.find('p', {"class": "date-start-month"})
        if itemDateDay is not None and itemDateMonth is not None:
            item['date'] = remove_space_control_characters(itemDateDay.contents[0] + ' ' + itemDateMonth.contents[0])

        itemPlace = container.find('p', {"class": "city"})
        if itemPlace is not None:
            item['place'] = remove_space_control_characters(itemPlace.contents[0])

        itemTitle = container.find('p', {"class": "event-name"})
        if itemTitle is not None:
            item['title'] = remove_space_control_characters(itemTitle.contents[0])

        itemUrl = container.find('a', {"class": "signup-link chaseanalytics-opt-exlnk"})
        if itemUrl is not None:
            item['url'] = itemUrl['href']

        output.append(item)
        print(item)
    print('JP Morgan Parser done!')


def morgan_stanley_parser():
    global output
    root_url = 'https://morganstanley.tal.net/vx/lang-en-GB/mobile-0/brand-2/candidate/jobboard/vacancy/2/adv/'
    page = requests.get(root_url)
    soup = BeautifulSoup(page.content, 'html.parser')
    tbody_soup = soup.find('tbody')

    list_items = tbody_soup.find_all('tr')

    for container in list_items:
        item = {}
        item['company'] = 'Morgan Stanley'

        itemTitle = container['data-title']
        if itemTitle is not None:
            item['title'] = remove_space_control_characters(itemTitle)

        itemPlace = container.find_all('td', {"class": "comm_list_tbody"})
        itemPlace = itemPlace[1]
        if itemPlace is not None:
            item['place'] = remove_space_control_characters(itemPlace.contents[0])

        itemDate = container.find_all('td', {"class": "comm_list_tbody"})
        itemDate = itemDate[2]
        if itemPlace is not None:
            item['date'] = remove_space_control_characters(itemDate.contents[0])

        itemUrl = container.find('a', {"class": "subject"})
        if itemUrl is not None:
            item['url'] = itemUrl['href']
        output.append(item)
        print(item)
    print('Morgan Stanley Parser is done!')


def goldman_parser():
    root_url = 'https://www.goldmansachs.com/a/data/events/'
    driver = webdriver.Chrome()
    driver.get(root_url)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    tbody_soup = soup.find('tbody', {"id": "eventBody"})
    driver.close()

    list_items = tbody_soup.find_all('tr', {"class": "eventRow"})

    for container in list_items:
        item = {}
        item['company'] = 'Goldman Sachs'

        itemTitle = container.find('td', {"class": "eventName"})
        if itemTitle is not None:
            item['title'] = remove_space_control_characters(itemTitle.contents[0])

        itemPlace = container.find('td', {"class": "eventLocation"})
        if itemPlace is not None:
            item['place'] = remove_space_control_characters(itemPlace.contents[0])

        item['url'] = 'TO REGISTER AND VIEW MORE EVENTS, PLEASE GO TO "MY GS EVENTS".'

        itemDate = container.find('td', {"class": "eventDate"})
        if itemDate is not None:
            item['date'] = remove_space_control_characters(itemDate.contents[0])
        print(item)
        output.append(item)
    print('Goldman Sachs Parser is done!')


def blackstone_parser():
    pass


def hsbc_parser():
    root_url = 'https://www.hsbc.com/careers/careers-events?page=1&take=100'
    page = requests.get(root_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    list_items = soup.find_all('li', {"class": "calendar-events__item"})

    for container in list_items:
        item = {}
        item['company'] = 'HSBC'

        itemTitle = container.find('h2', {"class": "calendar-event__header"})
        if itemTitle is not None:
            item['title'] = remove_space_control_characters(itemTitle.contents[0])

        itemPlace = container.find('p', {"class": "calendar-event__body"})
        if itemPlace is not None:
            item['place'] = remove_space_control_characters(itemPlace.contents[0].text)

        itemUrl = container.find('a', {"class": "calendar-event"})
        if itemUrl is not None:
            item['url'] = urljoin(root_url, itemUrl['href'])

        itemDate = container.find('div', {"class": "calendar-event__date"})
        if itemDate is not None:
            item['date'] = remove_space_control_characters(itemDate["aria-label"])
        print(item)
        output.append(item)
    print('HSBC Parser is done!')


def create_output_file():
    filename = 'careerEventsOutput.csv'
    with open(filename, 'w', newline='', encoding="utf-8") as output_file:
        fieldnames = ['company', 'title', 'date', 'place', 'url']
        w = csv.DictWriter(output_file, fieldnames=fieldnames)
        w.writeheader()
        for item in output:
            w.writerow(item)
    print('File successfully created!')


def main():
    hsbc_parser()
    goldman_parser()
    bane_parser()
    bcg_parser()
    morgan_stanley_parser()
    jp_morgan_parser()
    print(output)
    create_output_file()
    print('All done!')


main()
