import requests
from bs4 import BeautifulSoup
import pprint
from time import sleep
from random import randint


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for index, item in enumerate(links):
        title = links[index].getText()
        href = links[index].get('href', None)
        vote = subtext[index].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hn)


hn_links = []
hn_subtext = []

# Scrape first 2 pages
for index in range(1, 3):
    URL = 'https://news.ycombinator.com/news?p=' + str(index)
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')

    hn_links.extend(links)
    hn_subtext.extend(subtext)

    # Time interval between requests
    sleep(randint(2, 5))


pprint.pprint(create_custom_hn(hn_links, hn_subtext))
