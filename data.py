#!/usr/bin/python3

import logging

from bs4 import BeautifulSoup
from parse import compile

from mysql_config import config
import gamedb


def generate_unique_id():
    # TODO
    return None


class PROTOTYPE:
    def __init__(self, soup: BeautifulSoup, check_db: bool = False,
                 use_db: bool = False):
        """Initialize PROTOTYPE object.

        Args:
            soup: If given, then use data in soup to initialize/check for
                existence in database.
            check_db: If True, then the object will not be populated if
                data correspoinding to data in soup exists in the database.
                If False, then attempt to populate object using getdata.
                Ignored if soup is not given or is None.
            use_db: Whether or not to use the database. For debugging.
        """
        self.prototype_id = generate_unique_id()
        self.in_database = False
        if soup:
            self.get_data(soup, check_db, use_db)
        else:
            self.attr1 = None
            self.attr2 = None
            # ...

    check_existence_sql = """SELECT title FROM {table} WHERE title='?'""" \
                          .format(table=config.config['tables']['Game'])

    def check_database(self):
        """Return database tuple if a tuple with ____ is in the
        database, return None otherwise.

        If such a tuple exists in the database, then set self.in_database to
        True. Else, leave it alone.
        """
        if not self.title:
            return False

        cu = gamedb.db.cursor()
        cu.execute(Game.check_existence_sql, ("""TODO""",))     # TODO
        tuple = cu.fetchone()
        cu.close()

        if tuple:
            self.in_database = True
        return tuple


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
        self.game_id = generate_unique_id()
        self.in_database = False
        if soup:
            self.get_data(soup, check_db, use_db)
        else:
            self.earliest_release_date = None
            self.reception = None
            self.title = None

    check_existence_sql = "SELECT title FROM game WHERE title='%s'"

    def check_database(self):
        """Return database tuple if a tuple with title=self.title is in the
        database, return None otherwise.

        self.in_database is True if such a tuple exists in the database, False
        otherwise.
        """
        if not self.title:
            return False

        with gamedb.db.cursor() as cu:
            cu.execute(Game.check_existence_sql, (self.title,))
            tuple = cu.fetchone()

        self.in_database = True if tuple else False
        return tuple

    insert_sql = "INSERT INTO game VALUES ('%s', '%s', '%s', '%s')"

    def insert_into_database(self):
        with gamedb.db.cursor() as cu:
            cu.execute(Game.insert_sql, (self.game_id,
                                         self.earliest_release_date,
                                         self.reception, self.title))

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
            tuple = self.check_database()
            if tuple:
                if check_db:
                    return
                self.get_data_from_tuple(tuple)
            else:
                self.get_earliest_release_date(soup)
                self.get_reception(soup)
        else:
            self.get_earliest_release_date(soup)
            self.get_reception(soup)
            self.get_title(soup)

    def get_data_from_tuple(self, tuple):
        self.game_id, self.earliest_release_date, self.reception, self.title \
            = tuple

    def get_earliest_release_date(self, soup: BeautifulSoup):
        # TODO
        self.earliest_release_date = None
        logging.error('Game.get_earliest_release_date called yet not implemented')
        pass

    reception_parse = compile('{num:d}/{den:d}')

    def get_reception(self, soup: BeautifulSoup):
        table = soup.body.find('div', id='content') \
                         .find('div', id='bodyContent') \
                         .find('div', id='mw-content-text') \
                         .find('div', attrs={'class': 'mw-parser-output'}) \
                         .find('th', string='Aggregate score').parent.parent
        score_str = table.find('a', string='Metacritic').parent.next_sibling \
                         .next_sibling.sup.previous_sibling
        parsed_score = Game.reception_parse.search(score_str)
        self.reception = 100 * float(parsed_score['num']) \
                             / float(parsed_score['den'])

    def get_title(self, soup: BeautifulSoup):
        self.title = soup.body.find('div', id='content') \
                              .find('h1', id='firstHeading').i.string
        print(self.title)


class Platform:
    def __init__(self, soup=None):
        if soup:
            pass
        else:
            pass


class GameRelease:
    def __init__(self, soup: BeautifulSoup = None, game: Game = None,
                 platform: Platform = None):
        self.release_id = generate_unique_id()
        if platform:
            self.platform_id = platform.platform_id
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
        self.game_releases = []
        if soup:
            self.get_data(soup)

    def get_data(self, soup):
        pass
