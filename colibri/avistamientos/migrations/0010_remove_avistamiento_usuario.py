# Generated by Django 5.1.6 on 2025-04-06 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('avistamientos', '0009_avistamiento_usuario'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avistamiento',
            name='usuario',
        ),
    ]
