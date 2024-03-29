# Generated by Django 3.1.7 on 2023-07-06 21:40

import adminapp.models.empresa
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CiudadadPermitida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eliminado', models.BooleanField(default=False, help_text='Parametro que nos dira si el objeto a sido eleminado o no')),
                ('modificable', models.BooleanField(default=True, help_text='Parametro que nos dira si el registro puede ser modificado o no')),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha en el que el registro fue creado')),
                ('fecha_de_modificacion', models.DateTimeField(auto_now=True, help_text='Fecha en el que el registro fue modifcado', null=True)),
                ('description', models.CharField(help_text='Ciudada permitida Description', max_length=100)),
                ('usuario_creo', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que creo el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ciudadadpermitida_con_relacion_a_usuariocreo', to=settings.AUTH_USER_MODEL)),
                ('usuario_elimino', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que elimino el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ciudadadpermitida_con_relacion_a_usuarioelimino', to=settings.AUTH_USER_MODEL)),
                ('usuario_modifico', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que modifico el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='ciudadadpermitida_con_relacion_a_usuariomodifico', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eliminado', models.BooleanField(default=False, help_text='Parametro que nos dira si el objeto a sido eleminado o no')),
                ('modificable', models.BooleanField(default=True, help_text='Parametro que nos dira si el registro puede ser modificado o no')),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha en el que el registro fue creado')),
                ('fecha_de_modificacion', models.DateTimeField(auto_now=True, help_text='Fecha en el que el registro fue modifcado', null=True)),
                ('cantidad_empresas', models.PositiveIntegerField(default=5)),
                ('vencimiento', models.DateField(null=True)),
                ('cantidad_movimientos', models.PositiveIntegerField(default=500, null=True)),
                ('timbres_restantes', models.PositiveIntegerField(default=0)),
                ('timbres_usados', models.PositiveIntegerField(default=0)),
                ('invitado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='invitado_por', to=settings.AUTH_USER_MODEL)),
                ('usuario', models.OneToOneField(blank=True, default=None, help_text='Fk a usuario para conocer el usuario que propietario de la cuenta', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='relacion_cuenta_de_usuario', to=settings.AUTH_USER_MODEL)),
                ('usuario_creo', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que creo el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cuenta_con_relacion_a_usuariocreo', to=settings.AUTH_USER_MODEL)),
                ('usuario_elimino', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que elimino el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cuenta_con_relacion_a_usuarioelimino', to=settings.AUTH_USER_MODEL)),
                ('usuario_modifico', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que modifico el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cuenta_con_relacion_a_usuariomodifico', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PaymentWithMercadoPago',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eliminado', models.BooleanField(default=False, help_text='Parametro que nos dira si el objeto a sido eleminado o no')),
                ('modificable', models.BooleanField(default=True, help_text='Parametro que nos dira si el registro puede ser modificado o no')),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha en el que el registro fue creado')),
                ('fecha_de_modificacion', models.DateTimeField(auto_now=True, help_text='Fecha en el que el registro fue modifcado', null=True)),
                ('action', models.CharField(blank=True, max_length=255, null=True)),
                ('api_version', models.CharField(blank=True, max_length=10, null=True)),
                ('data', models.JSONField(blank=True, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('data_id', models.BigIntegerField(blank=True, null=True, unique=True)),
                ('live_mode', models.BooleanField(blank=True, default=False, null=True)),
                ('payment_type', models.CharField(blank=True, max_length=255, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=255, null=True)),
                ('user_id', models.CharField(help_text='Es lo mismo que collector_id y preference_id', max_length=255)),
                ('coupon_code', models.CharField(blank=True, max_length=255, null=True)),
                ('coupon_labels', models.CharField(blank=True, max_length=255, null=True)),
                ('date_of_expiration', models.DateTimeField(blank=True, null=True)),
                ('expiration_date_from', models.DateTimeField(blank=True, null=True)),
                ('expiration_date_to', models.DateTimeField(blank=True, null=True)),
                ('expires', models.BooleanField(blank=True, default=False, null=True)),
                ('external_reference', models.CharField(blank=True, max_length=255, null=True)),
                ('init_point', models.URLField(blank=True, null=True)),
                ('internal_metadata', models.JSONField(blank=True, null=True)),
                ('items', models.JSONField(blank=True, null=True)),
                ('nueva_orden', models.JSONField(blank=True, null=True)),
                ('pagado', models.BooleanField(default=False)),
                ('usuario_creo', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que creo el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='paymentwithmercadopago_con_relacion_a_usuariocreo', to=settings.AUTH_USER_MODEL)),
                ('usuario_elimino', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que elimino el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='paymentwithmercadopago_con_relacion_a_usuarioelimino', to=settings.AUTH_USER_MODEL)),
                ('usuario_modifico', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que modifico el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='paymentwithmercadopago_con_relacion_a_usuariomodifico', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HorarioAcceso',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eliminado', models.BooleanField(default=False, help_text='Parametro que nos dira si el objeto a sido eleminado o no')),
                ('modificable', models.BooleanField(default=True, help_text='Parametro que nos dira si el registro puede ser modificado o no')),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha en el que el registro fue creado')),
                ('fecha_de_modificacion', models.DateTimeField(auto_now=True, help_text='Fecha en el que el registro fue modifcado', null=True)),
                ('hora_inicio', models.TimeField()),
                ('hora_fin', models.TimeField()),
                ('usuario_creo', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que creo el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='horarioacceso_con_relacion_a_usuariocreo', to=settings.AUTH_USER_MODEL)),
                ('usuario_elimino', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que elimino el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='horarioacceso_con_relacion_a_usuarioelimino', to=settings.AUTH_USER_MODEL)),
                ('usuario_modifico', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que modifico el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='horarioacceso_con_relacion_a_usuariomodifico', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eliminado', models.BooleanField(default=False, help_text='Parametro que nos dira si el objeto a sido eleminado o no')),
                ('modificable', models.BooleanField(default=True, help_text='Parametro que nos dira si el registro puede ser modificado o no')),
                ('fecha_de_creacion', models.DateTimeField(auto_now_add=True, help_text='Fecha en el que el registro fue creado')),
                ('fecha_de_modificacion', models.DateTimeField(auto_now=True, help_text='Fecha en el que el registro fue modifcado', null=True)),
                ('rfc', models.CharField(blank=True, max_length=13, null=True, unique=True, validators=[django.core.validators.RegexValidator(message='El formato del RFC no es correcto. Ej. XAXX010101000', regex='^([A-Z&Ññ]{3,4}|[A-Z][AEIOU][A-Z]{2})\\d{2}((01|03|05|07|08|10|12)(0[1-9]|[12]\\d|3[01])|02(0[1-9]|[12]\\d)|(04|06|09|11)(0[1-9]|[12]\\d|30))([A-Z0-9]{2}[0-9A])?$')])),
                ('razon_social', models.CharField(db_index=True, max_length=250, verbose_name='Razón social *')),
                ('nombre_comercial', models.CharField(db_index=True, max_length=200, verbose_name='Nombre comercial *')),
                ('cer', models.FileField(blank=True, null=True, upload_to='administracion/efirma')),
                ('key', models.FileField(blank=True, null=True, upload_to='administracion/efirma')),
                ('contrasena', models.CharField(blank=True, max_length=20, null=True)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('logo', models.ImageField(blank=True, help_text='Su imagen se re-dimensionara (200px~100px)', null=True, upload_to=adminapp.models.empresa.upload_to)),
                ('sdk_private', models.CharField(blank=True, default=None, max_length=100, null=True, unique=True)),
                ('sdk_public', models.CharField(blank=True, default=None, max_length=100, null=True, unique=True)),
                ('nombre_para_pagos', models.CharField(db_index=True, max_length=200, null=True, verbose_name='Nombre con el que accederán los clientes de esta empresa*')),
                ('ciudades_permitidas', models.ManyToManyField(blank=True, help_text='Ciudades permitidas a las que pertenece la empresa', related_name='relacion_ciudades_permitidas_a_empresa', to='adminapp.CiudadadPermitida')),
                ('cuenta', models.ForeignKey(blank=True, help_text='Fk a cuenta de usuario a la que pertenece la empresa', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='relacion_cuenta_a_empresa', to='adminapp.cuenta')),
                ('horario_de_acceso', models.ForeignKey(blank=True, default=None, help_text='Horario de acceso al portal del cliente.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='horarios_acceso', to='adminapp.horarioacceso')),
                ('usuario_creo', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que creo el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='empresa_con_relacion_a_usuariocreo', to=settings.AUTH_USER_MODEL)),
                ('usuario_elimino', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que elimino el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='empresa_con_relacion_a_usuarioelimino', to=settings.AUTH_USER_MODEL)),
                ('usuario_modifico', models.ForeignKey(blank=True, help_text='Fk a usuario para conocer el usuario que modifico el registro', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='empresa_con_relacion_a_usuariomodifico', to=settings.AUTH_USER_MODEL)),
                ('usuarios', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
