# Generated by Django 4.1.5 on 2023-02-01 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0002_remove_product_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="unit",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="gestion.unite"
            ),
        ),
    ]
