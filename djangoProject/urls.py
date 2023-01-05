"""djangoProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from frontend_project.views import show_page, show_demand_page, show_geography_page, show_skills_page, \
    show_vacancies_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', show_page),
    path('demand.html', show_demand_page),
    path('geography.html', show_geography_page),
    path('skills.html', show_skills_page),
    path('vacancies.html', show_vacancies_page),
    path("information.html", show_page)
]
