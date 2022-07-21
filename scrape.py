import requests
from bs4 import BeautifulSoup
from numpy import nan
import csv
import re
import pandas as pd

url = "https://en.wikipedia.org/wiki/Transistor_count"
# webページデータを取得
page = requests.get(url)
# htmlをパース
soup = BeautifulSoup(page.text, 'html.parser')

tables = soup.find_all(class_="wikitable", limit=2) 
table = tables[1].tbody
rows = table.find_all('tr')
columns = [v.text.replace('\n', '') for v in rows[0].find_all('th')]
df = pd.DataFrame(columns=columns)
for i in range(len(rows)):
    tds = rows[i].find_all('td')
    if len(tds) == len(columns):
        values = [ td.text.replace('\n', '').replace('\xa0', ' ') for td in tds ]
        df = df.append(pd.Series(values, index=columns), ignore_index=True)

df = df.replace(re.compile(r'\[.*?\]'), '', regex=True)\
        .replace(re.compile(r'\(.*?\)'), '', regex=True)\
        .replace('?', nan, regex=False)

int_list = ['MOS transistor count', 'Transistor density, tr./mm2'] 
df[int_list] = df[int_list].replace(re.compile(r"\D"), '', regex=True)

df.to_csv('data/processor.csv')
