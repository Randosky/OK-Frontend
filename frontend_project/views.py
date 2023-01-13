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


def show_vacancies_page(request):
    return render(request, "vacancies.html")
