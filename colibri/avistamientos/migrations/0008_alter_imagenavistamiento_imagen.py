# Generated by Django 5.1.6 on 2025-03-14 06:43

import avistamientos.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avistamientos', '0007_avistamiento_estado_conservacion_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagenavistamiento',
            name='imagen',
            field=models.ImageField(upload_to='avistamientos/', validators=[avistamientos.models.validar_extension_imagen]),
        ),
    ]
