# Generated by Django 3.1.7 on 2021-05-04 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccounts',
            name='first_name',
            field=models.CharField(blank=True, max_length=150, verbose_name='first name'),
        ),
    ]
