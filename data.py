#!/usr/bin/python3

import datetime
import logging
import random
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from parse import compile
import pymysql
import requests

import gamedb


random.seed()


wikipedia_baseurl = 'https://en.wikipedia.org/'


def wiki_body_content(soup: BeautifulSoup):
    return soup.body.find('div', id='content').find('div', id='bodyContent')


def wiki_infobox(soup: BeautifulSoup):
    return soup.body.find('div', id='content').find('div', id='bodyContent') \
                    .find('table', class_='infobox')


def wiki_title(soup: BeautifulSoup):
    return soup.body.find('div', id='content').find('h1', id='firstHeading') \
               .i.string


def random_date():
    year = random.randint(2000, 2017)
    month = random.randint(1, 12)
    day = random.randint(1, 27)
    return datetime.date(year, month, day)


r'''
class Prototype:
    def __init__(self, soup: BeautifulSoup = None, check_db: bool = False,
                 use_db: bool = True):
        """Initialize Prototype object.

        Args:
            soup: If given, then use data in soup to initialize/check for
                existence in database.
            check_db: If True, then the object will not be populated if
                data correspoinding to data in soup exists in the database.
                If False, then attempt to populate object using getdata.
                Ignored if soup is not given or is None.
            use_db: Whether or not to use the database. For debugging.
        """
        self.prototype_id = None
        self.in_database = False
        if soup:
            self.get_data(soup, check_db, use_db)
        else:
            self.attrN = None

    check_sql_id = "SELECT * FROM prototype WHERE id=%s"
    check_sql_TODO = "SELECT * FROM prototype WHERE TODO=%s"

    def check_database(self):
        """Return database tuple if a tuple with title=self.title is in the
        database, return None otherwise. (SLIGHTLY DIFFERENT, TODO)

        self.in_database is True if such a tuple exists in the database, False
        otherwise.
        """
        if self.prototype_id:
            sql = Prototype.check_sql_id
            check = self.prototype_id
        elif self.TODO:
            sql = Prototype.check_sql_TODO
            check = self.TODO
        else:
            self.in_database = False
            return None

        with gamedb.db.cursor() as cu:
            cu.execute(sql, (check,))
            tuple_ = cu.fetchone()

        self.in_database = tuple_ is not None
        return tuple_

    insert_sql = """INSERT INTO prototype (attr1, ... TODO)
                    VALUES (%s, ... TODO)"""

    def insert_into_database(self):
        with gamedb.db.cursor() as cu:
            cu.execute(Prototype.insert_sql, (self.TODO))
        gamedb.db.commit()

    def get_data(self, soup: BeautifulSoup, check_db: bool = False,
                 use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database. For debugging.
        """
        if use_db:
            self.get_TODO(soup)
            tuple_ = self.check_database()
            if tuple_:
                if not check_db:
                    self.get_data_from_tuple(tuple_)
            else:
                # get rest of attributes
                pass
        else:
            # get all attributes
            pass

    def get_data_from_tuple(self, tuple_):
        # TODO unpack tuple into attributes
        pass

    def get_date(self, soup: BeautifulSoup):
        # TODO
        self.date = random_date()

    def get_title(self, soup: BeautifulSoup):
        self.title = wiki_title(soup)
'''


