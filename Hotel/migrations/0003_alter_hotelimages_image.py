# Generated by Django 4.1.7 on 2023-03-29 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hotel', '0002_hotelimages'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hotelimages',
            name='image',
            field=models.ImageField(upload_to='hotel_images'),
        ),
    ]
