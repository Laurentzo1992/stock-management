# Generated by Django 4.1.5 on 2023-02-01 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(model_name="product", name="description",),
    ]