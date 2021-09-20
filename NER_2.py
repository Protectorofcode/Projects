import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import csv
import sqlite3
import json
import re

#Имена
from natasha import NamesExtractor
from natasha.markup import show_markup, show_json

extractor = NamesExtractor()

text = '''
Благодарственное письмо   Хочу поблагодарить учителей моего, теперь уже бывшего, одиннадцатиклассника:  Бушуева Вячеслава Владимировича и Бушуеву Веру Константиновну. Они вовлекали сына в интересные внеурочные занятия, связанные с театром и походами.

Благодарю прекрасного учителя 1"А" класса - Волкову Наталью Николаевну, нашего наставника, тьютора - Ларису Ивановну, за огромнейший труд, чуткое отношение к детям, взаимопонимание! Огромное спасибо!
'''
matches = extractor(text)
spans = [_.span for _ in matches]
facts = [_.fact.as_json for _ in matches]
show_markup(text, spans)
show_json(facts)

print(facts[1]['first'])
print(facts[1]['middle'])

#Геолокация
GEO = rule(
    and_(
        gram('NOUN')
    ),
    and_(
        gram('NOUN')
    ),
    gram('ADJF').optional().repeatable(),
    dictionary({
        'федерация',
        'республика',
        'край'
    })
)

text = 'Отправить отчет в краснодарский край'
parser = Parser(GEO)
facts = []

for match in parser.findall(text):
    facts.extend(_.value for _ in match.tokens)

facts

#Личности
from yargy.interpretation import fact
from yargy.pipelines import morph_pipeline
from yargy.predicates import gram

from natasha import (
    NamesExtractor,
    AddressExtractor,
    DatesExtractor,
    MoneyExtractor
)

Person = fact(
    'Person',
    ['position', 'name']
)
Name = fact(
    'Name',
    ['first', 'last']
)


POSITION = morph_pipeline([
    'начальника',
    'президент'
])

NAME = rule(
    gram('Name').interpretation(
        Name.first.inflected()
    ),
    gram('Surn').interpretation(
        Name.last.inflected()
    )
).interpretation(
    Name
)

PERSON = rule(
    POSITION.interpretation(
        Person.position.inflected()
    ),
    NAME.interpretation(
        Person.name
    )
).interpretation(
    Person
)



parser = Parser(PERSON)
text = '''
12 марта по приказу начальника Сергея Иванова ...
'''


facts = []

for match in parser.findall(text):
        facts.extend(_.value for _ in match.tokens)

facts

from yargy import or_
from yargy.predicates import caseless, normalized, dictionary

#Даты

MONTHS = {
    'январь',
    'февраль',
    'март',
    'апрель',
    'мая',
    'июнь',
    'июль',
    'август',
    'сентябрь',
    'октябрь',
    'ноябрь',
    'декабрь'
}
MONTH_NAME = dictionary(MONTHS)
YEAR_WORDS = or_(
    rule(caseless('г'), '.'),
    rule(normalized('год'))
)

DAY = and_(
    gte(1),
    lte(31)
)
MONTH = and_(
    gte(1),
    lte(12)
)
YEAR = and_(
    gte(1),
    lte(2018)
)

DATE = or_(
    rule(
        YEAR,
        '-',
        MONTH,
        '-',
        DAY
    ),
    rule(
        DAY,
        MONTH_NAME,
        YEAR,
        YEAR_WORDS.optional()
    )
)

parser = Parser(DATE)
text = '''
8 января 2014 года, 15 июня 2001 г.,
31 февраля 2018'''

dates = []

for match in parser.findall(text):
        dates.extend(_.value for _ in match.tokens)

dates

#Какие-то специфичные вещи, например компьютер
text = "У меня сломался комп модели Lenovo 3. Что делать?"

from yargy import rule, and_, Parser
from yargy.predicates import gte, lte

from yargy.predicates import gram, is_capitalized, dictionary

PC = rule(
    and_(
        gram('VERB')  
                     
    ),
    dictionary({
        'комп',
        'компьютер',
        'Lenovo'
    }),
    and_(
        gram('NOUN'),   
    ),
    dictionary({
        'Lenovo'
    })
)

parser = Parser(PC)
facts = []

for match in parser.findall(text):
    facts.extend(_.value for _ in match.tokens)

facts  

facts[1]
pr = ‘%’ + facts[1] + ‘%’

f = open('ExampleDataset.csv')
csv_reader = csv.reader(f, delimiter=';')


con = sqlite3.Connection('newdb.sqlite')

cur = con.cursor()

cur.execute('CREATE TABLE "stuff" ("Text" varchar(12), "Category" varint(12), "Solution" varchar(12));')
# cur.execute("DROP TABLE stuff")

cur.executemany('INSERT INTO stuff VALUES (?, ?, ?)', csv_reader)
con.commit()

cur.execute("SELECT * FROM stuff ")
print(cur.fetchall())

cur.execute("SELECT Solution from stuff WHERE Text LIKE (?)", (word,))
pr = cur.fetchall()
str1 =  str(pr[1])

str1 = re.sub('[\\\\\'[\]!"$%&()*+,-./:;<=>?@^_`{|}~«»\n]', '', str1)

print(str1)
