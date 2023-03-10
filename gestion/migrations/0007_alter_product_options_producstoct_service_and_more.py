# Generated by Django 4.1.5 on 2023-02-04 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("gestion", "0006_product_alerte_stock"),
    ]

    operations = [
        migrations.AlterModelOptions(name="product", options={"ordering": ["code"]},),
        migrations.AddField(
            model_name="producstoct",
            name="Service",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="gestion.services",
                verbose_name="services",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="producstoct",
            name="demandeur",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="gestion.friendwork",
                verbose_name="Demandeurs",
            ),
            preserve_default=False,
        ),
    ]
