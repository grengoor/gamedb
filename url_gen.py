#!/usr/bin/python3

import os
import random
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests

wikipedia_baseurl = 'https://en.wikipedia.org/'
URL_FILENAME = 'url.txt'

# No PC games because the format is too different from the other platforms,
# and that would elongate the execution time
list_urls = (
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Xbox_360_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Xbox_One_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_GameCube_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Nintendo_64_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Nintendo_Entertainment_System_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Nintendo_Switch_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Super_Nintendo_Entertainment_System_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Wii_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Wii_U_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Game_Boy_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Game_Boy_Color_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Game_Boy_Advance_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Nintendo_DS_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_Nintendo_3DS_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_PlayStation_3_games_released_on_disc'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_PlayStation_4_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_PlayStation_4_games'),
    urljoin(wikipedia_baseurl,
            '/wiki/List_of_PlayStation_Vita_games_(A%E2%80%93L)'),
)
urls_len = len(list_urls)


def gls_method1(soup: BeautifulSoup):
    return soup.find('table', id='softwarelist')


def gls_method2(soup: BeautifulSoup):
    return soup.find('table', class_='wikitable sortable')


gls_methods = (
    gls_method1,
    gls_method1,
    gls_method2,
    gls_method1,
    gls_method1,
    gls_method1,
    gls_method1,
    gls_method1,
    gls_method1,
    gls_method1,
    gls_method2,
    gls_method2,
    gls_method1,
    gls_method1,
    gls_method1,
    gls_method1,
    gls_method1,
    gls_method1,
)


def game_list_soup(i: int):
    """i: index of list_urls"""
    r = requests.get(list_urls[i])
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')
    return gls_methods[i](soup)


def download_all_urls(file_):
    for i, game_list in enumerate(map(game_list_soup, range(len(list_urls)))):
        for tr in game_list('tr'):
            try:
                print(tr.td.a['href'].encode('utf-8'), file=file_)
            except BaseException:
                continue


def main():
    if not os.path.exists(URL_FILENAME):
        with open(URL_FILENAME, 'w') as file_:
            download_all_urls(file_)
    else:
        print('File "{}" exists'.format(URL_FILENAME))


if __name__ == '__main__':
    main()
