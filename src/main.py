#!/usr/bin/python3
import re
import os
import requests
import json
from typing import Callable, Optional
from lxml import html
from csvwriter import CsvWriter

data_dir = f"{os.path.dirname(os.path.realpath(__file__))}".replace("src", "data")
csv_path = data_dir + '/data.csv'
json_path = data_dir + '/data.json'

class LanguageDetails(object):
    def __init__(self, name: str, native_name: str, iso_code: str):
        self.name = name
        self.native_name = native_name
        self.iso_code = iso_code

def parse_name(string: str) -> str:
    names = string.split(',')
    name = names[0]
    cleaned = re.sub(r'\s*\(.*?\)', '', name)
    return cleaned

def parse_native_name(string: str) -> str:
    names = string.split(';')
    name = names[0]
    cleaned = re.sub(r'\s*\(.*?\)', '', name)
    return cleaned

def get_cell_text(cells: list, index: int, parser: Optional[Callable[[str], str]]) -> str:
    cell = cells[index]
    for style in cell.xpath('.//style'):
        style.getparent().remove(style)
    text = cell.text_content().strip()
    if parser:
        text = parser(text)
    return text

def get_language_details() -> list:
    res = requests.get('https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes')
    content = html.fromstring(res.content)

    languages = []
    table = content.xpath('.//table[@id="Table"]')[0]
    for row in table.cssselect('tr'):
        cells = row.cssselect('td')
        if len(cells) == 0:
            continue
        if len(cells) == 10:
            native_name = get_cell_text(cells, 7, parse_native_name)
        else:
            native_name = get_cell_text(cells, 6, parse_native_name)
        name = get_cell_text(cells, 0, parse_name)
        iso_code = get_cell_text(cells, 1, None)
        languages.append(LanguageDetails(name, native_name, iso_code))
    return languages;

def write_csv(file_path: str, languages: list):
    with open(file_path, 'w+') as file:
        writer = CsvWriter(file)
        writer.write_row("name", "native name", "iso code")
        for language in languages:
            writer.write_row(language.name, language.native_name, language.iso_code)

def write_json(file_path: str, languages: list):
    with open(json_path, 'w+') as file:
        to_write = []
        for language in languages:
            to_write.append({'name': language.name, 'nativeName': language.native_name, 'isoCode': language.iso_code})
        json.dump(to_write, file, ensure_ascii=False)


print("Getting language info from Wikipedia")
languages = get_language_details()

print("Writing csv file")
write_csv(csv_path, languages)

print("Writing json file")
write_json(json_path, languages)
