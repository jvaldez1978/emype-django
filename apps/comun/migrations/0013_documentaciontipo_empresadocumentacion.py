# Generated by Django 3.1 on 2020-09-03 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comun', '0012_remove_empresarepresentante_vencimiento_documento_identidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentacionTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaDocumentacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('documento', models.FileField(upload_to='uploads/empresa/documentacion/documentos/')),
                ('documentacion_tipo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='empdoc_documentaciontipo', to='comun.documentaciontipo')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='empdoc_empresa', to='comun.empresa')),
            ],
        ),
    ]