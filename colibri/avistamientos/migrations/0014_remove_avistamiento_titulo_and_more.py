# Generated by Django 5.1.7 on 2025-04-07 01:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avistamientos', '0013_eliminacionparcialavistamiento_avistamiento_titulo'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avistamiento',
            name='titulo',
        ),
        migrations.AddField(
            model_name='eliminacionparcialavistamiento',
            name='usuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='eliminacionparcialavistamiento',
            name='titulo',
            field=models.CharField(max_length=255),
        ),
    ]
