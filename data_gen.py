#!/usr/bin/python3

import os
import logging

import requests
from bs4 import BeautifulSoup

import data

URL_FILE = 'url.txt'
LOG_FILE = 'data_gen.log'

def get_urls_tmp():
    urls = ('https://en.wikipedia.org/wiki/Phoenix_Wright:_Ace_Attorney',
            'https://en.wikipedia.org/wiki/Dark_Souls_III')
    for url in urls:
        yield url

# Return an iterable of urls
def get_urls(file_):
    # TODO
    return get_urls_tmp()

# Raise requests.exceptions.HTTPError if there's a bad request
def data_gen(url):
    r = requests.get(url)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')

    game = data.Game()
    game.get_data(url)

def main():
    logging.basicConfig(filename=LOG_FILE, level=logging.ERROR,
                        format='%(asctime)s %(message)s')
    with open(URL_FILE, "r+") as f:
        errors = 0
        for url in get_urls(f):
            try:
                data_gen(url)
            except requests.exceptions.HTTPError:
                logging.error('HTML request to {url} failed.'.format(url=url))
                errors += 1
                if errors >= 3:
                    logging.error('Exited due to too many errors.')
                    break

if __name__ == '__main__':
    main()

