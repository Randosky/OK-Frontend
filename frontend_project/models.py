from django.db import models
import math
from statistics import mean
import pandas as pd
import sqlite3


class Profession(models.Model):
    name = models.CharField("Название", max_length=40)
    description = models.TextField("Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"


class StatByYear(models.Model):
    years = models.IntegerField("Год")
    salary = models.FloatField("Средняя зарплата")
    salary_vac = models.FloatField("Средняя зарплата - Frontend-программист")
    count = models.FloatField("Количество вакансий")
    count_vac = models.FloatField("Количество вакансий - Frontend-программист")

    class Meta:
        verbose_name = "Статистика по годам"
        verbose_name_plural = "Статистик по годам"


class StatByArea(models.Model):
    area_name_sal = models.CharField("Город", max_length=40)
    salary = models.FloatField("Уровень зарплат")
    area_name_vac = models.CharField("Город", max_length=40)
    count = models.FloatField("Доля вакансий")

    class Meta:
        verbose_name = "Статистика по городам"
        verbose_name_plural = "Статистик по городам"
