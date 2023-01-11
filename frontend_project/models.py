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
