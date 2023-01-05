from django.db import models
import math
from statistics import mean
import pandas as pd
import sqlite3


class Profession(models.Model):
    name = models.CharField("Название")
    description = models.TextField("Описание")
    s_cur_to_digits = {"BYR": 1, "USD": 2, "EUR": 3, "KZT": 4, "UAH": 5}

    def __init__(self, *args, **kwargs):
        self.df = pd.read_csv("C:\\Users\\bosso\\PycharmProjects\\djangoProject\\static\\vacancies_with_skills.csv")
        self.con = sqlite3.connect("CB_Currency.db")
        self.cur = self.con.cursor()
        super().__init__(*args, **kwargs)


    def get_salary(self, s_from, s_to, s_cur, date):
        year_month = date[1] + "/" + date[0]
        s_cur_value = 0

        if s_cur != "RUR" and (s_cur == s_cur) and s_cur in ["BYN", "BYR", "EUR", "KZT", "UAH", "USD"]:
            s_cur.replace("BYN", "BYR")
            self.cur.execute("SELECT * FROM CB_Currency WHERE date == :year_month", {"year_month": year_month})
            s_cur_value = self.cur.fetchall()[0][self.s_cur_to_digits[s_cur]]
        elif s_cur == "RUR":
            s_cur_value = 1

        if math.isnan(s_from) and not (math.isnan(s_to)):
            return s_to * s_cur_value
        elif not (math.isnan(s_from)) and math.isnan(s_to):
            return s_from * s_cur_value
        elif not (math.isnan(s_from)) and not (math.isnan(s_to)):
            return mean([s_from, s_to]) * s_cur_value

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Профессия"
        verbose_name_plural = "Профессии"
