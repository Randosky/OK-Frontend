from django.shortcuts import render
from frontend_project.models import Profession


def show_page(request):
    data = {"profession": Profession.objects.get(id=1)}
    return render(request, "information.html", data)
