from bs4 import BeautifulSoup
import requests
from collections import Counter


class PikabuGrabber:
    HEADERS = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,"
                  "*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Cache-Control": 'no-cache',
        "Connection": "keep-alive",
        "Cookie": input("Insert cookie: "),
        "Host": 'pikabu.ru',
        "Pragma": "no-cache",
        "Referer": "https://pikabu.ru",
        "TE": "Trailers",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:71.0) Gecko/'
                      '20100101 Firefox/71.0',
    }

    def __init__(self):
        self.session = requests.Session()
        self.headers = self.HEADERS

    def get_pages(self, url, quantity):
        result = []
        params = {'page': quantity}
        for n in range(1, quantity + 1):
            params['page'] = n
            result.append(self.session.get(url,
                                           params=params,
                                           headers=self.headers).text)
        return result


def count_all_tags(pages):
    tags_list = []
    for page in pages:
        soup = BeautifulSoup(page, 'html.parser')
        articles = soup.find_all('article', limit=10)
        for art in articles:
            tags = art.find_all('a', {'class': 'tags__tag', "data-tag": True})
            for tag in tags:
                word = tag.get('data-tag')
                tags_list.append(word)

    return tags_list


def find_top10_tags(all_tags):
    return Counter(all_tags).most_common(10)


if __name__ == '__main__':
    grabber = PikabuGrabber()
    pages = grabber.get_pages(url='https://pikabu.ru/new/subs', quantity=10)

    all_tags = count_all_tags(pages)
    number_of_all_tags = len(all_tags)
    top_10_tags = find_top10_tags(all_tags)

    with open('top10.txt', 'w') as file:
        file.write('Top10 Tags:\n\n')
        for tag in top_10_tags:
            file.write(f"{tag[0]} - {tag[1]}\n")
        file.write(f"\nTotal amount of tags: {number_of_all_tags}")
