# Generated by Django 3.1 on 2020-08-09 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0002_auto_20200809_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tiposociedad',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]