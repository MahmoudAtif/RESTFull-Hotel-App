# Generated by Django 4.1.7 on 2023-04-03 15:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Room', '0005_alter_room_floor_alter_room_room_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='discount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=3, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
