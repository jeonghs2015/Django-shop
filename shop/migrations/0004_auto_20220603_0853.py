# Generated by Django 3.1.3 on 2022-06-03 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20220603_0850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='stock',
            field=models.PositiveBigIntegerField(blank=True, default=0),
        ),
    ]
