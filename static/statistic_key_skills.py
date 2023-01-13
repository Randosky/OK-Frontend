import csv
import re
import os
import sqlite3

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def quick_quit(msg):
    print(msg)
    exit(0)


class DataSet:
    def __init__(self, file_name):
        if os.stat(file_name).st_size == 0:
            quick_quit("Пустой файл")

        self.data = [row for row in csv.reader(open(file_name, encoding="utf_8_sig"))]
        self.names = self.data[0]
        self.all_data = [row for row in self.data[1:] if len(row) == len(self.names) and row.count('') == 0]

        if len(self.all_data) == 0:
            quick_quit('Нет данных')


class Vacancy:
    name: str
    key_skills: str or list
    salary_from: int or float
    salary_to: int or float
    salary_currency: str
    area_name: str
    published_at: str or int

    def __init__(self, pers_data):
        for name, item in pers_data.items():
            self.__setattr__(name, self.formatter(name, item))

    @staticmethod
    def formatter(key, value):
        if key == 'key_skills' and type(value) == list:
            return value
        else:
            return value


def parse_html(info):
    info = re.sub('<.*?>', '', info)
    info = info.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in info.split('\n')]
    return res[0] if len(res) == 1 else res


def sort_area_dict(dictionary):
    sorted_tuples = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)[:10]
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict


dataset = DataSet("vacancies_with_skills.csv")
(names, all_vac_data) = dataset.names, dataset.all_data

pd.set_option("expand_frame_repr", False)
df = pd.DataFrame(columns=["published_at", "key_skills", "count"])
all_skills = {}
for year in range(2015, 2023):
    all_skills[year] = {}

for data in all_vac_data:
    parsed_data = Vacancy(dict(zip(names, map(parse_html, data))))
    if 'frontend' in parsed_data.name or 'фронтенд' in parsed_data.name or 'вёрстка' in parsed_data.name or 'верстка' in parsed_data.name or 'верста' in parsed_data.name or 'front end' in parsed_data.name or 'angular' in parsed_data.name or 'html' in parsed_data.name or 'css' in parsed_data.name or 'react' in parsed_data.name or 'vue' in parsed_data.name:
        for year in range(2015, 2023):
            if year == int(parsed_data.published_at[:4]):
                for skill in parsed_data.key_skills:
                    if skill in all_skills[year].keys():
                        all_skills[year][skill] += 1
                    else:
                        all_skills[year][skill] = 0

for year in range(2015, 2023):
    all_skills[year] = sort_area_dict(all_skills[year])
    for i, skill in enumerate(all_skills[year]):
        df.loc[len(df.index)] = [year, list(all_skills[year].keys())[i], list(all_skills[year].values())[i]]

df["id"] = [i for i in range(len(df))]
df = df[['id'] + [x for x in df.columns if x != 'id']]


connection = sqlite3.connect("../db.sqlite3")
cursor = connection.cursor()
df.to_sql(name="frontend_project_statbyskills", con=connection, if_exists='replace', index=False)
connection.commit()