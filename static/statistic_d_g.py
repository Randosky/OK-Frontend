import math
import sqlite3
from statistics import mean

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt, ticker


def sort_area_dict(dictionary):
    sorted_tuples = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)[:10]
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict


con = sqlite3.connect("new_vac_with_dif_currencies.db")
cur = con.cursor()
database_length = pd.read_sql("SELECT COUNT(*) From new_vac_with_dif_currencies", con).to_dict()["COUNT(*)"][0]

# Динамика уровня зарплат по годам
s_groups_by_y = pd.read_sql("SELECT years, ROUND(AVG(salary)) From new_vac_with_dif_currencies GROUP BY years", con)
salaries_by_year = dict(s_groups_by_y[["years", "ROUND(AVG(salary))"]].to_dict("split")["data"])

# Динамика количества вакансий по годам
v_groups_by_y = pd.read_sql("SELECT years, COUNT(name) From new_vac_with_dif_currencies GROUP BY years", con)
vacancies_by_year = dict(v_groups_by_y[["years", "COUNT(name)"]].to_dict("split")["data"])

# Динамика уровня зарплат по годам для выбранной профессии
i_v_s_groups_by_y = pd.read_sql("SELECT years, ROUND(AVG(salary)) From new_vac_with_dif_currencies "
                                "WHERE name LIKE '%фронтенд%' "
                                "OR name LIKE '%frontend%' "
                                "OR name LIKE '%вёрстка%' "
                                "OR name LIKE '%верстка%' "
                                "OR name LIKE '%верста%' "
                                "OR name LIKE '%front end%' "
                                "OR name LIKE '%angular%' "
                                "OR name LIKE '%html%' "
                                "OR name LIKE '%css%' "
                                "OR name LIKE '%react%' "
                                "OR name LIKE '%vue%' "
                                "GROUP BY years", con)
inp_vacancy_salary = dict(i_v_s_groups_by_y[["years", "ROUND(AVG(salary))"]].to_dict("split")["data"])

# Динамика количества вакансий по годам для выбранной профессии
i_v_c_groups_by_y = pd.read_sql("SELECT years, COUNT(name) From new_vac_with_dif_currencies "
                                "WHERE name LIKE '%фронтенд%' "
                                "OR name LIKE '%frontend%' "
                                "OR name LIKE '%вёрстка%' "
                                "OR name LIKE '%верстка%' "
                                "OR name LIKE '%верста%' "
                                "OR name LIKE '%front end%' "
                                "OR name LIKE '%angular%' "
                                "OR name LIKE '%html%' "
                                "OR name LIKE '%css%' "
                                "OR name LIKE '%react%' "
                                "OR name LIKE '%vue%' "
                                "GROUP BY years", con)
inp_vacancy_count = dict(i_v_c_groups_by_y[["years", "COUNT(name)"]].to_dict("split")["data"])

# Уровень зарплат по городам (в порядке убывания)
s_a_groups_by_c = pd.read_sql("SELECT area_name, ROUND(AVG(salary)), COUNT(area_name) From new_vac_with_dif_currencies "
                              "GROUP BY area_name "
                              "ORDER BY COUNT(area_name) DESC ", con)

s_a_groups_by_c = s_a_groups_by_c[s_a_groups_by_c["COUNT(area_name)"] >= 0.01 * database_length]
salaries_areas = dict(s_a_groups_by_c[["area_name", "ROUND(AVG(salary))"]].to_dict("split")["data"])
salaries_areas = sort_area_dict(salaries_areas)

# Доля вакансий по городам (в порядке убывания)
v_a_groups_by_c = pd.read_sql("SELECT area_name, COUNT(area_name) From new_vac_with_dif_currencies "
                              "GROUP BY area_name "
                              "ORDER BY COUNT(area_name) DESC "
                              "LIMIT 10", con)
v_a_groups_by_c["COUNT(area_name)"] = round(v_a_groups_by_c["COUNT(area_name)"] / database_length * 100, 2)
vacancies_areas = dict(v_a_groups_by_c[["area_name", 'COUNT(area_name)']].to_dict("split")["data"])

# Доля прочих вакансии
others_df = pd.read_sql("SELECT area_name, COUNT(area_name) From new_vac_with_dif_currencies "
                        "GROUP BY area_name "
                        "ORDER BY COUNT(area_name) DESC "
                        "LIMIT 10, -1", con)
