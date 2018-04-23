#!/usr/bin/python3

import logging

from bs4 import BeautifulSoup
import requests

import data

DEBUGGING = True
if 'DEBUGGING' not in globals():
    DEBUGGING = False

URL_FILE = 'url.txt'
LOG_FILE = 'data_gen.log'


def get_urls_tmp():
    urls = (
            'https://en.wikipedia.org/wiki/Super_Mario_Bros.',
            # 'https://en.wikipedia.org/wiki/Super_Mario_World',
            # 'https://en.wikipedia.org/wiki/Phoenix_Wright:_Ace_Attorney',
            # 'https://en.wikipedia.org/wiki/Dark_Souls_III',
            )
    for url in urls:
        yield url


# Return an iterable of urls
def get_urls(file_):
    # TODO
    return get_urls_tmp()


def data_gen(game_url: str):
    r = requests.get(game_url)
    r.raise_for_status()
    game_soup = BeautifulSoup(r.text, 'lxml')

    game = data.Game(game_soup)
    if not game.in_database:
        game.insert_into_database()
        for employee in game.employees:
            employee.insert_if_not_exist()
        else:
            game.employees.append(data.Employee.generic())

        for dcompany in game.developing_companies:
            dcompany.insert_if_not_exist(data.Company.DEV)
        else:
            game.developing_companies.append(data.Company.generic())
            for dcompany in game.developing_companies:
                dcompany.insert_if_not_exist(data.Company.DEV)

        for pcompany in game.publishing_companies:
            pcompany.insert_if_not_exist(data.Company.PUB)
        else:
            game.publishing_companies.append(data.Company.generic())
            for pcompany in game.publishing_companies:
                pcompany.insert_if_not_exist(data.Company.PUB)
    print('"{title}" {reception} {release_date}'
          .format(title=game.title, reception=game.reception,
                  release_date=game.earliest_release_date))

    try:
        game_release = data.GameRelease(game_soup, game=game)
    except BaseException:
        logging.error('data_gen_test: {}: Failed to get GameReleases'
                      .format(game.title))
        game_release = data.GameRelease(game=game)
        if DEBUGGING:
            raise
    if game_release.releases:
        game_release.insert_into_database()
    else:
        game_release.releases.append(data.GameRelease.generic_r(game))

    data.Develops.insert(game, game_release)


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
                if errors >= 20:
                    logging.error('Exited due to too many HTTP errors.')
                    break


if __name__ == '__main__':
    main()
