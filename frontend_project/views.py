from django.shortcuts import render
from frontend_project.models import Profession


def show_page(request):
    data = {"profession": Profession.objects.get(id=1)}
    return render(request, "information.html", data)


def show_demand_page(request):
    return render(request, "demand.html")


def show_geography_page(request):
    return render(request, "geography.html")


def show_skills_page(request):
    return render(request, "skills.html")


def show_vacancies_page(request):
    return render(request, "vacancies.html")
