# Generated by Django 3.2.9 on 2022-01-12 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_auto_20220112_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale_statistics',
            name='date',
            field=models.DateField(),
        ),
    ]