class Game:
    def __init__(self, soup: BeautifulSoup = None, check_db: bool = False,
                 use_db: bool = True):
        """Initialize Game object.

        Args:
            soup: If given, then use data in soup to initialize/check for
                existence in database.
            check_db: If True, then the object will not be populated if
                data correspoinding to data in soup exists in the database.
                If False, then attempt to populate object using getdata.
                Ignored if soup is not given or is None.
            use_db: Whether or not to use the database. For debugging.
        """
        self.game_id = None
        self.in_database = False
        if soup:
            self.get_data(soup, check_db, use_db)
        else:
            self.earliest_release_date = None
            self.reception = None
            self.title = None

    check_sql_id = "SELECT * FROM game WHERE game_id=%s"
    check_sql_title = "SELECT * FROM game WHERE title=%s"

    def check_database(self):
        """Return database tuple if a tuple with title=self.title is in the
        database, return None otherwise. (SLIGHTLY DIFFERENT, TODO)

        self.in_database is True if such a tuple exists in the database, False
        otherwise.
        """
        if self.game_id:
            sql = Game.check_sql_id
            check = self.game_id
        elif self.title:
            sql = Game.check_sql_title
            check = self.title
        else:
            self.in_database = False
            return None

        with gamedb.db.cursor() as cu:
            cu.execute(sql, (check,))
            tuple_ = cu.fetchone()

        self.in_database = tuple_ is not None
        return tuple_

    insert_sql = """INSERT INTO game (earliest_release_date, reception, title)
                    VALUES (%s, %s, %s)"""

    def insert_into_database(self):
        with gamedb.db.cursor() as cu:
            cu.execute(Game.insert_sql, (self.earliest_release_date,
                                         self.reception, self.title))
        gamedb.db.commit()

    def get_data(self, soup: BeautifulSoup, check_db: bool = False,
                 use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database. For debugging.
        """
        if use_db:
            self.get_title(soup)
            tuple_ = self.check_database()
            if tuple_:
                if not check_db:
                    self.get_data_from_tuple(tuple_)
            else:
                self.get_earliest_release_date(soup)
                self.get_reception(soup)
        else:
            self.get_earliest_release_date(soup)
            self.get_reception(soup)
            self.get_title(soup)

    def get_data_from_tuple(self, tuple_):
        self.game_id, self.earliest_release_date, self.reception, self.title \
            = tuple_

    def get_earliest_release_date(self, soup: BeautifulSoup):
        # TODO
        year = random.randint(2000, 2017)
        month = random.randint(1, 12)
        day = random.randint(1, 27)
        self.earliest_release_date = datetime.date(year, month, day)

    reception_parse = compile('{num:d}/{den:d}')

    def get_reception(self, soup: BeautifulSoup):
        table = wiki_body_content(soup) \
                .find('div', id='mw-content-text') \
                .find('div', class_='mw-parser-output') \
                .find('th', string='Aggregate score').parent.parent
        score_str = table.find('a', string='Metacritic').parent.next_sibling \
                         .next_sibling.sup.previous_sibling
        parsed_score = Game.reception_parse.search(score_str)
        self.reception = 100 * float(parsed_score['num']) \
                             / float(parsed_score['den'])

    def get_title(self, soup: BeautifulSoup):
        self.title = wiki_title(soup)


class GameRelease:
    """Releases belonging to one Game."""

    def __init__(self, soup: BeautifulSoup = None, game: Game = Game(),
                 check_db: bool = False, use_db: bool = True):
        """Initialize GameRelease object.

        Args:
            soup: If given, then use data in soup to initialize/check for
                existence in database.
            game: Use as self.game.
            check_db: If True, then the object will not be populated if
                data correspoinding to data in soup exists in the database.
                If False, then attempt to populate object using getdata.
                Ignored if soup is not given or is None.
            use_db: Whether or not to use the database. For debugging.
        """
        self.in_database = False
        if soup:
            self.get_data(soup, game, check_db, use_db)
        else:
            self.game = game
            # List of tuples containing release_id, platform, region,
            # release_date
            self.releases = []
            self.title = game.title

    check_sql_id = "SELECT * FROM game_release WHERE id=%s"
    check_sql_title = "SELECT * FROM game_release WHERE title=%s"

    def check_database(self, check_db: bool = False):
        """Return database tuple if a tuple with title=self.title is in the
        database, return None otherwise. (SLIGHTLY DIFFERENT, TODO)

        self.in_database is True if such a tuple exists in the database, False
        otherwise.
        """
        # if self.release_id:
        #     sql = GameRelease.check_sql_id
        #     check = self.release_id
        if self.title:
            sql = GameRelease.check_sql_title
            check = self.title
        else:
            self.in_database = False
            return None

        with gamedb.db.cursor() as cu:
            cu.execute(sql, (check,))
            if check_db:
                tuples = [cu.fetchone()]
            else:
                tuples = cu.fetchall()

        self.in_database = bool(tuples)
        return tuples

    insert_sql = """INSERT INTO game_release (game_id, platform_id, region,
                    release_date, title) VALUES (%s, %s, %s, %s, %s)"""

    def insert_into_database(self):
        for release in self.releases:
            try:
                with gamedb.db.cursor() as cu:
                    cu.execute(GameRelease.insert_sql,
                               (self.game.game_id, release[1], release[2],
                                release[3], self.title))
                gamedb.db.commit()
            except pymysql.err.InternalError:
                logging.error(
                    'Attempted to insert NULL in non-NULLable column for {}.'
                    .format(self.title))

    def get_data(self, soup: BeautifulSoup, game: Game = Game(),
                 check_db: bool = False, use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database. For debugging.
        """
        self.game = game
        self.title = game.title
        if use_db:
            if not self.title:
                self.get_title(soup)
            tuples = self.check_database(check_db)
            if tuples:
                if not check_db:
                    self.get_data_from_tuples(tuples)
            else:
                self.get_releases(soup)
        else:
            if not self.title:
                self.get_title(soup)
            self.get_releases(soup)

    def get_data_from_tuples(self, tuples):
        _, self.game.game_id, _, _, _, self.title = tuples[0]
        for t in tuples:
            platform = Platform()
            release_id, _, platform.platform_id, region, release_date, _ = t
            self.releases.append((release_id, platform, region, release_date))

    def get_releases(self, soup: BeautifulSoup):
        # TEST
        url = 'https://en.wikipedia.org/wiki/Phoenix_Wright:_Ace_Attorney'
        r = requests.get(url)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, 'lxml')
        # /TEST

        infobox = wiki_infobox(soup)
        release_li = infobox.find('th', string='Release').parent.td.ul.li
        current_platform = None
        for child in release_li.children:
            if child.name == 'b':
                current_platform = Platform()
                current_platform = child.string
                print(child.string)
            elif current_platform and child.name == 'div' \
                                  and 'plainlist' in child['class']:
                for li in child.find_all('li'):
                    pass

        # TODO

    def get_title(self, soup: BeautifulSoup):
        self.title = wiki_title(soup)


