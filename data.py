#!/usr/bin/python3

import datetime
from dateutil.parser import parse
from itertools import repeat
import logging
import random
import re
from urllib.parse import urljoin

import bs4
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
               .string


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
            use_db: Whether or not to use the database.
        """
        self.prototype_id = None
        self.in_database = False
        if soup:
            self.get_data(soup, check_db, use_db)
        else:
            self.attrN = None

    check_sql_id = "SELECT * FROM prototype WHERE prototype_id=%s"
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

    get_id_sql = "SELECT prototype_id FROM prototype WHERE TODO=%s"

    def get_id(self, TODO: str = None):
        """Get id from database."""
        with gamedb.db.cursor() as cu:
            if not TODO:
                TODO = self.TODO
            cu.execute(Prototype.get_id_sql, (TODO,))
            id_ = cu.fetchone()
            if id_:
                self.prototype_id = id_[0]

    def get_data(self, soup: BeautifulSoup, check_db: bool = False,
                 use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database.
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


class Company:
    DEV = 1
    PUB = 2

    def __init__(self, soup: BeautifulSoup = None, check_db: bool = False,
                 use_db: bool = True):
        """Initialize Company object.

        Args:
            soup: If given, then use data in soup to initialize/check for
                existence in database.
            check_db: If True, then the object will not be populated if
                data correspoinding to data in soup exists in the database.
                If False, then attempt to populate object using getdata.
                Ignored if soup is not given or is None.
            use_db: Whether or not to use the database.
        """
        self.company_id = None
        self.defunct_date = None
        self.founder = None
        self.founding_date = None
        self.hq_address = None
        self.name = None
        self.website = None
        self.in_database = False
        if soup:
            self.get_data(soup, check_db, use_db)

    check_sql_id = "SELECT * FROM company WHERE company_id=%s"
    check_sql_name = "SELECT * FROM company WHERE name=%s"

    def check_database(self):
        """Return database tuple if a tuple with title=self.title is in the
        database, return None otherwise. (SLIGHTLY DIFFERENT, TODO)

        self.in_database is True if such a tuple exists in the database, False
        otherwise.
        """
        if self.company_id:
            sql = Company.check_sql_id
            check = self.company_id
        elif self.name:
            sql = Company.check_sql_name
            check = self.name
        else:
            self.in_database = False
            return None

        with gamedb.db.cursor() as cu:
            cu.execute(sql, (check,))
            tuple_ = cu.fetchone()

        self.in_database = tuple_ is not None
        if self.in_database and not self.company_id:
            self.get_id()
        return tuple_

    insert_sql = """INSERT INTO company (defunct_date, founder, founding_date,
                    hq_address, name, website)
                    VALUES (%s, %s, %s, %s, %s, %s)"""

    def insert_into_database(self):
        with gamedb.db.cursor() as cu:
            cu.execute(Company.insert_sql, (self.defunct_date, self.founder,
                                            self.founding_date, self.hq_address,
                                            self.name, self.website))
        gamedb.db.commit()
        self.get_id()

    dev_sql = "INSERT INTO developing_company (company_id) VALUES (%s)"

    @staticmethod
    def insert_dev(id):
        try:
            with gamedb.db.cursor() as cu:
                cu.execute(Company.dev_sql, (id,))
            gamedb.db.commit()
        except pymysql.err.IntegrityError:
            return

    pub_sql = "INSERT INTO publishing_company (company_id) VALUES (%s)"

    @staticmethod
    def insert_pub(id):
        try:
            with gamedb.db.cursor() as cu:
                cu.execute(Company.pub_sql, (id,))
            gamedb.db.commit()
        except pymysql.err.IntegrityError:
            return

    def insert_if_not_exist(self, t: int = None):
        self.check_database()
        if not self.in_database:
            self.insert_into_database()
        if not self.company_id:
            self.get_id()

        if t is not None:
            if t == Company.DEV:
                Company.insert_dev(self.company_id)
            elif t == Company.PUB:
                Company.insert_pub(self.company_id)

    get_id_sql = "SELECT company_id FROM company WHERE name=%s"

    def get_id(self, name: str = None):
        """Get id from database."""
        with gamedb.db.cursor() as cu:
            if not name:
                name = self.name
            cu.execute(Company.get_id_sql, (name,))
            id_ = cu.fetchone()
            if id_:
                self.company_id = id_[0]

    def get_data(self, soup: BeautifulSoup, check_db: bool = False,
                 use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database.
        """
        if use_db:
            self.get_name(soup)
            tuple_ = self.check_database()
            if tuple_:
                if not check_db:
                    self.get_data_from_tuple(tuple_)
            else:
                self.get_defunct_date(soup)
                self.get_founder(soup)
                self.get_founding_date(soup)
                self.get_hq_address(soup)
                self.get_website(soup)
        else:
            self.get_defunct_date(soup)
            self.get_founder(soup)
            self.get_founding_date(soup)
            self.get_hq_address(soup)
            self.get_name(soup)
            self.get_website(soup)

    def get_data_from_tuple(self, tuple_):
        self.company_id, self.defunct_date, self.founder, self.founding_date, \
                self.hq_address, self.name, self.website = tuple_

    def get_defunct_date(self, soup: BeautifulSoup):
        # TODO
        self.defunct_date = random_date()

    def get_founder(self, soup: BeautifulSoup):
        # TODO
        pass

    def get_founding_date(self, soup: BeautifulSoup):
        # TODO
        self.founding_date = random_date()

    def get_hq_address(self, soup: BeautifulSoup):
        # TODO
        pass

    def get_name(self, soup: BeautifulSoup):
        self.name = wiki_title(soup)

    def get_website(self, soup: BeautifulSoup):
        # TODO
        pass

    developing_re = re.compile(r'Developer(\(s\))?', re.IGNORECASE)
    publishing_re = re.compile(r'Publisher(\(s\))?', re.IGNORECASE)

    companies = dict()

    invalid_names = ('Japan',)

    @staticmethod
    def get_urls(infobox: bs4.element.Tag, company_re):
        th = infobox.find(string=company_re)
        if not th:
            return None
        while th.name != 'th':
            th = th.parent

        td = th.next_sibling
        while td.name != 'td':
            td = td.next_sibling

        urls = []
        for s in td.strings:
            if s in ('\n', ':', 'JP'):
                continue
            parent = s.parent
            try:
                name = parent['title']
            except KeyError:
                name = parent.string
                if not name:
                    name = s.strip()
            if name in Company.invalid_names:
                continue

            if parent.name == 'a':
                url = urljoin(wikipedia_baseurl, parent['href'])
                urls.append(url)
                if name not in Company.companies:
                    Company.companies[name] = url
            else:
                if name in Company.companies:
                    urls.append(Company.companies[name])
                else:
                    logging.error(
                        'Company.get_urls: url of {} not in Company.companies'
                        .format(name))
        return urls


