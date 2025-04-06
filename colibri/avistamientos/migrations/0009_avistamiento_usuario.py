# Generated by Django 5.1.6 on 2025-04-06 18:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('avistamientos', '0008_alter_imagenavistamiento_imagen'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='avistamiento',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=models.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
