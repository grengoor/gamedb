#!/usr/bin/python3


def generate_unique_id():
    # TODO
    return None


class Game:
    def __init__(self, soup=None):
        self.game_id = generate_unique_id()
        self.earliest_release_date = None
        self.reception = None
        self.title = None
        if soup is not None:
            self.get_data(soup)

    # Get data by using BeautifulSoup to extract HTML elements
    def get_data(self, soup):
        self.get_earliest_release_date(soup)
        self.get_reception(soup)
        self.get_title(soup)

    def get_earliest_release_date(self, soup):
        # TODO
        pass

    def get_reception(self, soup):
        table = soup.body.find('div', id='content') \
                         .find('div', id='bodyContent') \
                         .find('div', id='mw-content-text') \
                         .find('div', attrs={'class': 'mw-parser-output'}) \
                         .find('th', string='Aggregate score').parent.parent
        score_str = table.find('a', string='Metacritic').parent.next_sibling \
                         .next_sibling.sup.previous_sibling
        # TODO: scan the string for rating

    def get_title(self, soup):
        self.title = soup.body.find('div', id='content') \
                              .find('h1', id='firstHeading').i.string
        print(self.title)
