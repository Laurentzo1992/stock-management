# Generated by Django 4.1.5 on 2023-02-03 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0005_rename_nom_friendwork_nom_prenom_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="alerte_stock",
            field=models.PositiveIntegerField(default=25),
            preserve_default=False,
        ),
    ]