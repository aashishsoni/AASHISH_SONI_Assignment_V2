# Generated by Django 3.2.9 on 2022-01-13 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0009_alter_userprofile_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='country_city',
            old_name='City',
            new_name='name',
        ),
    ]