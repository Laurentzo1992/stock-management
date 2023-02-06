# Generated by Django 4.1.5 on 2023-02-02 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0003_alter_product_unit"),
    ]

    operations = [
        migrations.RenameField(
            model_name="producstoct", old_name="pruduct", new_name="product",
        ),
        migrations.AddField(
            model_name="producstoct",
            name="mouvement",
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="product",
            name="stock",
            field=models.PositiveIntegerField(default=200),
            preserve_default=False,
        ),
    ]