# Generated by Django 4.1.5 on 2023-01-13 14:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('frontend_project', '0003_alter_statbyskills_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='statbyskills',
            name='name',
        ),
    ]
