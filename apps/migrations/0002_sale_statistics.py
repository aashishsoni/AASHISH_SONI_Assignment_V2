# Generated by Django 3.2.9 on 2022-01-04 06:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='sale_statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('product', models.CharField(max_length=120)),
                ('sales_number', models.IntegerField()),
                ('revenue', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='User_data', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