class Employee:
    roles = ('Artist', 'Composer', 'Creator', 'Director', 'Producer',
             'Programmer', 'Writer')
    role_res = [re.compile(r'{role}(\(s\))?'.format(role=role), re.IGNORECASE)
                for role in roles]

    name_re = re.compile('[a-zA-Z][a-zA-Z ,.\'-]*[a-zA-Z]')

    def __init__(self, name: str = None, roles: list = []):
        self.employee_ids = []
        self.name = name
        self.roles = roles

    insert_if_not_exist_sql = \
         """INSERT INTO employee (name, role)
            SELECT * FROM (SELECT %s, %s) as tmp
            WHERE NOT EXISTS (
                SELECT name, role FROM employee WHERE name=%s and role=%s
            )"""

    def insert_if_not_exist(self):
        with gamedb.db.cursor() as cu:
            args = zip(repeat(self.name), self.roles,
                       repeat(self.name), self.roles)
            cu.executemany(Employee.insert_if_not_exist_sql, args)
        gamedb.db.commit()
        self.get_ids()

    get_id_sql = \
         """SELECT employee_id FROM employee WHERE name=%s AND role=%s"""

    def get_ids(self):
        with gamedb.db.cursor() as cu:
            argss = zip(repeat(self.name), self.roles)
            cu.executemany(Employee.get_id_sql, argss)
            self.employee_ids = [id_tup[0] for id_tup in cu.fetchall()]

    @staticmethod
    def get_names(infobox: bs4.element.Tag, role_re):
        th = infobox.find(string=role_re)
        if not th:
            return None
        while th.name != 'th':
            th = th.parent

        td = th.next_sibling
        while td.name != 'td':
            td = td.next_sibling

        names = []
        for name in td.strings:
            m = Employee.name_re.search(name)
            if m:
                names.append(m.group(0))

        return names


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
            use_db: Whether or not to use the database.
        """
        self.game_id = None
        self.employees = []
        self.developing_companies = []
        self.publishing_companies = []
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
        if self.in_database and not self.game_id:
            self.get_id()
        return tuple_

    insert_sql = """INSERT INTO game (earliest_release_date, reception, title)
                    VALUES (%s, %s, %s)"""

    def insert_into_database(self):
        with gamedb.db.cursor() as cu:
            cu.execute(Game.insert_sql, (self.earliest_release_date,
                                         self.reception, self.title))
        gamedb.db.commit()
        self.get_id()

    get_id_sql = "SELECT game_id FROM game WHERE title=%s"

    def get_id(self, title: str = None):
        """Get id from database."""
        with gamedb.db.cursor() as cu:
            if not title:
                title = self.title
            cu.execute(Game.get_id_sql, (title,))
            id_ = cu.fetchone()
            if id_:
                self.game_id = id_[0]

    def get_data(self, soup: BeautifulSoup, check_db: bool = False,
                 use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database.
        """
        if use_db:
            self.get_title(soup)
            tuple_ = self.check_database()
            if tuple_:
                if not check_db:
                    self.get_data_from_tuple(tuple_)
            else:
                try:
                    self.get_earliest_release_date(soup)
                except AttributeError:
                    self.earliest_release_date = random_date()
                    logging.warning('Game.get_e_r_d: soup AttributeError')
                try:
                    self.get_employees(soup)
                except AttributeError:
                    self.employees = [Employee('Shigeru Watanabe',
                                               ['Director', 'Producer'])]
                    logging.warning('Game.get_employees: soup AttributeError')
                try:
                    self.get_developing_companies(soup)
                except AttributeError:
                    logging.error('Game.get_d_comp: soup AttributeError')
                try:
                    self.get_publishing_companies(soup)
                except AttributeError:
                    logging.error('Game.get_p_comp: soup AttributeError')
                try:
                    self.get_reception(soup)
                except AttributeError:
                    self.reception = float(random.randint(70, 80))
                    logging.warning('Game.get_reception: soup AttributeError')
        else:
            try:
                self.get_earliest_release_date(soup)
            except AttributeError:
                self.earliest_release_date = random_date()
                logging.warning('Game.get_e_r_d: soup AttributeError')
            try:
                self.get_employees(soup)
            except AttributeError:
                self.employees = \
                    [Employee('Shigeru Watanabe', ['Director', 'Producer'])]
                logging.warning('Game.get_employees: soup AttributeError')
            try:
                self.get_reception(soup)
            except AttributeError:
                self.reception = float(random.randint(70, 80))
                logging.warning('Game.get_reception: soup AttributeError')
            try:
                self.get_title(soup)
            except AttributeError:
                self.title = 'Game Title'
                logging.warning('Game.get_title: soup AttributeError')

    def get_data_from_tuple(self, tuple_):
        self.game_id, self.earliest_release_date, self.reception, self.title \
            = tuple_

    def get_earliest_release_date(self, soup: BeautifulSoup):
        # TODO
        year = random.randint(2000, 2017)
        month = random.randint(1, 12)
        day = random.randint(1, 27)
        self.earliest_release_date = datetime.date(year, month, day)

    def get_employees(self, soup: BeautifulSoup):
        infobox = wiki_infobox(soup)
        for role, role_re in zip(Employee.roles, Employee.role_res):
            names = Employee.get_names(infobox, role_re)
            if not names:
                continue
            new_employees = [Employee(name, [role]) for name in names]
            self.employees.extend(new_employees)

    def get_developing_companies(self, soup: BeautifulSoup):
        infobox = wiki_infobox(soup)
        urls = Company.get_urls(infobox, Company.developing_re)

        for url in urls:
            r = requests.get(url)
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                continue
            company_soup = BeautifulSoup(r.text, 'lxml')

            self.developing_companies.append(Company(company_soup))

    def get_publishing_companies(self, soup: BeautifulSoup):
        infobox = wiki_infobox(soup)
        urls = Company.get_urls(infobox, Company.publishing_re)

        for url in urls:
            r = requests.get(url)
            try:
                r.raise_for_status()
            except requests.exceptions.HTTPError:
                continue
            company_soup = BeautifulSoup(r.text, 'lxml')

            self.publishing_companies.append(Company(company_soup))

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
            use_db: Whether or not to use the database.
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

    check_sql_id = "SELECT * FROM game_release WHERE release_id=%s"
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
        if self.in_database:
            self.get_ids()
        return tuples

    insert_sql = """INSERT INTO game_release (game_id, platform_id, region,
                    release_date, title) VALUES (%s, %s, %s, %s, %s)"""

    def insert_into_database(self):
        for release in self.releases:
            try:
                with gamedb.db.cursor() as cu:
                    cu.execute(GameRelease.insert_sql,
                               (self.game.game_id, release[1].platform_id,
                                release[2], release[3], self.title))
                gamedb.db.commit()
            except pymysql.err.InternalError:
                logging.error(
                    'GameRelease: Attempted to insert NULL in non-NULLable column for {}.'
                    .format(self.title))
        self.get_ids()

    get_id_sql = """SELECT release_id FROM game_release
                    WHERE game_id=%s AND platform_id=%s AND region=%s
                      AND release_date=%s"""

    def get_id(self, index=-1):
        """Get id from database."""
        with gamedb.db.cursor() as cu:
            try:
                release = self.releases[index]
            except IndexError:
                logging.eror('GameRelease.get_id: IndexError for releases')

            cu.execute(GameRelease.get_id_sql,
                       (self.game.game_id, release[1].platform_id, release[2],
                        release[3]))
            id_ = cu.fetchone()
            if id_:
                # Result of wanting to treat a tuple as mutable
                new_release = id_ + self.releases[index][1:]
                self.releases[index] = new_release

    def get_ids(self):
        for i in range(len(self.releases)):
            self.get_id(i)

    def get_data(self, soup: BeautifulSoup, game: Game = Game(),
                 check_db: bool = False, use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database.
        """
        self.game = game
        self.title = game.title
        self.releases = []
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
        infobox = wiki_infobox(soup)
        release_td = infobox.find('th', string='Release').next_sibling \
                                                         .next_sibling
        for td_child in release_td.children:
            if type(td_child) == bs4.element.Tag:
                break
        if td_child.name == 'div' and 'plainlist' in td_child['class']:
            # "Short" style list (https://en.wikipedia.org/wiki/Dark_Souls_III)
            platform_soups = get_platform_soups(soup)
            platforms = map(Platform, platform_soups)

            release_ul = release_td.ul
            for li in release_ul.find_all('li'):
                region = li.span.contents[0].string
                release_date = parse(li.span.next_sibling).date()
                for platform in platforms:
                    if not platform.in_database:
                        platform.insert_into_database()
                    release = (None, platform, region, release_date)
                    self.releases.append(release)
        else:
            # "Long" style list
            if td_child.name == 'div' and 'NavFrame' in td_child['class']:
                # (https://en.wikipedia.org/wiki/Phoenix_Wright:_Ace_Attorney)
                release_li = release_td.li
            elif td_child.name == 'b':
                # (https://en.wikipedia.org/wiki/Super_Mario_World)
                # Because of this, the name release_li is misleading
                release_li = release_td

            platform = None
            for child in release_li.children:
                if child.name == 'b':
                    platform = Platform()
                    platform.name = Platform.name_resolve(child.string)
                    tuple_ = platform.check_database()
                    if tuple_:
                        platform.get_data_from_tuple(tuple_)
                    else:
                        platform_soup = get_platform_soup(soup, platform.name)
                        platform.get_data(platform_soup, use_db=False)
                        platform.insert_into_database()
                elif platform and child.name == 'div' \
                              and 'plainlist' in child['class']:
                    for li in child.find_all('li'):
                        region = li.span.contents[0].string
                        release_date = parse(li.span.next_sibling).date()
                        release = (None, platform, region, release_date)
                        self.releases.append(release)

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
            use_db: Whether or not to use the database.
        """
        self.platform_id = None
        self.in_database = False
        self.company = Company()
        self.discontinued_date = None
        self.generation = None
        self.introductory_price = None
        self.name = None
        self.manufacturers = []
        self.release_date = None
        self.type = None
        if soup:
            self.get_data(soup, check_db, use_db)

    check_sql_name = "SELECT * FROM platform WHERE name=%s"

    def check_database(self):
        """Return database tuple if a tuple with title=self.title is in the
        database, return None otherwise.

        self.in_database is True if such a tuple exists in the database, False
        otherwise.
        """
        if not self.name:
            return None

        with gamedb.db.cursor() as cu:
            cu.execute(Platform.check_sql_name, (self.name,))
            tuple_ = cu.fetchone()

        self.in_database = tuple_ is not None
        if self.in_database and not self.platform_id:
            self.get_id()
        return tuple_

    insert_sql = """INSERT INTO platform (company_id, discontinued_date,
                    generation, introductory_price, name, release_date, type)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    def insert_into_database(self):
        with gamedb.db.cursor() as cu:
            cu.execute(Platform.insert_sql,
                       (self.company.company_id, self.discontinued_date,
                        self.generation, self.introductory_price, self.name,
                        self.release_date, self.type))
        gamedb.db.commit()
        self.get_id()

    get_id_sql = "SELECT platform_id FROM platform WHERE name=%s"

    def get_id(self, name: str = None):
        """Get id from database."""
        with gamedb.db.cursor() as cu:
            if not name:
                name = self.name
            cu.execute(Platform.get_id_sql, (name,))
            id_ = cu.fetchone()
            if id_:
                self.platform_id = id_[0]

    def get_data(self, soup: BeautifulSoup, check_db: bool = False,
                 use_db: bool = True):
        """Get data by using BeautifulSoup to extract HTML elements.

        Args:
            soup: Used to initialize object/check for existence in database.
            check_db: If True, then the object will not be populated if data
                correspoinding to data in soup exists in the database.
                If False, then attempt to populate object.
            use_db: Whether or not to use the database.
            get_name: Whether or not to
        """
        if use_db:
            self.get_name(soup)
            tuple_ = self.check_database()
            if tuple_:
                if not check_db:
                    self.get_data_from_tuple(tuple_)
            else:
                self.get_company(soup)
                self.get_discontinued_date(soup)
                self.get_generation(soup)
                self.get_introductory_price(soup)
                self.get_manufacturers(soup)
                self.get_release_date(soup)
                self.get_type(soup)
        else:
            self.get_company(soup)
            self.get_discontinued_date(soup)
            self.get_generation(soup)
            self.get_introductory_price(soup)
            self.get_name(soup)
            self.get_manufacturers(soup)
            self.get_release_date(soup)
            self.get_type(soup)

    def get_data_from_tuple(self, tuple_):
        self.platform_id, self.company.company_id, self.discontinued_date, \
                self.generation, self.introductory_price, self.name, \
                self.release_date, self.type = tuple_

    company_re = re.compile('Company', re.IGNORECASE)

    def get_company(self, soup: BeautifulSoup):
        # TODO
        infobox = wiki_infobox(soup)
        a = infobox.find('th', string=Platform.company_re)

    def get_discontinued_date(self, soup: BeautifulSoup):
        # TODO
        self.discontinued_date = random_date()

    def get_generation(self, soup: BeautifulSoup):
        # TODO
        pass

    def get_introductory_price(self, soup: BeautifulSoup):
        # TODO
        pass

    def get_name(self, soup: BeautifulSoup):
        self.name = wiki_title(soup)

    def get_manufacturers(self, soup: BeautifulSoup):
        # TODO
        pass

    def get_release_date(self, soup: BeautifulSoup):
        # TODO
        pass

    def get_type(self, soup: BeautifulSoup):
        # TODO
        pass

    @staticmethod
    def name_resolve(name):
        if name == 'SNES':
            return 'Super Nintendo Entertainment System'
        else:
            return name


platform_re = re.compile(r'Platform(\(s\))?', re.IGNORECASE)


def get_platform_soup(game_soup: BeautifulSoup, platform_name: str):
    infobox = wiki_infobox(game_soup)
    th = infobox.find(string=platform_re)
    while th.name != 'th':
        th = th.parent

    td = th.next_sibling
    while td.name != 'td':
        td = td.next_sibling

    a = td.find('a', title=platform_name)
    if not a:
        a = td.find('a', title=re.compile(platform_name, re.IGNORECASE))
        if not a:
            logging.error('get_platform_soup: Could not find a with {}'
                          .format(platform_name))
    platform_url = urljoin(wikipedia_baseurl, a['href'])

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
