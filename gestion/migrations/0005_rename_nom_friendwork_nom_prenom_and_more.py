# Generated by Django 4.1.5 on 2023-02-03 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0004_rename_pruduct_producstoct_product_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="friendwork", old_name="nom", new_name="nom_prenom",
        ),
        migrations.RemoveField(model_name="friendwork", name="prenom",),
    ]
