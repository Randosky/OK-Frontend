import re

import requests
from django.shortcuts import render
from frontend_project.models import Profession, StatByYear, StatByArea, StatBySkills


def show_page(request):
    data = {"profession": Profession.objects.get(id=1)}
    return render(request, "information.html", data)


def show_demand_page(request):
    data = {"stat_by_year": StatByYear.objects.all()}
    return render(request, "demand.html", data)


def show_geography_page(request):
    data = {"stat_by_area": StatByArea.objects.all()}
    return render(request, "geography.html", data)


def show_skills_page(request):
    all_data = {}
    data = []
    for year in range(2015, 2022):
        all_data[year] = {}
    for i, objects in enumerate(StatBySkills.objects.all()):
        if i % 10 == 0:
            data = []
            all_data[objects.published_at] = data
        data.append(objects)

    data = {"stat_by_skills": all_data}
    return render(request, "skills.html", data)


def parse_html(info):
    info = re.sub('<.*?>', '', info)
    info = info.replace("\r\n", "\n")
    res = [' '.join(word.split()) for word in info.split('\n')]
    return res[0] if len(res) == 1 else res


def show_vacancies_page(request):
    url = "https://api.hh.ru/vacancies/73507648/similar_vacancies?date_from=2022-12-07T01:00:00&date_to=2022-12-07T23:59:00"
    vacancies_list = []
    pages = requests.get(url).json()
    for page in range(pages["pages"] + 1):
        if pages["per_page"] < 100:
            params = {'page': page}
        else:
            params = {'per_page': '100', 'page': page}
        vacancies_response = requests.get(url, params=params)
        vacancies_json = vacancies_response.json()
        vacancies_items = vacancies_json["items"]
        for vacancy in vacancies_items:
            try:
                vacancies_list.append(vacancy)
            except TypeError:
                continue

    vacancy_items = []
    for vacancy in vacancies_list:
        salary = "Не указано на сайте HH.ru"
        if type(vacancy["salary"]).__name__ != "NoneType":
            if type(vacancy["salary"]["from"]).__name__ != "NoneType" and type(
                    vacancy["salary"]["to"]).__name__ == "NoneType":
                salary = vacancy["salary"]["from"]
            elif type(vacancy["salary"]["from"]).__name__ == "NoneType" and type(
                    vacancy["salary"]["to"]).__name__ != "NoneType":
                salary = vacancy["salary"]["to"]
            else:
                salary = (vacancy["salary"]["from"] + vacancy["salary"]["to"]) / 2

        get_url = f"https://api.hh.ru/vacancies/{vacancy['id']}"
        vacancy_info = requests.get(get_url).json()
        skills = ", ".join([skill["name"] for skill in vacancy_info["key_skills"]])

        vacancy_items.append([vacancy["published_at"], vacancy["area"]["name"], salary, vacancy["employer"]["name"],
                              skills, parse_html(vacancy_info["description"]), vacancy["name"]])

        vacancy_items = sorted(vacancy_items, key=lambda v: v[0])
        data = {"vac": vacancy_items}
    return render(request, "vacancies.html", data)
