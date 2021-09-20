import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from pandas import DataFrame, Series

import csv
import sqlite3
import json
import re

#�����
from natasha import NamesExtractor
from natasha.markup import show_markup, show_json

extractor = NamesExtractor()

text = '''
���������������� ������   ���� ������������� �������� �����, ������ ��� �������, ��������������������:  ������� ��������� ������������� � ������� ���� ��������������. ��� ��������� ���� � ���������� ���������� �������, ��������� � ������� � ��������.

��������� ����������� ������� 1"�" ������ - ������� ������� ����������, ������ ����������, ������� - ������ ��������, �� ����������� ����, ������ ��������� � �����, ���������������! �������� �������!
'''
matches = extractor(text)
spans = [_.span for _ in matches]
facts = [_.fact.as_json for _ in matches]
show_markup(text, spans)
show_json(facts)

print(facts[1]['first'])
print(facts[1]['middle'])

#����������
GEO = rule(
    and_(
        gram('NOUN')
    ),
    and_(
        gram('NOUN')
    ),
    gram('ADJF').optional().repeatable(),
    dictionary({
        '���������',
        '����������',
        '����'
    })
)

text = '��������� ����� � ������������� ����'
parser = Parser(GEO)
facts = []

for match in parser.findall(text):
    facts.extend(_.value for _ in match.tokens)

facts

#��������
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
    '����������',
    '���������'
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
12 ����� �� ������� ���������� ������ ������� ...
'''


facts = []

for match in parser.findall(text):
        facts.extend(_.value for _ in match.tokens)

facts

from yargy import or_
from yargy.predicates import caseless, normalized, dictionary

#����

MONTHS = {
    '������',
    '�������',
    '����',
    '������',
    '���',
    '����',
    '����',
    '������',
    '��������',
    '�������',
    '������',
    '�������'
}
MONTH_NAME = dictionary(MONTHS)
YEAR_WORDS = or_(
    rule(caseless('�'), '.'),
    rule(normalized('���'))
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
8 ������ 2014 ����, 15 ���� 2001 �.,
31 ������� 2018'''

dates = []

for match in parser.findall(text):
        dates.extend(_.value for _ in match.tokens)

dates

#�����-�� ����������� ����, �������� ���������
text = "� ���� �������� ���� ������ Lenovo 3. ��� ������?"

from yargy import rule, and_, Parser
from yargy.predicates import gte, lte

from yargy.predicates import gram, is_capitalized, dictionary

PC = rule(
    and_(
        gram('VERB')  
                     
    ),
    dictionary({
        '����',
        '���������',
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
pr = �%� + facts[1] + �%�

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

str1 = re.sub('[\\\\\'[\]!"$%&()*+,-./:;<=>?@^_`{|}~��\n]', '', str1)

print(str1)
