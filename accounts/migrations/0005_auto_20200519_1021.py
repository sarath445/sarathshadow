# Generated by Django 3.0.5 on 2020-05-19 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccounts',
            name='phone',
            field=models.IntegerField(null=True),
        ),
    ]
