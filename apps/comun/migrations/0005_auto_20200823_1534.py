# Generated by Django 3.1 on 2020-08-23 20:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0004_auto_20200809_1424'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.RenameField(
            model_name='empresaexperiencia',
            old_name='actividad',
            new_name='detalle',
        ),
        migrations.RenameField(
            model_name='empresaexperiencia',
            old_name='fin',
            new_name='fecha',
        ),
        migrations.RemoveField(
            model_name='empresaexperiencia',
            name='comentarios',
        ),
        migrations.RemoveField(
            model_name='empresaexperiencia',
            name='inicio',
        ),
        migrations.AddField(
            model_name='empresaexperiencia',
            name='contacto_correo',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresaexperiencia',
            name='contacto_nombre',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='empresaexperiencia',
            name='contacto_telefono',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='empresacertificacion',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='empcert_empresa', to='comun.empresa'),
        ),
        migrations.AlterField(
            model_name='empresaexperiencia',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='empexp_empresa', to='comun.empresa'),
        ),
        migrations.AlterField(
            model_name='empresaexperiencia',
            name='moneda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='empexp_moneda', to='comun.moneda'),
        ),
        migrations.AlterField(
            model_name='empresaexperienciadocumentacion',
            name='empresa_experiencia',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='expexpdoc_empresaexperiencia', to='comun.empresaexperiencia'),
        ),
        migrations.AlterField(
            model_name='empresaparticipacionaccionaria',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='emppartacc_empresa', to='comun.empresa'),
        ),
        migrations.AlterField(
            model_name='empresaparticipacionaccionaria',
            name='empresa_representante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='emppartacc_empresarepresentante', to='comun.empresarepresentante'),
        ),
        migrations.AlterField(
            model_name='empresarepresentante',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='emore_empresa', to='comun.empresa'),
        ),
        migrations.AlterField(
            model_name='informaciontributaria',
            name='empresa',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='inftrib_empresa', to='comun.empresa'),
        ),
        migrations.CreateModel(
            name='EmpresaTags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='et_empresa', to='comun.empresa')),
                ('tags', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='et_tags', to='comun.tags')),
            ],
        ),
    ]