others = round(others_df["COUNT(area_name)"].sum() / database_length * 100, 2)

print("Динамика уровня зарплат по годам:", salaries_by_year)
print("Динамика количества вакансий по годам:", vacancies_by_year)
print("Динамика уровня зарплат по годам для выбранной профессии:", inp_vacancy_salary)
print("Динамика количества вакансий по годам для выбранной профессии:", inp_vacancy_count)
print("Уровень зарплат по городам (в порядке убывания):", salaries_areas)
print("Доля вакансий по городам (в порядке убывания):", vacancies_areas)
print("Доля прочих вакансий", others)

class ReportDemand:
    def __init__(self, vac_name, dicts_by_year):
        self.generate_image(vac_name, dicts_by_year)

    @staticmethod
    def generate_image(vac_name, dicts_by_year):
        x_nums = np.arange(len(dicts_by_year[0].keys()))
        width = 0.4
        x_list1 = x_nums - width / 2
        x_list2 = x_nums + width / 2
        fig = plt.figure()

        ax = fig.add_subplot(211)
        ax.set_title("Уровень зарплат по годам")
        ax.bar(x_list1, dicts_by_year[0].values(), width, label="средняя з/п")
        ax.bar(x_list2, dicts_by_year[1].values(), width, label=f"з/п \n{vac_name.lower()}")
        ax.set_xticks(x_nums, dicts_by_year[0].keys(), rotation="vertical")
        ax.tick_params(axis="both", labelsize=8)
        ax.legend(fontsize=8)
        ax.grid(True, axis="y")

        ax = fig.add_subplot(212)
        ax.set_title("Количество вакансий по годам")
        ax.bar(x_list1, dicts_by_year[2].values(), width, label="Количество вакансий")
        ax.bar(x_list2, dicts_by_year[3].values(), width, label=f"Количество вакансий \n{vac_name.lower()}")
        ax.set_xticks(x_nums, dicts_by_year[2].keys(), rotation="vertical")
        ax.tick_params(axis="both", labelsize=8)
        ax.legend(fontsize=8)
        ax.grid(True, axis="y")

        plt.tight_layout()
        plt.savefig("demand.png")


class ReportGeography:
    def __init__(self, dicts_by_area, vac_with_others):
        self.generate_image(dicts_by_area, vac_with_others)

    @staticmethod
    def generate_image(dicts_by_area, vac_with_others):
        y1_cities = np.arange(len(dicts_by_area[0].keys()))
        y1_cities_names = {}
        for key, value in dicts_by_area[0].items():
            if "-" in key or " " in key:
                key = key.replace("-", "-\n")
                key = key.replace(" ", "\n")
            y1_cities_names[key] = value

        fig = plt.figure()

        ax = fig.add_subplot(211)
        ax.set_title("Уровень зарплат по городам")
        width = 0.8
        ax.barh(y1_cities, dicts_by_area[0].values(), width, align="center")
        ax.set_yticks(y1_cities, labels=y1_cities_names.keys(), horizontalalignment="right", verticalalignment="center")
        ax.tick_params(axis="x", labelsize=8)
        ax.tick_params(axis="y", labelsize=6)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(100000))
        ax.invert_yaxis()
        ax.grid(True, axis="x")

        ax = fig.add_subplot(212)
        ax.set_title("Доля вакансий по городам")
        dicts_by_area[1]["Другие"] = vac_with_others
        ax.pie(dicts_by_area[1].values(), labels=dicts_by_area[1].keys(), textprops={'size': 6},
               colors=["#ff8006", "#28a128", "#1978b5", "#0fbfd0", "#bdbe1c", "#808080", "#e478c3", "#8d554a",
                       "#9567be",
                       "#d72223", "#1978b5", "#ff8006"])
        ax.axis('equal')

        plt.tight_layout()
        plt.savefig("geography.png")


dicts_list_by_year = [salaries_by_year, inp_vacancy_salary, vacancies_by_year, inp_vacancy_count]
dicts_list_by_area = [salaries_areas, vacancies_areas]

report_demand = ReportDemand("Frontend-программист", dicts_list_by_year)
report_geography = ReportGeography(dicts_list_by_area, others)
