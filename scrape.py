import requests
from bs4 import BeautifulSoup as bsoup

site = 'https://news.ycombinator.com/news'
query_param = '?p='
num_of_pages = int(
    input('Enter the number of pages you would like to scrape: '))
popularity = int(input('Enter the number of votes required for a post: '))
links = []
subtext = []

for page in range(1, num_of_pages+1):
    hn_url = site + query_param + str(page)
    res = requests.get(hn_url)
    new_soup = bsoup(res.text, 'html.parser')
    links += new_soup.select('.storylink')
    subtext += new_soup.select('.subtext')


def sort_by_votes(hnlist):
    # whenever sorting with dictionaries
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points >= popularity:
                hn.append({'title': title, 'link': href, 'votes': points})
    return sort_by_votes(hn)


stories = create_custom_hn(links, subtext)

for story in enumerate(stories):
    print('Title:', story[1]['title'])
    print('Link to article:', story[1]['link'])
    print('Votes:', story[1]['votes'], '\n')
