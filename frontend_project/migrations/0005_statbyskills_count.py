# Generated by Django 4.1.5 on 2023-01-13 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend_project', '0004_remove_statbyskills_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='statbyskills',
            name='count',
            field=models.IntegerField(default=2, verbose_name='Частота появления'),
            preserve_default=False,
        ),
    ]