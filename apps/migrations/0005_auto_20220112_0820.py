# Generated by Django 3.2.9 on 2022-01-12 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0004_country_country_city'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='address',
            new_name='age',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='full_name',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='mobile',
            new_name='country',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_image',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
