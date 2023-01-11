import sqlite3
import pandas as pd


def sort_area_dict(dictionary):
    sorted_tuples = sorted(dictionary.items(), key=lambda item: item[1], reverse=True)[:10]
    sorted_dict = {k: v for k, v in sorted_tuples}
    return sorted_dict


con = sqlite3.connect("new_vac_with_dif_currencies.db")
cur = con.cursor()
database_length = pd.read_sql("SELECT COUNT(*) From new_vac_with_dif_currencies", con).to_dict()["COUNT(*)"][0]

# Динамика уровня зарплат по годам
salaries_by_year = pd.read_sql("SELECT years, ROUND(AVG(salary)) From new_vac_with_dif_currencies GROUP BY years", con)
salaries_by_year.columns = ['years', 'salary']

# Динамика количества вакансий по годам
vacancies_by_year = pd.read_sql("SELECT years, COUNT(name) From new_vac_with_dif_currencies GROUP BY years", con)
vacancies_by_year.columns = ['years', 'count']

# Динамика уровня зарплат по годам для выбранной профессии
inp_vacancy_salary = pd.read_sql("SELECT years, ROUND(AVG(salary)) From new_vac_with_dif_currencies "
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
inp_vacancy_salary.columns = ['years', 'salary_vac']

# Динамика количества вакансий по годам для выбранной профессии
inp_vacancy_count = pd.read_sql("SELECT years, COUNT(name) From new_vac_with_dif_currencies "
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
inp_vacancy_count.columns = ['years', 'count_vac']

# Уровень зарплат по городам (в порядке убывания)
s_a_groups_by_c = pd.read_sql("SELECT area_name, ROUND(AVG(salary)), COUNT(area_name) From new_vac_with_dif_currencies "
                              "GROUP BY area_name "
                              "ORDER BY COUNT(area_name) DESC ", con)

s_a_groups_by_c = s_a_groups_by_c[s_a_groups_by_c["COUNT(area_name)"] >= 0.01 * database_length]
salaries_areas = dict(s_a_groups_by_c[["area_name", "ROUND(AVG(salary))"]].to_dict("split")["data"])
salaries_areas = pd.DataFrame(list(sort_area_dict(salaries_areas).items()), columns=['area_name', 'ROUND(AVG(salary))'])
salaries_areas.columns = ['area_name_sal', 'salary']

# Доля вакансий по городам (в порядке убывания)
vacancies_areas = pd.read_sql("SELECT area_name, COUNT(area_name) From new_vac_with_dif_currencies "
                              "GROUP BY area_name "
                              "ORDER BY COUNT(area_name) DESC "
                              "LIMIT 10", con)
vacancies_areas["COUNT(area_name)"] = round(vacancies_areas["COUNT(area_name)"] / database_length * 100, 2)
vacancies_areas.columns = ['area_name_vac', 'count']

# Доля прочих вакансии
others_df = pd.read_sql("SELECT area_name, COUNT(area_name) From new_vac_with_dif_currencies "
                        "GROUP BY area_name "
                        "ORDER BY COUNT(area_name) DESC "
                        "LIMIT 10, -1", con)
others = round(others_df["COUNT(area_name)"].sum() / database_length * 100, 2)

dicts_list_by_year = salaries_by_year.merge(inp_vacancy_salary,
                                            how="outer").merge(vacancies_by_year,
                                                               how="outer").merge(inp_vacancy_count, how="outer")

dicts_list_by_area = salaries_areas.join(vacancies_areas, how="outer")

dicts_list_by_year["id"] = [i for i in range(len(dicts_list_by_year))]
dicts_list_by_year = dicts_list_by_year[['id'] + [x for x in dicts_list_by_year.columns if x != 'id']]

dicts_list_by_area["id"] = [i for i in range(len(dicts_list_by_area))]
dicts_list_by_area = dicts_list_by_area[['id'] + [x for x in dicts_list_by_area.columns if x != 'id']]

connection = sqlite3.connect("../db.sqlite3")
cursor = connection.cursor()
dicts_list_by_year.to_sql(name="frontend_project_statbyyear", con=connection, if_exists='replace', index=False)
connection.commit()

connection_2 = sqlite3.connect("../db.sqlite3")
cursor_2 = connection_2.cursor()
dicts_list_by_area.to_sql(name="frontend_project_statbyarea", con=connection_2, if_exists='replace', index=False)
connection_2.commit()
