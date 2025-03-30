# Generated by Django 5.1.6 on 2025-03-28 22:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoReporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Reporte',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField()),
                ('fecha_reporte', models.DateTimeField(auto_now_add=True)),
                ('foto_url', models.URLField(blank=True, null=True)),
                ('ubicacion', models.CharField(blank=True, max_length=255, null=True)),
                ('alerta_enviada', models.BooleanField(default=False)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tipo_reporte', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reportes.tiporeporte')),
            ],
        ),
    ]
