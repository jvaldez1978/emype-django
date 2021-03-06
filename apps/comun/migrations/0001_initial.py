# Generated by Django 3.1 on 2020-08-09 17:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActividadEconomica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_ciiu', models.CharField(max_length=25, unique=True)),
                ('nombre', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Certificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descricion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Distrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DocumentoIdentidadTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_corto', models.CharField(max_length=10, unique=True)),
                ('nombre_completo', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_documento', models.CharField(max_length=25, unique=True)),
                ('razon_social', models.CharField(max_length=250, unique=True)),
                ('nombre_comercial', models.CharField(max_length=250, unique=True)),
                ('cantidad_trabajadores', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaActividadEconomica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaArchivo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(upload_to='uploads/empresa/principal/documentos/')),
                ('observaciones', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaArchivoTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaCertificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vigencia_desde', models.DateField()),
                ('vigencia_hasta', models.DateField()),
                ('proceso', models.CharField(max_length=100)),
                ('comentarios', models.TextField()),
                ('documento', models.FileField(upload_to='uploads/empresa/certificaciones/documentos/')),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaExperiencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.CharField(max_length=100)),
                ('actividad', models.CharField(max_length=250)),
                ('valor', models.DecimalField(decimal_places=2, max_digits=16)),
                ('inicio', models.DateField()),
                ('fin', models.DateField()),
                ('comentarios', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaExperienciaDocumentacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=250)),
                ('documento', models.FileField(upload_to='uploads/empresa/experiencia/documentos/')),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaInformacionBancaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_cuenta', models.CharField(max_length=50)),
                ('nombre_titular', models.CharField(max_length=100)),
                ('certificado', models.FileField(upload_to='uploads/empresa/infobancaria/certificados/')),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaLocacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direccion', models.TextField()),
                ('telefonos', models.CharField(max_length=25)),
                ('latitud', models.DecimalField(decimal_places=15, max_digits=20)),
                ('longitud', models.DecimalField(decimal_places=15, max_digits=20)),
                ('foto', models.ImageField(upload_to='uploads/empresa/locacion/foto/')),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaLocacionTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaParticipacionAccionaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('porcentaje', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaRedSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaRepresentante',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_documento_identidad', models.CharField(max_length=15)),
                ('vencimiento_documento_identidad', models.DateField()),
                ('pdf_documento_identidad', models.FileField(upload_to='uploads/empresa/representantes/documentos/')),
                ('apellido_paterno', models.CharField(max_length=100)),
                ('apellido_materno', models.CharField(max_length=100)),
                ('nombres', models.CharField(max_length=100)),
                ('correo', models.EmailField(max_length=100)),
                ('telefonos', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaRepresentanteTipo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_corto', models.CharField(max_length=10, unique=True)),
                ('nombre_completo', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_corto', models.CharField(max_length=2, unique=True)),
                ('nombre_completo', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Financiera',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Moneda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_corto', models.CharField(max_length=2, unique=True)),
                ('nombre_completo', models.CharField(max_length=50, unique=True)),
                ('icono', models.ImageField(upload_to='uploads/maestros/paises/iconos/')),
            ],
        ),
        migrations.CreateModel(
            name='PerfilUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RedSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('icono', models.ImageField(upload_to='uploads/maestros/redsocial/iconos/')),
                ('orden', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RegimenRecaudacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoCuentaBancaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoPersona',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TipoSociedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=100, unique=True)),
                ('pais', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='region_pais', to='comun.pais')),
            ],
        ),
        migrations.CreateModel(
            name='Provincia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.CharField(max_length=100, unique=True)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='provincia_region', to='comun.region')),
            ],
        ),
        migrations.CreateModel(
            name='InformacionTributaria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificado', models.FileField(upload_to='uploads/empresa/infotributaria/certificados/')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='it_empresa', to='comun.empresa')),
                ('regimen_recaudacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='it_regimenrecaudacion', to='comun.regimenrecaudacion')),
            ],
        ),
        migrations.CreateModel(
            name='EmpresaUsuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='eu_empresa', to='comun.empresa')),
                ('perfil', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='eu_perfil', to='comun.perfilusuario')),
            ],
        ),
    ]
