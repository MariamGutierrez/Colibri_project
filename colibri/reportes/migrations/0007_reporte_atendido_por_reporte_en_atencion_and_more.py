# Generated by Django 5.2 on 2025-05-02 03:47

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportes', '0006_merge_20250501_2134'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte',
            name='atendido_por',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='reportes_atendidos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='reporte',
            name='en_atencion',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='reporte',
            name='fecha_atencion',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