class Platform:
    def __init__(self, soup: BeautifulSoup = None, check_db: bool = False,
                 use_db: bool = True):
        """Initialize Platform object.

        Args:
            soup: If given, then use data in soup to initialize/check for
                existence in database.
            check_db: If True, then the object will not be populated if
                data correspoinding to data in soup exists in the database.
                If False, then attempt to populate object using getdata.
                Ignored if soup is not given or is None.
            use_db: Whether or not to use the database. For debugging.
        """
        self.platform_id = None
        self.in_database = False
        if soup:
            self.get_data(soup, check_db, use_db)
        else:
            self.company = None     # TODO?
            self.discontinued_date = None
            self.generation = None
            self.introductory_price = None
            self.name = None
            self.release_date = None
            self.type = None

    check_existence_sql = "SELECT * FROM platform WHERE TODO=%s"

    def check_database(self):
        """Return database tuple if a tuple with title=self.title is in the
        database, return None otherwise.

        self.in_database is True if such a tuple exists in the database, False
        otherwise.
        """
        if not self.TODO:
            return None

        with gamedb.db.cursor() as cu:
            cu.execute(Platform.check_existence_sql, (self.TODO,))
            tuple_ = cu.fetchone()

        self.in_database = tuple_ is not None
        return tuple_

    insert_sql = """INSERT INTO platform (attr1, ... TODO)
                    VALUES (%s, ... TODO)"""

    def insert_into_database(self):
        with gamedb.db.cursor() as cu:
            cu.execute(Platform.insert_sql, (self.TODO))
        gamedb.db.commit()

    def get_data(self, soup: BeautifulSoup, check_db: bool = False,
                 use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database. For debugging.
        """
        if use_db:
            self.get_TODO(soup)
            tuple_ = self.check_database()
            if tuple_:
                if not check_db:
                    self.get_data_from_tuple(tuple_)
            else:
                # get rest of attributes
                pass
        else:
            # get all attributes
            pass

    def get_data_from_tuple(self, tuple_):
        # unpack tuple into attributes
        pass

    def get_date(self, soup: BeautifulSoup):
        # TODO
        year = random.randint(2000, 2017)
        month = random.randint(1, 12)
        day = random.randint(1, 27)
        self.earliest_release_date = datetime.date(year, month, day)

    def get_title(self, soup: BeautifulSoup):
        self.title = wiki_title(soup)


platform_re = re.compile(r'Platform(\(s\))?', re.IGNORECASE)


def get_platform_soup(game_soup: BeautifulSoup, platform_name: str):
    infobox = wiki_infobox(game_soup)
    platform_a = infobox.find(string=platform_re).parent.parent.parent.td \
                        .find('a', string=platform_name)
    platform_url = urljoin(wikipedia_baseurl, platform_a['href'])

    r = requests.get(platform_url)
    r.raise_for_status()
    return BeautifulSoup(r.text, 'lxml')


def get_platform_soups(game_soup: BeautifulSoup):
    infobox = wiki_infobox(game_soup)
    platform_as = infobox.find(string=platform_re).parent.parent.parent.td \
                         .find_all('a')
    platform_urls = \
            [urljoin(wikipedia_baseurl, x['href']) for x in platform_as]
    for url in platform_urls:
        r = requests.get(url)
        r.raise_for_status()
        yield BeautifulSoup(r.text, 'lxml')


"""
class GameRelease:
    def __init__(self, soup: BeautifulSoup = None, game: Game = None,
                 platform: Platform = None):
        self.release_id = None
        self.platform_id = platform.platform_id if platform else None
        self.region = None
        self.release_date = None
        if game:
            self.title = game.title


# GameReleases for a particular Game. Should be used instead of GameRelease
# since definition of one GameRelease depends on knowing what information has
# already been used for another GameRelease.
class GameReleases:
    def __init__(self, soup=None, game=None):
        if game:
            self.game_id = game.game_id
        self.game_id = game.game_id if game else None
        self.game_releases = []
        if soup:
            self.get_data(soup)

    def get_data(self, soup):
        pass
"""
