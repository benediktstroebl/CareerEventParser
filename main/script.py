import requests
from bs4 import BeautifulSoup
import csv
import re
import time

output = []


def remove_space_control_characters(string):
    s = str(string).replace('\n', '')
    s = s.replace('\t', '')
    s = s.replace('\r', '')
    s = s.strip()
    s = re.sub(' +', ' ', s)  # replaces 2 or more spaces with a single space
    return s


def bcg_parser():
    print('BCG Parser started! ')
    root_url = "https://www.bcg.com/careers/recruiting-events/default.aspx"
    local_page = requests.get(root_url)
    local_soup = BeautifulSoup(local_page.content, 'html.parser')
    item = {}
    location_URLs = []

    url_section = local_soup.find_all('div', {"class": "grid-column"})

    for a in url_section[2].find_all('a'):
        location_URLs.append(a['href'])

    for a in url_section[3].find_all('a'):
        location_URLs.append(a['href'])

    for location in location_URLs:
        print(location)
        location_page = requests.get(location)
        location_soup = BeautifulSoup(location_page.content, 'html.parser')

        text_section = location_soup.find_all('section', {"class": "text"})
        for section in text_section:
            if section is not None:  # no events at all in a location
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

                item['Url'] = location
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
    item = {}
    pagination_urls = [root_url]

    while len(pagination_urls) > 0:
        page_url = pagination_urls.pop(0)
        page_page = requests.get(page_url)
        page_soup = BeautifulSoup(page_page.content, 'html.parser')
        next_url = page_soup.find('div', {"class": "listPagination"}).find_all('a')
        print(next_url[len(next_url) - 1].get('href'))
        if next_url is not None:
            if next_url[len(next_url) - 1].contents[0] == 'Next >>':
                pagination_urls.append(next_url[len(next_url) - 1].get('href'))

        list_items = page_soup.find_all('li', {"class": "listSingleColumnItem autoClearer"})
        for list_item in list_items:

            itemDate = list_item.find('div', {"class": "box-list box-date"})
            if itemDate is not None:
                item['date'] = remove_space_control_characters(itemDate.contents[0])

            itemTitle = list_item.find('h3', {"class": "listSingleColumnItemTitle"}).find('a')
            if itemTitle is not None:
                item['title'] = remove_space_control_characters(itemTitle.contents[0])
                item['Url'] = itemTitle['href']

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
    page_page = requests.get(root_url)
    page_soup = BeautifulSoup(page_page.content, 'html.parser')
    item = {}

    event_container = page_soup.find_all('div', {"class": "filter-display-card events active"})
    print(event_container)

    for container in event_container:
        item['company'] = 'JP Morgan'

        itemDateDay = container.find('p', {"class": "date-start-day"})
        itemDateMonth = container.find('p', {"class": "date-start-month"})
        if itemDateDay is not None and itemDateMonth is not None:
            item['date'] = remove_space_control_characters(itemDateDay.contents[0]+' '+itemDateMonth.contents[0])

        itemPlace = container.find('p', {"class": "city"})
        if itemPlace is not None:
            item['place'] = remove_space_control_characters(itemPlace.contents[0])

        itemTitle = container.find('p', {"class": "event-name"})
        if itemTitle is not None:
            item['title'] = remove_space_control_characters(itemTitle.contents[0])

        itemUrl = container.find('a', {"class": "signup-link chaseanalytics-opt-exlnk"})
        if itemUrl is not None:
            item['Url'] = itemUrl['href']

        print(item)
    print('JP Morgan Parser done!')


def morgan_stanley_parser():
    pass


def goldman_parser():
    pass


def blackstone_parser():
    pass


jp_morgan_parser()
