# Generated by Django 3.1.3 on 2022-06-03 08:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stock',
            field=models.PositiveBigIntegerField(default=0),
        ),
    ]
