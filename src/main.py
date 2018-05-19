#!/usr/bin/python3
import requests
from lxml import html


class LanguageDetails(object):

    def __init__(self, family, name, native_name, iso_code, notes):
        self.family = family
        self.name = name
        self.native_name = native_name
        self.iso_code = iso_code
        self.notes = notes


def get_cell_text(cells, index):
    return cells[index].text_content().strip()


res = requests.get('https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes')
content = html.fromstring(res.content)

languages = []
table = content.get_element_by_id('Table')
for row in table.cssselect('tr'):
    cells = row.cssselect('td')
    if len(cells) == 0:
        continue
    languages.append(LanguageDetails(get_cell_text(cells, 1),
                                     get_cell_text(cells, 2),
                                     get_cell_text(cells, 3),
                                     get_cell_text(cells, 4),
                                     get_cell_text(cells, 8)))

for lang in languages:
    print('{}, {}, {}'.format(lang.name, lang.native_name, lang.notes))
