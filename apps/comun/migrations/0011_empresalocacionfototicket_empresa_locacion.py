# Generated by Django 3.1 on 2020-09-01 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0010_auto_20200901_0148'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresalocacionfototicket',
            name='empresa_locacion',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='elft_empresalocacion', to='comun.empresalocacion'),
            preserve_default=False,
        ),
    ]
