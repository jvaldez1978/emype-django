# Generated by Django 3.1 on 2020-09-03 17:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0013_documentaciontipo_empresadocumentacion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empresadocumentacion',
            old_name='documento',
            new_name='archivo',
        ),
    ]
